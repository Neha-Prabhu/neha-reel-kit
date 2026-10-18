"""Asteroid Launcher — Things I Found on the Internet, Day 5 (neal.fun/asteroid-launcher). First split-screen reel."""

AROLL = "src/aroll.mp4"
SRT = None
# exact spoken words (offline Whisper per segment + Vosk), one string per SEGS entry
LINES = [
    "This is such a cool website.",
    "So I found a website where I can launch an asteroid on any part of the earth and see how the results look like",
    "and I chose to destroy New York City for no reason.",
    "Today is day 5 of things I found on the internet instead of doomscrolling.",
    "Here I am, let me choose an asteroid.",
    "Oh, gold asteroid.",
    "Let me choose random settings.",
    "This will create a 25 kilometer wide crater apparently.",
    "So an estimated of 3 million people would be vaporized in the crater.",
    "The impact is equivalent to...",
    "400 gigatons of TNT",
    "and it would create a 48 kilometer",
    "of wide fireball.",
    "And how big is that? Oh, it's big.",
    "Oh, an estimation of 3 million people would receive 3rd degree burns.",
    "and then there is a 246 decibel shock wave that would",
    "kill almost...",
    "I should not use the word kill,",
    "that would impact almost 8 million people.",
    "and a 5 km/s peak wind",
    "would destroy 8 million people again.",
    "Wow.",
    "I mean this is so interesting. If you want to try this out, you do not have to comment for the link. Because here it is.",
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed)
    (0.30, 2.25, 1.1),    # 0  This is such a cool website.
    (2.49, 7.62, 1.1),    # 1  So I found a website ... results look like
    (7.71, 10.08, 1.1),   # 2  and I chose to destroy New York City for no reason.
    (10.59, 13.75, 1.1),  # 3  Today is day 5 ...
    (14.01, 15.90, 1.1),  # 4  Here I am, let me choose an asteroid.      <- split screen starts
    (18.39, 19.50, 1.2),  # 5  Oh, gold asteroid.                         (cut "uh, Carbon- oh, uh" fumble before it)
    (19.62, 21.78, 1.2),  # 6  Let me choose random settings.
    (22.98, 25.90, 1.1),  # 7  This will create a 25 kilometer wide crater apparently.
    (26.19, 29.42, 1.1),  # 8  So an estimated of 3 million people ...
    (29.55, 31.10, 1.1),  # 9  The impact is equivalent to...
    (31.41, 33.52, 1.1),  # 10 400 gigatons of TNT
    (33.60, 36.95, 1.1),  # 11 and it would create a 48 kilometer
    (37.22, 38.33, 1.1),  # 12 of wide fireball.
    (38.34, 40.95, 1.1),  # 13 And how big is that? Oh, it's big.
    (41.37, 45.25, 1.1),  # 14 Oh, an estimation of 3 million people ... burns.
    (45.66, 48.93, 1.1),  # 15 and then there is a 246 decibel shock wave that would   (hiccup kept, 'oops' pop)
    (49.05, 50.20, 1.1),  # 16 kill almost...
    (50.33, 51.88, 1.1),  # 17 I should not use the word kill,
    (52.02, 54.72, 1.1),  # 18 that would impact almost 8 million people.
    (54.86, 57.10, 1.1),  # 19 and a 5 km/s peak wind
    (57.51, 60.10, 1.1),  # 20 would destroy 8 million people again.
    (60.54, 61.00, 1.2),  # 21 Wow.                                       (unclear rest of the line cut — ask her)
    (62.67, 68.02, 1.1),  # 22 I mean this is so interesting ... here it is.   <- back to full frame
]

WALL = None
INTRO = dict(line=3, frames="build/intro_frames", label="Day 5", title="Things I Found on the Internet Instead of Doomscrolling")
#   build intro frames (classic blue):  python assets/intro/build_intro.py --out reels/split_site_oct18/build/intro_frames
HOOK_END = None

POPS = [
    dict(img="img/02_nyc_crater.png", w=330, r=22, at=("w", 2, "New"), until=("cut", 2), x=855, y=900, sfx=False),
    # blooper kept on purpose: hiccup between "decibel" and "shock" -> "oops ✦" next to her face (bottom panel)
    dict(img="img/15_oops.png", at=36.18, until=("cut", 15), x=800, y=1010, sfx=False),
]
BROLL = []
FULL = (0, 50, 1920, 1080)                            # whole site, browser bar cropped (16:9)
PANEL = lambda y: (1280, y, 640, 360)                  # punch-in on the results column (+ a bit of map)
SPLIT = dict(
    at=("cut", 3), until=("cut", 21), src="src/site_rec.mp4", wall=None, sfx=False,   # whoosh_soft in EXTRA_SFX
    top=(90, 200, 900, 506), bottom=(90, 846, 900, 690), face_crop=(0, 470, 1080, 828), cap_y=776,
    blur=[(8, 52, 170, 60)],                           # NEAL.FUN logo — link only shows at the end
    clips=[
        dict(at=("cut", 3), rec=9.0, speed=2.0, crop=(1200, 70, 720, 405)),     # 4  let me choose an asteroid
        dict(at=("cut", 4), rec=16.2, speed=1.0, crop=(1200, 70, 720, 405)),    # 5  oh, gold asteroid
        dict(at=("cut", 5), rec=17.3, speed=2.0, crop=(1200, 330, 720, 405)),   # 6  random settings (sliders)
        dict(at=("cut", 6), rec=26.6, speed=1.5, crop=FULL),                    # 7  launch -> impact
        dict(at=("w", 7, "25"), rec=33.0, speed=1.0, crop=(500, 100, 1420, 799)),  # 7  25 km wide crater
        dict(at=("cut", 7), rec=36.0, speed=1.0, crop=PANEL(300)),              # 8  3 million vaporized
        dict(at=("cut", 8), rec=40.0, speed=1.0, crop=PANEL(560)),              # 9-10 equivalent to 400 gigatons
        dict(at=("cut", 10), rec=53.0, speed=1.0, crop=PANEL(760)),             # 11 48 km ...
        dict(at=("cut", 11), rec=65.6, speed=1.0, crop=FULL),                   # 12 wide fireball
        dict(at=("cut", 12), rec=72.0, speed=1.0, crop=FULL),                   # 13 how big is that
        dict(at=("cut", 13), rec=74.0, speed=1.0, crop=PANEL(380)),             # 14 3rd degree burns
        dict(at=("cut", 14), rec=80.0, speed=1.0, crop=FULL),                   # 15-16 shock wave rings
        dict(at=("cut", 17), rec=88.0, speed=1.0, crop=PANEL(470)),             # 18 8 million people
        dict(at=("cut", 18), rec=94.0, speed=1.0, crop=FULL),                   # 19 peak wind
        dict(at=("cut", 19), rec=100.0, speed=1.0, crop=PANEL(50)),             # 20 destroy 8 million again
        dict(at=("cut", 20), rec=102.0, speed=1.0, crop=FULL),                  # 21 wow
    ],
)
# SFX: "space disaster movie, but sassy" — quiet, under her voice. (file, at, volume); kit sfx or reel-local src/ file
EXTRA_SFX = [
    ("impact_boom.mp3", (("w", 2, "New"), -0.05), 0.20),       # crater pop on "New York City"
    ("whoosh_soft.mp3", (("cut", 3), -0.12), 0.30),           # split screen comes in
    ("mouse_click.mp3", (("cut", 3), 0.55), 0.30),            # clicking through asteroids
    ("mouse_click.mp3", (("cut", 3), 1.15), 0.30),
    ("sparkle.mp3", ("w", 5, "gold"), 0.28),                  # gold asteroid
    ("mouse_click.mp3", (("cut", 5), 0.45), 0.20),            # sliders
    ("mouse_click.mp3", (("cut", 5), 1.10), 0.20),
    ("impact_boom.mp3", (("cut", 6), 0.25), 0.38),            # launch flash (rec 27.0 at 1.5x)
    ("src/sfx_riser_tail.wav", (("w", 10, "400"), -2.40), 0.30),  # builds under "equivalent to..." -> peaks on 400
    ("fire_whoosh.mp3", (("cut", 11), -0.05), 0.32),          # wide fireball
    ("pop.mp3", 36.18, 0.14),                                 # oops
    ("impact_boom_big.mp3", (("w", 15, "shock"), -0.03), 0.30),  # 246 decibel shock wave
    ("src/sfx_scratch_short.wav", (("cut", 16), -0.42), 0.20),  # "kill almost..." record scratch
]
WEIGHTED = []
URL = "neal.fun/asteroid-launcher"
URL_AT = ("w", 22, "here")
HOLD = 1.3
ZOOMS = []
