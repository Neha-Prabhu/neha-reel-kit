"""Load a reel spec (reels/<name>/reel.py) and resolve times against the cut."""
import importlib.util, json, os


class Spec:
    def __init__(self, mod, folder):
        self.__dict__.update({k: v for k, v in vars(mod).items() if not k.startswith("_")})
        self.folder = folder

    def path(self, p):
        return p if os.path.isabs(p) else os.path.join(self.folder, p)

    def get(self, k, default=None):
        return getattr(self, k, default)


def load_spec(path):
    path = os.path.abspath(path)
    s = importlib.util.spec_from_file_location("reel_spec", path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return Spec(m, os.path.dirname(path))


class Clock:
    """Resolves time references used in specs:
         3.2                      -> absolute seconds on the rough cut
         ("cut", i)               -> i-th picture cut (cut 0 = end of line 0)
         ("start", L) / ("end", L) -> first / last moment of line L
         ("w", L, "word", nth)    -> start of a spoken word in line L (nth occurrence, default 0)
       any of these + an offset:  (("cut", 8), 0.10)
    """
    def __init__(self, cuts, words):
        self.cuts = cuts["picture_cuts"]; self.words = words
        self.lines = sorted({w["line"] for w in words})

    def word(self, L, w, nth=0):
        hits = [x for x in self.words if x["line"] == L and x["w"].strip(",.?:!").lower() == w.lower()]
        if len(hits) <= nth: raise KeyError(f"word {w!r} #{nth} not in line {L}: {[x['w'] for x in self.words if x['line'] == L]}")
        return hits[nth]["s"]

    def __call__(self, ref):
        if isinstance(ref, (int, float)): return float(ref)
        if isinstance(ref[0], tuple): return self(ref[0]) + ref[1]
        kind = ref[0]
        if kind == "cut": return self.cuts[ref[1]]
        if kind == "start": return min(x["s"] for x in self.words if x["line"] == ref[1])
        if kind == "end": return max(x["e"] for x in self.words if x["line"] == ref[1])
        if kind == "w": return self.word(ref[1], ref[2], ref[3] if len(ref) > 3 else 0)
        raise ValueError(ref)
