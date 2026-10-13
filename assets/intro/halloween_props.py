"""usage: python halloween_props.py <frames_in> <frames_out>
Halloween version of the stop-motion desk intro (Day 5 only): draws flat sticker-style props onto frames_notext.
Props keep clear of the title area (upper wall) and her face."""
import glob, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import sys
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
INK = (38, 32, 44); ORANGE = (240, 128, 40); ORANGE_D = (205, 95, 25); PURPLE = (150, 95, 200); GREEN = (95, 140, 70)
WHITE = (255, 255, 255)
S = 3  # supersample


def outline(img, border=8, shadow=True):
    pad = border * 3
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(img, (pad, pad))
    g = big.split()[3].filter(ImageFilter.MaxFilter(border * 2 + 1))
    out = Image.new("RGBA", big.size, (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", big.size, (20, 20, 40, 0)); sh.putalpha(g.point(lambda v: int(v * 0.28)).filter(ImageFilter.GaussianBlur(6)))
        out.alpha_composite(sh, (4, 8))
    wh = Image.new("RGBA", big.size, WHITE + (0,)); wh.putalpha(g)
    out.alpha_composite(wh); out.alpha_composite(big); return out


def canvas(w, h):
    return Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))


def done(im):
    return im.resize((im.width // S, im.height // S), Image.LANCZOS)


def pumpkin(w=190):
    h = int(w * 0.85); im = canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = im.size
    d.rounded_rectangle([W_ * .46, 0, W_ * .56, H_ * .2], 8 * S, fill=GREEN)
    for x0, x1, c in [(0, .45, ORANGE_D), (.55, 1, ORANGE_D), (.12, .62, ORANGE), (.38, .88, ORANGE)]:
        d.ellipse([W_ * x0, H_ * .12, W_ * x1, H_], fill=c)
    d.ellipse([W_ * .25, H_ * .12, W_ * .75, H_], fill=ORANGE)
    # face
    d.polygon([(W_ * .30, H_ * .48), (W_ * .42, H_ * .48), (W_ * .36, H_ * .34)], fill=INK)
    d.polygon([(W_ * .58, H_ * .48), (W_ * .70, H_ * .48), (W_ * .64, H_ * .34)], fill=INK)
    d.chord([W_ * .26, H_ * .42, W_ * .74, H_ * .86], 10, 170, fill=INK)
    d.rectangle([W_ * .40, H_ * .62, W_ * .46, H_ * .69], fill=ORANGE); d.rectangle([W_ * .54, H_ * .62, W_ * .60, H_ * .69], fill=ORANGE)
    return outline(done(im))


def bat(w=120):
    h = int(w * 0.5); im = canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = im.size
    pts = [(0, H_ * .25), (W_ * .18, H_ * .05), (W_ * .30, H_ * .35), (W_ * .42, H_ * .2), (W_ * .5, H_ * .3), (W_ * .58, H_ * .2),
           (W_ * .70, H_ * .35), (W_ * .82, H_ * .05), (W_, H_ * .25), (W_ * .86, H_ * .55), (W_ * .76, H_ * .5), (W_ * .66, H_ * .78),
           (W_ * .5, H_ * .62), (W_ * .34, H_ * .78), (W_ * .24, H_ * .5), (W_ * .14, H_ * .55)]
    d.polygon(pts, fill=INK)
    d.ellipse([W_ * .40, H_ * .15, W_ * .60, H_ * .55], fill=INK)
    d.polygon([(W_ * .41, H_ * .22), (W_ * .43, 0), (W_ * .48, H_ * .2)], fill=INK); d.polygon([(W_ * .52, H_ * .2), (W_ * .57, 0), (W_ * .59, H_ * .22)], fill=INK)
    d.ellipse([W_ * .44, H_ * .3, W_ * .48, H_ * .36], fill=(250, 220, 80)); d.ellipse([W_ * .52, H_ * .3, W_ * .56, H_ * .36], fill=(250, 220, 80))
    return outline(done(im), 6)


def ghost(w=110):
    h = int(w * 1.15); im = canvas(w, h); d = ImageDraw.Draw(im); W_, H_ = im.size
    d.ellipse([0, 0, W_, W_], fill=WHITE); d.rectangle([0, W_ / 2, W_, H_ * .85], fill=WHITE)
    for k in range(4):
        d.ellipse([W_ * k / 4, H_ * .75, W_ * (k + 1) / 4, H_], fill=WHITE)
    d.ellipse([W_ * .28, W_ * .35, W_ * .40, W_ * .52], fill=INK); d.ellipse([W_ * .60, W_ * .35, W_ * .72, W_ * .52], fill=INK)
    d.ellipse([W_ * .44, W_ * .58, W_ * .56, W_ * .72], fill=INK)
    g = done(im)
    return outline(g, 6)   # sticker on the laptop


def spider(w=110):
    im = canvas(w, w); d = ImageDraw.Draw(im); W_ = im.size[0]; c = W_ / 2
    for side in (-1, 1):
        for k in range(4):
            a = math.radians(-50 + k * 33)
            x1, y1 = c + side * W_ * .22 * math.cos(a), c + W_ * .22 * math.sin(a)
            x2, y2 = c + side * W_ * .46 * math.cos(a - .5), c + W_ * .40 * math.sin(a) + W_ * .12
            d.line([(c, c), (x1, y1), (x2, y2)], fill=INK, width=5 * S, joint="curve")
    d.ellipse([c - W_ * .2, c - W_ * .2, c + W_ * .2, c + W_ * .24], fill=INK)
    d.ellipse([c - W_ * .08, c - W_ * .06, c - W_ * .02, c + W_ * .02], fill=WHITE); d.ellipse([c + W_ * .02, c - W_ * .06, c + W_ * .08, c + W_ * .02], fill=WHITE)
    return outline(done(im), 5)


def cobweb(r=230):
    im = canvas(r, r); d = ImageDraw.Draw(im); R = im.size[0]; col = (255, 255, 255, 235)
    angs = [0, 18, 36, 54, 72, 90]
    for a in angs:
        d.line([(R, 0), (R - R * math.cos(math.radians(a)), R * math.sin(math.radians(a)))], fill=col, width=3 * S)
    for k in range(1, 5):
        rr = R * k / 4.6
        pts = [(R - rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a))) for a in angs]
        for p0, p1 in zip(pts, pts[1:]):
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            sag = 0.12 * rr
            ctl = (mx - sag * 0.7, my + sag * 0.7)
            seg = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * ctl[0] + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * ctl[1] + u * u * p1[1]) for u in np.linspace(0, 1, 12)]
            d.line(seg, fill=col, width=3 * S)
    return done(im)


def bunting(width=1080, n=11):
    im = canvas(width, 120); d = ImageDraw.Draw(im); Wd = im.size[0]
    d.line([(0, 18 * S), (Wd / 2, 40 * S), (Wd, 18 * S)], fill=INK, width=3 * S)
    for k in range(n):
        x0 = Wd * (k + .1) / n; x1 = Wd * (k + .9) / n; xm = (x0 + x1) / 2
        y = 18 * S + (40 - 18) * S * (1 - abs(xm - Wd / 2) / (Wd / 2))
        d.polygon([(x0, y), (x1, y), (xm, y + 80 * S)], fill=[ORANGE, PURPLE, INK][k % 3])
    return done(im)


PUMPKIN, GHOST, SPIDER, WEB, FLAGS = pumpkin(), ghost(), spider(), cobweb(), bunting(880, 9)
BATS = [bat(130), bat(100), bat(85)]

frames = sorted(glob.glob(f"{SRC}/f*.png"))
for i, p in enumerate(frames):
    fr = Image.open(p).convert("RGBA")
    rng = np.random.default_rng(100 + i)
    j = lambda a=3: tuple(int(v) for v in rng.integers(-a, a + 1, 2))   # stop-motion jitter
    fr.alpha_composite(FLAGS, (105, 1290))                               # bunting hanging off the desk edge
    fr.alpha_composite(WEB, (1080 - WEB.width, 0))                         # cobweb, top-right corner
    # bats flapping beside the lamp and under the pegboard (wing size wobbles per frame = flap)
    for k, (b, (x, y)) in enumerate(zip(BATS, [(20, 860), (900, 930), (30, 985)])):
        s = 1.0 if (i + k) % 2 == 0 else 0.85
        bb = b.resize((b.width, max(1, int(b.height * s))), Image.LANCZOS)
        dx, dy = j(4); fr.alpha_composite(bb, (x + dx, y + dy + (b.height - bb.height) // 2))
    # spider dangling on a thread from the top, bobbing
    sy = 640 + int(18 * math.sin(i * 0.8))
    ImageDraw.Draw(fr).line([(1052, 0), (1052, sy)], fill=(70, 60, 80), width=3)
    fr.alpha_composite(SPIDER, (1052 - SPIDER.width // 2, sy - 16))
    # pumpkin on the book stack, ghost sticker on the laptop
    dx, dy = j(2); fr.alpha_composite(PUMPKIN, (905 - PUMPKIN.width // 2 + dx, 1085 - PUMPKIN.height + 22 + dy))
    fr.alpha_composite(GHOST, (722 - GHOST.width // 2, 1190 - GHOST.height // 2))   # over the heart sticker
    fr.convert("RGB").save(f"{OUT}/{os.path.basename(p)}")
print(len(frames), "frames")
