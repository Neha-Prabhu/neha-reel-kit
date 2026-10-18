"""Skin story — skinsort.com finds what broke me out (one-off talking reel). Media (src/, img/, build/) not in git.
Trims agreed with Neha (cut only, no reshoot): "Story time, I had started to break out ... what to do." (draft 4) / "and what not" / "I went onto this website," / "Well,".
Product + brand names blurred in every screen recording (don't give the brands a bad name)."""

AROLL = "src/aroll.MP4"
SRT = None                       # Edits has no .srt export
ASR_JSON = "build/asr_cut.json"  # Vosk on build/voice_clean.wav; text from Whisper small.en
LINES = [
    "My skin went from this",
    "to this,",
    "and no, this isn't sponsored.",
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
WORD_FIX = {(14, "link"): 25.47, (3, "dermats"): 3.88, (4, "stress"): 6.70}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed) — draft 2: each line ends where the word's tail actually dies + a short breath
    (0.00, 1.08, 1.1),   # 0  My skin went from this
    (1.13, 1.68, 1.1),   # 1  to this,
    (1.82, 3.45, 1.1),   # 2  and no, this isn't sponsored.
    (6.73, 8.34, 1.1),   # 4  I went to multiple dermats and they say
    (8.34, 11.55, 1.2),  # 5  it could be adult acne, ... hormones, ... stress   [and what not — cut]
    (12.60, 14.43, 1.1), # 6  When nothing helped, I found this website
    (14.64, 16.96, 1.1), # 7  where if you add your skincare products and makeup products,
    (17.55, 20.43, 1.1), # 8  it tells you whether it might have caused your acne or not.
    (22.07, 24.25, 1.1), # 9  [I went onto this website,] added every single product I use
    (24.47, 26.25, 1.1), # 10 and it flagged my foundation,
    (26.38, 28.00, 1.1), # 11 the thing that I use every day.
    (28.17, 31.45, 1.1), # 12 Also pointed out a few more irritating ingredients in my other products.
    (31.49, 33.60, 1.1), # 13 After I switched them out, you can see the difference.   (draft 1 clipped "difference")
    (33.75, 35.55, 1.1), # 14 And I don't like to gatekeep such websites.               (draft 1 clipped "websites")
    (36.27, 38.60, 1.1), # 15 [Well,] this is the link and you do not have to comment for it.
]

WALL = None                      # brand blue
INTRO = None
HOOK_END = None

# Pops: middle row of the 3x3 grid, left/right column, below her face (face track: x ~300-720, y ~520-900).
L_X, R_X, CY = 190, 890, 1040
POPS = [
    # hook: before on top, after below — big, allowed over her face; gone by "this isn't sponsored" (line 2 is clean A-roll)
    dict(img="img/01_before_sq.jpg", w=560, r=28, at=("w", 0, "this"), until=("w", 2, "this"), x=540, y=445),
    dict(img="img/02_after_sq.jpg",  w=560, r=28, at=("w", 1, "this"), until=("w", 2, "this"), x=540, y=1013),
    # "multiple dermats" -> her pill-bottle illustration (photo pop, bg kept)
    dict(img="img/pills.jpg", w=360, r=22, at=("w", 3, "dermats"), until=("cut", 3), x=R_X - 10, y=CY - 20),
    # "you can SEE the difference" -> self-obsessed kitten (photo pop, rembg can't separate white fur from the bg)
    dict(img="img/kitten.jpg", w=330, r=22, at=("w", 12, "see"), until=("w", 13, "like"), x=R_X - 10, y=CY - 10),
    # link ending: skinsort logo, centred just above the captions; URL bar on top
    dict(img="img/15_skinsort_logo.png", w=460, r=24, at=("w", 14, "link"), until=999, x=540, y=1240, sfx=False),
]

# Screen recordings = desktop (3432x2080). Each step gets its own crop (jump-zoom), ad bar + browser/URL bar cropped off.
# Product + brand names blurred everywhere (blur boxes are in cropped-source pixels).
REC = "src/foundation_flag.mov"
SEARCH = (990, 470, 1400, 1200)   # search box crop
TYPED = (60, 60, 460, 100)        # what she typed
PICK = (("cut", 6), 0.97)         # her click on the product (src 5.9)
BROLL = [
    # "I FOUND this website" -> skinsort home
    dict(src=REC, at=("w", 5, "found"), until=("cut", 5), start=1.0, crop=(330, 110, 2550, 1450),
         width=880, y=820, cap_y=1200, sfx=False),
    # "where if you add your skincare..." -> typing. Only the typed text + the product she picks are blurred;
    # the other results stay readable so people see there are options.
    dict(src=REC, at=("cut", 5), until=(("cut", 6), -0.08), start=1.75, crop=SEARCH,
         blur=[TYPED, (90, 480, 480, 75)], width=760, y=800, cap_y=1265, sfx=False),
    # list re-sorted with her product on top -> she clicks it. Every result here is the same brand, so the little
    # brand line under each one is blurred too (otherwise the brand is readable).
    dict(src=REC, at=(("cut", 6), -0.08), until=PICK, start=4.85, crop=SEARCH,
         blur=[TYPED, (90, 190, 480, 75)] + [(195, y - 20, 110, 40) for y in (376, 505, 634, 766, 895, 1024, 1153)],
         width=760, y=800, cap_y=1265, sfx=False),
    # "... caused your acne or not. / Added every single product I use" -> product page (photo + name blurred), Save goes dark
    dict(src=REC, at=PICK, until=("cut", 8), start=6.0, crop=(240, 330, 2560, 1330),
         blur=[(60, 50, 840, 850), (1010, 40, 1040, 175)], width=880, y=820, cap_y=1185, sfx=False),
    # "and it FLAGGED my foundation" -> zoom on What's inside, cursor lands on pore-clogger
    dict(src=REC, at=("cut", 8), until=("cut", 9), start=9.5, crop=(1230, 1280, 1560, 370),
         width=900, y=840, cap_y=1080, sfx=False),
    # "a few more irritating ingredients in my other products" -> "Not a match" box of another product (no names in crop)
    dict(src="src/other_flags.mov", at=("cut", 10), until=("cut", 11), start=0.0, speed=0.5, crop=(1240, 760, 1200, 770),
         width=820, y=820, cap_y=1215, sfx=False),
]

# "adult acne / hormones / stress" -> butter words, left / right / left, pop on each
WEIGHTED = [
    (4, "adult", 2, 215, 1040),
    (4, "hormones,", 1, 850, 1020),
    (4, "stress.", 1, 220, 1020),
]
URL = "skinsort.com"
URL_AT = ("w", 14, "link")
NO_CAPTION_LINES = [0, 1]   # the before/after pops say it
URL_Y = 300
HOLD = 1.3
ZOOMS = []

EXTRA_SFX = [  # (file, at, volume) — subtle
    ("pop.mp3", ("w", 4, "adult"), 0.18), ("pop.mp3", ("w", 4, "hormones"), 0.18), ("pop.mp3", ("w", 4, "stress"), 0.18),
    ("whoosh_soft.mp3", (("w", 5, "found"), -0.05), 0.35),        # into the website
    ("build/typing_cut.wav", (("cut", 5), 0.2), 0.30),                     # typing in the search
    ("mouse_click.mp3", (PICK, -0.03), 0.45),                               # selects the product
    ("mouse_click.mp3", (PICK, 1.88), 0.45),                               # Save
    ("ding.mp3", ("w", 9, "flagged"), 0.30),                      # the flag
    ("whoosh_soft.mp3", (("cut", 9), -0.05), 0.30),               # back to her
    ("whoosh_soft.mp3", (("cut", 10), -0.05), 0.30),               # into the other product
    ("ding.mp3", ("w", 11, "irritating"), 0.18), ("ding.mp3", ("w", 11, "products"), 0.18),
    ("whoosh_soft.mp3", (("cut", 11), -0.05), 0.30),               # back to her
    ("sparkle.mp3", ("w", 12, "see"), 0.35),                        # "you can see the difference"
    ("ding.mp3", ("w", 14, "link"), 0.22),                          # link
]
