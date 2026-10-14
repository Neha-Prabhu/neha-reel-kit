# Assets — reusable across any reel or series

Rule: anything Neha sends that can be reused in another video goes here (snake_case name, right folder,
one line in this list, commit + push). Anything tied to one script (that reel's photos, recordings, A-roll)
stays out of git — it lives in reels/<name>/img|src locally only.

| folder | what | notes |
|---|---|---|
| `fonts/` | Diagramm-UltraBoldItalic (captions, labels, weighted words), Monigue (titles), ProvidenceSans (handwritten accent), Poppins Medium/Bold (URL bar, UI), Fredoka SemiBold/Bold + Nunito Regular/Bold (Pawmuch site fonts — card pops) | |
| `sfx/` | pop, whoosh, whoosh_soft, ding, sparkle, typing, mouse_click, thud, shutter, shutter_single (one click), crumple (paper) | pop = every image landing |
| `textures/` | orange_soft, orange_red, orange_grid_bats | wall for B-roll / intro on themed reels |
| `overlays/` | paper_crumple_greenscreen.mp4 — paper ball opens into a sheet; blue bg = key out, green = image goes here | 1920x1080, 2 s; rotate 90° for portrait |
| `logos-and-ui/` | pinterest_logo (.png/.avif), whatsapp_bubble_anim.mp4 (white + green chat bubbles on black — key out black) | for text hooks / mock UI pops |
| `logos-and-ui/` | pawmuch_cat_icon.png, pawmuch_pin.png — Pawmuch listing-card icons (used by tools/pawmuch_card.py) | rebuild listing screenshots as identical card pops |
| `intro/` | build_intro.py (stop-motion desk intro card), heads/ (head cutouts), halloween_props.py | optional intro card |
