"""Text hook 'CD burner / in 2026' in Providence Sans (her words), two lines, hard ink shadow (no blur, no outline).
'CD burner' butter yellow, 'in 2026' pink — same palette as the earlier hooks. Her CD photo -> round sticker
(circle cut, the reel adds the white outline) that sits beside the text.   python make_hook.py
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


l1, l2 = line("CD burner", 150, BUTTER), line("in 2026", 150, PINK)
txt = Image.new("RGBA", (max(l1.width, l2.width), l1.height + 26 + l2.height), (0, 0, 0, 0))
txt.alpha_composite(l1, ((txt.width - l1.width) // 2, 0)); txt.alpha_composite(l2, ((txt.width - l2.width) // 2, l1.height + 26))
if txt.width > 640: txt = txt.resize((640, int(txt.height * 640 / txt.width)), Image.LANCZOS)
out = Image.new("RGBA", (txt.width + SH, txt.height + SH), (0, 0, 0, 0))
sh = Image.new("RGBA", txt.size, INK + (255,)); sh.putalpha(txt.split()[3])
out.alpha_composite(sh, (SH, SH)); out.alpha_composite(txt, (0, 0))
os.makedirs(os.path.join(D, "img"), exist_ok=True)
p = os.path.join(D, "img", "00_hook.png"); out.save(p); print(p, out.size)

# CD sticker: circle cut of her photo (the disc fills the frame)
cd = Image.open(os.path.join(D, "img", "00_cd_sticker.jpg")).convert("RGBA")
S = 4; m = Image.new("L", (cd.width * S, cd.height * S), 0)
ImageDraw.Draw(m).ellipse([3 * S, 3 * S, (cd.width - 3) * S, (cd.height - 3) * S], fill=255)
cd.putalpha(m.resize(cd.size, Image.LANCZOS))
p = os.path.join(D, "img", "00_cd_sticker.png"); cd.save(p); print(p, cd.size)
