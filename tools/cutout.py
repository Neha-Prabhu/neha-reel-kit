"""Remove a plain white background from a website card image and crop off the text under the object.
  python tools/cutout.py card.png out.png [ymax]        (ymax = y pixel where the card text starts)
Complex backgrounds: use iPhone long-press "lift subject" and save as PNG instead."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit.gfx import cutout_white_bg
cutout_white_bg(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
