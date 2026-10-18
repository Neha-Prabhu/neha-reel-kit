"""Pass 2+3 — full edit from a spec: intro, B-roll, pops, captions (normal + weighted), URL, end hold, zooms, SFX.

  python -m reelkit.render reels/<name>/reel.py                  # full render -> build/final.mp4 (+ _send.mp4 <30MB)
  python -m reelkit.render reels/<name>/reel.py 0.5 4.3 17.6    # preview stills only -> build/prev_<t>.jpg + sheet

House style (all from Neha's feedback, Days 3-5):
  * pops: INSTANT (no grow-in), borderless, straight (no tilt), never over her face, pop SFX on the frame they land
  * cutouts (bg removed) get a white outline so they read against the room
  * top ~440px stays free while a text hook is on screen
  * captions: white Diagramm UltraBold Italic 60 + soft shadow, max 3 words, above the bottom 20% (IG UI)
  * weighted words: Diagramm, butter yellow, soft shadow, bigger, placed freely off her face, each word on its own frame
  * exactly ONE caption element on screen at a time (each ends when the next starts)
  * B-roll recordings: white rounded phone card on the wall, top clear of the IG "Reels" header
  * URL pops above her head on "here it is", no typing sound; last frame held ~1.3 s
  * intro card is optional — only when the reel/series uses one (INTRO in the spec)
"""
import glob, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
from .gfx import (W, H, FPS, SFX, BUTTER, INK, CREAM, WHITE, F_DIA, F_MON, font, paper, wall, rounded, sticker,
                  card, soft, load, place, url_bar)
from .spec import load_spec, Clock

SAFE_BOTTOM = int(H * 0.80) - 20
CAP_Y = 1400


class Reel:
    def __init__(self, spec):
        self.s = spec
        self.cuts = json.load(open(spec.path("build/cuts.json")))
        self.CW = json.load(open(spec.path(spec.get("WORDS_JSON", "build/words.json"))))
        self.T = Clock(self.cuts, self.CW)
        self.src = spec.path("build/roughcut.mp4")
        self.voice = spec.path("build/voice_clean.wav")
        self.wall = wall(spec.get("WALL"))
        self.hook_end = self.T(spec.HOOK_END) if spec.get("HOOK_END") is not None else 0
        self._pops(); self._brolls(); self._split(); self._intro(); self._captions()
        self.url_t = self.T(spec.URL_AT) if spec.get("URL") else None
        self.url = url_bar(spec.URL) if spec.get("URL") else None
        self.hold = spec.get("HOLD", 1.3)
        self.zooms = [(self.T(a), self.T(b), z) for a, b, z in spec.get("ZOOMS", [])]
        self.slow = self._slow_zooms(spec.get("SLOW_ZOOM"))
        self._kinetic()

    # ---------- pops ----------
    def _pops(self):
        self.pops, self.pop_sfx = [], []   # pop sfx=False = no pop sound (e.g. a text hook on frame 1)
        for p in self.s.get("POPS", []):
            im = load(self.s.path(p["img"]), w=p.get("w"), h=p.get("h"), r=p.get("r", 0), outline=p.get("outline", 0))
            self.pops.append((im, self.T(p["at"]), self.T(p["until"]), p["x"], p["y"]))
            if p.get("sfx", True): self.pop_sfx.append(self.T(p["at"]))
        self.boxes = [(t0, t1, x - im.width / 2, y - im.height / 2, x + im.width / 2, y + im.height / 2)
                      for im, t0, t1, x, y in self.pops]

    # ---------- B-roll screen recordings on the wall ----------
    def _brolls(self):
        self.brolls = []
        for b in self.s.get("BROLL", []):
            a, z = self.T(b["at"]), self.T(b["until"])
            cw = b.get("width", 620)
            probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", self.s.path(b["src"])], capture_output=True, text=True).stdout.split(",")
            sw, shh = int(probe[0]), int(probe[1])
            crop = ""
            if b.get("crop"):   # (x, y, w, h) in source pixels — e.g. cut the status bar (time/battery)
                cx_, cy_, sw, shh = b["crop"]; crop = f"crop={sw}:{shh}:{cx_}:{cy_},"
            ch = int(cw * shh / sw) // 2 * 2
            n = int(round((z - a) * FPS)) + 2
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(b.get("start", 0)), "-i", self.s.path(b["src"]), "-an",
                                  "-vf", f"setpts=(PTS-STARTPTS)/{b.get('speed', 1.0)},fps={FPS},{crop}scale={cw}:{ch}",
                                  "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            fs = cw * ch * 3
            frames = [raw[i * fs:(i + 1) * fs] for i in range(len(raw) // fs)]
            k = cw / sw   # blur boxes (x, y, w, h) in (cropped) source pixels -> card pixels; hides URL bars / logos
            blur = [tuple(int(v * k) for v in (x, y, x + w, y + h)) for x, y, w, h in b.get("blur", [])]
            self.brolls.append(dict(sfx=b.get("sfx", True), a=a, z=z, frames=frames, size=(cw, ch), y=b.get("y", 800), cap_y=b.get("cap_y", 1445),
                                    blur=blur, wall=wall(b["wall"]) if b.get("wall") else None,
                                    # over=True: video sits ON her A-roll (no wall) with a plain white border, at (x, y)
                                    over=b.get("over", False), x=b.get("x", W / 2), border=b.get("border", 8), r=b.get("r", 18)))

    def broll_frame(self, b, t):
        i = min(len(b["frames"]) - 1, int((t - b["a"]) * FPS))
        im = Image.frombuffer("RGB", b["size"], b["frames"][i], "raw", "RGB", 0, 1).copy()
        for bx in b["blur"]:
            im.paste(im.crop(bx).filter(ImageFilter.GaussianBlur(16)), bx[:2])
        if b["over"]:
            return sticker(rounded(im, b["r"]), b["border"])
        return card(im)

    # ---------- split screen: site recording in a rectangle on top, her A-roll cropped into a rectangle below ----------
    # SPLIT = dict(at=("cut", 3), until=("cut", 21), src="src/site.mp4", wall=None,
    #              top=(90, 200, 900, 506), bottom=(90, 846, 900, 690),   # (x, y, w, h) on the 1080x1920 frame
    #              face_crop=(0, 470, 1080, 828),                         # A-roll window (x, y, w, h) -> bottom box
    #              cap_y=776, sfx=True, blur=[(x, y, w, h), ...],          # blur boxes in recording pixels (logos/links)
    #              clips=[dict(at=("start", 4), rec=9.0, speed=2.0, crop=(x, y, w, h)), ...])
    #   sharp corners, no card/border; each clip runs until the next one starts (hard jump cuts / punch-ins);
    #   everything else (gap, sides, IG button + caption zone) is wall. Captions sit in the gap at cap_y.
    def _split(self):
        S = self.s.get("SPLIT"); self.split = None
        if not S: return
        a, z = self.T(S["at"]), self.T(S["until"])
        clips = [dict(c, t=self.T(c["at"])) for c in S["clips"]]
        for i, c in enumerate(clips): c["z"] = clips[i + 1]["t"] if i + 1 < len(clips) else z
        self.split = dict(S, a=a, z=z, clips=clips, src_path=self.s.path(S["src"]),
                          wall_im=wall(S["wall"]) if S.get("wall") else self.wall, rd=None)

    def _clip_frame(self, c, t):
        S = self.split; tx, ty, tw, th = S["top"]; k = int((t - c["t"]) * FPS)
        rd = S["rd"]
        if rd is None or rd["c"] is not c or rd["k"] > k:
            if rd: rd["p"].kill()
            x, y, w, h = c["crop"]; sp = c.get("speed", 1.0)
            p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{c['rec'] + k / FPS * sp:.3f}", "-i", S["src_path"], "-an",
                                  "-vf", f"crop={w}:{h}:{x}:{y},scale={tw}:{th}:flags=lanczos,setpts=(PTS-STARTPTS)/{sp},fps={FPS}",
                                  "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=10 ** 7)
            rd = S["rd"] = dict(c=c, p=p, k=k, last=None)
        n = tw * th * 3
        while rd["k"] <= k:
            b = rd["p"].stdout.read(n)
            if len(b) == n: rd["last"] = b
            rd["k"] += 1
        im = Image.frombuffer("RGB", (tw, th), rd["last"], "raw", "RGB", 0, 1).copy()
        x, y, w, h = c["crop"]; sx, sy = tw / w, th / h
        for bx, by, bw, bh in S.get("blur", []):
            box = (int((bx - x) * sx), int((by - y) * sy), int((bx + bw - x) * sx), int((by + bh - y) * sy))
            box = (max(0, box[0]), max(0, box[1]), min(tw, box[2]), min(th, box[3]))
            if box[2] > box[0] and box[3] > box[1]:
                im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
        return im

    def split_frame(self, t, base):
        S = self.split; fr = S["wall_im"].copy()
        c = next(c for c in S["clips"] if c["t"] <= t < c["z"]) if t >= S["clips"][0]["t"] else S["clips"][0]
        fr.paste(self._clip_frame(c, max(t, c["t"])), S["top"][:2])
        fx, fy, fw, fh = S.get("face_crop", (0, 470, 1080, 828)); bx, by, bw, bh = S["bottom"]
        fr.paste(base.convert("RGB").resize((bw, bh), Image.LANCZOS, box=(fx, fy, fx + fw, fy + fh)), (bx, by))
        return fr

    # ---------- optional intro card: stop-motion frames + a label pop (e.g. "Day 5") + typed title ----------
    def _intro(self):
        it = self.s.get("INTRO")
        self.intro = None
        if not it: return
        L = it["line"]
        a = self.cuts["picture_cuts"][L - 1] if L > 0 else 0.0
        b = self.cuts["picture_cuts"][L] if L < len(self.cuts["picture_cuts"]) else self.cuts["duration"]
        SC, IY = 0.82, 175
        bg = paper((W, H), it.get("bg", (112, 136, 178)), seed=11)
        frames = []
        for p in sorted(glob.glob(self.s.path(it["frames"]) + "/f*.png")):
            fr = bg.copy()
            c = sticker(rounded(Image.open(p).convert("RGB").resize((int(W * SC), int(H * SC)), Image.LANCZOS), 28))
            fr.alpha_composite(c, ((W - c.width) // 2, IY - 36)); frames.append(fr)
        fd = font(F_DIA, int(175 * SC)); txt = it.get("label") or (f"Day {self.s.DAY}" if self.s.get("DAY") is not None else "")
        dimg = Image.new("RGBA", (600, 260), (0, 0, 0, 0)); dd = ImageDraw.Draw(dimg)
        dd.text((306, 26), txt, font=fd, fill=INK, anchor="ma"); dd.text((300, 20), txt, font=fd, fill=BUTTER, anchor="ma")
        day = dimg.crop(dimg.getbbox()).rotate(-4, expand=True, resample=Image.BICUBIC) if txt else None
        title = it.get("title") or self.s.get("TITLE", "")
        ft = font(F_MON, int(98 * SC)); lines, cur = [], ""
        for w_ in title.split():
            c_ = (cur + " " + w_).strip()
            if ft.getbbox(c_)[2] <= 940 * SC: cur = c_
            else: lines.append(cur); cur = w_
        lines.append(cur)
        # typing: first title word -> just before the cut, weighted by syllables
        from .words import syllables
        tw = title.split() or [""]; first = tw[0]
        try: t0 = self.T(("w", L, first))
        except KeyError: t0 = a + 0.25
        t1 = b - 0.12; tot = sum(syllables(w) for w in tw); acc = 0; WT = []
        for w_ in tw:
            WT.append((w_, t0 + (t1 - t0) * acc / tot)); acc += syllables(w_)
        self.intro = dict(a=a, b=b, frames=frames, day=day, day_t=a + 0.05, lines=lines, ft=ft, WT=WT, t1=t1, title=title,
                          SC=SC, IY=IY, ty0=IY + int(it.get("title_y", 270) * SC), lh=int(98 * SC * 1.12))

    def intro_frame(self, t):
        I = self.intro
        fr = I["frames"][min(len(I["frames"]) - 1, int((t - I["a"]) * 8))].copy()
        if I["day"] is not None and t >= I["day_t"]: place(fr, I["day"], W // 2, I["IY"] + int(130 * I["SC"]))
        n = 0
        for i, (w_, ts) in enumerate(I["WT"]):
            if t < ts: break
            te = I["WT"][i + 1][1] if i + 1 < len(I["WT"]) else I["t1"]
            dur = min(max(te - ts, 0.08), 0.3)
            k = len(w_) if t >= ts + dur else int(len(w_) * (t - ts) / dur) + 1
            n += (1 if i else 0) + min(k, len(w_))
        d = ImageDraw.Draw(fr); left = n; ft = I["ft"]
        for li, line in enumerate(I["lines"]):
            if left <= 0: break
            part = line[:left]; lw = ft.getbbox(line)[2]
            x0 = W // 2 - lw // 2; y0 = I["ty0"] + li * I["lh"]
            d.text((x0 + 4, y0 + 4), part, font=ft, fill=INK); d.text((x0, y0), part, font=ft, fill=CREAM)
            if left <= len(line) and n < len(I["title"]):
                cx = x0 + (ft.getbbox(part)[2] if part else 0) + 6
                d.rectangle([cx, y0 + 6, cx + 5, y0 + I["lh"] - 10], fill=CREAM)
            left -= len(line) + 1
        return fr

    # ---------- captions ----------
    def _cap(self, text, _c={}):
        if text not in _c:
            f = font(F_DIA, 60); tw = int(f.getlength(text)) + 40
            im = Image.new("RGBA", (tw, 110), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((tw // 2, 20), text, font=f, fill=WHITE, anchor="ma")
            _c[text] = soft(im.crop(im.getbbox()))
        return _c[text]

    @staticmethod
    def _big(t_, size=112):
        f = font(F_DIA, size); asc, desc = f.getmetrics()
        im = Image.new("RGBA", (int(f.getlength(t_)) + 40, asc + desc + 10), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, asc), t_, font=f, fill=BUTTER, anchor="ls")
        bb = im.getbbox(); im = im.crop((bb[0], max(0, bb[1] - 4), bb[2], min(im.height, bb[3] + 4)))
        if im.width > 960: im = im.resize((960, int(im.height * 960 / im.width)), Image.LANCZOS)
        return soft(im)

    def _captions(self):
        CW = self.CW; WSET = {}; self.kin = []
        for gi, (L, w0, n, cx, cy) in enumerate(self.s.get("WEIGHTED", [])):
            lw = [x for x in CW if x["line"] == L]
            i0 = next(i for i, x in enumerate(lw) if x["w"].strip(",.?:!").lower() == w0.strip(",.?:!").lower())
            words = lw[i0:i0 + n]; items = []
            if cy < 0:   # negative y = one row, side by side
                cy = -cy; imgs = [self._big(x["w"].rstrip(",."), 100) for x in words]
                rw = sum(im.width - 60 for im in imgs) + 26 * (len(imgs) - 1); x_ = cx - rw // 2 - 30
                for im, x in zip(imgs, words):
                    items.append((im, x_, cy - im.height // 2, x["s"])); x_ += im.width - 60 + 26
            else:        # stacked, one word per row
                imgs = [self._big(x["w"].rstrip(",.")) for x in words]
                rowh = [im.height - 52 for im in imgs]; y = cy - sum(rowh) // 2 - 30
                for im, x, rh in zip(imgs, words, rowh):
                    items.append((im, cx - im.width // 2, y, x["s"])); y += rh
            items = [(im, max(-10, min(W + 10 - im.width, x_)), y_, ta) for im, x_, y_, ta in items]
            for k in range(n): WSET[(L, i0 + k)] = gi
            self.kin.append([words[0]["s"], None, items])
        skip = set(self.s.get("NO_CAPTION_LINES", [])) | ({self.s.INTRO["line"]} if self.s.get("INTRO") else set())
        self.chunks = []
        for L in sorted({x["line"] for x in CW}):
            if L in skip: continue
            ws = [x for x in CW if x["line"] == L]; cur = []
            for i, x in enumerate(ws):
                if (L, i) in WSET:
                    if cur: self.chunks.append({"text": " ".join(y["w"] for y in cur), "s": cur[0]["s"], "words": cur}); cur = []
                    continue
                cur.append(x)
                if x["w"][-1] in ",.?:!" or len(cur) == 3 or i == len(ws) - 1 or (L, i + 1) in WSET:
                    self.chunks.append({"text": " ".join(y["w"] for y in cur), "s": cur[0]["s"], "words": cur}); cur = []
        ev = sorted([("c", c["s"], c) for c in self.chunks] + [("k", g[0], g) for g in self.kin], key=lambda e: e[1])
        ia = self.intro["a"] if self.intro else 1e9
        for i, (kind, s_, obj) in enumerate(ev):
            nxt = ev[i + 1][1] if i + 1 < len(ev) else s_ + 1.5
            if ia > s_: nxt = min(nxt, ia)
            if kind == "c": obj["e"] = nxt
            else: obj[1] = nxt
        if self.chunks: self.chunks[-1]["e"] += self.s.get("HOLD", 1.3)

    # ---------- kinetic captions (opt-in) ----------
    # CAPTIONS = dict(font="Margarine-Regular.ttf", size=80, y=1130, key=[(line, "word"), ...], key_scale=1.3,
    #                 faces="build/faces.json")
    #   words appear one by one as she says them (no animation), key words butter + bigger,
    #   each chunk sits in the free spot nearest (540, y) that clears pops, her face, the URL bar and the bottom 20%.
    def _kinetic(self):
        K = self.s.get("CAPTIONS"); self.kc = None
        if not K: return
        from .gfx import FONTS
        fp = K["font"] if os.path.isabs(K["font"]) else os.path.join(FONTS, K["font"])
        size = K.get("size", 80); fN = font(fp, size); fK = font(fp, int(size * K.get("key_scale", 1.3)))
        keys = {(L, w.lower()) for L, w in K.get("key", [])}
        # face track [(t, x0, y0, x1, y1)]; drop misdetections far below a head (shirt folds etc.)
        self.faces = [f for f in (json.load(open(self.s.path(K["faces"]))) if K.get("faces") else [])
                      if f[1] is not None and f[2] < K.get("face_max_top", 800)]
        self.kY = K.get("y", 1130); sp = fN.getlength(" ")
        asc = max(fN.getmetrics()[0], fK.getmetrics()[0]); lh = int(asc * 1.02)

        def lay(its, maxw):   # -> (size, [xy per word]); greedy rows, centred
            rows, cur, cw_ = [], [], 0
            for i in its:
                wd = i["f"].getlength(i["w"])
                if cur and cw_ + sp + wd > maxw: rows.append(cur); cur, cw_ = [], 0
                cur.append(i); cw_ += (sp if len(cur) > 1 else 0) + wd
            rows.append(cur)
            rw = [sum(i["f"].getlength(i["w"]) for i in r) + sp * (len(r) - 1) for r in rows]
            Wc = int(max(rw)) + 30; xy = []
            for ri, r in enumerate(rows):
                x_ = (Wc - rw[ri]) / 2
                for i in r: xy.append((x_, asc + ri * lh)); x_ += i["f"].getlength(i["w"]) + sp
            return (Wc, lh * len(rows) + int(asc * 0.35)), xy

        self.kc = []
        for c in self.chunks:
            its = []
            for x in c["words"]:
                k = (x["line"], x["w"].strip(",.?:!").lower()) in keys
                its.append(dict(w=x["w"], f=fK if k else fN, col=BUTTER if k else WHITE, s=x["s"]))
            # layouts: one row, two rows, one word per row — the best (position + layout) score wins
            vars_ = [(0, lay(its, K.get("maxw", 960)))]
            if len(its) > 1: vars_ += [(50, lay(its, 480)), (110, lay(its, 10))]
            c2 = dict(s=c["s"], e=c["e"], its=its, cache={}); best = None
            for pen, (size, xy) in vars_:
                c2["size"] = size; r = self._kpos(c2)
                if r and (best is None or r[0] + pen < best[0]): best = (r[0] + pen, r[1], size, xy)
            if best is None:
                print(f"! no free spot for caption at {c2['s']:.2f}"); best = (0, (W / 2, self.kY)) + vars_[0][1]
            c2["pos"], c2["size"], c2["xy"] = best[1], best[2], best[3]
            self.kc.append(c2)

    def _kimg(self, c, n):
        if n not in c["cache"]:
            im = Image.new("RGBA", c["size"], (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            for i, xy in list(zip(c["its"], c["xy"]))[:n]: d.text(xy, i["w"], font=i["f"], fill=i["col"], anchor="ls")
            c["cache"][n] = soft(im)
        return c["cache"][n]

    def _kpos(self, c):
        s0, s1 = c["s"], c["e"]; cw, ch = c["size"][0] + 20, c["size"][1]
        for b in self.brolls:
            if b["a"] - 0.1 <= s0 < b["z"]: return 0, (W / 2, b["cap_y"])
        obs = [(x0 - 20, y0 - 20, x1 + 20, y1 + 20) for t0, t1, x0, y0, x1, y1 in self.boxes if t0 < s1 and t1 > s0]
        obs += [(x - 30, y - 30, x2 + 30, y2 + 40) for t, x, y, x2, y2 in self.faces if s0 - 0.2 <= t <= s1 + 0.2]
        if self.url is not None and self.url_t < s1:
            uy = self.s.get("URL_Y", 300); obs.append((40, uy - 100, W - 40, uy + 100))
        best = None
        for dy in (0, 70, -60, 140, 210, 245, 280, 315, 350, -120):
            for x in (540, 620, 460, 700, 380, 780, 300, 860, 220):
                y = self.kY + dy
                if x - cw / 2 < 20 or x + cw / 2 > W - 20 or y + ch / 2 > SAFE_BOTTOM: continue
                if any(a < x + cw / 2 and c_ > x - cw / 2 and b_ < y + ch / 2 and d > y - ch / 2 for a, b_, c_, d in obs): continue
                sc = abs(dy) + 0.5 * abs(x - 540)
                if best is None or sc < best[0]: best = (sc, x, y)
        return (best[0], (best[1], best[2])) if best else None

    def cap_pos(self, t, cw, ch):
        if self.split and self.split["a"] <= t < self.split["z"]: return W / 2, self.split.get("cap_y", 776)
        if t < self.hook_end: return W / 2, CAP_Y
        for b in self.brolls:
            if b["a"] <= t < b["z"]: return W / 2, b["cap_y"]
        act = [bx for bx in self.boxes if bx[0] <= t < bx[1]]
        hits = lambda cx, cy: any(x0 < cx + cw / 2 and x1 > cx - cw / 2 and y0 < cy + ch / 2 and y1 > cy - ch / 2
                                  for _, _, x0, y0, x1, y1 in act)
        cands = [(W / 2, CAP_Y)]
        for _, _, x0, y0, x1, y1 in act:
            cands += [(max(cw / 2 + 20, x0 / 2), CAP_Y), (min(W - cw / 2 - 20, (x1 + W) / 2), CAP_Y),
                      (W / 2, min(SAFE_BOTTOM - ch / 2, y1 + ch / 2 + 10)), (W / 2, y0 - ch / 2 - 10)]
        for cx, cy in cands:
            if not hits(cx, cy) and cy + ch / 2 <= SAFE_BOTTOM: return cx, cy
        return W / 2, CAP_Y

    # ---------- slow zooms: A-roll split into ~2-3 s blocks at picture cuts; each block eases in (or back out) ----------
    def _slow_zooms(self, Z):
        """SLOW_ZOOM = dict(amount=1.07, min=2.0, pattern="iio", skip_lines=[...]) -> [(t0, t1, z0, z1, ax, ay)].
        Lines are merged into blocks of >= min s (never split). Blocks follow the pattern (in, in, out, ...):
        in->in resets back to 1.0 on the line cut (the jump cut hides it), in->out / out->in flow on smoothly.
        Anchored on her face (mean face-track centre over the block) so she stays put while the room moves."""
        if not Z: return []
        amt, lo, hi = Z.get("amount", 1.07), Z.get("min", 2.0), Z.get("max", 3.2)
        cuts = [0.0] + self.cuts["picture_cuts"] + [self.cuts["duration"] + self.hold]
        skip = set(Z.get("skip_lines", []))
        busy = [(b["a"], b["z"]) for b in self.brolls] + ([(self.intro["a"], self.intro["b"])] if self.intro else [])
        lines = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)
                 if i not in skip and not any(a < cuts[i + 1] - 0.05 and b > cuts[i] + 0.05 for a, b in busy)]
        blocks, cur = [], None
        for a, b in lines:   # merge touching lines into blocks of >= lo s; split anything longer than hi
            if cur and abs(cur[1] - a) < 1e-3 and cur[1] - cur[0] < lo: cur[1] = b
            else:
                if cur: blocks.append(cur)
                cur = [a, b]
        if cur: blocks.append(cur)
        out = blocks   # never split inside a line: a reset mid-sentence reads as a glitch
        faces = [f for f in json.load(open(self.s.path("build/faces.json")))
                 if f[1] is not None and f[2] < 800] if os.path.exists(self.s.path("build/faces.json")) else []
        res = []
        for i, (a, b) in enumerate(out):
            fs = [f for f in faces if a <= f[0] <= b]
            ax = sum((f[1] + f[3]) / 2 for f in fs) / len(fs) if fs else W / 2
            ay = sum((f[2] + f[4]) / 2 for f in fs) / len(fs) if fs else 760
            pat = Z.get("pattern", "iio")   # i = slow zoom in, o = slow zoom out; i->i = reset (punch back) on the cut
            z0, z1 = (1.0, amt) if pat[i % len(pat)] == "i" else (amt, 1.0)
            res.append((a, b, z0, z1, ax, ay))
        return res

    # ---------- one frame ----------
    def frame(self, t, base):
        fr = base
        for z0, z1, zs in self.zooms:   # hard punch-in, anchored on her face
            if z0 <= t < z1:
                ax, ay = self.s.get("ZOOM_ANCHOR", (540, 700))
                fr = fr.crop((int(ax - ax / zs), int(ay - ay / zs), int(ax + (W - ax) / zs), int(ay + (H - ay) / zs))).resize((W, H), Image.LANCZOS)
        for a, b, z0, z1, ax, ay in self.slow:
            if a <= t < b:
                u = (t - a) / (b - a); u = u * u * (3 - 2 * u)          # ease in-out
                zs = z0 + (z1 - z0) * u
                fr = fr.resize((W, H), Image.BICUBIC, box=(ax - ax / zs, ay - ay / zs, ax + (W - ax) / zs, ay + (H - ay) / zs))
        if self.intro and self.intro["a"] <= t < self.intro["b"]: fr = self.intro_frame(t)
        if self.split and self.split["a"] <= t < self.split["z"]: fr = self.split_frame(t, fr)
        for b in self.brolls:
            if b["a"] <= t < b["z"]:
                if b["over"]: place(fr, self.broll_frame(b, t), b["x"], b["y"])
                else: fr = (b["wall"] or self.wall).copy(); place(fr, self.broll_frame(b, t), W / 2, b["y"])
        for im, t0, t1, x, y in self.pops:
            if t0 <= t < t1: place(fr, im, x, y)
        if self.url and t >= self.url_t: place(fr, self.url, W / 2, self.s.get("URL_Y", 300))
        for g0, g1, items in self.kin:
            if g0 <= t < g1:
                for im, x_, y_, ta in items:
                    if t >= ta: fr.alpha_composite(im, (int(x_), int(y_)))
        if self.kc is not None:
            for c in self.kc:
                if c["s"] <= t < c["e"]:
                    n = max(1, sum(1 for i in c["its"] if i["s"] <= t)); place(fr, self._kimg(c, n), *c["pos"]); break
            return fr
        for c in self.chunks:
            if c["s"] <= t < c["e"]:
                ci = self._cap(c["text"]); place(fr, ci, *self.cap_pos(t, ci.width, ci.height)); break
        return fr

    def sfx_list(self):
        sfx = [("pop.mp3", t0, 0.22) for t0 in self.pop_sfx]
        if self.intro and self.intro["day"] is not None: sfx.append(("pop.mp3", self.intro["day_t"], 0.30))
        sfx += [("pop.mp3", b["a"], 0.20) for b in self.brolls if b["sfx"]]   # sfx=False: jump-cut continuations / own SFX
        if self.split and self.split.get("sfx", True): sfx.append(("pop.mp3", self.split["a"], 0.20))
        if self.url: sfx.append(("pop.mp3", self.url_t, 0.32))
        sfx += [(f if os.path.isabs(f) or os.path.exists(os.path.join(SFX, f)) else self.s.path(f), self.T(at), v)
                for f, at, v in self.s.get("EXTRA_SFX", [])]   # kit sfx name, or a reel-local trimmed file
        return sfx


def run(spec_path, only=()):
    spec = load_spec(spec_path); R = Reel(spec)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0",
                                R.src], capture_output=True, text=True).stdout)
    NF = int(round((dur + R.hold) * FPS)); last = None
    rd = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", R.src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=10 ** 8)
    vid = spec.path("build/_video.mp4")
    enc = None if only else subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                                              "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    prev = []
    for fi in range(NF):
        t = fi / FPS
        raw = rd.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: raw = last
        last = raw
        if only and not any(abs(t - o) < 0.5 / FPS for o in only): continue
        fr = R.frame(t, Image.frombuffer("RGB", (W, H), raw, "raw", "RGB", 0, 1).convert("RGBA"))
        if only:
            p = spec.path(f"build/prev_{t:.2f}.jpg"); fr.convert("RGB").resize((360, 640)).save(p); prev.append(p)
        else: enc.stdin.write(fr.convert("RGB").tobytes())
    rd.kill()
    if only:
        sheet = Image.new("RGB", (360 * len(prev), 640))
        for i, p in enumerate(prev): sheet.paste(Image.open(p), (360 * i, 0))
        sheet.save(spec.path("build/preview_sheet.jpg")); print("preview ->", spec.path("build/preview_sheet.jpg")); return
    enc.stdin.close(); enc.wait()
    sfx = R.sfx_list(); ins = ["-i", vid, "-i", R.voice]; fc = ""
    for j, (f_, t0, v) in enumerate(sfx):
        ins += ["-i", os.path.join(SFX, f_)]; dms = int(t0 * 1000)
        fc += f"[{j + 2}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={v},adelay={dms}|{dms}[s{j}];"
    fc += "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad[v0];[v0]" + "".join(f"[s{j}]" for j in range(len(sfx)))
    fc += f"amix=inputs={len(sfx) + 1}:normalize=0:duration=first,atrim=0:{NF / FPS:.3f},alimiter=limit=0.94:attack=5:release=80:level=false[a]"
    out = spec.path("build/final.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *ins, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out, "-c:v", "libx264", "-crf", "22", "-maxrate", "6M", "-bufsize", "12M",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", spec.path("build/final_send.mp4")], check=True)
    print("done", round(NF / FPS, 2), "s ->", out)


if __name__ == "__main__":
    run(sys.argv[1], [float(x) for x in sys.argv[2:]])
