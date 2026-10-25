"""boss_prank — pranked my boss with WowMouse on my smartwatch (Doublepoint WowMouse).
Draft 1 = colour grade + B-roll only (rendered with ffmpeg; pops/captions/URL come in the next round)."""

AROLL = "src/aroll.mp4"          # her own pre-trimmed 1080x1920 24 fps export, 31.5 s
LINES = [
    "I used my smartwatch to prank my boss.",
    "He used to keep belting me for not using AI in my work, when he didn't even know how to move stuff around in PPT.",
    "So I downloaded this app on my smartwatch, connected it to his Mac and just played with him all day.",
    "I played music when he was in a meeting.",
    "Opened his YouTube when he was sharing his screen.",
    "And kicked him out of the meeting with his manager.",
    "This entire thing was so fun that I wanted to open his WhatsApp and text someone.",
    "But I love my job.",
    "If you want to do something similar or prank anyone, you do not have to comment for this link",
    # "because it's called Wow Mouse" -> cut (end at 30.55 s); URL pops instead
]
END = 30.55

GRADE = dict(aroll="assets/luts/warm_pop.cube", broll="assets/luts/warm_pop_light.cube")

BROLL = [  # (src, src_in, src_out, tl_start, tl_end) — overlay on A-roll, own audio at 0.35
    ("src/far_boss_boggled.MOV", 2.6, 4.5, 11.0, 12.91),   # "...played with him all day"
]
# Draft 2: YouTube + kicked-out play back to back as full cutaways (A-roll paused, room left for music).
# Her line sits under each so it ends on the payoff; clip sound 0.9, ducked to 0.3 under her voice.
CUTAWAYS = [  # inserted after A-roll 15.44; A-roll resumes at 20.22 ("This entire thing...")
    dict(src="src/youtube_play.MOV", parts=[(2.0, 7.5, 1.5), (7.5, 9.6, 1.0)], voice=(15.44, 17.62)),  # explains -> YouTube at 7.6
    dict(src="src/kicked_him_out.mov", parts=[(0.0, 4.3, 1.5), (4.3, 7.5, 1.0)], voice=(18.09, 20.17)), # she turns -> his reaction -> looks back
]

URL = "doublepoint.com"          # to confirm with her
