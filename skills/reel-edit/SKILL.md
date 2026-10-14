---
name: reel-edit
description: Edit one of Neha's Instagram reels from her raw footage: remove pauses, J cuts, B-roll, pops, captions, SFX and export, in her house style. Works for any series or one-off reel.
---

# Reel edit

Neha shoots her own A-roll; you do the edit. The result must look hand-made by an intermediate VN/Edits editor, never "AI-generated". This skill is about the editing work only — it does not assume any particular series, intro or format. Series elements (an intro card, a label like "Day 5", a CTA) are added only if she asks for them or the reel's spec has them.

## Tools
- Use **neha-reel-kit** (private GitHub repo on her account): attach it with add_repo and clone; if GitHub isn't reachable, ask her to upload `neha-reel-kit.zip`. `README.md` has the commands, `STYLE.md` the full rule list.
- Needs python3, pillow, numpy, scipy, ffmpeg (`pip install ... --break-system-packages`).
- Each reel = a folder copied from `reels/_template` with a `reel.py` spec; media goes in `src/` and `img/`.

## 1. Intake (ask once, one message, only for what's missing)
- Original A-roll + its auto-caption **.srt** exported from Edits/CapCut — gives her exact words and timings. No .srt → ask her to paste exactly what she said. Never caption from the script.
- B-roll / screen recordings and images, named by the line they belong to: `NN_<what>.png`; `_keep-bg` = never remove the background, `_cutout` = remove it.
- Theme/colours if any, URL if the reel ends on a link, text hook only if she has one (never invent one).

## 2. Rough cut — checkpoint: pacing only
- Downscale 4K to 1080x1920 first (trims on 4K get OOM-killed). `python -m reelkit.roughcut <spec> --detect` drafts segments.
- Remove every pause; one segment per spoken line; never clip a line's last word.
- Speed 1.1x by default; 1.2x for list lines and fast throwaway lines.
- J cut = exactly 1 frame (next line's audio leads the picture by 1/30 s). Longer shows her looking away.
- Audio: mono → trim + atempo per segment → +11 dB → light limiter, one encode. Never loudnorm (pumping) or rubberband (robotic/double voice).
- Picture cuts on the 30 fps grid, audio segments trimmed to exact length → lip sync never drifts.
- Send the rough cut; ask only: any clipped word or gap left?

## 3. Full edit — in ONE pass
- Words: `python -m reelkit.words <spec>` (SRT or exact LINES); check every line.
- **B-roll / screen recordings:** white rounded phone card on a plain/textured wall, top clear of the IG "Reels" header, time it so what she says is on screen; blur any URL bar or logo that would give away the link early.
- **Pops:** instant (no grow-in), borderless, straight (no tilt), never over her face, land on the word ("like *this* …"), placed where she points/holds; pop SFX on the landing frame. Hook pops: max 3 small images, face visible, top ~440 px free for a text hook, gone before the payoff line.
- **Cutouts:** white-background cards → `tools/cutout.py` (crop off card text); complex backgrounds → ask for an iPhone "lift subject" PNG. Cutouts get a white outline so they don't blend into the room. Images marked keep-bg stay whole.
- **Captions:** white Diagramm UltraBold Italic + soft shadow (no outlines), ≤3 words, always above the bottom 20% (IG UI), one caption element on screen at a time, dodge images sideways instead of dropping lower.
- **Weighted words:** the nouns/items/numbers that carry the line ("devilish heart", "17 supplies") — not adverbs. Diagramm, butter yellow, soft shadow, bigger, placed freely off her face, each word appears as she says it, tight line spacing.
- **Link endings:** URL bar pops above her head on "here it is", no typing sound; hold the last frame ~1.3 s.
- **Theme:** if a reel has a theme colour/texture, use it everywhere (intro and B-roll walls alike).
- **Zoom cuts:** optional hard punch-ins (~1.18x, anchored on her face) on plain A-roll stretches only; she preferred without on past reels — suggest, don't assume.
- Always render preview stills first (`python -m reelkit.render <spec> t1 t2 …`), look at them, fix collisions (face, captions vs images, bottom 20%, text vs props), then the full render. Send the <30 MB `final_send.mp4`.

## 4. Feedback rounds
- Change only what she asks for; if she asks for a summary, summarise before editing.
- After each render, list what changed in a few bullets and flag anything uncertain (word timing, which image goes where) as a question.
- New lasting preference → add it to `STYLE.md` in the kit and commit. Final reel → commit its spec + img/ (not src/ or build/).
