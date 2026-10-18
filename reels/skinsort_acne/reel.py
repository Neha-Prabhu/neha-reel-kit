"""Skin story — skinsort.com finds what broke me out (one-off talking reel). Media (src/, img/, build/) not in git.
Trims agreed with Neha (cut only, no reshoot): "Story time," / "and what not" / "I went onto this website," / "Well,".
Product + brand names blurred in every screen recording (don't give the brands a bad name)."""

AROLL = "src/aroll.MP4"
SRT = None                       # Edits has no .srt export
ASR_JSON = "build/asr_cut.json"  # Vosk on build/voice_clean.wav; text from Whisper small.en
LINES = [
    "My skin went from this",
    "to this,",
    "and no, this isn't sponsored.",
    "I had started to break out last year and I didn't know what to do.",
    "I went to multiple dermats and they say",
    "it could be adult acne, it could be hormones, it could be stress.",
    "When nothing helped, I found this website",
    "where if you add your skincare products and makeup products,",
    "it tells you whether it might have caused your acne or not.",
    "Added every single product I use",
    "and it flagged my foundation,",
    "the thing that I use every day.",
    "Also pointed out a few more irritating ingredients in my other products.",
    "After I switched them out, you can see the difference.",
    "And I don't like to gatekeep such websites.",
    "This is the link and you do not have to comment for it.",
]
WORD_FIX = {(15, "the"): 26.28, (15, "link"): 26.37}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed)
    (0.00, 1.04, 1.1),   # 0  My skin went from this
    (1.13, 1.62, 1.1),   # 1  to this,
    (1.82, 3.35, 1.1),   # 2  and no, this isn't sponsored.
    (3.99, 6.62, 1.1),   # 3  [Story time,] I had started to break out last year ...
    (6.73, 8.34, 1.1),   # 4  I went to multiple dermats and they say
    (8.34, 11.47, 1.2),  # 5  it could be adult acne, ... hormones, ... stress   [and what not — cut]
    (12.60, 14.35, 1.1), # 6  When nothing helped, I found this website
    (14.64, 16.90, 1.1), # 7  where if you add your skincare products and makeup products,
    (17.55, 20.33, 1.1), # 8  it tells you whether it might have caused your acne or not.
    (22.07, 24.17, 1.1), # 9  [I went onto this website,] added every single product I use
    (24.47, 26.14, 1.1), # 10 and it flagged my foundation,
    (26.38, 27.89, 1.1), # 11 the thing that I use every day.
    (28.17, 31.32, 1.1), # 12 Also pointed out a few more irritating ingredients in my other products.
    (31.49, 33.30, 1.1), # 13 After I switched them out, you can see the difference.
    (33.75, 35.18, 1.1), # 14 And I don't like to gatekeep such websites.
    (36.27, 38.38, 1.1), # 15 [Well,] this is the link and you do not have to comment for it.
]

WALL = None                      # brand blue
INTRO = None
HOOK_END = None

# Pops: middle row of the 3x3 grid, left/right column, below her face (face track: x ~300-720, y ~520-900).
L_X, R_X, CY = 190, 890, 1040
POPS = [
    # hook: "from THIS (before) ... to THIS (after)" — back to back, both stay through "isn't sponsored"
    dict(img="img/01_before_photo.jpg", w=330, r=22, at=("w", 0, "this"), until=("cut", 2), x=L_X, y=CY),
    dict(img="img/02_after_photo.jpg",  w=330, r=22, at=("w", 1, "this"), until=("cut", 2), x=R_X, y=CY),
    # "multiple dermats" -> her pill-bottle illustration (photo pop, bg kept)
    dict(img="img/pills.jpg", w=360, r=22, at=("w", 4, "dermats"), until=("cut", 4), x=R_X - 10, y=CY - 20),
    # "you can SEE the difference" -> self-obsessed kitten (photo pop, rembg can't separate white fur from the bg)
    dict(img="img/kitten.jpg", w=330, r=22, at=("w", 13, "see"), until=("w", 14, "like"), x=R_X - 10, y=CY - 10),
    # link ending: site screenshot in the left column, URL bar on top
    dict(img="img/15_site_home.png", w=380, r=22, at=("w", 15, "link"), until=999, x=L_X + 20, y=CY, sfx=False),
]

# Screen recordings = desktop (3432x2080). Each step gets its own crop (jump-zoom), ad bar + browser/URL bar cropped off.
# Product + brand names blurred everywhere (blur boxes are in cropped-source pixels).
REC = "src/foundation_flag.mov"
BROLL = [
    # "I FOUND this website" -> skinsort home
    dict(src=REC, at=("w", 6, "found"), until=("cut", 6), start=1.0, crop=(330, 110, 2550, 1450),
         width=880, y=820, cap_y=1200, sfx=False),
    # "where if you add your skincare..." -> typing in search, then the result list, click (src 1.9 -> 5.9)
    dict(src=REC, at=("cut", 6), until=14.87, start=1.9, crop=(990, 470, 1400, 1200),
         blur=[(60, 60, 460, 100), (190, 160, 1110, 1010)], width=760, y=800, cap_y=1265, sfx=False),
    # "... caused your acne or not. / Added every single product I use" -> product page, Save goes dark (src 7.9)
    dict(src=REC, at=14.87, until=("cut", 9), start=6.4, crop=(240, 330, 2560, 1330),
         blur=[(60, 50, 840, 850), (1010, 40, 1040, 175)], width=880, y=820, cap_y=1185, sfx=False),
    # "and it FLAGGED my foundation" -> zoom on What's inside (red X: pore-clogger, fungal-acne, fragrance...)
    dict(src=REC, at=("cut", 9), until=("cut", 10), start=8.9, crop=(1230, 1280, 1560, 370),
         width=900, y=840, cap_y=1080, sfx=False),
    # "a few more irritating ingredients in my other products" -> the "Not a match" box of another product (no names in crop)
    dict(src="src/other_flags.mov", at=("cut", 11), until=("cut", 12), start=0.0, speed=0.5, crop=(1240, 760, 1200, 770),
         width=820, y=820, cap_y=1215, sfx=False),
]

# "adult acne / hormones / stress" -> butter words, left / right / left, pop on each
WEIGHTED = [
    (5, "adult", 2, 215, 1040),
    (5, "hormones,", 1, 850, 1020),
    (5, "stress.", 1, 220, 1020),
]
URL = "skinsort.com"
URL_AT = ("w", 15, "link")
URL_Y = 300
HOLD = 1.3
ZOOMS = []

EXTRA_SFX = [  # (file, at, volume) — subtle
    ("pop.mp3", ("w", 5, "adult"), 0.18), ("pop.mp3", ("w", 5, "hormones"), 0.18), ("pop.mp3", ("w", 5, "stress"), 0.18),
    ("whoosh_soft.mp3", (("w", 6, "found"), -0.05), 0.35),        # into the website
    ("build/typing_cut.wav", ("cut", 6), 0.30),                     # typing in the search
    ("mouse_click.mp3", 14.84, 0.45),                               # selects the product
    ("mouse_click.mp3", 16.36, 0.45),                               # Save
    ("ding.mp3", ("w", 10, "flagged"), 0.30),                      # the flag
    ("whoosh_soft.mp3", (("cut", 10), -0.05), 0.30),               # back to her
    ("whoosh_soft.mp3", (("cut", 11), -0.05), 0.30),               # into the other product
    ("ding.mp3", ("w", 12, "irritating"), 0.18), ("ding.mp3", ("w", 12, "products"), 0.18),
    ("whoosh_soft.mp3", (("cut", 12), -0.05), 0.30),               # back to her
    ("sparkle.mp3", ("w", 13, "see"), 0.35),                        # "you can see the difference"
    ("ding.mp3", ("w", 15, "link"), 0.22),                          # link
]
