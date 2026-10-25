"""boss_prank — pranked my boss with WowMouse on my smartwatch (Doublepoint WowMouse).
Draft 5: base cut from render_cut.py (grade, muted B-roll), then reelkit adds kinetic captions + sticker pops.

AROLL = "src/aroll.mp4"          # her own pre-trimmed 1080x1920 24 fps export, 31.5 s
# Draft 4: the graded/B-roll cut (build/roughcut.mp4 = draft 3, 30 fps) is the base; reelkit adds kinetic captions.
# LINES are on that cut (build/cuts.json audio_starts); word timings from Vosk -> build/asr_cut.json
ASR_JSON = "build/asr_cut.json"
LINES = [
    "I used my smartwatch",
    "to prank my boss.",                       # own line so its captions sit wholly on the boggled shot
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
# base cut = render_cut.py -> build/roughcut.mp4 + voice_clean.wav (grade, B-roll muted)
#   boggled: src 3.8-4.9 at ~0.9x on "to prank my boss" (1.17-2.40) — draft 5 (was on "played with him all day")
# Draft 3: full cutaways back to back (A-roll cut 13.15 -> resumes 20.22 "This entire thing...").
CUTAWAYS = [
    # under BOTH lines "I played music…meeting" + "Opened his YouTube…screen" (pause between removed); ~0.7 s of song after
    dict(src="src/youtube_play.MOV", parts=[(3.0, 7.5, 1.6), (7.5, 9.6, 1.0)], voice=[(13.15, 15.10), (15.40, 17.62)]),
    # approved: she turns -> does it -> his reaction -> he looks back, she's turned away; line ends on his reaction
    dict(src="src/kicked_him_out.mov", parts=[(0.0, 4.3, 1.5), (4.3, 7.5, 1.0)], voice=(18.09, 20.17)),
]

POPS = [   # AI-app stickers land on "AI" (both sides of her face); nervous cat on "But I love my job"
    dict(img="img/01_chatgpt_sticker.png", w=230, outline=10, at=("w", 2, "AI"), until=("w", 3, "how"), x=165, y=830),
    dict(img="img/01_claude_sticker.png", w=250, outline=10, at=("w", 2, "AI"), until=("w", 3, "how"), x=890, y=830, sfx=False),
    dict(img="img/09_nervous_cat.jpg", w=300, r=28, outline=10, at=("w", 10, "But"), until=("start", 11), x=890, y=880),
]

# faces.json: Haar misses the boss in cutaways -> hand boxes 1.17-2.40 boggled (360,1020,740,1420), 13.15-18.06 (560,450,980,1350) and 18.0-24.1 (180,880,660,1330)
CAPTIONS = dict(font="Diagramm-UltraBoldItalic.ttf", size=72, y=1140, key_scale=1.3, faces="build/faces.json", face_max_top=1400,
                key=[(0, "smartwatch"), (1, "prank"), (1, "boss"), (2, "AI"), (3, "PPT"), (4, "app"), (4, "smartwatch"), (5, "Mac"),
                     (5, "all"), (5, "day"), (6, "music"), (7, "YouTube"), (8, "kicked"), (8, "manager"),
                     (9, "WhatsApp"), (10, "love"), (10, "job"), (11, "prank"), (12, "comment"), (12, "link")])
URL = ""                         # WowMouse URL to confirm with her, then URL_AT = ("w", 12, "link")
URL_AT = ("w", 12, "link")
HOLD = 0.4
CAP_MAX_TAIL = 1.0               # clear captions ~1 s after the last word (music-only stretches stay clean)
