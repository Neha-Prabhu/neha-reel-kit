"""Word timings on the rough-cut timeline -> build/words.json  [{"w", "s", "e", "line"}]

Best:   spec.SRT = "aroll.srt"   (export auto-captions from Edits/CapCut on the ORIGINAL A-roll)
        -> exact words she said, mapped through the cut.  line = rough-cut segment index.
Backup: spec.LINES = ["exact words of segment 0", "segment 1", ...]  (one string per SEGS entry)
        -> words spread over detected syllable peaks inside each segment (good to ~0.1 s).

  python -m reelkit.words reels/<name>/reel.py
"""
import json, re, sys
import numpy as np
from .spec import load_spec


def syllables(word):
    w = re.sub(r"[^a-z0-9]", "", word.lower())
    if not w: return 1
    if w.isdigit(): return {1: 1, 2: 2}.get(len(w), 3)
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1: n -= 1
    return max(1, n)


def _src_to_out(segs, t):
    acc = 0.0
    for i, (a, b, k) in enumerate(segs):
        if a - 0.05 <= t <= b + 0.05: return i, acc + (min(max(t, a), b) - a) / k
        acc += (b - a) / k
    return None, None


def from_srt(spec, cuts):
    txt = open(spec.path(spec.SRT), encoding="utf-8-sig").read()
    ts = lambda s: (lambda h, m, x: int(h) * 3600 + int(m) * 60 + float(x.replace(",", ".")))(*s.split(":"))
    words = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        ls = block.strip().splitlines()
        if len(ls) < 3: continue
        a, b = [ts(x.strip()) for x in ls[1].split("-->")]
        toks = " ".join(ls[2:]).split(); syl = [syllables(t) for t in toks]; tot = sum(syl); acc = 0
        for tok, n in zip(toks, syl):
            st = a + (b - a) * acc / tot; acc += n
            line, o = _src_to_out(cuts["segs"], st)
            if line is not None: words.append({"w": tok, "s": round(o, 3), "line": line})
    return words


def from_lines(spec, cuts):
    import scipy.io.wavfile as wav
    from scipy.signal import butter, sosfiltfilt, find_peaks
    from scipy.ndimage import uniform_filter1d
    import subprocess
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", spec.path("build/voice_clean.wav"), "-ac", "1", "-ar", "16000",
                    spec.path("build/vc16.wav")], check=True)
    sr, x = wav.read(spec.path("build/vc16.wav")); x = x.astype(float) / 32768
    y = sosfiltfilt(butter(4, [300, 3000], btype="band", fs=sr, output="sos"), x)
    hop, win = int(sr * .01), int(sr * .03)
    e = np.array([np.sqrt(np.mean(y[i:i + win] ** 2) + 1e-12) for i in range(0, len(y) - win, hop)])
    d = uniform_filter1d(20 * np.log10(e), 5)
    pk, _ = find_peaks(d, prominence=3, distance=8, height=np.median(d)); peaks = pk * 0.01
    bnd = cuts["audio_starts"] + [cuts["duration"]]
    words = []
    for L, text in enumerate(spec.LINES):
        s0, s1 = bnd[L], bnd[L + 1]
        toks = text.split(); syl = [syllables(t) for t in toks]; N = sum(syl)
        P = [p for p in peaks if s0 - 0.03 <= p <= s1 + 0.03]; k = 0
        for tok, n in zip(toks, syl):
            i0 = min(int(round(k * len(P) / N)), len(P) - 1)
            words.append({"w": tok, "s": round(float(max(s0, P[i0] - 0.07) if P else s0 + (s1 - s0) * k / N), 3), "line": L}); k += n
    return words


def build(spec):
    cuts = json.load(open(spec.path("build/cuts.json")))
    words = from_srt(spec, cuts) if spec.get("SRT") else from_lines(spec, cuts)
    words.sort(key=lambda w: w["s"])
    for i, w in enumerate(words):
        nxt = words[i + 1] if i + 1 < len(words) else None
        line_end = cuts["audio_starts"][w["line"] + 1] if w["line"] + 1 < len(cuts["audio_starts"]) else cuts["duration"]
        w["e"] = round(min(nxt["s"], line_end) if nxt and nxt["line"] == w["line"] else line_end, 3)
    json.dump(words, open(spec.path("build/words.json"), "w"), indent=0)
    for L in sorted({w["line"] for w in words}):
        print(L, " ".join(f"{w['w']}@{w['s']}" for w in words if w["line"] == L))


if __name__ == "__main__":
    build(load_spec(sys.argv[1]))
