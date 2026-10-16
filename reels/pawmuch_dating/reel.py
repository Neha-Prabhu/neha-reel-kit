"""Cats with 'dating profiles' — Pawmuch (pawmuch.com). One-off reel.
Media (src/, img/, build/) is not in git (script-specific).
Card pops rebuilt from her Pawmuch listing screenshots with tools/pawmuch_card.py so all four match."""

AROLL = "src/aroll.MP4"
SRT = None                       # Edits has no .srt export
ASR_JSON = "build/asr_cut.json"  # Vosk word timings on build/voice_clean.wav; text from Whisper small.en per segment
LINES = [
    "I think I found a website where cats might have dating profiles.",
    "So this is Nacho and Taco.",
    "One has nacho like ears and the other has a taco shell on his head.",
    "This is Hotchy Potchy,",
    "who is an absolute diva.",
    "This is Milo, who's known as Professional Cuddle Inspector.",
    "And then this one,",
    "the future CEO of your house.",
    "Except these are not dating profiles, they're real animals looking for a home.",
    "So go to this website, scroll,",
    "find your match and apply and wait for a reply,",
    "just like your dating apps.",
    "It's called Pawmuch and the link is in my bio.",
]
WORD_FIX = {}
WORDS_JSON = "build/words.json"

SEGS = [
    (0.00, 3.18, 1.1),   # 0  I think I found a website where cats might have dating profiles.
    (3.31, 4.56, 1.1),   # 1  So this is Nacho and Taco.
    (4.92, 8.47, 1.1),   # 2  One has nacho like ears and the other has a taco shell on his head.
    (8.73, 10.00, 1.1),  # 3  This is Hotchy Potchy,
    (10.23, 12.14, 1.1), # 4  who is an absolute diva.
    (12.29, 15.10, 1.1), # 5  This is Milo, who's known as Professional Cuddle Inspector.
    (15.26, 16.20, 1.2), # 6  And then this one,
    (16.23, 17.99, 1.1), # 7  the future CEO of your house.
    (18.08, 21.31, 1.1), # 8  Except these are not dating profiles, they're real animals looking for a home.
    (21.54, 23.04, 1.1), # 9  So go to this website, scroll,
    (23.28, 25.58, 1.2), # 10 find your match and apply and wait for a reply,
    (25.83, 27.15, 1.1), # 11 just like your dating apps.
    (27.52, 29.66, 1.1), # 12 It's called Pawmuch and the link is in my bio.
]

WALL = None
INTRO = None
HOOK_END = None

# ("cut", n) = the picture cut at the END of line n.
# --- pops. Middle row of the 3x3 grid, side picked from the face track (build/faces.json): her face sits centre-right
#     for Nacho/Hotchy/Poppy and centre-left for Milo + the ending, so it's L, L, R, L, R rather than strict alternation.
CARD_W = 500                     # cards from tools/pawmuch_card.py, all identical
CY = 1020
L_X, R_X = 262, 818
POPS = [
    # text hook (mockup C, built by make_hook.py): top, clear of the IG header, through the opening line, no pop sound
    dict(img="img/00_hook.png", at=0.0, until=("cut", 0), x=540, y=355, sfx=False),
    dict(img="img/02_nacho_taco_card.png", w=400, at=("w", 1, "Nacho"),  until=("cut", 2), x=215, y=CY),
    dict(img="img/04_hotchy_card.png",     w=400, at=("w", 3, "Hotchy"), until=("cut", 4), x=215, y=CY),
    dict(img="img/05_milo_card.png",       w=CARD_W, at=("w", 5, "Milo"),   until=("cut", 5), x=R_X, y=CY - 100),
    dict(img="img/06_poppy_card.png",      w=CARD_W, at=("w", 6, "this"),   until=("cut", 7), x=L_X, y=CY),
    # ending: her Pawmuch homepage screenshot (desktop hero card, nav cropped) under the URL bar
    dict(img="img/12_homepage.png", w=460, r=24, at=("w", 12, "Pawmuch"), until=999, x=840, y=CY),
]
# "go to this website, scroll / find your match and apply" -> her recording, phone card on the pink wall.
# Stops at the Apply tap (src ~17.3 s): from ~18.2 s the form shows her name, email and phone number.
_B = dict(src="src/08_scroll.mov", crop=(0, 145, 1180, 2115), width=620, y=830, cap_y=1480, wall="pink_paper.jpg")
BROLL = [   # jump cuts at near-real speed (one scroll, open a profile, Apply) instead of one sped-up run
    dict(_B, at=("cut", 8),          until=("cut", 9),          start=1.0,  speed=1.5),   # one scroll through listings
    dict(_B, at=("cut", 9),          until=("w", 10, "apply"),  start=8.4,  speed=2.0),   # tapping into Coco = "your match"
    dict(_B, at=("w", 10, "apply"),  until=("cut", 10),         start=16.9, speed=1.0),   # Apply to adopt tap
]
WEIGHTED = []
CAPTIONS = dict(font="Margarine-Regular.ttf", size=72, y=1140, key_scale=1.3, maxw=1040, faces="build/faces.json",
                key=[(1, "Nacho"), (1, "Taco"), (2, "nacho"), (2, "ears"),
                     (2, "taco"), (2, "shell"), (3, "Hotchy"), (3, "Potchy"), (4, "diva"), (5, "Milo"),
                     (5, "Cuddle"), (5, "Inspector"), (7, "CEO"), (8, "real"), (8, "animals"),
                     (8, "home"), (9, "scroll"), (10, "match"), (10, "apply"), (10, "reply"), (11, "dating"),
                     (11, "apps"), (12, "Pawmuch"), (12, "bio")])
URL = "pawmuch.com"
URL_AT = ("w", 12, "Pawmuch")
URL_Y = 300
HOLD = 1.3
ZOOMS = []
# slow zooms (trial): A-roll in ~2-3 s blocks, alternating slow zoom-in / zoom-out, resets on the line cuts
SLOW_ZOOM = dict(amount=1.07, min=2.0, pattern="iio")
