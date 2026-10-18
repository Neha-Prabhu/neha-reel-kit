"""Groove Pizza (apps.musedlab.org/groovepizza) — one-off, split screen. Music hook: she vibes to the Billie Jean beat first.

Audio: src/aroll.mov = her iPhone A-roll cropped to 9:16 + the screen recording's clean music mixed under her mic,
synced by cross-correlation (rec time = A-roll time + 6.164 s; music ducked -7 dB under her lines, -1 dB elsewhere).
Music segments stay at 1.0x and every cut sits on the 117 BPM beat grid (beat 0.5104 s; phase 0.106 in the hook,
0.434 after she restarts playback at ~6 s) so the beat never stutters across a cut. Only the closing talk runs 1.1x.
"""

AROLL = "src/aroll.mov"
# bottom split window from the ORIGINAL landscape clip (face + torso + laptop edge; the 9:16 crop is face-only)
AROLL_WIDE = ("/mnt/user-data/uploads/IMG_9682_2.MOV", "3318:2160:522:0", 900, 586)   # roughcut --wide
SRT = None
LINES = [
    "",                                                                   # 0  hook: vibing to the beat (no words)
    "So if you know, this is Billie Jean's starting part. And what if I change, what if I do this?",
    "Or this?",
    "Or this.",
    "",                                                                   # 4  beat only (final shape)
    "This is so much fun. So I found this website where you can actually, you know, play around with drum beats on a pizza. This is, I think, called Groove Pizza and I'll add the link here, so go check it out.",
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {(1, "So"): 5.46, (5, "link"): 32.62, (5, "here"): 32.97}
WORDS_JSON = "build/words.json"

B = 0.5104
g = lambda k: round(0.4338 + k * B, 3)       # beat grid after playback restarts (A-roll seconds)
SEGS = [  # (source start, source end, speed)
    (0.106, 5.210, 1.0),      # 0  hook — 10 beats of her vibing (kept long on purpose, she asked)
    (g(19), g(32), 1.0),      # 1  So if you know ... what if I do this?        <- split screen starts
    (g(42), g(50), 1.0),      # 2  (clicking) Or this? + new beat
    (g(61), g(71), 1.0),      # 3  Or this. + shape appears and grows
    (g(77), g(81), 1.0),      # 4  1 bar of the final pattern
    (g(85), 56.62, 1.1),      # 5  This is so much fun ... go check it out.     <- back to full frame
]

WALL = None
INTRO = None
HOOK_END = None
CAP_MAX_TAIL = 1.0                 # captions clear during the beat-only stretches instead of hanging there

POPS = []
BROLL = []
D = 6.164                                             # rec time = A-roll time + D (audio cross-correlation)
SITE = (360, 45, 1520, 1080)                          # pizza + step grid + play button, browser bar and sidebar cropped
SPLIT = dict(
    at=("cut", 0), until=("cut", 4), src="src/site_rec.mp4", wall=None, sfx=False,   # whoosh_soft in EXTRA_SFX
    top=(90, 200, 900, 640), bottom=(90, 950, 900, 586), face_src="build/roughcut_wide.mp4", face_crop=(0, 0, 900, 586), cap_y=895,
    blur=[],                                          # site logo + URL bar are outside SITE; link only shows at the end
    clips=[   # each panel clip = the exact moment of the recording she's looking at (synced to the cut)
        dict(at=("cut", 0), rec=10.160 + D, speed=1.0, crop=SITE),   # 1  Billie Jean ... what if I do this
        dict(at=("cut", 1), rec=21.898 + D, speed=1.0, crop=SITE),   # 2  or this?
        dict(at=("cut", 2), rec=31.612 + D, speed=1.0, crop=SITE),   # 3  or this. (shape appears)
        dict(at=("cut", 3), rec=39.775 + D, speed=1.0, crop=SITE),   # 4  final pattern
    ],
)
EXTRA_SFX = [
    ("whoosh_soft.mp3", (("cut", 0), -0.12), 0.22),   # split screen comes in
]
WEIGHTED = []
URL = "apps.musedlab.org/groovepizza"
URL_AT = ("w", 5, "here")
HOLD = 1.3
ZOOMS = []
