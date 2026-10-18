"""Text hook 'Internet / on a pizza' in Providence Sans (her words), two lines, hard ink shadow (no blur, no outline).
'Internet' butter yellow, 'on a pizza' pink — same palette as the workation hook.   python make_hook.py -> img/00_hook.png
"""
import os
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); FONT = os.path.join(D, "..", "..", "assets", "fonts", "ProvidenceSans.ttf")
PINK, BUTTER, INK, SH = (242, 189, 218), (247, 226, 122), (38, 32, 44), 7


def line(text, size, col):
    f = ImageFont.truetype(FONT, size); bb = f.getbbox(text)
    im = Image.new("RGBA", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - bb[0], 2 - bb[1]), text, font=f, fill=col)
    return im


l1, l2 = line("Internet", 150, BUTTER), line("time machine", 150, PINK)
txt = Image.new("RGBA", (max(l1.width, l2.width), l1.height + 26 + l2.height), (0, 0, 0, 0))
txt.alpha_composite(l1, ((txt.width - l1.width) // 2, 0)); txt.alpha_composite(l2, ((txt.width - l2.width) // 2, l1.height + 26))
if txt.width > 900: txt = txt.resize((900, int(txt.height * 900 / txt.width)), Image.LANCZOS)
out = Image.new("RGBA", (txt.width + SH, txt.height + SH), (0, 0, 0, 0))
sh = Image.new("RGBA", txt.size, INK + (255,)); sh.putalpha(txt.split()[3])
out.alpha_composite(sh, (SH, SH)); out.alpha_composite(txt, (0, 0))
os.makedirs(os.path.join(D, "img"), exist_ok=True)
p = os.path.join(D, "img", "00_hook.png"); out.save(p); print(p, out.size)
