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
from PIL import Image, ImageDraw
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
        self._pops(); self._brolls(); self._intro(); self._captions()
        self.url_t = self.T(spec.URL_AT) if spec.get("URL") else None
        self.url = url_bar(spec.URL) if spec.get("URL") else None
        self.hold = spec.get("HOLD", 1.3)
        self.zooms = [(self.T(a), self.T(b), z) for a, b, z in spec.get("ZOOMS", [])]

    # ---------- pops ----------
    def _pops(self):
        self.pops = []
        for p in self.s.get("POPS", []):
            im = load(self.s.path(p["img"]), w=p.get("w"), h=p.get("h"), r=p.get("r", 0), outline=p.get("outline", 0))
            self.pops.append((im, self.T(p["at"]), self.T(p["until"]), p["x"], p["y"]))
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
            ch = int(cw * int(probe[1]) / int(probe[0])) // 2 * 2
            n = int(round((z - a) * FPS)) + 2
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(b.get("start", 0)), "-i", self.s.path(b["src"]), "-an",
                                  "-vf", f"setpts=(PTS-STARTPTS)/{b.get('speed', 1.0)},fps={FPS},scale={cw}:{ch}",
                                  "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
            fs = cw * ch * 3
            frames = [raw[i * fs:(i + 1) * fs] for i in range(len(raw) // fs)]
            self.brolls.append(dict(a=a, z=z, frames=frames, size=(cw, ch), y=b.get("y", 800), cap_y=b.get("cap_y", 1445)))

    def broll_frame(self, b, t):
        i = min(len(b["frames"]) - 1, int((t - b["a"]) * FPS))
        return card(Image.frombuffer("RGB", b["size"], b["frames"][i], "raw", "RGB", 0, 1))

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
                    if cur: self.chunks.append({"text": " ".join(y["w"] for y in cur), "s": cur[0]["s"]}); cur = []
                    continue
                cur.append(x)
                if x["w"][-1] in ",.?:!" or len(cur) == 3 or i == len(ws) - 1 or (L, i + 1) in WSET:
                    self.chunks.append({"text": " ".join(y["w"] for y in cur), "s": cur[0]["s"]}); cur = []
        ev = sorted([("c", c["s"], c) for c in self.chunks] + [("k", g[0], g) for g in self.kin], key=lambda e: e[1])
        ia = self.intro["a"] if self.intro else 1e9
        for i, (kind, s_, obj) in enumerate(ev):
            nxt = ev[i + 1][1] if i + 1 < len(ev) else s_ + 1.5
            if ia > s_: nxt = min(nxt, ia)
            if kind == "c": obj["e"] = nxt
            else: obj[1] = nxt
        if self.chunks: self.chunks[-1]["e"] += self.s.get("HOLD", 1.3)

    def cap_pos(self, t, cw, ch):
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

    # ---------- one frame ----------
    def frame(self, t, base):
        fr = base
        for z0, z1, zs in self.zooms:   # hard punch-in, anchored on her face
            if z0 <= t < z1:
                ax, ay = self.s.get("ZOOM_ANCHOR", (540, 700))
                fr = fr.crop((int(ax - ax / zs), int(ay - ay / zs), int(ax + (W - ax) / zs), int(ay + (H - ay) / zs))).resize((W, H), Image.LANCZOS)
        if self.intro and self.intro["a"] <= t < self.intro["b"]: fr = self.intro_frame(t)
        for b in self.brolls:
            if b["a"] <= t < b["z"]:
                fr = self.wall.copy(); place(fr, self.broll_frame(b, t), W / 2, b["y"])
        for im, t0, t1, x, y in self.pops:
            if t0 <= t < t1: place(fr, im, x, y)
        if self.url and t >= self.url_t: place(fr, self.url, W / 2, self.s.get("URL_Y", 300))
        for g0, g1, items in self.kin:
            if g0 <= t < g1:
                for im, x_, y_, ta in items:
                    if t >= ta: fr.alpha_composite(im, (int(x_), int(y_)))
        for c in self.chunks:
            if c["s"] <= t < c["e"]:
                ci = self._cap(c["text"]); place(fr, ci, *self.cap_pos(t, ci.width, ci.height)); break
        return fr

    def sfx_list(self):
        sfx = [("pop.mp3", t0, 0.22) for _, t0, *_ in self.pops]
        if self.intro and self.intro["day"] is not None: sfx.append(("pop.mp3", self.intro["day_t"], 0.30))
        sfx += [("pop.mp3", b["a"], 0.20) for b in self.brolls]
        if self.url: sfx.append(("pop.mp3", self.url_t, 0.32))
        sfx += [(f, self.T(at), v) for f, at, v in self.s.get("EXTRA_SFX", [])]
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
