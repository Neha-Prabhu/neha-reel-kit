"""Text hook: a big '3' with 'workation / websites' stacked beside it (each line half the 3's height) -> img/00_hook.png.
White Monigue, hard ink shadow (no blur, no outline)."""
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(D, "..", "..", "assets", "fonts")
FONT = os.path.join(F, "Monigue.otf")
NUM = os.path.join(F, "Diagramm-UltraBoldItalic.ttf")   # Monigue has no digits
WHITE, INK, SH = (255, 255, 255), (38, 32, 44), 7


def glyphs(text, size):
    f = ImageFont.truetype(NUM if text.isdigit() else FONT, size); bb = f.getbbox(text)
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), text, font=f, fill=WHITE)
    return im


def fit_h(text, h):          # font size whose ink height is h
    s = h
    while glyphs(text, s).height > h: s -= 2
    while glyphs(text, s + 2).height <= h: s += 2
    return glyphs(text, s)


GAP = 22
three = fit_h("3", 300)
l1 = fit_h("workation", (three.height - GAP) // 2)
l2 = fit_h("websites", (three.height - GAP) // 2)
Wd = three.width + 30 + max(l1.width, l2.width)
txt = Image.new("RGBA", (Wd, three.height), (0, 0, 0, 0))
txt.alpha_composite(three, (0, 0))
x = three.width + 30
txt.alpha_composite(l1, (x, 0)); txt.alpha_composite(l2, (x, three.height - l2.height))
if txt.width > 960: txt = txt.resize((960, int(txt.height * 960 / txt.width)), Image.LANCZOS)
out = Image.new("RGBA", (txt.width + SH, txt.height + SH), (0, 0, 0, 0))
sh = Image.new("RGBA", txt.size, INK + (255,)); sh.putalpha(txt.split()[3])
out.alpha_composite(sh, (SH, SH)); out.alpha_composite(txt, (0, 0))
out.save(os.path.join(D, "img", "00_hook.png")); print(out.size)
