"""Text hook: a big '3' with 'workation / websites' stacked beside it (each line half the 3's height).
'3' = pink from her t-shirt, words = butter yellow, hard ink shadow (no blur, no outline).

  python make_hook.py monigue      -> img/00_hook_monigue.png    (Monigue has no digits: the 3 is Diagramm)
  python make_hook.py providence   -> img/00_hook_providence.png
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(D, "..", "..", "assets", "fonts")
STYLE = sys.argv[1] if len(sys.argv) > 1 else "monigue"
FONT = os.path.join(F, {"monigue": "Monigue.otf", "providence": "ProvidenceSans.ttf"}[STYLE])
NUM = os.path.join(F, "Diagramm-UltraBoldItalic.ttf") if STYLE == "monigue" else FONT
PINK, BUTTER, INK, SH = (242, 189, 218), (247, 226, 122), (38, 32, 44), 7


def glyphs(text, size, col):
    f = ImageFont.truetype(NUM if text.isdigit() else FONT, size); bb = f.getbbox(text)
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), text, font=f, fill=col)
    return im


def fit_h(text, h, col):          # font size whose ink height is h
    s = h
    while glyphs(text, s, col).height > h: s -= 2
    while glyphs(text, s + 2, col).height <= h: s += 2
    return glyphs(text, s, col)


GAP = 22
three = fit_h("3", 300, PINK)
l1 = fit_h("workation", (three.height - GAP) // 2, BUTTER)
l2 = fit_h("websites", (three.height - GAP) // 2, BUTTER)
txt = Image.new("RGBA", (three.width + 30 + max(l1.width, l2.width), three.height), (0, 0, 0, 0))
txt.alpha_composite(three, (0, 0))
x = three.width + 30
txt.alpha_composite(l1, (x, 0)); txt.alpha_composite(l2, (x, three.height - l2.height))
if txt.width > 960: txt = txt.resize((960, int(txt.height * 960 / txt.width)), Image.LANCZOS)
out = Image.new("RGBA", (txt.width + SH, txt.height + SH), (0, 0, 0, 0))
sh = Image.new("RGBA", txt.size, INK + (255,)); sh.putalpha(txt.split()[3])
out.alpha_composite(sh, (SH, SH)); out.alpha_composite(txt, (0, 0))
p = os.path.join(D, "img", f"00_hook_{STYLE}.png"); out.save(p); print(p, out.size)
