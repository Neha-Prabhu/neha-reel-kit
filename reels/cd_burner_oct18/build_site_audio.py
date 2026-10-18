"""Site sounds from the screen recording (Burn click, drive tray, burn hum, eject, copy click, the 30 s preview) laid on
the cut timeline -> build/site_audio.wav, mixed under her voice via EXTRA_SFX.   python build_site_audio.py
SITE_AUDIO in reel.py: (cut-timeline start, end, recording start, volume) — always real speed, so nothing sounds warped.
Pieces are placed with numpy (ffmpeg 6.1's amix drops adelay'd silence and shortens the file)."""
import json, os, subprocess, sys, wave
import numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "..", ".."))
from reelkit.spec import load_spec, Clock

SR = 48000
S = load_spec(os.path.join(D, "reel.py"))
cuts = json.load(open(S.path("build/cuts.json"))); T = Clock(cuts, json.load(open(S.path(S.WORDS_JSON))))
total = cuts["duration"] + S.get("HOLD", 1.3)
out = np.zeros((int(total * SR), 2), np.float32)
for a, z, rec, vol in S.SITE_AUDIO:
    a, z = T(a), T(z); n = int((z - a) * SR)
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{rec:.3f}", "-i", S.path(S.REC), "-vn", "-t", f"{z - a:.3f}",
                          "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2)[:n].copy()
    f_in, f_out = min(int(0.02 * SR), len(x)), min(int(0.06 * SR), len(x))
    x[:f_in] *= np.linspace(0, 1, f_in)[:, None]; x[len(x) - f_out:] *= np.linspace(1, 0, f_out)[:, None]
    i0 = int(a * SR); out[i0:i0 + len(x)] += x * vol
pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open(S.path("build/site_audio.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("->", S.path("build/site_audio.wav"), round(total, 2), "s")
