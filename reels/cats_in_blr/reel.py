"""Cats in Bangalore up for adoption — Pawmuch (pawmuch.com). One-off reel.
Media (src/, img/, build/) is not in git (script-specific).
Card pops are rebuilt from her Pawmuch listing screenshots with tools/pawmuch_card.py so all five match."""

AROLL = "src/aroll.MP4"
SRT = None                       # Edits has no .srt export -> she sends the caption text after draft 1
WORDS_JSON = "build/words.json"

# rough cut: (source start, source end, speed) — one entry per spoken phrase (words from an offline transcript, approx)
SEGS = [
    (0.00, 2.75, 1.1),   # 0  ...if you've been thinking about adopting a cat
    (3.02, 4.03, 1.1),   # 1  I mean, getting
    (4.63, 6.97, 1.1),   # 2  one of these babies might literally be waiting for you
    (7.57, 8.76, 1.1),   # 3  This is Hachimi
    (8.95, 11.97, 1.1),  # 4  an anime reference. I mean who would not want ...
    (12.39, 12.77, 1.2), # 5  Hachimi?
    (12.90, 13.30, 1.2), # 6  ... I don't know
    (14.32, 17.32, 1.1), # 7  but she ... known to run around the house
    (17.54, 19.02, 1.1), # 8  Then this, Kiki and Konan
    (19.13, 21.10, 1.1), # 9  two really really cuddly sisters
    (21.12, 22.71, 1.1), # 10 then we have Salt and Pepper
    (22.76, 24.68, 1.1), # 11 ... at this point
    (24.79, 26.91, 1.1), # 12 This is Nala, she's also from Bangalore
    (26.95, 30.01, 1.1), # 13 waiting for her next cuddle partner because she loves loves sleeping
    (30.14, 39.43, 1.1), # 14 and finally we have this majestic looking Bingus ... zero survival instincts. More more more such good kitties
    (39.50, 41.69, 1.1), # 15 up for adoption from Bangalore right now
    (41.86, 44.24, 1.1), # 16 so if you are looking for a kitten
    (44.51, 45.65, 1.1), # 17 please please please
    (45.82, 47.16, 1.1), # 18 go to pawmuch.com
    (47.22, 48.36, 1.1), # 19 apply to adopt
    (48.50, 50.17, 1.1), # 20 get connected with them
    (50.23, 52.22, 1.1), # 21 and get your next cuddly partner
]

WALL = None
INTRO = None
HOOK_END = None

# card pops: all five built by tools/pawmuch_card.py at the same size; lands on the cat's name
CARD_W = 580
BROLL = []
WEIGHTED = []
NO_CAPTION_LINES = list(range(len(SEGS)))   # draft 1: no captions yet (she sends the text)
URL = ""
URL_AT = ("w", 18, "go")
HOLD = 1.3
ZOOMS = []

# x = side she gestures to; y keeps the card below her chin and above the bottom 20%
POPS = [
    dict(img="img/03_hachimi_card.png",     w=CARD_W, at=("w", 3, "goose"),   until=("cut", 7),       x=320, y=1215),
    dict(img="img/08_kiki_konan_card.png",  w=CARD_W, at=("w", 8, "gig"),     until=("w", 10, "salt"), x=760, y=1215),
    dict(img="img/10_salt_pepper_card.png", w=CARD_W, at=("w", 10, "salt"),   until=("cut", 11),      x=320, y=1215),
    dict(img="img/12_nala_card.png",        w=CARD_W, at=("w", 12, "not"),    until=("cut", 13),      x=760, y=1215),
    dict(img="img/14_bingus_card.png",      w=CARD_W, at=("w", 14, "hurting"), until=("w", 14, "more"), x=320, y=1215),
]
