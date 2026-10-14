---
name: reel-edit
description: Edit one of Neha's Instagram reels from her raw footage: remove pauses, J cuts, B-roll, pops, captions, SFX and export, in her house style. Works for any series or one-off reel.
---

# Reel edit

Neha shoots her own A-roll; you do the edit. The result must look hand-made by an intermediate VN/Edits editor, never "AI-generated". This skill is about the editing work only — it does not assume any particular series, intro or format. Series elements (an intro card, a label like "Day 5", a CTA) are added only if she asks for them or the reel's spec has them.

## Tools
- Use **neha-reel-kit** (private GitHub repo `Neha-Prabhu/neha-reel-kit`): attach it with add_repo (push access) and clone; if GitHub isn't reachable, ask her to upload `neha-reel-kit.zip`. `README.md` has the commands, `STYLE.md` the full rule list.
- Needs python3, pillow, numpy, scipy, ffmpeg (`pip install ... --break-system-packages`).
- Each reel = a folder copied from `reels/_template` with a `reel.py` spec; media goes in `src/` and `img/` (local only, gitignored). Commit the `reel.py` spec after each draft so the repo stays clean.
- Reusable assets live in `assets/` (fonts, sfx, textures, overlays, logos-and-ui, intro) — check `assets/README.md` before asking her for something she may have sent before.
- Kit tools: `tools/cutout.py` (white-bg cards), `tools/pawmuch_card.py` (listing screenshots → identical card pops), `tools/face_track.py` (face boxes → pop sides + caption dodging).

### Offline helpers (the shell can't reach Hugging Face etc.; these routes work)
- **Transcript (Edits has no .srt export):**
  - Exact words: Whisper small.en via `pip install sherpa-onnx`, model from GitHub releases `k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.en.tar.bz2`. Run it per rough-cut segment (whole file is capped at 30 s).
  - Word timings: Vosk small model, bundled in the npm package `transcribe2texts` (`npm pack transcribe2texts` → `vosk-model-small-en-us-0.15/`); `pip install vosk --no-deps` plus a stub `srt.py` on PYTHONPATH. Run it on `build/voice_clean.wav`, save as `build/asr_cut.json`.
  - In the spec: `LINES` (exact words, one per segment) + `ASR_JSON` → `python -m reelkit.words` aligns them; fix stragglers with `WORD_FIX = {(line, "word"): t}`.
  - Re-run Whisper on each cut segment to catch clipped last words (e.g. "I don't" = "know" got cut → extend the segment end).
- **Background removal:** `pip install "rembg[cpu]"`, models from `github.com/danielgatis/rembg/releases/download/v0.0.0/<name>.onnx` into `~/.u2net/` (`u2net`, `isnet-general-use`). Try both and look — u2net kept thin parts (bag "ears") that isnet dropped. Only ask her for an iPhone "lift subject" PNG if both fail.
- **Face track:** OpenCV 5 dropped Haar cascades → `pip install --target <dir> "opencv-python-headless==4.12.0.88" "numpy<2.3"` and run `tools/face_track.py` with that PYTHONPATH. Drop detections whose top is below ~800 px (shirt folds).
- **A website's fonts:** `npm pack @fontsource/<font>` → convert the .woff to .ttf with fonttools → `assets/fonts/`.

## 1. Intake (ask once, one message, only for what's missing)
- Original A-roll. Her exact words: an .srt if she has one; otherwise transcribe offline (above) and show her the lines you're unsure of with draft 1 — she confirms or corrects in feedback. Never caption from the script.
- B-roll / screen recordings and images, named by the line they belong to: `NN_<what>.png`. **`<name>_sticker`** (e.g. `kid_sticker.jpg`) = make it a sticker (background removed + white outline). Any other image is a normal photo pop: background kept, rounded corners, no border. Don't decide this yourself — the file name tells you. (Older reels used `_cutout` / `_keep-bg` — treat `_cutout` like `_sticker`.)
- Theme/colours or wall texture if any, URL if the reel ends on a link, text hook only if she has one (never invent one), caption font if she wants a special one for this reel.

## 2. Rough cut — pacing
- Downscale 4K to 1080x1920 first (trims on 4K get OOM-killed). `python -m reelkit.roughcut <spec> --detect` drafts segments; cross-check against the ASR word gaps — quiet words ("Him?", trailing "know") can sit inside a "silence".
- Remove every pause; one segment per spoken line; never clip a line's last word.
- Speed 1.1x by default; 1.2x for list lines and fast throwaway lines.
- J cut = exactly 1 frame (next line's audio leads the picture by 1/30 s). Longer shows her looking away.
- Audio: mono → trim + atempo per segment → +11 dB → light limiter, one encode. Never loudnorm (pumping) or rubberband (robotic/double voice).
- Picture cuts on the 30 fps grid, audio segments trimmed to exact length → lip sync never drifts.
- If she asks straight for an edit, go to the full draft and ask the pacing questions (clipped word? gap? fumble?) alongside it; otherwise send the rough cut first.

## 3. Full edit — in ONE pass
- Words: `python -m reelkit.words <spec>`; check every line.
- **Where pops go:** the MIDDLE ROW of the IG 3x3 grid (y ≈ 640–1280, her line of vision — not low), in the left or right column, alternating, always on the side away from her face at that moment (use the face track). Captions then take the other side.
- **Pops:** instant (no grow-in), borderless, straight (no tilt), never over her face, land on the word (the name, "like *this* …"), pop SFX on the landing frame; stay up until the next item starts. Hook pops: max 3 small images, face visible, top ~440 px free for a text hook, gone before the payoff line.
- **Website / listing screenshots:** never mix raw crops. Rebuild them as identical cards (same photo size, pill, name, location, 2-line description, site fonts) — `tools/pawmuch_card.py` for Pawmuch; same idea for other sites. Use only the text that's visible on her screenshot (end with "…" like the site).
- **Funny cutaways** (a word joke — "adopting a kid… I meant kitten", "I see the resemblance" → Toothless): pop SFX, up for the beat and gone; sticker or photo per the file name.
- **Stickers (`_sticker` files only):** white-background cards → `tools/cutout.py` (crop off card text); other photos → rembg. Always a white outline so they don't blend into the room. Images without `_sticker` keep their background.
- **B-roll / screen recordings:** white rounded phone card on a plain/textured wall (per-clip `wall=`, e.g. `pink_paper.jpg` for Pawmuch), top clear of the IG "Reels" header. Use `crop=` to cut the status bar (time, battery, recording dot) and the browser bar; `blur=` for anything else that gives the link away early. Speed long scrolls up (~2.5x) so it fits the line.
- **Captions (default):** white Diagramm UltraBold Italic + soft shadow (no outlines), ≤3 words, above the bottom 20% (IG UI), one caption element on screen at a time, dodge images sideways instead of dropping lower.
- **Kinetic captions (when she asks — font may change per reel, e.g. Margarine):** `CAPTIONS = dict(font=..., size=78, y=1140, key=[(line, "word"), ...], faces="build/faces.json")`. Words appear as she says them (no motion), key words (names, the joke words, the link, numbers) butter yellow + bigger, and each chunk auto-places into the free space around pops, her face and the URL bar — so the captions move around the frame. Check the render log for "no free spot".
- **Weighted words** (default style only): the nouns/items/numbers that carry the line — not adverbs. Diagramm, butter yellow, soft shadow, bigger, off her face, each word as she says it.
- **Link endings:** URL bar pops at the top on the link word / "here it is", no typing sound; a website screenshot (status bar + browser bar cropped) can pop in a side column at the same time; both stay to the end; hold the last frame ~1.3 s.
- **Theme:** if a reel has a theme colour/texture, use it everywhere (intro and B-roll walls alike).
- **Zoom cuts:** optional hard punch-ins (~1.18x, anchored on her face) on plain A-roll stretches only; she preferred without on past reels — suggest, don't assume.
- Always render preview stills first (`python -m reelkit.render <spec> t1 t2 …`), look at them, fix collisions (face, captions vs images, bottom 20%, text vs props), then the full render. Send the <30 MB `final_send.mp4`.

## 4. Feedback rounds
- Change only what she asks for; if she asks for a summary, summarise before editing.
- After each render, list what changed in a few bullets and flag anything uncertain (a word you couldn't hear, which image goes where) as a question.
- She often dictates feedback (voice-to-text): read through misspellings ("bingos" = Bingus, "Pomach" = Pawmuch).
- New lasting preference → add it to `STYLE.md` in the kit and commit. Reel → commit its `reel.py` spec (never media).
- **Assets she sends:** if it's reusable across videos/series (font, SFX, texture, overlay/green-screen, logo, UI animation), save it to `assets/<category>/` with a snake_case name, add a line to `assets/README.md`, commit and push. If it's specific to one script (that reel's photos, recordings, A-roll), keep it local in the reel folder — never commit it. Your call; when unsure, ask "reuse later?".
