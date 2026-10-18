"""Burn CD (burncd.online) — Things I Found on the Internet Instead of Doomscrolling, Day 7.

A-roll: iPhone portrait 1440x2560. Screen recording: Mac Chrome, 3434x2080 @120 fps, with the site's own sounds
(Burn click, drive tray, burn hum, eject) — Neha asked to keep them on the burn B-roll: SITE_AUDIO ->
build_site_audio.py -> build/site_audio.wav -> EXTRA_SFX.
Text hook (her words): "CD burner in 2026" + her CD photo as a sticker beside it (make_hook.py).
"""

AROLL = "src/aroll.mp4"
SRT = None
LINES = [
    "I just burned a CD in 2026",                                  # 0  (unclear: "burned")
    "without a CD drive.",                                         # 1
    "Because honestly Gen Z got robbed of",                        # 2
    "everything cool.",                                            # 3
    "Today is day 7 of things I found on the internet instead of doomscrolling.",  # 4  intro card
    "So burning a CD used to be one whole event.",                 # 5
    "Going to a shop, getting it done,",                           # 6
    "writing with the sketch pen. It is just so nostalgic to me.", # 7
    "And it always ended with",                                    # 8
    "me praying",                                                  # 9
    "it doesn't fail at 98 or 99%.",                               # 10
    "Well, this website",                                          # 11
    "brings it back for us.",                                      # 12
    "You search for the songs and drop them on the disc.",         # 13
    "And then you hit burn and it actually simulates the burn.",   # 14
    "It's so cool.",                                               # 15
    "Once it's done, you can write a cheesy little note and share the CD with someone.",  # 16 (unclear: "the CD")
    "Though, it's only a 30 second preview of the song.",          # 17 (unclear: "Though")
    "But intention matters, right?",                               # 18
    "So you can send it to your friend, your crush,",              # 19
    "not your ex.",                                                # 20
    "And you do not have to comment for the link",                 # 21
    "because here it is.",                                         # 22
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {}
WORDS_JSON = "build/words.json"

SEGS = [  # (source start, source end, speed[, silence after]) — tails cut where the word dies (~-58 dB)
    (0.00, 1.73, 1.1),    # 0
    (1.91, 3.04, 1.1),    # 1
    (3.04, 4.99, 1.1),    # 2
    (5.08, 5.90, 1.1),    # 3
    (5.91, 8.97, 1.1),    # 4  intro
    (9.00, 11.57, 1.1),   # 5
    (11.66, 13.38, 1.2),  # 6  list
    (13.40, 16.30, 1.1),  # 7
    (16.31, 17.51, 1.1),  # 8
    (17.52, 18.25, 1.1),  # 9
    (18.34, 20.58, 1.1),  # 10
    (20.58, 21.74, 1.1),  # 11
    (21.76, 22.91, 1.1),  # 12
    (22.98, 25.14, 1.1),  # 13  ("Let me type" + the restarted "then you hit burn" cut)
    (27.45, 30.26, 1.1, 0.5),  # 14  + 0.5 s of the site's burn sound under the progress bar
    (30.31, 31.21, 1.1),  # 15
    (31.31, 34.69, 1.1),  # 16
    (34.81, 37.57, 1.1),  # 17
    (37.58, 39.08, 1.1),  # 18
    (39.30, 41.07, 1.1),  # 19
    (41.41, 42.49, 1.1),  # 20
    (42.49, 44.29, 1.1),  # 21
    (44.30, 45.37, 1.1),  # 22
]

WALL = None                      # brand blue
INTRO = dict(line=4, frames="build/intro_frames", label="Day 7", title="Things I Found on the Internet Instead of Doomscrolling")
#   python assets/intro/build_intro.py --out reels/cd_burner_oct18/build/intro_frames
HOOK_END = None

POPS = [
    # text hook (her words) + her CD sticker beside it, top of the frame, through the opening line — no pop sound
    dict(img="img/00_hook.png", at=0.0, until=("cut", 1), x=400, y=330, sfx=False),
    dict(img="img/00_cd_sticker.png", w=220, outline=10, at=0.0, until=("cut", 1), x=890, y=330, sfx=False),
    # link ending: the CD player screenshot under the URL bar (both her hands go up into the side columns here)
    dict(img="img/22_player.png", w=290, r=18, at=("w", 22, "here"), until=99, x=540, y=505),
]

REC = "src/rec.mov"
WIZ = (1000, 520, 1416, 1100)    # CD Burn Wizard window (recording px, x y w h) — same 900x700 card for every clip
PLAYER = (780, 330, 1920, 1492)  # case + player + CD Player window (same aspect as WIZ)
CARD = dict(width=900, y=830, cap_y=1420)
BROLL = [
    # 13 search (typing) -> add songs to the disc
    dict(src=REC, at=("cut", 12), until=("w", 13, "drop"), start=4.0, speed=2.5, crop=WIZ, **CARD),
    dict(src=REC, at=("w", 13, "drop"), until=("cut", 13), start=24.0, speed=1.5, crop=WIZ, sfx=False, **CARD),
    # 14 "hit burn" = the click (rec 32.0 lands on "burn") -> drive tray -> progress bar filling
    dict(src=REC, at=("cut", 13), until=("w", 14, "simulates"), start=31.45, speed=1.0, crop=WIZ, sfx=False, **CARD),
    dict(src=REC, at=("w", 14, "simulates"), until=("cut", 14), start=37.0, speed=4.0, crop=WIZ, sfx=False, **CARD),
    # 15 "It's so cool" -> finalising -> CD Burned Successfully
    dict(src=REC, at=("cut", 14), until=("cut", 15), start=51.2, speed=2.0, crop=WIZ, sfx=False, **CARD),
    # 16 Finish (eject) -> note on the case -> copy link -> the friend opens it ("From me to me")
    dict(src=REC, at=("cut", 15), until=("w", 16, "write"), start=55.4, speed=1.0, crop=WIZ, sfx=False, **CARD),
    dict(src=REC, at=("w", 16, "write"), until=("w", 16, "share"), start=58.0, speed=1.5, crop=WIZ, sfx=False, **CARD),
    dict(src=REC, at=("w", 16, "share"), until=("w", 16, "with"), start=72.25, speed=1.0, crop=WIZ, sfx=False, **CARD),
    dict(src=REC, at=("w", 16, "with"), until=("cut", 16), start=83.0, speed=1.3, crop=PLAYER, sfx=False, **CARD),
    # 17 the CD player playing the 0:30 preview
    dict(src=REC, at=("cut", 16), until=("cut", 17), start=92.0, speed=1.0, crop=PLAYER, sfx=False, **CARD),
]
# site sounds under her voice (build_site_audio.py -> build/site_audio.wav): (start, end, recording start, volume)
SITE_AUDIO = [
    (("cut", 13), ("w", 14, "simulates"), 31.45, 3.0),   # Burn click + drive tray
    (("w", 14, "simulates"), ("cut", 14), 37.0, 2.5),     # burn hum
    (("cut", 14), ("cut", 15), 51.2, 1.5),                # last track + done
    (("cut", 15), ("w", 16, "write"), 55.4, 2.0),         # Finish -> eject
    (("w", 16, "share"), ("w", 16, "with"), 72.25, 5.0),  # copy link click
    (("cut", 16), ("cut", 17), 92.0, 0.35),               # the 30 s preview, quiet under her line
]
EXTRA_SFX = [("build/site_audio.wav", 0.0, 1.0)]
WEIGHTED = [(10, "98", 3, 540, -1150)]   # "98 or 99%" in butter, one row
URL = "burncd.online"
URL_AT = ("w", 22, "here")
HOLD = 1.3
ZOOMS = []
