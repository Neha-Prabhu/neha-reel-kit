"""Day 5 — Halloween origami (origami.me/halloween-origami). Final = "pass 3i": orange theme, 3-pop hook, no zooms.
Media (src/, img/, build/) is not in git (script-specific) — kept as an example spec."""

AROLL = "src/halloween_Aroll.MP4"
SRT = None                       # next time: export auto-captions .srt from Edits on the original A-roll
WORDS_JSON = "build/words.json"

# rough cut: (source start, source end, speed) — one entry per spoken line
SEGS = [
    (0.57, 4.24, 1.1),   # 0  Pinterest Halloween DIYs are cute until they require some 17 supplies.
    (5.14, 6.36, 1.1),   # 1  This one just needs a paper.
    (6.70, 9.25, 1.2),   # 2  Day 5 of Things I Found on the Internet Instead of Doomscrolling   (intro)
    (9.47, 15.33, 1.2),  # 3  This website has 18 free Halloween origami tutorials ranging from ghost, bat, pumpkin, skulls,
    (15.49, 18.89, 1.1), # 4  which I genuinely didn't know ... one sheet of paper.
    (19.23, 21.71, 1.1), # 5  And some of them can be made under just five minutes,
    (22.06, 23.25, 1.1), # 6  like this devilish heart
    (23.42, 24.51, 1.1), # 7  or this origami crow.
    (24.67, 26.48, 1.1), # 8  You could make them into a wall decor,
    (26.62, 28.00, 1.1), # 9  you could make a bat garland,
    (28.22, 30.04, 1.1), # 10 or it could be a party activity in itself.
    (30.40, 32.16, 1.1), # 11 There's even a tutorial for a witch hat
    (32.41, 33.87, 1.1), # 12 that you could gift as a souvenir.
    (34.07, 36.80, 1.1), # 13 So if you want to try this out, you do not have to comment for the link
    (37.05, 37.95, 1.1), # 14 Because here it is. Bye.
]

DAY = 5
WALL = "orange_soft.jpg"         # B-roll wall (assets/textures). None = classic blue
INTRO = dict(line=2, frames="build/intro_frames", label="Day 5", title="Things I Found on the Internet Instead of Doomscrolling",
             bg=(176, 84, 40), title_y=232)
#   build intro frames:  python assets/intro/build_intro.py --out <tmp> --wall assets/textures/orange_soft.jpg --witch-hat
#                        python assets/intro/halloween_props.py <tmp> reels/day05_halloween/build/intro_frames

HOOK_END = 1.23                  # hook pops clear on "are"

POPS = [
    # hook: 3 small pins around her, face + top (text-hook zone) clear
    dict(img="img/hook_lanterns.png", w=330, r=22, at=0.06, until=1.23, x=225, y=1130),
    dict(img="img/hook_jellycat.png", w=300, r=22, at=0.30, until=1.23, x=860, y=1120),
    dict(img="img/hook_ghosts.png",   w=380, r=22, at=0.54, until=1.23, x=540, y=1360),
    # cutouts next to her hands, white outline
    dict(img="img/06_heart_cutout.png", w=300, outline=10, at=("w", 6, "this"), until=("cut", 6), x=225, y=840),
    dict(img="img/07_crow_cutout.png",  h=500, outline=10, at=("w", 7, "this"), until=("cut", 7), x=945, y=1065),
    dict(img="img/09_garland.jpg", w=360, r=22, at=(("cut", 8), 0.10), until=("cut", 9), x=820, y=1215),
    # witch hat: whole image, no bg removal, on "witch", held through "souvenir"
    dict(img="img/11_witchhat_keep-bg.png", w=600, r=22, at=24.57, until=("cut", 12), x=540, y=1330),
]

BROLL = [  # scroll recording on line 3, "18 free tutorials" on screen as she says it
    dict(src="src/04_scroll_tutorials.mov", at=("cut", 2), until=("cut", 3), start=0.8, speed=1.3, width=620, y=800, cap_y=1445),
]

# weighted words: (line, first word, n words, centre x, centre y)  — negative y = one row instead of stacked
WEIGHTED = [
    (0, "17", 2, 540, 1250), (1, "paper.", 1, 540, 1250), (4, "one", 2, 540, 1250), (5, "five", 2, 540, 1250),
    (6, "devilish", 2, 770, 1250), (7, "origami", 2, 330, 1250), (8, "wall", 2, 540, 1250), (9, "bat", 2, 320, 1250),
    (10, "party", 2, 540, 1250), (11, "witch", 2, 540, -1050), (12, "souvenir.", 1, 540, 1050), (13, "comment", 1, 540, 1250),
]

URL = "origami.me/halloween-origami"
URL_AT = ("w", 14, "here")
HOLD = 1.3
ZOOMS = []   # tried 4 punch-ins (1.18x) — she preferred without
