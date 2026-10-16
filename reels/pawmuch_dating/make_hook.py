"""Text hook 'Cat Dating App' + pink 'it's a match!' pill (mockup C) -> img/00_hook.png (transparent, 1080 wide)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(D, "..", "..", "assets", "fonts")
W, H = 1080, 300
im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fm = ImageFont.truetype(os.path.join(F, "Monigue.otf"), 170)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 4, 116), "Cat Dating App", font=fm, fill=(0, 0, 0, 150), anchor="mm")
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
d = ImageDraw.Draw(im); d.text((W / 2, 110), "Cat Dating App", font=fm, fill=(255, 255, 255), anchor="mm")
pf = ImageFont.truetype(os.path.join(F, "Fredoka-Bold.ttf"), 40)
d.rounded_rectangle((W / 2 - 200, 190, W / 2 + 200, 260), radius=35, fill=(232, 120, 150))
d.text((W / 2, 225), "it's a match!", font=pf, fill=(255, 255, 255), anchor="mm")
im.crop(im.getbbox()).save(os.path.join(D, "img", "00_hook.png"))
