"""Groove Pizza (apps.musedlab.org/groovepizza) — one-off, split screen. Music hook: she vibes to the Billie Jean beat first.

Audio: src/aroll.mov = her iPhone A-roll cropped to 9:16 + the screen recording's clean music mixed under her mic,
synced by cross-correlation (rec time = A-roll time + 6.164 s; music ducked -7 dB under her lines, -1 dB elsewhere).
Music segments stay at 1.0x and every cut sits on the 117 BPM beat grid (beat 0.5104 s; phase 0.106 in the hook,
0.434 after she restarts playback at ~6 s) so the beat never stutters across a cut. Only the closing talk runs 1.1x.
"""

AROLL = "src/aroll.mov"
# bottom split window from the ORIGINAL landscape clip (face + torso + laptop edge; the 9:16 crop is face-only)
AROLL_WIDE = ("/mnt/user-data/uploads/IMG_9682_2.MOV", "3840:2160:0:0", 1152, 648)   # roughcut --wide
SRT = None
LINES = [
    "",                                                                   # 0  hook: vibing to the beat (no words)
    "So if you know, this is Billie Jean's starting part.",
    "What if I do this?",                                                 # "And what if I change," cut (repeat)
    "Or this?",
    "Or this.",
    "",                                                                   # 5  beat only (final shape)
    "This is so much fun. So I found this website where you can actually, you know, play around with drum beats on a pizza. This is, I think, called Groove Pizza and I'll add the link here, so go check it out.",
]
ASR_JSON = "build/asr_cut.json"
WORD_FIX = {(1, "So"): 5.46, (6, "link"): 30.58, (6, "here"): 30.93}
WORDS_JSON = "build/words.json"

B = 0.5104
g = lambda k: round(0.4338 + k * B, 3)       # beat grid after playback restarts (A-roll seconds)
SEGS = [  # (source start, source end, speed)
    (0.106, 5.210, 1.0),      # 0  hook — 10 beats of her vibing (kept long on purpose, she asked)
    (g(19), g(25), 1.0),      # 1  So if you know ... starting part.            <- split screen starts
    (g(29), g(32), 1.0),      # 2  What if I do this?   (skips "And what if I change," — the repeat)
    (g(42), g(50), 1.0),      # 3  (clicking) Or this? + new beat
    (g(61), g(71), 1.0),      # 4  Or this. + shape appears and grows
    (g(77), g(81), 1.0),      # 5  1 bar of the final pattern
    (g(85), 56.62, 1.1),      # 6  This is so much fun ... go check it out.     <- back to full frame
]

WALL = None
INTRO = None
HOOK_END = None
CAP_MAX_TAIL = 1.0                 # captions clear during the beat-only stretches instead of hanging there

POPS = []
BROLL = []
D = 6.164                                             # rec time = A-roll time + D (audio cross-correlation)
SITE = (360, 45, 1520, 1080)                          # pizza + step grid + play button, browser bar and sidebar cropped
FPS = 30
def rec_at(i):   # recording time at the picture cut that starts segment i (same maths as roughcut, J cut = 1 frame)
    st = [sum((b - a) / k for a, b, k in SEGS[:n]) for n in range(len(SEGS))]
    t0 = round((st[i] + 1 / FPS) * FPS) / FPS
    return round(SEGS[i][0] + (t0 - st[i]) * SEGS[i][2] + D, 3)

SPLIT = dict(
    at=("cut", 0), until=("cut", 5), src="src/site_rec.mp4", wall=None, sfx=False,   # whoosh_soft in EXTRA_SFX
    top=(90, 200, 900, 640), bottom=(90, 950, 900, 586), cap_y=895,
    face_src="build/roughcut_wide.mp4", face_crop=(157, 0, 995, 648),   # face + torso + laptop edge
    blur=[],                                          # site logo + URL bar are outside SITE; link only shows at the end
    clips=[dict(at=("cut", i - 1), rec=rec_at(i), speed=1.0, crop=SITE) for i in range(1, 6)],   # panel = the exact moment she sees
)
# outside the split: her landscape clip stays landscape, centred on the wall (no 9:16 crop)
SOLO = dict(src="build/roughcut_wide.mp4", box=(90, 707, 900, 506), crop=(0, 0, 1152, 648), cap_y=1310)
EXTRA_SFX = [
    ("whoosh_soft.mp3", (("cut", 0), -0.12), 0.22),   # split screen comes in
]
WEIGHTED = []
URL = "apps.musedlab.org/groovepizza"
URL_AT = ("w", 6, "here")
HOLD = 1.3
ZOOMS = []
