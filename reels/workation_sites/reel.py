"""Workation websites — one-off reel: Drive & Listen, Radio Garden, WindowSwap.
Screen recordings (Mac, 1920x1164) go full-focus on a wall card; image pops only alternate left/right."""

AROLL = "src/aroll.mp4"
SRT = None
# exact spoken words (offline Whisper per segment + Vosk timings), one string per SEGS entry
LINES = [
    "Here are 3 websites that will make you feel like you're on a workation without being on one.",
    "First one is Drive and Listen.",
    "You just pick a city and it shows you a video of you driving through it.",
    "And the radio that is playing is that city's actual radio*.",         # she said "video" — captioned radio* (her call)
    "For example, I just tried Ahmedabad and Bangalore for you.",          # both recordings are Bangalore — fine by her
    "And of course you can see the traffic.",
    "The next one is Radio Garden.",
    "Here you spin the globe and tap on any dot.",
    "And now you're listening to that place's live radio right now.",
    "And the last one is my favourite, that is WindowSwap.",
    "People from all over the world have posted a video of the view from their window",
    "so that the others can enjoy it.",
    "Some have rain, some have traffic, some have just plants over the balcony.",
    "It's really pretty and I think you should try it.",
    "So save this for the next time you're bored of your playlist while working.",
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {(12, "rain"): 29.82, (12, "some", 0): 30.15, (12, "have", 1): 30.30, (12, "traffic"): 30.45,
            (12, "some", 1): 30.96, (12, "have", 2): 31.08, (12, "just"): 31.20, (12, "plants"): 31.50}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed)
    (0.01, 3.49, 1.1),    # 0  hook
    (3.50, 4.83, 1.1),    # 1  First one is Drive and Listen.
    (4.85, 8.07, 1.1),    # 2  pick a city ... driving through it
    (8.07, 10.93, 1.1),   # 3  actual radio
    (11.18, 14.05, 1.1),  # 4  Ahmedabad and Bangalore
    (14.07, 15.55, 1.1),  # 5  see the traffic
    (15.81, 17.10, 1.1),  # 6  The next one is Radio Garden.
    (17.11, 19.51, 1.1),  # 7  spin the globe, tap on any dot
    (19.93, 22.98, 1.1, 2.3),  # 8  live radio right now  + 2.3 s silence: Mumbai radio plays (under the card)
    (22.99, 25.13, 1.1),  # 9  last one ... WindowSwap
    (25.26, 29.28, 1.1),  # 10 people from all over the world ...
    (29.29, 30.91, 1.1),  # 11 so that the others can enjoy it
    (30.95, 34.95, 1.2),  # 12 rain / traffic / plants (list line)
    (35.01, 36.99, 1.1),  # 13 really pretty
    (36.99, 39.94, 1.1),  # 14 save this
]

WALL = None
INTRO = None
HOOK_END = None

POPS = [
    dict(img="img/00_hook_providence.png", at=0.0, until=("cut", 0), x=540, y=385, sfx=False),          # text hook (make_hook.py)
    dict(img="img/01_beach-laptop_sticker.png", w=280, outline=10, at=("w", 0, "workation"), until=("cut", 0), x=905, y=830),
    dict(img="img/14_save_sticker.png", h=170, outline=10, at=("w", 14, "save"), until=(("end", 14), 1.5), x=925, y=900),
]

# Mac screen recordings 1920x1164: crop the browser bar (top 52 px) -> 1920x1112. Punch-ins keep the same aspect.
FULL = (0, 52, 1920, 1112)
CARD = dict(width=920, y=820, cap_y=1250)                 # full-focus: white card on the wall, captions under it
DL, RG, WS = "src/driveandlisten.mov", "src/radiogarden.mov", "src/windowswap.mov"
TO = "src/driveandlisten_toronto.mov"                     # Retina 3434x2080 — same layout x1.7885
K = 3434 / 1920
T = lambda b: tuple(int(round(v * K)) for v in b)
DL_AD = [(1525, 668, 380, 360)]                           # sidebar ad (cropped-recording pixels)
RG_AD = [(1575, 12, 345, 300)]                            # top-right ad
OVER = dict(over=True, width=820, x=540, y=1195, cap_y=1490, border=8, r=18)   # B-roll ON her A-roll, white border
BROLL = [
    # Drive & Listen — lines 2-5: Toronto while she explains, Bangalore night on "Ahmedabad", Bangalore day on "Bangalore"
    dict(src=TO, at=("cut", 1), until=("cut", 2), start=0.0, crop=T(FULL), blur=[T(b) for b in DL_AD], **CARD),          # pick a city -> video
    dict(src=TO, at=("cut", 2), until=("cut", 3), start=12.0, crop=T((1360, 300, 560, 324)), sfx=False, **CARD),       # radio: punch-in on the station panel (playing)
    dict(src=TO, at=("cut", 3), until=("w", 4, "Ahmedabad"), start=9.0, crop=T(FULL), blur=[T(b) for b in DL_AD], sfx=False, **CARD),
    dict(src=DL, at=("w", 4, "Ahmedabad"), until=("w", 4, "Bangalore"), start=0.5, crop=FULL, blur=DL_AD, sfx=False, **CARD),
    dict(src=DL, at=("w", 4, "Bangalore"), until=("cut", 5), start=7.3, crop=FULL, blur=DL_AD, sfx=False, **CARD),      # daytime traffic
    # Radio Garden — lines 7-8
    dict(src=RG, at=("cut", 6), until=("w", 7, "tap"), start=1.2, speed=2.0, crop=FULL, blur=RG_AD, **CARD),      # spin the globe
    dict(src=RG, at=("w", 7, "tap"), until=("cut", 7), start=19.3, crop=FULL, blur=RG_AD, sfx=False, **CARD),     # tap Mumbai
    dict(src=RG, at=("cut", 7), until=("w", 8, "live"), start=21.0, crop=FULL, blur=RG_AD, sfx=False, **CARD),
    dict(src=RG, at=("w", 8, "live"), until=("cut", 8), start=22.5, crop=(0, 793, 640, 371), sfx=False, **CARD),  # punch-in: Mumbai station playing
    # WindowSwap — lines 9-11 stay on her A-roll (her call), line 12: windows over her A-roll
    dict(src=WS, at=("cut", 11), until=("w", 12, "traffic"), start=28.0, crop=FULL, **OVER),                      # rain (Bangalore pool)
    dict(src=WS, at=("w", 12, "traffic"), until=("w", 12, "plants"), start=42.0, crop=FULL, **OVER),              # city view — no traffic window in the recording
    dict(src=WS, at=("w", 12, "plants"), until=("cut", 12), start=5.0, crop=FULL, **OVER),                         # plants
]
EXTRA_SFX = [("build/rg_radio_beat.wav", ("w", 8, "live"), 1.0)]   # Mumbai station: soft under "live radio right now", full in the pause
WEIGHTED = [   # website names: butter, big, below her face
    (1, "Drive", 3, 540, -1380),
    (6, "Radio", 2, 540, -1380),
    (9, "WindowSwap", 1, 540, -1380),
]
URL = ""
URL_AT = ("w", 0, "here")
HOLD = 1.3
ZOOMS = []
