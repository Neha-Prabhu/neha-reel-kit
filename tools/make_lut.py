"""Build Neha's 'warm pop' grade as a 33-point .cube LUT (works in VN, CapCut, Edits, Premiere, ffmpeg lut3d).
python tools/make_lut.py assets/luts/warm_pop.cube [--strength 1.0]"""
import sys, numpy as np, colorsys
out = sys.argv[1]; k = float(sys.argv[sys.argv.index("--strength")+1]) if "--strength" in sys.argv else 1.0
N = 33
g = np.linspace(0, 1, N)
b, gg, r = np.meshgrid(g, g, g, indexing="ij")          # .cube order: R fastest
rgb = np.stack([r, gg, b], -1).reshape(-1, 3)

def scurve(x, amt):   # filmic contrast around mid-grey, soft toe/shoulder
    s = x + amt * (x - 0.5) * (1 - np.abs(2 * x - 1)) * 1.0
    return np.clip(s, 0, 1)

x = rgb.copy()
# 1) lift blacks a hair, then contrast S-curve
x = 0.012 + x * 0.988
x = scurve(x, 0.32 * k)
# 2) vibrance: boost low-saturation colours more than already-saturated ones
lum = (x @ np.array([0.2126, 0.7152, 0.0722]))[:, None]
mx, mn = x.max(1, keepdims=True), x.min(1, keepdims=True)
sat = (mx - mn) / (mx + 1e-6)
x = lum + (x - lum) * (1 + (0.55 * k) * (1 - sat) ** 1.5 + 0.10 * k)
# 3) protect skin: pull hues near skin (orange ~ 15–45°) back toward a gentler boost
h = np.array([colorsys.rgb_to_hsv(*np.clip(p, 0, 1))[0] for p in rgb]) * 360
skin = np.exp(-((h - 28) / 18) ** 2)[:, None] * (sat > 0.08)
x = x * (1 - 0.35 * skin) + (lum + (rgb - lum) * (1 + 0.25 * k)) * 0.35 * skin
# 4) split tone: cool-teal shadows, warm highlights (subtle)
lum = (np.clip(x, 0, 1) @ np.array([0.2126, 0.7152, 0.0722]))[:, None]
sh, hi = (1 - lum) ** 2, lum ** 2
x = x + k * (sh * np.array([-0.018, 0.006, 0.022]) + hi * np.array([0.022, 0.008, -0.020]))
x = np.clip(x, 0, 1)
with open(out, "w") as f:
    f.write(f'TITLE "Neha warm pop {k}"\nLUT_3D_SIZE {N}\n')
    for p in x: f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
print("wrote", out)
