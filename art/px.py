"""Pixel toolkit for R5-House: one palette, index canvases, lighting, PNG out.

Every image on the page is drawn here at 1x into palette indices, then lit
(day = golden hour, night = moon/lamp/monitor) and saved as PNG. The page
scales them up with image-rendering: pixelated at an integer scale.
"""
import numpy as np
from PIL import Image

# ---------------------------------------------------------------- palette
PAL = [
    ('k0', '#0d0b1a'),  # ink / outline
    ('n1', '#161a3a'), ('n2', '#222b5c'), ('n3', '#33438a'), ('n4', '#4f69b5'), ('n5', '#86a2dc'), ('n6', '#c4d4f2'),
    ('w0', '#2a1a14'), ('w1', '#4a2c1c'), ('w2', '#70432a'), ('w3', '#9c6438'), ('w4', '#c99258'),
    ('c0', '#fffaf0'), ('c1', '#efe2c0'), ('c2', '#d4bc8e'),
    ('g1', '#6e4c10'), ('g2', '#b5821a'), ('g3', '#ffb612'), ('g4', '#ffe08a'),
    ('r1', '#4e1420'), ('r2', '#9a2430'), ('r3', '#d9483b'),
    ('o1', '#b8501e'), ('o2', '#f08a24'), ('o3', '#ffc35c'),
    ('p1', '#5c2f6e'), ('p2', '#a8487a'), ('p3', '#e7807a'),
    ('e1', '#183326'), ('e2', '#2c5a36'), ('e3', '#5f9444'),
    ('s1', '#3b3c4c'), ('s2', '#6b6e80'), ('s3', '#a7abbe'),
    ('t1', '#1f6b72'), ('t2', '#45c4b4'), ('t3', '#a8f0de'),
]
NAMES = [n for n, _ in PAL]
IDX = {n: i for i, n in enumerate(NAMES)}
RGB = np.array([[int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)] for _, h in PAL], dtype=np.int32)
T = 255  # transparent index

# one-char legend used by every hand-drawn grid
LEGEND = {
    'K': 'k0', '1': 'n1', '2': 'n2', '3': 'n3', '4': 'n4', '5': 'n5', '6': 'n6',
    'a': 'w0', 'b': 'w1', 'c': 'w2', 'd': 'w3', 'e': 'w4',
    'W': 'c0', 'P': 'c1', 'Q': 'c2',
    'y': 'g1', 'h': 'g2', 'G': 'g3', 'Y': 'g4',
    'r': 'r1', 'R': 'r2', 'T': 'r3',
    'o': 'o1', 'O': 'o2', 'U': 'o3',
    'v': 'p1', 'V': 'p2', 'p': 'p3',
    'j': 'e1', 'J': 'e2', 'L': 'e3',
    '7': 's1', '8': 's2', '9': 's3',
    'u': 't1', 'n': 't2', 'N': 't3',
}


def lum(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def dist(a, b):
    rm = (a[0] + b[0]) / 2
    dr, dg, db = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return (2 + rm / 256) * dr * dr + 4 * dg * dg + (2 + (255 - rm) / 256) * db * db


def nearest(target, allowed):
    best, bi = 1e18, None
    for i in allowed:
        d = dist(target, RGB[i])
        if d < best:
            best, bi = d, i
    return bi


EMISSIVE_FAMILY = {IDX['t1'], IDX['t2'], IDX['t3']}


def _build_maps():
    n = len(PAL)
    L = [lum(RGB[i]) for i in range(n)]
    dim = list(range(n))
    warm = list(range(n))
    for i in range(n):
        c = RGB[i]
        tgt = (c[0] * .64, c[1] * .68, c[2] * .84 + 6)
        allowed = [j for j in range(n) if L[j] < L[i] - 6 and j not in EMISSIVE_FAMILY]
        dim[i] = nearest(tgt, allowed) if allowed else i
        tgt = (min(255, c[0] * 1.1 + 26), min(255, c[1] * 1.08 + 16), c[2] * .95)
        allowed = [j for j in range(n) if L[j] >= L[i] - 2 and j not in EMISSIVE_FAMILY]
        warm[i] = nearest(tgt, allowed) if allowed else i
    # hand corrections so families stay coherent at night
    fix_dim = {'n1': 'k0', 'n2': 'n1', 'n3': 'n2', 'n4': 'n3', 'n5': 'n4', 'n6': 'n5',
               'w0': 'k0', 'w1': 'w0', 'w2': 'w1', 'w3': 'w2', 'w4': 'w3',
               'c0': 'c1', 'c1': 's3', 'c2': 's2',
               'g4': 'g3', 'g3': 'g2', 'g2': 'g1', 'g1': 'w0',
               'r3': 'r2', 'r2': 'r1', 'r1': 'k0', 'o3': 'o2', 'o2': 'o1', 'o1': 'r1',
               'p3': 'p2', 'p2': 'p1', 'p1': 'n1', 'e3': 'e2', 'e2': 'e1', 'e1': 'k0',
               's3': 's2', 's2': 's1', 's1': 'n1', 'k0': 'k0'}
    for a, b in fix_dim.items():
        dim[IDX[a]] = IDX[b]
    fix_warm = {'w3': 'w4', 'w2': 'w3', 'w1': 'w2', 'w4': 'o3', 'c1': 'c0', 'c2': 'c1',
                'n3': 'n4', 'n2': 'n3', 'n1': 'n2', 'g3': 'g4', 'g2': 'g3', 'r2': 'r3', 'o2': 'o3',
                'e2': 'e3', 's2': 's3', 's1': 's2', 'k0': 'n1', 'n4': 'n5', 'r1': 'r2', 'e1': 'e2'}
    for a, b in fix_warm.items():
        warm[IDX[a]] = IDX[b]
    return dim, warm


DIM, WARM = _build_maps()
DIM2 = [DIM[DIM[i]] for i in range(len(PAL))]

# black-and-gold palette for the 7-orb ending (applied on top of the night render)
GOLDMAP = list(range(len(PAL)))
for a, b in {'n1': 'k0', 'n2': 'w0', 'n3': 'g1', 'n4': 'g2', 'n5': 'g3', 'n6': 'g4',
             'p1': 'w0', 'p2': 'g1', 's1': 'k0', 's2': 'g1', 's3': 'g2', 't1': 'g1', 't2': 'g3', 't3': 'g4',
             'e1': 'k0', 'e2': 'w1', 'e3': 'g2'}.items():
    GOLDMAP[IDX[a]] = IDX[b]

BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + .5) / 16


def C(name):
    if name in IDX:
        return IDX[name]
    return IDX[LEGEND[name]]


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, fill=None):
        self.w, self.h = w, h
        self.a = np.full((h, w), T if fill is None else C(fill), dtype=np.uint8)
        self.em = np.zeros((h, w), dtype=bool)   # emissive: never darkened

    def copy(self):
        c = Canvas(self.w, self.h)
        c.a = self.a.copy(); c.em = self.em.copy()
        return c

    # -- primitives
    def px(self, x, y, c, em=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = C(c) if isinstance(c, str) else c
            self.em[y, x] = em

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.a[y, x]
        return T

    def rect(self, x, y, w, h, c, em=False):
        x0, y0, x1, y1 = max(0, x), max(0, y), min(self.w, x + w), min(self.h, y + h)
        if x1 > x0 and y1 > y0:
            self.a[y0:y1, x0:x1] = C(c) if isinstance(c, str) else c
            self.em[y0:y1, x0:x1] = em

    def frame(self, x, y, w, h, c):
        self.rect(x, y, w, 1, c); self.rect(x, y + h - 1, w, 1, c)
        self.rect(x, y, 1, h, c); self.rect(x + w - 1, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c, em=False, dash=None):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err, i = dx + dy, 0
        while True:
            if dash is None or (i % dash[0]) < dash[1]:
                self.px(x0, y0, c, em)
            i += 1
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def ellipse(self, cx, cy, rx, ry, c, em=False):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if ((x - cx + .5) / (rx + .01)) ** 2 + ((y - cy + .5) / (ry + .01)) ** 2 <= 1:
                    self.px(x, y, c, em)

    def disc(self, cx, cy, r, c, em=False):
        self.ellipse(cx, cy, r, r, c, em)

    def poly(self, pts, c, em=False):
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
                if (y0 <= y + .5 < y1) or (y1 <= y + .5 < y0):
                    xs.append(x0 + (y + .5 - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(round(xs[i])), int(round(xs[i + 1]))):
                    self.px(x, y, c, em)

    def dither(self, x, y, w, h, c1, c2, level=.5, em=False):
        """fill with c2 where bayer < level, else c1"""
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px(xx, yy, c2 if BAYER[yy % 4][xx % 4] < level else c1, em)

    def blit(self, spr, x, y, flip=False, em=None):
        sh, sw = spr.a.shape
        for yy in range(sh):
            for xx in range(sw):
                v = spr.a[yy, sw - 1 - xx] if flip else spr.a[yy, xx]
                if v != T:
                    e = spr.em[yy, sw - 1 - xx] if flip else spr.em[yy, xx]
                    self.px(x + xx, y + yy, int(v), bool(e) if em is None else em)

    def text(self, x, y, s, c, em=False, font=None):
        f = font or FONT35
        cx = x
        for ch in s:
            g = f.get(ch.upper())
            if g is None:
                cx += 2
                continue
            for yy, row in enumerate(g):
                for xx, v in enumerate(row):
                    if v == '#':
                        self.px(cx + xx, y + yy, c, em)
            cx += len(g[0]) + 1
        return cx - x - 1

    def outline(self, c='k0'):
        """add a 1px outline around opaque pixels (in place, grows into transparency)"""
        m = self.a != T
        o = np.zeros_like(m)
        o[1:, :] |= m[:-1, :]; o[:-1, :] |= m[1:, :]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
        o &= ~m
        self.a[o] = C(c)

    # -- output
    def render(self, mapping=None, light=None, gold=False):
        a = self.a.astype(np.int32)
        out = a.copy()
        if light is not None:
            # light: float array (h,w) of tier level 0..3 (0 night, 1 dim, 2 base, 3 warm)
            hh, ww = a.shape
            by = np.tile(BAYER, (hh // 4 + 1, ww // 4 + 1))[:hh, :ww]
            base = np.floor(light)
            frac = np.clip((light - base - .5) * 2.6 + .5, 0, 1)   # narrow dither bands, solid tiers
            tier = (base + (frac > by)).astype(np.int32)
            tier = np.clip(tier, 0, 3)
            tabs = [np.array(DIM2 + [T] * (256 - len(PAL))), np.array(DIM + [T] * (256 - len(PAL))),
                    np.arange(256), np.array(WARM + [T] * (256 - len(PAL)))]
            for t in range(4):
                sel = (tier == t) & (a != T) & (~self.em)
                out[sel] = tabs[t][a[sel]]
        if mapping is not None:
            m = np.array(mapping + [T] * (256 - len(mapping)))
            sel = out != T
            out[sel] = m[out[sel]]
        if gold:
            m = np.array(GOLDMAP + [T] * (256 - len(GOLDMAP)))
            sel = out != T
            out[sel] = m[out[sel]]
        img = np.zeros(a.shape + (4,), dtype=np.uint8)
        sel = out != T
        img[sel, :3] = RGB[out[sel]]
        img[sel, 3] = 255
        return Image.fromarray(img, 'RGBA')

    def save(self, path, **kw):
        self.render(**kw).save(path, optimize=True)


def grid(rows, legend=None, em_chars=''):
    """Canvas from a list of strings using the global legend."""
    rows = [r for r in rows if r is not None]
    w = max(len(r) for r in rows)
    c = Canvas(w, len(rows))
    leg = dict(LEGEND)
    if legend:
        leg.update(legend)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in (' ', '.'):
                continue
            c.px(x, y, leg[ch], em=ch in em_chars)
    return c


def strip(frames):
    """horizontal sprite sheet from equal-size canvases"""
    w, h = frames[0].w, frames[0].h
    s = Canvas(w * len(frames), h)
    for i, f in enumerate(frames):
        s.blit(f, i * w, 0)
    return s


# ---------------------------------------------------------------- light fields
def blur(m, r):
    """separable box blur, 2 passes (soft light edges)"""
    m = m.astype(np.float32)
    for _ in range(2):
        k = 2 * r + 1
        p = np.pad(m, ((0, 0), (r, r)), mode='edge')
        cs = np.cumsum(np.pad(p, ((0, 0), (1, 0))), axis=1)
        m = (cs[:, k:] - cs[:, :-k]) / k
        p = np.pad(m, ((r, r), (0, 0)), mode='edge')
        cs = np.cumsum(np.pad(p, ((1, 0), (0, 0))), axis=0)
        m = (cs[k:, :] - cs[:-k, :]) / k
    return m


class Light:
    def __init__(self, w, h, ambient):
        self.w, self.h = w, h
        self.f = np.full((h, w), float(ambient), dtype=np.float32)

    def pool(self, cx, cy, rx, ry, strength, core=1.0):
        yy, xx = np.mgrid[0:self.h, 0:self.w]
        d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        v = np.clip(1 - d, 0, 1) ** core
        self.f += strength * v

    def shaft(self, pts, strength, soft=3):
        c = Canvas(self.w, self.h)
        c.poly(pts, 'k0')
        m = (c.a != T).astype(np.float32)
        if soft:
            m = blur(m, soft)
        self.f += strength * m

    def shade(self, x, y, w, h, amount, soft=3):
        m = np.zeros((self.h, self.w), np.float32)
        m[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = 1
        if soft:
            m = blur(m, soft)
        self.f -= amount * m

    def set(self, x, y, w, h, v):
        self.f[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = v

    def clip(self, x, y, w, h, amb):
        m = np.ones_like(self.f, dtype=bool)
        m[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = False
        self.f[m] = amb

    def get(self):
        return np.clip(self.f, 0, 3.0)

    def sub(self, x, y, w, h):
        """light sub-field for a sprite placed at (x,y)"""
        out = np.zeros((h, w), np.float32)
        f = self.get()
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if x1 > x0 and y1 > y0:
            out[y0 - y:y1 - y, x0 - x:x1 - x] = f[y0:y1, x0:x1]
        return out


# ---------------------------------------------------------------- 3x5 font for baked numbers/letters
_F = {
    '0': ['###', '#.#', '#.#', '#.#', '###'], '1': ['.#.', '##.', '.#.', '.#.', '###'],
    '2': ['##.', '..#', '.#.', '#..', '###'], '3': ['##.', '..#', '.#.', '..#', '##.'],
    '4': ['#.#', '#.#', '###', '..#', '..#'], '5': ['###', '#..', '##.', '..#', '##.'],
    '6': ['.##', '#..', '###', '#.#', '###'], '7': ['###', '..#', '.#.', '.#.', '.#.'],
    '8': ['###', '#.#', '###', '#.#', '###'], '9': ['###', '#.#', '###', '..#', '##.'],
    'A': ['.#.', '#.#', '###', '#.#', '#.#'], 'B': ['##.', '#.#', '##.', '#.#', '##.'],
    'C': ['.##', '#..', '#..', '#..', '.##'], 'D': ['##.', '#.#', '#.#', '#.#', '##.'],
    'E': ['###', '#..', '##.', '#..', '###'], 'F': ['###', '#..', '##.', '#..', '#..'],
    'G': ['.##', '#..', '#.#', '#.#', '.##'], 'H': ['#.#', '#.#', '###', '#.#', '#.#'],
    'I': ['###', '.#.', '.#.', '.#.', '###'], 'J': ['..#', '..#', '..#', '#.#', '.#.'],
    'K': ['#.#', '#.#', '##.', '#.#', '#.#'], 'L': ['#..', '#..', '#..', '#..', '###'],
    'M': ['#.#', '###', '###', '#.#', '#.#'], 'N': ['##.', '#.#', '#.#', '#.#', '#.#'],
    'O': ['.#.', '#.#', '#.#', '#.#', '.#.'], 'P': ['##.', '#.#', '##.', '#..', '#..'],
    'R': ['##.', '#.#', '##.', '#.#', '#.#'], 'S': ['.##', '#..', '.#.', '..#', '##.'],
    'T': ['###', '.#.', '.#.', '.#.', '.#.'], 'U': ['#.#', '#.#', '#.#', '#.#', '###'],
    'V': ['#.#', '#.#', '#.#', '#.#', '.#.'], 'W': ['#.#', '#.#', '###', '###', '#.#'],
    'X': ['#.#', '#.#', '.#.', '#.#', '#.#'], 'Y': ['#.#', '#.#', '.#.', '.#.', '.#.'],
    'Z': ['###', '..#', '.#.', '#..', '###'], '-': ['...', '...', '###', '...', '...'],
    '.': ['.', '.', '.', '.', '#'], ':': ['.', '#', '.', '#', '.'], '/': ['..#', '..#', '.#.', '#..', '#..'],
}
FONT35 = _F
# 3x4 tiny digits (for setlist tempos where space is tight)
FONT34 = {
    '0': ['###', '#.#', '#.#', '###'], '1': ['.#.', '##.', '.#.', '###'], '2': ['##.', '..#', '.#.', '###'],
    '3': ['###', '.##', '..#', '###'], '4': ['#.#', '#.#', '###', '..#'], '5': ['###', '##.', '..#', '##.'],
    '6': ['#..', '###', '#.#', '###'], '7': ['###', '..#', '.#.', '.#.'], '8': ['###', '###', '#.#', '###'],
    '9': ['###', '#.#', '###', '..#'],
}
