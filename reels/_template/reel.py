"""<reel name> — <topic> (<url>). Copy this folder to reels/<NN>_<slug>/ and fill in."""

AROLL = "src/aroll.MOV"
SRT = "src/aroll.srt"            # auto-captions exported from Edits/CapCut on the ORIGINAL A-roll (exact words + timing)
# LINES = ["...", ...]           # fallback if no .srt: exact spoken words, one string per SEGS entry

SEGS = [  # (source start, source end, speed) — draft from: python -m reelkit.roughcut reels/<name>/reel.py --detect
    # 1.1 normal, 1.2 for list lines / fast throwaway lines. One entry per spoken line.
]

WALL = None                      # B-roll wall: None = brand blue; or a texture in assets/textures (e.g. "orange_soft.jpg")
INTRO = None                     # optional intro card, e.g.:
# INTRO = dict(line=2, frames="build/intro_frames", label="Day 6", title="Series title here", bg=(112, 136, 178))
#   line = index of the spoken line it covers; frames from assets/intro/build_intro.py
HOOK_END = None                  # time the hook pops clear (captions stay centred until then)

POPS = [
    # dict(img="img/01_hook_x.png", w=330, r=22, at=0.06, until=("w", 0, "are"), x=225, y=1130),
    # dict(img="img/06_x_cutout.png", w=300, outline=10, at=("w", 6, "this"), until=("cut", 6), x=225, y=840),
]
BROLL = [
    # dict(src="src/04_scroll.mov", at=("cut", 2), until=("cut", 3), start=0.0, speed=1.0, width=620, y=800, cap_y=1445),
]
WEIGHTED = [
    # (line, first word, n words, centre x, centre y)   negative y = one row
]
URL = ""                         # leave empty if the reel doesn't end on a link
URL_AT = ("w", 0, "here")
HOLD = 1.3
ZOOMS = []                       # optional hard punch-ins: (at, until, 1.18)
