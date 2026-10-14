"""Rebuild a Pawmuch listing screenshot as a clean, consistent card pop.

Every card comes out the same size and layout (photo, "Cat" pill, name, pin + location, 2-line description),
so a reel with several listings doesn't jump between screenshot crops.

  python tools/pawmuch_card.py out.png photo.jpg x0 y0 x1 y1 "Name" "Location" "Description" [--pill Cat]
      photo.jpg + box = the photo area of her screenshot (crop is filled to the card's photo ratio)

Fonts match the site: Fredoka (name), Nunito (body/location). Emojis via Noto Color Emoji.
"""
import argparse, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(KIT, "assets", "fonts"); UI = os.path.join(KIT, "assets", "logos-and-ui")
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

CW, PH = 1000, 860                       # card width, photo height
CREAM = (254, 253, 248); INK = (72, 54, 50); PLUM = (116, 62, 86); PILL = (223, 237, 202)
R = 44                                   # corner radius


def f(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)


def emoji(ch, h):
    fe = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=fe, embedded_color=True)
    im = im.crop(im.getbbox()); return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


EMO = re.compile(r"([\U0001F300-\U0001FAFF☀-➿]️?)")


def runs(text):
    return [p for p in EMO.split(text) if p]


def run_w(parts, font, eh):
    return sum(emoji(p, eh).width + 6 if EMO.fullmatch(p) else font.getlength(p) for p in parts)


def wrap(text, font, maxw, eh, lines=2):
    words = text.split(); out = []; cur = ""
    for i, w in enumerate(words):
        t = (cur + " " + w).strip()
        if run_w(runs(t), font, eh) <= maxw: cur = t; continue
        out.append(cur); cur = w
        if len(out) == lines:
            last = out[-1]
            while run_w(runs(last + "..."), font, eh) > maxw: last = last[:-1].rstrip()
            out[-1] = last.rstrip(",. ") + "..."; return out
    out.append(cur); return out[:lines]


def draw_runs(card, d, xy, parts, font, fill, eh):
    x, y = xy
    for p in parts:
        if EMO.fullmatch(p):
            e = emoji(p, eh); card.alpha_composite(e, (int(x) + 3, int(y - e.height + 6))); x += e.width + 6
        else:
            d.text((x, y), p, font=font, fill=fill, anchor="ls"); x += font.getlength(p)


def build(photo, box, name, loc, desc, pill="Cat", shadow=True):
    card = Image.new("RGBA", (CW, 1220), CREAM + (255,)); d = ImageDraw.Draw(card)
    # photo: fill the card's photo ratio from the given box (centre crop of the box if ratios differ)
    src = Image.open(photo).convert("RGB").crop(box)
    k = max(CW / src.width, PH / src.height)
    src = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
    x0, y0 = (src.width - CW) // 2, (src.height - PH) // 2
    card.paste(src.crop((x0, y0, x0 + CW, y0 + PH)), (0, 0))
    # pill
    pf = f("Nunito-Bold.ttf", 44); icon = Image.open(os.path.join(UI, "pawmuch_cat_icon.png")).convert("RGBA")
    icon = icon.resize((int(icon.width * 56 / icon.height), 56), Image.LANCZOS)
    pw = 36 + icon.width + 16 + int(pf.getlength(pill)) + 40; phh = 94
    px, py = 40, PH - 40 - phh
    d.rounded_rectangle([px, py, px + pw, py + phh], phh // 2, fill=PILL)
    card.alpha_composite(icon, (px + 36, py + (phh - icon.height) // 2))
    d.text((px + 36 + icon.width + 16, py + phh // 2 + 2), pill, font=pf, fill=INK, anchor="lm")
    # text panel
    L = 48; y = PH + 38
    nf = f("Fredoka-SemiBold.ttf", 80)
    while nf.getlength(name) > CW - 2 * L: nf = f("Fredoka-SemiBold.ttf", nf.size - 2)
    d.text((L, y + 72), name, font=nf, fill=INK, anchor="ls"); y += 96
    pin = Image.open(os.path.join(UI, "pawmuch_pin.png")).convert("RGBA"); pin = pin.resize((int(pin.width * 46 / pin.height), 48), Image.LANCZOS)
    card.alpha_composite(pin, (L, y + 6))
    d.text((L + pin.width + 14, y + 44), loc, font=f("Nunito-Bold.ttf", 44), fill=PLUM, anchor="ls"); y += 72
    df = f("Nunito-Regular.ttf", 45)
    for i, line in enumerate(wrap(desc, df, CW - 2 * L, 44)):
        draw_runs(card, d, (L, y + 46 + i * 62), runs(line), df, INK, 44)
    # rounded card + soft shadow (no border)
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], R, fill=255)
    card.putalpha(m)
    if not shadow: return card
    pad = 60; out = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (30, 15, 25, 0)); a = Image.new("L", out.size, 0); a.paste(m, (pad, pad + 14))
    sh.putalpha(a.point(lambda v: int(v * 0.32)).filter(ImageFilter.GaussianBlur(22)))
    out.alpha_composite(sh); out.alpha_composite(card, (pad, pad))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("photo"); ap.add_argument("box", nargs=4, type=int)
    ap.add_argument("name"); ap.add_argument("loc"); ap.add_argument("desc"); ap.add_argument("--pill", default="Cat")
    ap.add_argument("--no-shadow", action="store_true")
    a = ap.parse_args()
    build(a.photo, tuple(a.box), a.name, a.loc, a.desc, a.pill, not a.no_shadow).save(a.out)
    print(a.out)
