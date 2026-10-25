"""boss_prank base cut (grade + B-roll, B-roll MUTED) -> build/cut.mp4; reelkit then adds captions/pops.
Voice pieces are adelay-ed to absolute times and amixed (per-segment apad/atrim drifted ~1 s in draft 3)."""
import subprocess
L = "/home/claude/neha-reel-kit/assets/luts/"; FPS = 30
BOG = (3.8, 4.9, 1.17, 2.40)        # boggled: src in/out -> timeline "to prank my boss" (~0.9x)
YT = [(3.0, 7.5, 1.6), (7.5, 9.6, 1.0)]
KK = [(0.0, 4.3, 1.5), (4.3, 7.5, 1.0)]
d = lambda p: sum((o - i) / s for i, o, s in p)
y0 = 13.15; k0 = y0 + d(YT); a2 = k0 + d(KK); END = a2 + (30.55 - 20.22)
VOICE = [(0, 13.15, 0), (13.15, 15.10, 13.15), (15.40, 17.62, 15.10),
         (18.09, 20.17, k0 + 4.3 / 1.5 + 0.3 - 2.08), (20.22, 30.55, a2)]
fc = []
def clip(inp, parts, tag):
    for k, (i, o, s) in enumerate(parts):
        fc.append(f"[{inp}:v]trim={i}:{o},setpts=(PTS-STARTPTS)/{s},fps={FPS},scale=1080:1920,setsar=1,lut3d={L}warm_pop_light.cube[{tag}{k}]")
    fc.append("".join(f"[{tag}{k}]" for k in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[{tag}]")
fc.append(f"[0:v]trim=0:{y0},setpts=PTS-STARTPTS,fps={FPS},lut3d={L}warm_pop.cube,scale=1080:1920,setsar=1[a1]")
si, so, ts, te = BOG
fc.append(f"[1:v]trim={si}:{so},setpts=(PTS-STARTPTS)*{(te-ts)/(so-si):.4f}+{ts}/TB,fps={FPS},scale=1080:1920,setsar=1,lut3d={L}warm_pop_light.cube[bog]")
fc.append(f"[a1][bog]overlay=eof_action=pass:enable='between(t,{ts},{te-0.001})'[v1]")
clip(2, YT, "yt"); clip(3, KK, "kk")
fc.append(f"[0:v]trim=20.22:30.55,setpts=PTS-STARTPTS,fps={FPS},lut3d={L}warm_pop.cube,scale=1080:1920,setsar=1[a2]")
fc.append("[v1][yt][kk][a2]concat=n=4:v=1:a=0[v]")
for k, (a, b, at) in enumerate(VOICE):
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,adelay={int(round(at*1000))}:all=1[p{k}]")
fc.append("".join(f"[p{k}]" for k in range(len(VOICE))) + f"amix=inputs={len(VOICE)}:normalize=0,atrim=0:{END:.3f}[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "src/aroll.mp4", "-i", "src/far_boss_boggled.MOV", "-i", "src/youtube_play.MOV",
                "-i", "src/kicked_him_out.mov", "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "build/cut.mkv"], check=True)
print(f"YT {y0}-{k0:.3f}  KK {k0:.3f}-{a2:.3f}  end {END:.3f}")
