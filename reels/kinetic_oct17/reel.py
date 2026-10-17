"""Comment-for-link addiction — the new Instagram addiction (one-off talking reel, kinetic Diagramm captions)."""

AROLL = "src/aroll.mp4"
SRT = None
# exact spoken words (offline Whisper per segment + Vosk), one string per SEGS entry
LINES = [
    "There's a new level of Instagram addiction that has been unlocked",
    "in this era,",
    "and you know what is that?",
    "It started off with us opening Instagram more frequently.",
    "Then it started off as doomscrolling",
    "that happened when they made the reel tab as the main tab.",
    "And now the new addiction",
    "is comment for this link.",
    "I have been posting my doomscrolling series lately",
    "and I always end it with saying you do not have to comment for the link",
    "and people still comment.",
    "I mean...",
    "look at this.",
    "And I realized",
    "this is a new form of addiction that now Instagram has given us.",
    "So please be mindful of your scrolling next time.",
    "So yeah,",
    "that's the content.",
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed)
    (0.00, 3.06, 1.1),   # 0  There's a new level of Instagram addiction that has been unlocked
    (3.45, 4.34, 1.1),   # 1  in this era,
    (4.41, 5.41, 1.1),   # 2  and you know what is that?
    (5.43, 8.66, 1.1),   # 3  It started off with us opening Instagram more frequently.
    (8.91, 10.75, 1.1),  # 4  Then it started off as doomscrolling
    (10.75, 13.10, 1.1), # 5  that happened when they made the reel tab as the main tab.
    (13.19, 15.45, 1.1), # 6  And now the new addiction
    (15.68, 17.47, 1.1), # 7  is comment for this link.
    (18.03, 20.66, 1.1), # 8  I have been posting my doomscrolling series lately
    (20.79, 23.68, 1.1), # 9  and I always end it with saying you do not have to comment for the link
    (23.76, 25.40, 1.1), # 10 and people still comment.
    (25.50, 26.03, 1.1), # 11 I mean...
    (26.52, 27.36, 1.1), # 12 look at this.
    (28.02, 29.12, 1.1), # 13 And I realized
    (29.38, 33.16, 1.1), # 14 this is a new form of addiction that now Instagram has given us.
    (33.16, 35.36, 1.1), # 15 So please be mindful of your scrolling next time.
    (35.44, 36.24, 1.1), # 16 So yeah,
    (36.49, 37.52, 1.1), # 17 that's the content.
]

WALL = None
INTRO = None
HOOK_END = None

POPS = []
BROLL = []
WEIGHTED = []
CAPTIONS = dict(font="Diagramm-UltraBoldItalic.ttf", size=72, y=1140, key_scale=1.3, faces="build/faces.json",
                key=[(0, "addiction"), (0, "unlocked"), (1, "era"), (3, "Instagram"), (3, "frequently"),
                     (4, "doomscrolling"), (5, "reel"), (5, "main"), (6, "addiction"), (7, "comment"), (7, "link"),
                     (8, "doomscrolling"), (9, "not"), (10, "still"), (10, "comment"), (14, "addiction"),
                     (15, "mindful"), (17, "content")])
URL = ""
URL_AT = ("w", 0, "here")
HOLD = 1.3
ZOOMS = []
