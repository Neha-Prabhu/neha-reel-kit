"""Cats in Bangalore up for adoption — Pawmuch (pawmuch.com). One-off reel.
Media (src/, img/, build/) is not in git (script-specific).
Card pops are rebuilt from her Pawmuch listing screenshots with tools/pawmuch_card.py so all five match."""

AROLL = "src/aroll.MP4"
SRT = None                       # Edits has no .srt export
ASR_JSON = "build/asr_cut.json"  # Vosk word timings on build/voice_clean.wav; text below from Whisper small.en + her corrections
LINES = [
    "If you're in Bangalore and you've been thinking about adopting a kid",
    "I meant kitten,",
    "one of these babies might literally be waiting for you.",
    "This is Bingus,",
    "and I see the resemblance. I mean, who would not want her? Him? Her?",
    "I don't know.",
    "But she's a tiny sassy lady who's known to run around her house.",
    "Then this, Kiki and Konan,",
    "two very very cuddly sisters.",
    "Then we have Salt and Pepper,",
    "it's self explanatory at this point.",
    "This is Nala, she's also from Bangalore,",
    "waiting for her next cuddle partner because she loves, loves sleeping.",
    "And finally we have this majestic looking Hachimi. She's playful, cuddly and has zero survival instincts.",
    "There are more, more, more such kittens",
    "up for adoption from Bangalore right now.",
    "So if you are looking for a kitten,",
    "please, please, please",
    "go to pawmuch.com,",
    "apply to adopt,",
    "get connected with them,",
    "and get your next cuddly partner.",
]
WORD_FIX = {(6, "a"): 11.2, (6, "tiny"): 11.33, (6, "sassy"): 11.52, (6, "lady"): 11.74, (6, "who's"): 12.0, (6, "known"): 12.17, (6, "to"): 12.43, (6, "run"): 12.5, (6, "around"): 12.67, (6, "her"): 12.94, (6, "house"): 13.0}   # hand fixes where ASR timing was off
WORDS_JSON = "build/words.json"

# rough cut: (source start, source end, speed) — one entry per spoken phrase (words from an offline transcript, approx)
SEGS = [
    (0.00, 2.75, 1.1),   # 0  If you're in Bangalore and you've been thinking about adopting a kid
    (3.02, 4.03, 1.1),   # 1  I meant kitten,
    (4.63, 6.97, 1.1),   # 2  one of these babies might literally be waiting for you.
    (7.57, 8.76, 1.1),   # 3  This is Bingus,
    (8.95, 12.77, 1.1),  # 4  and I see the resemblance. I mean, who would not want her? Him? Her?
    (12.90, 13.70, 1.2), # 5  I don't know.
    (14.32, 17.32, 1.1), # 6  But she's a tiny sassy lady who's known to run around her house.
    (17.54, 19.02, 1.1), # 7  Then this, Kiki and Konan,
    (19.13, 21.10, 1.1), # 8  two very very cuddly sisters.
    (21.12, 22.71, 1.1), # 9  Then we have Salt and Pepper,
    (22.76, 24.68, 1.1), # 10 it's self explanatory at this point.
    (24.79, 26.91, 1.1), # 11 This is Nala, she's also from Bangalore,
    (26.95, 30.10, 1.1), # 12 waiting for her next cuddle partner because she loves, loves sleeping.
    (30.14, 37.12, 1.1), # 13 And finally we have this majestic looking Hachimi. She's playful, cuddly and has zero survival instincts.
    (37.12, 39.43, 1.1), # 14 There are more, more, more such kittens
    (39.50, 41.69, 1.1), # 15 up for adoption from Bangalore right now.
    (41.86, 44.24, 1.1), # 16 So if you are looking for a kitten,
    (44.51, 45.65, 1.1), # 17 please, please, please
    (45.82, 47.16, 1.1), # 18 go to pawmuch.com,
    (47.22, 48.36, 1.1), # 19 apply to adopt,
    (48.50, 50.17, 1.1), # 20 get connected with them,
    (50.23, 52.30, 1.1), # 21 and get your next cuddly partner.
]

WALL = None
INTRO = None
HOOK_END = None

# --- pops. Middle row of the 3x3 grid (y 640-1280), left or right column, always on the side away from her face
#     (face track: build/faces.json). Cards: tools/pawmuch_card.py, all identical. CARD_W includes the card's shadow.
CARD_W = 450
CY = 975                         # card centre = middle row
L_X, R_X = 228, 852              # left / right column centres
POPS = [
    # hook: "adopting a kid" -> "I meant kitten" (stickers: bg removed + white outline)
    dict(img="img/00_kid_cutout.png",     w=300, outline=10, at=("w", 0, "kid"),     until=("w", 1, "kitten"), x=R_X + 20, y=CY + 40),
    dict(img="img/01_kitten_cutout.png",  w=330, outline=10, at=("w", 1, "kitten"),  until=("cut", 2),         x=200, y=1150),
    dict(img="img/14_bingus_card.png",    w=CARD_W, at=("w", 3, "Bingus"),     until=("cut", 6),    x=L_X, y=CY),
    dict(img="img/04_toothless_cutout.png", w=280, outline=10, at=("w", 4, "resemblance"), until=("w", 4, "her"), x=R_X + 40, y=1040),
    dict(img="img/08_kiki_konan_card.png",  w=CARD_W, at=("w", 7, "Kiki"),   until=("cut", 8),    x=R_X, y=CY),
    dict(img="img/10_salt_pepper_card.png", w=CARD_W, at=("w", 9, "Salt"),   until=("cut", 10),   x=L_X, y=CY),
    dict(img="img/12_nala_card.png",        w=CARD_W, at=("w", 11, "Nala"),  until=("cut", 12),   x=R_X, y=CY),
    dict(img="img/03_hachimi_card.png",     w=CARD_W, at=("w", 13, "Hachimi"), until=("cut", 13), x=L_X - 15, y=CY),
    # end: website screenshot (status bar + Safari bar cropped) with the URL bar on top
    dict(img="img/18_site_crop.png", w=320, r=26, at=("w", 18, "pawmuch.com"), until=999, x=185, y=CY + 10),
]
# "There are more, more, more such kittens up for adoption ..." -> her Pawmuch scroll, phone card on the pink wall
BROLL = [
    dict(src="src/14_pawmuch_scroll.MP4", at=("cut", 13), until=("cut", 15), start=4.5, speed=2.6,
         crop=(0, 145, 1180, 2115), width=620, y=830, cap_y=1480, wall="pink_paper.jpg"),
]
WEIGHTED = []
CAPTIONS = dict(font="Margarine-Regular.ttf", size=78, y=1140, key_scale=1.3, faces="build/faces.json",
                key=[(0, "kid"), (1, "kitten"), (3, "Bingus"), (4, "resemblance"), (6, "sassy"), (6, "lady"),
                     (7, "Kiki"), (7, "and"), (7, "Konan"), (9, "Salt"), (9, "and"), (9, "Pepper"), (11, "Nala"),
                     (12, "sleeping"), (13, "Hachimi"), (13, "zero"), (14, "kittens"), (16, "kitten"),
                     (18, "pawmuch.com"), (21, "cuddly"), (21, "partner")])
URL = "pawmuch.com"
URL_AT = ("w", 18, "pawmuch.com")
URL_Y = 300
HOLD = 1.3
ZOOMS = []
