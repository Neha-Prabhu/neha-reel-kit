# House style — learned from feedback on her reels (applies to any series)

**Pacing / audio**
- Remove every pause; 1.1x speed; list lines and fast throwaway lines 1.2x. Never cut a line's last word.
- J cut = exactly 1 frame. Longer shows her looking away before the next line.
- Line ends: cut where the word's tail actually dies (below ~-58 dB, not the -40 dB silencedetect edge) + a ~0.1 s breath
  (~0.15 s at a full stop). Cutting at the detect edge clips endings ("difference", "websites") and lines feel like they never end.
- Audio: mono → trim + atempo per segment → +11 dB → light limiter, single encode. No loudnorm (pumps), no rubberband (robotic).
- Downscale 4K to 1080x1920 before any trimming.

**Pops**
- Instant (no grow-in), borderless, straight (no tilt), never over her face, pop SFX on the landing frame.
- Hook: max 3 small images, around her, face visible, top ~440 px free for the text hook; clear before the payoff word.
- Background-removed cutouts get a white outline (otherwise they blend into the room). Photos/pins: rounded corners, no border.
- Pops land on the word ("like *this* devilish heart"); pop where she points/holds.
- Sticker vs photo is decided by the FILE NAME: `<name>_sticker` = background removed + white outline; anything else = normal photo pop, background kept.
- Two modes: POP over the A-roll vs FULL FOCUS (screen recording / image takes over: wall + white phone card, centred,
  ~620-650 wide, centre y ~800-830, captions under it). Never mix them up.
- Pop position: MIDDLE ROW of the IG 3x3 grid (in her line of vision, not low), left or right column, alternating, always on
  the side away from her face (tools/face_track.py). Several listing screenshots in one reel → rebuild as identical cards
  (tools/pawmuch_card.py), never mixed crops.
- Funny cutaways ("adopting a kid — I meant kitten", "I see the resemblance" → Toothless): background-removed stickers
  with a white outline, popped with SFX, gone after the beat.

**Captions**
- White Diagramm UltraBold Italic 60, soft shadow (no outlines), ≤3 words, always above the bottom 20% (IG UI).
- Weighted words = the nouns/items/numbers (e.g. "devilish heart", "17 supplies"), NOT adverbs like "genuinely".
  Diagramm, butter yellow, soft shadow, bigger; placed freely off her face; tight line spacing.
- Kinetic captions (when she asks for them, e.g. Margarine on the cats reel; size ~72, 78 felt huge): words appear as she says them (no motion),
  key nouns/names butter + bigger, each chunk sits in the free space around the pops/her face (CAPTIONS in the spec).
- One caption element on screen at a time. Captions must use her EXACT spoken words — get the .srt or a transcript.

**Layout / brand**
- Brand: blue wall (142,166,200), butter (247,226,122), lavender, ink; fonts Diagramm (captions, labels, weighted words), Monigue (titles).
- Themed reels may swap the wall everywhere (e.g. Halloween: orange texture in intro AND B-roll).
- Screen recordings: white rounded phone card on the wall, top clear of the IG "Reels" header, URL bars/logos blurred.
- SPLIT SCREEN (site demos, third mode — SPLIT in the spec): from the line where she starts showing the site. Two sharp-cornered
  rectangles (no rounding, no white card), same width (~900), on the wall: site recording on top (16:9, below the IG header,
  browser bar cropped, logos/links blurred until the link ending, muted), her A-roll below cropped to an almost-square
  face + torso window (empty headroom trimmed). Everything else — sides, gap, IG buttons + caption zone — is wall.
  Right edge ≤ ~990 so the IG like/comment column sits on the wall. Captions in the gap between the rectangles.
  Top panel jump-cuts per line: full site view for the big visual moments, punch-ins on the results text she's reading.
- LANDSCAPE A-ROLL: never crop it to portrait. Keep it landscape, centred on the wall (texture or black, either is fine)
  whenever no B-roll/split is up (SOLO in the spec), captions below it; in a split screen the bottom window comes from
  the same landscape cut (AROLL_WIDE + `roughcut --wide` + SPLIT face_src).
- Cut repeated restarts ("what if I change, what if I do this" → keep only the finished phrase).
- MUSIC REELS (the site plays music, she vibes to it as the hook): don't over-trim the vibing hook — keep ~5 s of her
  enjoying it. Sync the screen recording's clean audio to the A-roll (cross-correlate), mix it under her mic, panel
  clips at the exact synced moment. Music stretches stay 1.0x and every cut sits on the song's beat grid so the beat
  never stutters; captions clear in beat-only stretches (CAP_MAX_TAIL).
- Long screen recordings: don't speed one run up to fit (confusing). Jump-cut it instead: ~1 s of one scroll, then ~1 s of the
  action the line names (opening a profile, tapping Apply), each at near-real speed (1-2x).
- Intro card (optional, only if the series uses one): stop-motion desk, label pop (e.g. "Day 5") + typed title; themed props allowed.
- URL pops above her head on "here it is" — no typing sound. Hold last frame ~1.3 s.
- No text hook unless she supplies the words. Zoom cuts: optional, she preferred without so far.

**Process**
- Rough cut first (pacing only) → full edit → one consolidated feedback round.
- Don't change anything she didn't ask for; summarise changes before editing when she asks for a summary.

## Colour
- A-roll grade: `assets/luts/warm_pop.cube` (contrast + vibrance, skin protected, warm highlights / cool shadows); B-roll gets `warm_pop_light.cube`. Rebuild with `tools/make_lut.py`.
- B-roll audio is always muted (she adds music on top); let reaction B-roll play out rather than cutting back to A-roll between related clips.
- Logo/icon stickers for a word (e.g. AI apps on "AI"): `anim="whoosh"` — whoosh up ABOVE her head, left + right, hold ~1.5 s, whoosh out. Not beside her face.
