"""boss_prank — pranked my boss with WowMouse on my smartwatch (Doublepoint WowMouse).
Draft 1 = colour grade + B-roll only (rendered with ffmpeg; pops/captions/URL come in the next round)."""

AROLL = "src/aroll.mp4"          # her own pre-trimmed 1080x1920 24 fps export, 31.5 s
# Draft 4: the graded/B-roll cut (build/roughcut.mp4 = draft 3, 30 fps) is the base; reelkit adds kinetic captions.
# LINES are on that cut (build/cuts.json audio_starts); word timings from Vosk -> build/asr_cut.json
ASR_JSON = "build/asr_cut.json"
LINES = [
    "I used my smartwatch to prank my boss.",
    "He used to keep belting me for not using AI in my work,",
    "when he didn't even know how to move stuff around in PPT.",
    "So I downloaded this app on my smartwatch,",
    "connected it to his Mac and just played with him all day.",
    "I played music when he was in a meeting.",
    "Opened his YouTube when he was sharing his screen.",
    "And kicked him out of the meeting with his manager.",
    "This entire thing was so fun that I wanted to open his WhatsApp and text someone.",
    "But I love my job.",
    "If you want to do something similar or prank anyone,",
    "you do not have to comment for this link.",
    # "because it's called Wow Mouse" -> cut; URL pops instead
]
END = 30.55

GRADE = dict(aroll="assets/luts/warm_pop.cube", broll="assets/luts/warm_pop_light.cube")

BROLL_AUDIO = 0                  # never use B-roll sound — she adds music on top
BROLL_NOTES = [  # (src, src_in, src_out, tl_start, tl_end) — overlay on A-roll (rendered in render3.py, not reelkit)
    ("src/far_boss_boggled.MOV", 2.6, 4.5, 11.0, 12.91),   # "...played with him all day"
]
# Draft 3: full cutaways back to back (A-roll cut 13.15 -> resumes 20.22 "This entire thing...").
CUTAWAYS = [
    # under BOTH lines "I played music…meeting" + "Opened his YouTube…screen" (pause between removed); ~0.7 s of song after
    dict(src="src/youtube_play.MOV", parts=[(3.0, 7.5, 1.6), (7.5, 9.6, 1.0)], voice=[(13.15, 15.10), (15.40, 17.62)]),
    # approved: she turns -> does it -> his reaction -> he looks back, she's turned away; line ends on his reaction
    dict(src="src/kicked_him_out.mov", parts=[(0.0, 4.3, 1.5), (4.3, 7.5, 1.0)], voice=(18.09, 20.17)),
]

# faces.json: Haar misses the boss in cutaways -> hand boxes 13.15-18.06 (560,450,980,1350) and 18.0-24.1 (180,880,660,1330)
CAPTIONS = dict(font="Diagramm-UltraBoldItalic.ttf", size=72, y=1140, key_scale=1.3, faces="build/faces.json", face_max_top=1400,
                key=[(0, "smartwatch"), (0, "prank"), (0, "boss"), (1, "AI"), (2, "PPT"), (3, "app"), (3, "smartwatch"), (4, "Mac"),
                     (4, "all"), (4, "day"), (5, "music"), (6, "YouTube"), (7, "kicked"), (7, "manager"),
                     (8, "WhatsApp"), (9, "love"), (9, "job"), (10, "prank"), (11, "comment"), (11, "link")])
URL = ""                         # WowMouse URL to confirm with her, then URL_AT = ("w", 11, "link")
URL_AT = ("w", 11, "link")
HOLD = 0.4
CAP_MAX_TAIL = 1.0               # clear captions ~1 s after the last word (music-only stretches stay clean)
