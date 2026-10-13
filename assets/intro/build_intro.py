"""Stop-motion desk intro for "Things I Found on the Internet Instead of Doomscrolling".
Renders 24 text-free frames (8 fps) — the reel engine adds the "Day N" pop + typed title on top.

  python build_intro.py --out frames_default                          # classic blue wall
  python build_intro.py --out frames_hw --wall ../textures/orange_soft.jpg --witch-hat
  python halloween_props.py frames_hw frames_hw_props                   # optional theme props
"""
import argparse as _ap
_p = _ap.ArgumentParser(); _p.add_argument("--out", default="frames_default"); _p.add_argument("--wall", default="")
_p.add_argument("--witch-hat", action="store_true"); _p.add_argument("--preview", default="")
_A = _p.parse_args()
import os
os.environ["OUTDIR"] = _A.out; os.environ["NOTEXT"] = "1"
if _A.wall: os.environ["WALLTEX"] = _A.wall
if _A.preview: os.environ["PREVIEW"] = _A.preview
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
WITCH_HAT = _A.witch_hat
"""Stop-motion bobble-head intro for 'Day 3 — Things I Found on the Internet Instead of Doomscrolling'."""
import math, random, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS_LOOK = 8          # stop-motion frame rate
N_FRAMES = 24         # 3 s at 8 fps
NOTEXT = bool(os.environ.get("NOTEXT"))
OUT = os.environ.get("OUTDIR", "frames")
os.makedirs(OUT, exist_ok=True)

# Brand palette
BLUE = (142, 166, 200)
WALL = tuple(int(v) for v in os.environ.get("WALL", "142,166,200").split(","))
PREVIEW = os.environ.get("PREVIEW")
BUTTER = (247, 226, 122)
LAVENDER = (226, 198, 242)
PINK = (236, 167, 196)
DUSTY_RED = (205, 92, 98)
INK = (38, 32, 44)
CREAM = (250, 243, 228)
WOOD = (222, 186, 140)
WOOD_D = (196, 156, 108)

# Stand-in fonts (swap for Diagramm Black Italic / Hello Sister / Margarine when provided)
F_DAY = os.path.join(FONTS, "Diagramm-UltraBoldItalic.ttf")
F_TITLE = os.path.join(FONTS, "Monigue.otf")
F_SMALL = os.path.join(FONTS, "Poppins-Bold.ttf")

rng = np.random.default_rng(7)


def paper_noise(size, base, amt=10):
    n = rng.normal(0, amt, (size[1], size[0], 1))
    arr = np.clip(np.array(base, dtype=float)[None, None, :] + n, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB").filter(ImageFilter.GaussianBlur(0.6))


def cutout(img, border=10, shadow=True):
    """Give an RGBA layer a white paper-cut border + soft drop shadow (collage look)."""
    pad = border * 3
    big = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    big.paste(img, (pad, pad), img)
    a = big.split()[3]
    grown = a.filter(ImageFilter.MaxFilter(border * 2 + 1))
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", big.size, (20, 20, 40, 0))
        sh.putalpha(grown.point(lambda v: int(v * 0.28)).filter(ImageFilter.GaussianBlur(8)))
        out.alpha_composite(sh, (6, 10))
    white = Image.new("RGBA", big.size, (255, 255, 255, 0))
    white.putalpha(grown)
    out.alpha_composite(white)
    out.alpha_composite(big)
    return out


def layer(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


# ---------- static props (drawn once, jittered per frame) ----------
def make_lamp():
    L = layer(360, 520)
    d = ImageDraw.Draw(L)
    d.ellipse([168, 238, 192, 262], fill=(120, 85, 60))
    # scalloped shade
    d.polygon([(110, 270), (250, 270), (330, 420), (30, 420)], fill=(240, 225, 196))
    for i in range(7):
        x = 30 + i * (300 / 7)
        d.pieslice([x, 395, x + 300 / 7, 445], 0, 180, fill=(240, 225, 196))
    for i in range(6):  # pleats
        x0 = 120 + i * 24
        d.line([(x0, 272), (40 + i * 56, 418)], fill=(220, 200, 165), width=3)
    d.ellipse([150, 425, 210, 470], fill=(255, 236, 170))
    return cutout(L, 8)


def make_clock():
    L = layer(300, 300)
    d = ImageDraw.Draw(L)
    cx = cy = 150
    pts = []
    for i in range(240):
        t = i / 240 * 2 * math.pi
        r = 138 + 8 * math.cos(12 * t)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    d.polygon(pts, fill=(176, 128, 90))
    d.ellipse([cx - 118, cy - 118, cx + 118, cy + 118], fill=CREAM)
    for k in range(12):
        t = k / 12 * 2 * math.pi
        r1, r2 = (96, 112) if k % 3 else (86, 112)
        d.line([(cx + r1 * math.sin(t), cy - r1 * math.cos(t)),
                (cx + r2 * math.sin(t), cy - r2 * math.cos(t))], fill=INK, width=5 if k % 3 == 0 else 3)
    return L


def clock_with_hands(base, minute):
    L = base.copy()
    d = ImageDraw.Draw(L)
    cx = cy = 150
    tm = minute / 60 * 2 * math.pi
    th = (10 + minute / 60) / 12 * 2 * math.pi
    d.line([(cx, cy), (cx + 62 * math.sin(th), cy - 62 * math.cos(th))], fill=INK, width=8)
    d.line([(cx, cy), (cx + 92 * math.sin(tm), cy - 92 * math.cos(tm))], fill=INK, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=DUSTY_RED)
    return cutout(L, 8)


def make_pegboard():
    PW, PH = 310, 380
    L = layer(PW, PH)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 0, PW, PH], 14, fill=(236, 214, 244), outline=(205, 178, 222), width=4)
    for yy in range(26, PH - 10, 30):
        for xx in range(26, PW - 10, 30):
            d.ellipse([xx - 4, yy - 4, xx + 4, yy + 4], fill=(196, 168, 214))
    def hook(x, y):
        d.line([(x, y), (x, y + 18)], fill=(120, 120, 130), width=4)
        d.arc([x - 8, y + 10, x + 8, y + 26], 0, 180, fill=(120, 120, 130), width=4)
    # polaroid with a cat doodle
    hook(86, 26)
    pol = layer(130, 150); pd = ImageDraw.Draw(pol)
    pd.rectangle([0, 0, 130, 150], fill=(252, 250, 246), outline=(220, 214, 206), width=2)
    pd.rectangle([12, 12, 118, 108], fill=(255, 220, 228))
    pd.ellipse([38, 44, 92, 96], fill=INK)
    pd.polygon([(40, 58), (46, 30), (62, 48)], fill=INK)
    pd.polygon([(90, 58), (84, 30), (68, 48)], fill=INK)
    pd.ellipse([52, 62, 60, 70], fill=BUTTER); pd.ellipse([70, 62, 78, 70], fill=BUTTER)
    pd.text((65, 128), "pawmuch", font=ImageFont.truetype(F_SMALL, 20), fill=INK, anchor="mm")
    pol = pol.rotate(-6, expand=True, resample=Image.BICUBIC)
    L.alpha_composite(pol, (20, 44))
    # tiny game controller on a hook
    hook(236, 26)
    d.rounded_rectangle([176, 58, 296, 116], 28, fill=BUTTER, outline=(210, 180, 80), width=3)
    d.ellipse([170, 80, 214, 132], fill=BUTTER); d.ellipse([258, 80, 302, 132], fill=BUTTER)
    d.rectangle([194, 78, 202, 104], fill=INK); d.rectangle([185, 87, 211, 95], fill=INK)
    d.ellipse([262, 76, 276, 90], fill=DUSTY_RED); d.ellipse([274, 90, 288, 104], fill=PINK)
    d.ellipse([224, 84, 234, 92], fill=INK); d.ellipse([238, 84, 248, 92], fill=INK)
    # little shelf with a plant and a heart
    d.rectangle([150, 236, 296, 248], fill=WOOD_D)
    d.line([(160, 248), (160, 262)], fill=(120, 120, 130), width=4)
    d.line([(286, 248), (286, 262)], fill=(120, 120, 130), width=4)
    d.polygon([(176, 236), (220, 236), (214, 200), (182, 200)], fill=DUSTY_RED)
    for ang in (-50, -20, 10, 40):
        t = math.radians(ang - 90)
        d.ellipse([198 + 30 * math.cos(t) - 12, 222 + 30 * math.sin(t) - 7,
                   198 + 30 * math.cos(t) + 12, 222 + 30 * math.sin(t) + 7], fill=(110, 160, 90))
    d.ellipse([238, 196, 262, 220], fill=PINK); d.ellipse([256, 196, 280, 220], fill=PINK)
    d.polygon([(240, 212), (278, 212), (259, 236)], fill=PINK)
    # headphones on a hook
    hook(86, 236)
    d.arc([40, 258, 132, 340], 180, 360, fill=INK, width=10)
    d.rounded_rectangle([32, 296, 56, 346], 10, fill=INK)
    d.rounded_rectangle([116, 296, 140, 346], 10, fill=INK)
    # sticky note
    d.polygon([(172, 282), (290, 276), (294, 360), (176, 366)], fill=BUTTER)
    d.text((233, 306), "find", font=ImageFont.truetype(F_SMALL, 24), fill=INK, anchor="mm")
    d.text((233, 336), "cool sites!", font=ImageFont.truetype(F_SMALL, 20), fill=INK, anchor="mm")
    return cutout(L, 8)


def make_laptop():
    L = layer(520, 330)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle([10, 0, 510, 300], 22, fill=(226, 228, 232), outline=(190, 192, 198), width=4)
    d.rounded_rectangle([0, 296, 520, 322], 8, fill=(200, 202, 208))
    # stickers (original designs)
    # strawberry
    d.ellipse([60, 190, 120, 260], fill=DUSTY_RED)
    d.polygon([(70, 196), (90, 178), (110, 196), (90, 205)], fill=(110, 160, 90))
    for sx, sy in [(78, 215), (98, 222), (85, 238), (104, 244)]:
        d.ellipse([sx, sy, sx + 5, sy + 7], fill=(255, 230, 150))
    # starburst
    def burst(cx, cy, r1, r2, n, col):
        pts = []
        for i in range(n * 2):
            r = r1 if i % 2 == 0 else r2
            t = i / (n * 2) * 2 * math.pi
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        d.polygon(pts, fill=col)
    burst(380, 90, 62, 30, 10, PINK)
    burst(170, 90, 36, 18, 8, (110, 140, 220))
    # heart
    d.ellipse([400, 200, 436, 236], fill=LAVENDER)
    d.ellipse([428, 200, 464, 236], fill=LAVENDER)
    d.polygon([(402, 224), (462, 224), (432, 266)], fill=LAVENDER)
    # cat-face sticker
    d.ellipse([230, 170, 320, 250], fill=BUTTER)
    d.polygon([(236, 190), (246, 150), (270, 176)], fill=BUTTER)
    d.polygon([(314, 190), (304, 150), (280, 176)], fill=BUTTER)
    d.ellipse([254, 196, 264, 208], fill=INK)
    d.ellipse([286, 196, 296, 208], fill=INK)
    d.polygon([(270, 214), (280, 214), (275, 221)], fill=PINK)
    # "neha much" label sticker
    f = ImageFont.truetype(F_SMALL, 24)
    d.rounded_rectangle([60, 40, 210, 80], 18, fill=INK)
    d.text((135, 60), "neha much", font=f, fill=CREAM, anchor="mm")
    return cutout(L, 6)


def make_can():
    L = layer(120, 220)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle([10, 20, 110, 210], 14, fill=(205, 208, 214))
    for i in range(10):  # metallic sheen
        x = 22 + i * 3
        d.line([(x, 28), (x, 202)], fill=(235, 237, 240), width=2)
    d.ellipse([10, 8, 110, 36], fill=(185, 188, 194))
    d.ellipse([22, 13, 98, 31], fill=(160, 163, 170))
    d.rectangle([10, 120, 110, 150], fill=DUSTY_RED)
    f = ImageFont.truetype(F_SMALL, 22)
    d.text((60, 92), "diet", font=f, fill=INK, anchor="mm")
    d.text((60, 136), "COLA", font=ImageFont.truetype(F_SMALL, 18), fill=CREAM, anchor="mm")
    d.line([(78, 22), (96, -40)], fill=PINK, width=8)
    return cutout(L, 6)


def make_books():
    L = layer(240, 230)
    d = ImageDraw.Draw(L)
    cols = [DUSTY_RED, BUTTER, (110, 140, 220), LAVENDER, PINK, (240, 240, 235), INK]
    y = 210
    for i, c in enumerate(cols):
        h = 24 + (i % 3) * 4
        off = (i * 13) % 22 - 10
        d.rectangle([20 + off, y - h, 220 + off, y], fill=c, outline=(60, 50, 60), width=2)
        y -= h
    return cutout(L, 6)


def make_torso():
    L = layer(470, 360)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 60, 470, 420], 120, fill=LAVENDER)
    d.rectangle([0, 200, 470, 360], fill=LAVENDER)
    d.ellipse([150, 30, 320, 120], fill=(210, 160, 130))  # neck
    d.chord([140, 20, 330, 160], 0, 180, fill=LAVENDER)
    return L


def make_legs():
    L = layer(330, 300)
    d = ImageDraw.Draw(L)
    d.polygon([(30, 0), (160, 0), (150, 260), (50, 260)], fill=(126, 156, 196))
    d.polygon([(170, 0), (300, 0), (280, 260), (180, 260)], fill=(118, 148, 190))
    d.line([(165, 0), (165, 60)], fill=(90, 115, 150), width=3)
    d.rounded_rectangle([30, 250, 160, 296], 20, fill=INK)
    d.rounded_rectangle([170, 250, 300, 296], 20, fill=INK)
    return L


def make_background():
    if not os.environ.get("WALLTEX"):
        bg = paper_noise((W, H), WALL, 9).convert("RGBA")
        return _floor(bg)
    _t = Image.open(os.environ["WALLTEX"]).convert("RGB")
    _k = max(W / _t.width, H / _t.height); _t = _t.resize((int(_t.width * _k) + 1, int(_t.height * _k) + 1), Image.LANCZOS)
    bg = _t.crop(((_t.width - W) // 2, (_t.height - H) // 2, (_t.width - W) // 2 + W, (_t.height - H) // 2 + H)).convert("RGBA")
    return _floor(bg)


def _floor(bg):
    # floor: star tiles
    floor_y = 1500
    tile = 120
    fl = Image.new("RGBA", (W, H - floor_y), (245, 242, 236, 255))
    d = ImageDraw.Draw(fl)
    for ty in range(-1, (H - floor_y) // tile + 2):
        for tx in range(-1, W // tile + 2):
            cx, cy = tx * tile + tile / 2, ty * tile + tile / 2
            pts = []
            for i in range(16):
                r = 52 if i % 2 == 0 else 18
                t = i / 16 * 2 * math.pi
                pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
            d.polygon(pts, fill=INK)
    bg.alpha_composite(fl, (0, floor_y))
    d = ImageDraw.Draw(bg)
    d.rectangle([0, floor_y - 8, W, floor_y + 4], fill=(228, 220, 205))  # skirting
    return bg


def make_desk():
    L = layer(900, 340)
    d = ImageDraw.Draw(L)
    d.rectangle([0, 0, 900, 46], fill=(234, 202, 160))         # top surface
    d.rectangle([0, 46, 900, 70], fill=WOOD_D)                  # edge
    d.rectangle([20, 70, 880, 330], fill=WOOD)                  # front
    for x0 in (40, 460):
        d.rectangle([x0, 92, x0 + 400, 196], outline=WOOD_D, width=5)
        d.rounded_rectangle([x0 + 170, 136, x0 + 230, 150], 6, fill=WOOD_D)
    # wood grain
    for i in range(18):
        y = 210 + i * 6 + (i % 3)
        d.line([(30, y), (870, y + (i % 5) - 2)], fill=(214, 176, 128), width=2)
    return cutout(L, 6)


# ---------- text ----------
def text_block(text, font_path, size, fill, stroke=INK, sw=0, shadow=True, maxw=None):
    f = ImageFont.truetype(font_path, size)
    lines = [text] if maxw is None else wrap(text, f, maxw)
    lh = int(size * 1.12)
    tw = max(f.getbbox(l)[2] for l in lines) + 40
    L = layer(tw, lh * len(lines) + 40)
    d = ImageDraw.Draw(L)
    for i, l in enumerate(lines):
        if shadow:  # hard shadow: solid, unblurred offset copy
            off = max(4, int(size * 0.045))
            d.text((tw // 2 + off, 20 + i * lh + off), l, font=f, fill=INK, anchor="ma")
        d.text((tw // 2, 20 + i * lh), l, font=f, fill=fill, anchor="ma", stroke_width=sw, stroke_fill=stroke)
    return L


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if f.getbbox(t)[2] <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines


# ---------- assemble ----------
heads = {k: Image.open(os.path.join(HERE, "heads", f"head{k}.png")).convert("RGBA") for k in "678"}
HEAD_SCALE = {"6": 0.70, "8": 0.68, "7": 0.88}
def witch_hat(w):
    S_ = 3; Wd = w * S_; Hd = int(w * 0.55) * S_
    im = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    HAT = (40, 30, 50); BAND = (150, 95, 200); BUCK = (250, 205, 90)
    by = Hd * 0.80
    d.polygon([(Wd * .30, by), (Wd * .70, by), (Wd * .60, Hd * .30), (Wd * .78, Hd * .06), (Wd * .52, Hd * .22), (Wd * .44, Hd * .40)], fill=HAT)  # bent cone
    d.polygon([(Wd * .31, by - Hd * .02), (Wd * .69, by - Hd * .02), (Wd * .665, by - Hd * .14), (Wd * .335, by - Hd * .14)], fill=BAND)
    d.rectangle([Wd * .46, by - Hd * .135, Wd * .54, by - Hd * .025], outline=BUCK, width=5 * S_)
    d.ellipse([0, by - Hd * .07, Wd, by + Hd * .13], fill=HAT)
    return im.resize((Wd // S_, Hd // S_), Image.LANCZOS)


HAT_PAD = {}
HAT_FIT = {"6": (0.92, 0.15), "8": (0.92, 0.15), "7": (1.05, 0.10)}   # (hat width / head width, brim y / head height)
for k, im in (list(heads.items()) if WITCH_HAT else []):
    fw, fy = HAT_FIT[k]
    hat = witch_hat(int(im.width * fw))
    brim_y = int(im.height * fy)
    pad_top = max(0, hat.height - brim_y - int(hat.height * 0.13))
    c = Image.new("RGBA", (max(im.width, hat.width), im.height + pad_top), (0, 0, 0, 0))
    c.alpha_composite(im, ((c.width - im.width) // 2, pad_top))
    c.alpha_composite(hat, ((c.width - hat.width) // 2, pad_top + brim_y - int(hat.height * 0.80)))
    heads[k] = c
    HAT_PAD[k] = (im.height, pad_top)
head_layers = {}
for k, im in heads.items():
    s = HEAD_SCALE[k]
    head_layers[k] = cutout(im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS), 8)

bg = make_background()
pegboard = make_pegboard()
pegboard = pegboard.resize((int(pegboard.width * 0.74), int(pegboard.height * 0.74)), Image.LANCZOS)
lamp, clock_base, laptop, can, books = make_lamp(), make_clock(), make_laptop(), make_can(), make_books()
desk, torso, legs = make_desk(), make_torso(), make_legs()
day = text_block("Day 3", F_DAY, 175, BUTTER, sw=0)
title = text_block("Things I Found on the Internet Instead of Doomscrolling", F_TITLE, 98, CREAM,
                   stroke=INK, sw=0, maxw=940)

NECK_K = {k: 1.0 for k in "678"}
NECK_K.update({k: (0.88 * h0 + p) / (0.88 * (h0 + p)) for k, (h0, p) in HAT_PAD.items()})
head_seq = (["6", "6", "8", "8", "7", "7"] * 4)[:N_FRAMES]

def jit(a=3):
    return random.randint(-a, a)

random.seed(3)
for i in ([N_FRAMES - 1] if PREVIEW else range(N_FRAMES)):
    fr = bg.copy()
    fr.alpha_composite(legs, (375 + jit(2), 1525 + jit(1)))
    lx = -30 + jit()
    ImageDraw.Draw(fr).line([(lx + 180 + 24, 0), (lx + 180 + 24, 560)], fill=(90, 70, 60), width=5)
    fr.alpha_composite(lamp, (lx, 300 + jit()))
    fr.alpha_composite(pegboard.rotate(jit(1) * 0.6, expand=True, resample=Image.BICUBIC), (790 + jit(), 600 + jit()))
    fr.alpha_composite(torso, (305 + jit(2), 880 + jit(2)))
    # bobble head: bounce + tilt
    k = head_seq[i]
    hl = head_layers[k]
    ang = [-6, 4, -3, 6, -5, 3][i % 6]
    bob = [0, -18, -6, -22, 0, -12][i % 6]
    hr = hl.rotate(ang, resample=Image.BICUBIC, expand=True)
    hx = W // 2 - hr.width // 2 + jit(4)
    neck_y = 950
    hy = neck_y - int(hr.height * 0.88 * NECK_K[k]) + bob
    fr.alpha_composite(hr, (hx, hy))
    fr.alpha_composite(desk, (70 + jit(1), 1215 + jit(1)))
    fr.alpha_composite(laptop, (270 + jit(2), 950 + jit(1)))
    fr.alpha_composite(can, (135 + jit(2), 1050 + jit(2)))
    fr.alpha_composite(books, (760 + jit(2), 1040 + jit(2)))

    # text: Day 3 pops in on frame 2, title on frame 5 (stop-motion overshoot)
    if i >= 2 and not NOTEXT:
        dl = day.rotate(-4, expand=True, resample=Image.BICUBIC)
        fr.alpha_composite(dl, (W // 2 - dl.width // 2, 35 - (dl.height - day.height) // 2))
    if i >= 5 and not NOTEXT:
        fr.alpha_composite(title, (W // 2 - title.width // 2, 250))

    fr.convert("RGB").save(f"{OUT}/f{i:03d}.png")
print("frames done")
if PREVIEW:
    Image.open(f"{OUT}/f{N_FRAMES - 1:03d}.png").save(PREVIEW)
    raise SystemExit

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS_LOOK), "-i", f"{OUT}/f%03d.png",
                "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                "-movflags", "+faststart", "Day3_intro.mp4"], check=True)

print("video done")
