"""Wayback Machine (web.archive.org) — one-off, landscape A-roll kept landscape on the brand wall.

A-roll: iPhone 1440x2560 file with the landscape shot letterboxed inside (picture = 1440x808 at y 876) -> AROLL_WIDE
cuts the picture out at full quality; SOLO centres it on the wall. Screen recording = FULL FOCUS (replaces her
completely, never split): jump cuts of typing the URL -> calendar -> YouTube 2005. Screenshots pop on the wall above
her window; the album + book stickers pop on the side of her window away from her face.
"""

AROLL = "src/aroll.mp4"
AROLL_WIDE = ("src/aroll.mp4", "1440:808:0:876", 1440, 808)   # roughcut --wide -> build/roughcut_wide.mp4
SRT = None
LINES = [
    "So you know how your mom has that one album of your 2008 horrible pictures? The internet also has one.",  # 0
    "You type in any website,",                                                    # 1
    "pick a year and it shows you exactly what the site looked like back then.",    # 2
    "Not a description, the actual site.",                                         # 3
    "So the first thing I did was check what",                                     # 4
    "Flipkart was in 2008 and guess what they were selling?",                      # 5
    "Books.",                                                                      # 6
    "Only books. Bro was basically a library with a delivery boy.",                # 7
    "And Zomato?",                                                                 # 8
    "It wasn't even called Zomato back then.",                                     # 9
    "It was called FoodieBay.",                                                    # 10
    "Sounds like my cousin's Instagram handle.",                                   # 11
    "This website has saved over trillions of web pages across the internet since 1996.",  # 12
    "So that the internet never forgets.",                                         # 13
    "Well, the site is called the Wayback Machine and here is the link.",          # 14
    "So let me know in the comments what your favorite website looked like back in 2008.",  # 15
    "Bye.",                                                                        # 16
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed) — cut where each word's tail dies (~-58 dB)
    (0.00, 5.27, 1.1),    # 0
    (5.32, 6.55, 1.1),    # 1
    (6.68, 9.90, 1.1),    # 2
    (9.94, 11.86, 1.1),   # 3
    (12.42, 14.00, 1.1),  # 4
    (14.10, 16.64, 1.1),  # 5
    (16.83, 17.36, 1.1),  # 6
    (17.42, 20.33, 1.1),  # 7
    (20.44, 21.27, 1.1),  # 8
    (21.29, 23.17, 1.1),  # 9
    (23.21, 24.64, 1.1),  # 10
    (24.70, 26.55, 1.2),  # 11 throwaway
    (26.57, 31.78, 1.1),  # 12
    (31.90, 33.66, 1.1),  # 13
    (33.78, 36.65, 1.1),  # 14
    (36.80, 40.72, 1.1),  # 15
    (41.13, 41.62, 1.1),  # 16
]

WALL = None                      # brand blue paper wall
INTRO = None
HOOK_END = None

FACE = (490, 760, 640, 930)       # her face inside the SOLO window (frame px) — pops stay in the side columns, clear of it
POPS = [
    # text hook (her script's hook, make_hook.py): top wall above her window, through the opening line, no pop sound
    dict(img="img/00_hook.png", at=0.0, until=("cut", 0), x=540, y=400, sfx=False),
    dict(img="img/00_album_sticker.png", w=300, outline=10, at=("w", 0, "album"), until=("w", 0, "The"), x=880, y=910),
    # screenshots: on the wall above her window (too detailed for a side-column pop), Wayback toolbar cropped off
    dict(img="img/05_flipkart.png", w=880, r=22, at=("w", 5, "Flipkart"), until=("cut", 7), x=540, y=455),
    dict(img="img/07_book_sticker.png", w=330, outline=10, at=("w", 6, "Books"), until=("w", 7, "Bro"), x=205, y=930),   # gone on "Bro"
    dict(img="img/10_foodiebay.png", w=880, r=22, at=("w", 10, "FoodieBay"), until=("cut", 11), x=540, y=480),
    # the reveal: Wayback logo (same one blurred in the screen recording) on "Wayback", under the URL bar, to the end
    dict(img="img/14_wayback_logo.png", w=600, r=22, at=("w", 14, "Wayback"), until=99, x=540, y=540),
]
# screen recording = FULL FOCUS: replaces her completely (wall + white card), jump cuts per phrase, browser bar +
# Internet Archive nav cropped, Wayback logo blurred until she names it at the end. Same 900x520 card for every clip.
REC = "src/rec.mov"
BROLL = [
    dict(src=REC, at=("cut", 0), until=("cut", 1), start=0.4, speed=2.0, crop=(520, 150, 920, 532),        # typing youtube.com
         blur=[(105, 25, 235, 90)], width=900, y=800, cap_y=1300),
    dict(src=REC, at=("cut", 1), until=("w", 2, "and"), start=4.2, speed=2.0, crop=(300, 300, 1320, 763),  # clicks 2005
         width=900, y=800, cap_y=1300, sfx=False),
    dict(src=REC, at=("w", 2, "and"), until=("w", 2, "what"), start=6.0, speed=1.3, crop=(300, 300, 1320, 763),  # picks a date
         width=900, y=800, cap_y=1300, sfx=False),
    dict(src=REC, at=("w", 2, "what"), until=("w", 3, "the"), start=42.0, speed=1.0, crop=(480, 120, 940, 543),  # YouTube, 2005
         width=900, y=800, cap_y=1300, sfx=False),
    dict(src=REC, at=("w", 3, "the"), until=("cut", 3), start=45.0, speed=1.0, crop=(500, 120, 700, 404),   # punch-in: the actual site
         width=900, y=800, cap_y=1300, sfx=False),
]
EXTRA_SFX = [
    ("build/typing_1s.wav", ("cut", 0), 0.16),
    ("mouse_click.mp3", (("w", 2, "and"), 0.35), 0.30),
    ("mouse_click.mp3", (("w", 2, "what"), -0.05), 0.30),
]
SOLO = dict(src="build/roughcut_wide.mp4", box=(90, 708, 900, 505), crop=(0, 0, 1440, 808), cap_y=1300)
WEIGHTED = [(12, "trillions", 1, 540, 470), (12, "1996.", 1, 540, 470)]   # numbers that carry the line, on the wall above her
URL = "web.archive.org"
URL_AT = ("w", 14, "here")
HOLD = 1.3
ZOOMS = []
