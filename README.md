# neha-reel-kit

Editing kit for **Neha Much** reels — any series or one-off.
One spec file per reel → rough cut → full edit (B-roll, pops, captions, URL, SFX, optional intro card). Used by the
`reel-edit` skill; see `STYLE.md` for the house rules every edit follows.

```
reelkit/        roughcut.py · words.py · render.py · gfx.py · spec.py
assets/         fonts/ sfx/ textures/ intro/ (stop-motion desk builder, heads, theme props)
reels/          _template/ + one folder per reel (reel.py + img/ in git; src/ and build/ are not)
tools/cutout.py white-background removal for website cards
```

## Per reel
```bash
pip install pillow numpy scipy --break-system-packages      # + ffmpeg
cp -r reels/_template reels/<NN>_<slug>                     # put A-roll, .srt, recordings in src/, images in img/
python -m reelkit.roughcut reels/<NN>_<slug>/reel.py --detect   # draft SEGS -> paste into reel.py
python -m reelkit.roughcut reels/<NN>_<slug>/reel.py            # build/roughcut.mp4  (approve pacing)
python -m reelkit.words    reels/<NN>_<slug>/reel.py            # build/words.json (from .srt, or LINES)
python assets/intro/build_intro.py --out reels/<NN>_<slug>/build/intro_frames [--wall assets/textures/x.jpg] [--witch-hat]
python -m reelkit.render   reels/<NN>_<slug>/reel.py 0.5 5.5 12  # preview stills
python -m reelkit.render   reels/<NN>_<slug>/reel.py            # build/final.mp4 + final_send.mp4 (<30 MB)
```

## Asset naming (send these with every reel)
`aroll.MOV`, `aroll.srt`, `NN_<what>.png` where NN = the script line it belongs to
(`01_hook_lanterns.png`, `09_garland.jpg`), suffix `_keep-bg` = never remove background, `_cutout` = remove it.

## Skills
`skills/` holds the source of the Claude skills that use this kit (reel-edit). Save them in Claude via the skill card; this copy is for versioning.
