"""Shared drawing helpers — Neha Much house style."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(KIT, "assets", "fonts")
SFX = os.path.join(KIT, "assets", "sfx")
TEXTURES = os.path.join(KIT, "assets", "textures")

# brand palette
BLUE = (142, 166, 200); BUTTER = (247, 226, 122); LAVENDER = (226, 198, 242)
INK = (38, 32, 44); CREAM = (250, 243, 228); WHITE = (255, 255, 255)

F_DIA = os.path.join(FONTS, "Diagramm-UltraBoldItalic.ttf")   # captions, intro label, big words
F_MON = os.path.join(FONTS, "Monigue.otf")                     # intro / title text
F_PRO = os.path.join(FONTS, "ProvidenceSans.ttf")              # handwritten accent (use sparingly)
F_URL = os.path.join(FONTS, "Poppins-Medium.ttf")              # URL bar


def font(path, size):
    return ImageFont.truetype(path, size)


def paper(size, base, amt=9, seed=7):
    """flat colour with a little paper grain"""
    rng = np.random.default_rng(seed)
    a = np.clip(np.array(base, float)[None, None] + rng.normal(0, amt, (size[1], size[0], 1)), 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGB").filter(ImageFilter.GaussianBlur(0.6)).convert("RGBA")


def cover(img, w=W, h=H):
    """scale-to-fill + centre crop"""
    img = img.convert("RGB")
    k = max(w / img.width, h / img.height)
    im = img.resize((int(img.width * k) + 1, int(img.height * k) + 1), Image.LANCZOS)
    x0, y0 = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")


def wall(spec_wall):
    """spec 'wall': None/'blue' -> brand blue paper; a colour tuple -> paper; a path -> texture"""
    if spec_wall in (None, "blue"): return paper((W, H), BLUE)
    if isinstance(spec_wall, tuple): return paper((W, H), spec_wall)
    p = spec_wall if os.path.exists(spec_wall) else os.path.join(TEXTURES, spec_wall)
    return cover(Image.open(p))


def rounded(img, r):
    img = img.convert("RGBA"); m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], r, fill=255)
    a = np.minimum(np.asarray(img.split()[3]), np.asarray(m)); img.putalpha(Image.fromarray(a))
    return img


def sticker(img, border=12):
    """white outline + soft drop shadow (used for cutouts and the intro card — NOT for photo pops)"""
    pad = border * 3
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.paste(img, (pad, pad), img)
    g = big.split()[3].filter(ImageFilter.MaxFilter(border * 2 + 1)) if border > 0 else big.split()[3]
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    sh = Image.new("RGBA", big.size, (20, 20, 40, 0)); sh.putalpha(g.point(lambda v: int(v * 0.3)).filter(ImageFilter.GaussianBlur(10)))
    out.alpha_composite(sh, (6, 12))
    wh = Image.new("RGBA", big.size, WHITE + (0,)); wh.putalpha(g)
    out.alpha_composite(wh); out.alpha_composite(big)
    return out


_CARD = {}
def card(img, r=40):
    """screen recording framed as a white rounded phone card"""
    if img.size not in _CARD:
        _CARD[img.size] = sticker(rounded(Image.new("RGB", img.size, WHITE), r))
    b = _CARD[img.size].copy(); b.alpha_composite(rounded(img, r), (36, 36)); return b


def soft(img, blur=7, dy=4, op=200):
    """soft drop shadow for text"""
    pad = 30
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (15, 10, 25, 0)); a = Image.new("L", out.size, 0); a.paste(img.split()[3], (pad + 2, pad + dy))
    sh.putalpha(a.point(lambda v: v * op // 255).filter(ImageFilter.GaussianBlur(blur)))
    out.alpha_composite(sh); out.alpha_composite(img, (pad, pad)); return out


def load(path, w=None, h=None, r=0, outline=0):
    """image for a pop: resize by width or height, optional rounded corners, optional white outline (cutouts)"""
    im = Image.open(path).convert("RGBA")
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    elif h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if r: im = rounded(im, r)
    if outline: im = sticker(im, outline)
    return im


def place(fr, img, cx, cy):
    fr.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))


def url_bar(url):
    bar = Image.new("RGBA", (980, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(bar)
    d.rounded_rectangle([24, 30, 954, 168], 69, fill=(25, 20, 40, 90))
    d.rounded_rectangle([10, 10, 940, 148], 69, fill=WHITE, outline=INK, width=6)
    d.ellipse([58, 52, 104, 98], outline=INK, width=7); d.line([(98, 92), (122, 116)], fill=INK, width=8)
    size = 58
    while font(F_URL, size).getlength(url) > 760: size -= 2
    d.text((150, 79), url, font=font(F_URL, size), fill=INK, anchor="lm")
    return bar


def cutout_white_bg(src, dst, ymax=None, tol_min=205, tol_sat=22):
    """remove a plain white/near-white background (e.g. a website card), crop off text below ymax"""
    from scipy import ndimage
    im = Image.open(src).convert("RGBA")
    if ymax: im = im.crop((0, 0, im.width, ymax))
    a = np.array(im).astype(int); rgb = a[..., :3]
    sat = rgb.max(2) - rgb.min(2)
    bg = ((rgb.min(2) > tol_min) & (sat < tol_sat)) | (a[..., 3] < 20)
    lab, n = ndimage.label(~bg)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.02 * sizes.max()])
    keep = ndimage.binary_fill_holes(keep)
    m = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(m); im.crop(im.getbbox()).save(dst)
