"""Pass 1 — rough cut.

  python -m reelkit.roughcut reels/<name>/reel.py --detect     # print speech regions -> paste into SEGS
  python -m reelkit.roughcut reels/<name>/reel.py              # build the cut

Writes into the reel folder: build/aroll_1080.mov, build/roughcut.mp4, build/voice_clean.wav, build/cuts.json

House rules baked in (from Days 3-5):
  * 4K is downscaled to 1080x1920 FIRST (a trim graph on 4K gets OOM-killed)
  * speed 1.1x by default; list lines and fast throwaway lines 1.2x
  * audio: mono -> per-segment trim + atempo -> concat -> +11 dB -> light limiter, ONE encode.
    (never loudnorm = pumping; never rubberband = robotic/double voice)
  * J cut = ONE frame (next line's audio starts 1/30 s before the picture cuts) — more shows her looking away
  * picture cuts land on the 30 fps grid, audio segments are trimmed to exact length -> lip sync never drifts
"""
import json, os, subprocess, sys
from .spec import load_spec

FPS = 30


def sh(*a, **k):
    return subprocess.run(list(a), check=True, **k)


def downscale(spec):
    out = spec.path("build/aroll_1080.mov")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sh("ffmpeg", "-loglevel", "error", "-y", "-i", spec.path(spec.AROLL), "-vf", "scale=1080:1920",
           "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "pcm_s16le", out)
    return out


def detect(spec, thresh=-40, min_sil=0.12):
    src = downscale(spec)
    r = subprocess.run(["ffmpeg", "-i", src, "-af", f"silencedetect=n={thresh}dB:d={min_sil}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    ss = [float(l.split("silence_start: ")[1]) for l in r.splitlines() if "silence_start" in l]
    se = [float(l.split("silence_end: ")[1].split()[0]) for l in r.splitlines() if "silence_end" in l]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout)
    starts = [0.0] + se; ends = ss + [dur]
    regs = [(a, b) for a, b in zip(starts, ends) if b - a > 0.15]
    print("# speech regions (merge regions that belong to one line; pad 0.03 before / 0.06 after)")
    for a, b in regs:
        print(f"    ({max(0, a - 0.03):.2f}, {b + 0.06:.2f}, 1.1),")


def build(spec):
    src = downscale(spec)
    SEGS = spec.SEGS; J = 1 / FPS; n = len(SEGS)
    fc = "[0:a]pan=mono|c0=0.5*c0+0.5*c1,aresample=48000[m];[m]asplit=%d%s;" % (n, "".join(f"[m{i}]" for i in range(n)))
    starts, T = [], 0.0
    for a, b, k in SEGS:
        starts.append(T); T += (b - a) / k
    NF = int(round(T * FPS))
    cf = [0] + [int(round((st + J) * FPS)) for st in starts[1:]] + [NF]
    for i, (a, b, k) in enumerate(SEGS):
        d = b - a; t0 = cf[i] / FPS; va = a + (t0 - starts[i]) * k; nfr = cf[i + 1] - cf[i]
        fc += (f"[0:v]trim=start={va:.4f}:duration={nfr / FPS * k + 0.2:.4f},setpts=(PTS-STARTPTS)/{k},fps={FPS},"
               f"trim=end_frame={nfr},setpts=PTS-STARTPTS[v{i}];"
               f"[m{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.010,afade=t=out:st={d - 0.02:.3f}:d=0.02,"
               f"atempo={k},apad,atrim=end={d / k:.4f}[a{i}];")
    fa = fc.split("[0:v]")[0] + "".join(p.split(";", 1)[1] for p in fc.split("[0:v]")[1:])   # audio-only graph
    fa += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a0];[a0]volume=11dB,alimiter=limit=0.94:attack=5:release=60[a]"
    # video: one encode per segment, then a lossless concat — a single 20+ branch trim graph gets OOM-killed
    vdir = spec.path("build/_segs"); os.makedirs(vdir, exist_ok=True); lst = []
    for i, (a, b, k) in enumerate(SEGS):
        t0 = cf[i] / FPS; va = a + (t0 - starts[i]) * k; nfr = cf[i + 1] - cf[i]; p = os.path.join(vdir, f"v{i:03d}.mp4")
        sh("ffmpeg", "-loglevel", "error", "-y", "-ss", f"{va:.4f}", "-i", src, "-an", "-vf",
           f"setpts=(PTS-STARTPTS)/{k},fps={FPS},trim=end_frame={nfr},setpts=PTS-STARTPTS",
           "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", str(FPS), p)
        lst.append(f"file '{p}'")
    open(os.path.join(vdir, "list.txt"), "w").write("\n".join(lst))
    sh("ffmpeg", "-loglevel", "error", "-y", "-i", src, "-filter_complex", fa, "-map", "[a]", "-c:a", "pcm_s16le",
       spec.path("build/voice_clean.wav"))
    sh("ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(vdir, "list.txt"),
       "-i", spec.path("build/voice_clean.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
       "-movflags", "+faststart", spec.path("build/roughcut.mp4"))
    json.dump({"segs": SEGS, "J": J, "picture_cuts": [c / FPS for c in cf[1:-1]], "audio_starts": starts, "duration": T},
              open(spec.path("build/cuts.json"), "w"), indent=1)
    print(f"rough cut {T:.2f}s -> {spec.path('build/roughcut.mp4')}")


if __name__ == "__main__":
    spec = load_spec(sys.argv[1])
    detect(spec) if "--detect" in sys.argv else build(spec)
