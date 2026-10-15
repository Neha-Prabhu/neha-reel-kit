"""Snow the rabbit up for adoption on Pawmuch (pawmuch.com). One-off reel.
Media (src/, img/, build/) is not in git (script-specific).
No .srt (Edits has no export): LINES from an offline transcript of the A-roll, names corrected by hand."""

AROLL = "src/aroll.MP4"
SRT = None
WORDS_JSON = "build/words.json"  # word timings from an offline timestamped transcript of the rough cut (names fixed)
LINES = [
    "Wait, you can adopt a rabbit?",
    "So we built Pawmuch for rescues of mostly kittens and dogs.",
    "But someone ended up posting a rabbit over there. His name is Snow, he's from Greater Noida",
    "and he's less than 1 year old. Apparently he eats everything, veggies, fruits, so basically a better diet than us.",
    "So if you've ever wanted a pet that doesn't knock off things",
    "from your table at 3am",
    "or",
    "bark at delivery guys,",
    "(unclear)",
    "why not a rabbit?",
    "Yeah, crazy things happen so go check out Pawmuch.",
]

SEGS = [  # (source start, source end, speed)
    (0.00, 1.53, 1.1),   # 0  Wait, you can adopt a rabbit?   <- hook
    (1.70, 5.11, 1.1),   # 1  So we built Pawmuch for rescues of mostly kittens and dogs
    (5.30, 9.66, 1.1),   # 2  But someone ended up posting a rabbit over there. His name is Snow ... Greater Noida
    (9.70, 15.36, 1.1),  # 3  and he's less than 1 year old ... better diet than us
    (15.49, 18.07, 1.1), # 4  So if you've ever wanted a pet that doesn't knock off things
    (18.23, 19.49, 1.1), # 5  from your table at 3am
    (19.82, 20.13, 1.1), # 6  or
    (20.40, 21.69, 1.1), # 7  bark at delivery guys
    (21.98, 23.78, 1.1), # 8  ?? (couldn't make out — ask her)
    (24.05, 25.20, 1.1), # 9  why not a rabbit?
    (25.42, 28.17, 1.1), # 10 Yeah, crazy things happen so go check out Pawmuch
]

WALL = None
INTRO = None
HOOK_END = None

# hook: knife-bunny sticker (bg removed -> white outline) beside her head from the first frame; clears at the end of the hook line
# listing card: her Pawmuch screenshot cropped to the card, lands on "rabbit", stays while she reads out his details.
#   middle row of the 3x3 grid (y 640-1280), right column = away from her face (build/faces.json)
POPS = [
    dict(img="img/01_hook_knife_bunny_cutout.png", w=370, outline=10, at=0.03, until=("cut", 0), x=860, y=650),
    dict(img="img/02_listing_card_keep-bg.png", w=360, r=22, at=("w", 2, "rabbit"), until=("cut", 3), x=880, y=975),
]
BROLL = []
WEIGHTED = []
# kinetic captions in Margarine: words appear as she says them, key words butter + bigger, auto-placed around the pops / her face
CAPTIONS = dict(font="Margarine-Regular.ttf", size=78, y=1140, key_scale=1.3, faces="build/faces.json",
                key=[(0, "rabbit"), (1, "Pawmuch"), (1, "kittens"), (1, "dogs"), (2, "rabbit"), (2, "Snow"),
                     (2, "Greater"), (2, "Noida"), (3, "1"), (3, "year"), (3, "veggies"), (3, "fruits"), (3, "diet"),
                     (4, "pet"), (5, "3am"), (7, "delivery"), (7, "guys"), (9, "rabbit"), (10, "Pawmuch")])
NO_CAPTION_LINES = [8]           # line 8 = the bit I couldn't make out
URL = ""
URL_AT = ("w", 10, "check")
HOLD = 1.3
ZOOMS = []
