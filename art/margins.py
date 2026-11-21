"""Margin tiles: the page beyond the scene's edges.

Each zone's left/right margin repeats a 64px tile built from the outer columns of the scene,
keeping only what reads as background (gradient dither, soil texture) so foreground details at
the edge (a mailbox flag, a star, a fence post) don't smear into stripes across the margin.
"""
from collections import Counter
import hashlib
from PIL import Image

T = 64          # tile width in art pixels
BAND = 4        # outer columns sampled per side
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def _rows(im, side):
    w, h = im.size
    xs = range(BAND) if side == 'L' else range(w - BAND, w)
    px = im.load()
    return [Counter(px[x, y] for x in xs) for y in range(h)]


def _r(x, y, salt):
    return hashlib.blake2b(f'{x},{y},{salt}'.encode(), digest_size=2).digest()[0] / 255


def tile(im, side):
    im = im.convert('RGBA')
    rows = _rows(im, side)
    h = len(rows)
    # colours that only show up in a few rows along the edge are foreground (a flag, lamp dots, a star):
    # rows that contain them borrow their background from the nearest clean row
    seen = Counter()
    for c in rows:
        seen.update(c.keys())
    rare = {k for k, n in seen.items() if n < h * 0.04}
    dirty = [any(k in rare for k in c) for c in rows]
    clean = []
    for y in range(h):
        if not dirty[y]:
            clean.append(y); continue
        for d in range(1, h):
            hit = next((yy for yy in (y - d, y + d) if 0 <= yy < h and not dirty[yy]), None)
            if hit is not None:
                clean.append(hit); break
        else:
            clean.append(y)
    # texture colours: present in plenty of rows (soil specks, wall grain), never one-off objects
    texture = {k for k, n in seen.items() if n >= h * 0.08}
    out = Image.new('RGBA', (T, h))
    op = out.load()
    for y in range(h):
        # a few neighbouring rows together, so speckled soil reads as speckles and not as strata
        c = Counter()
        for dy in (-2, -1, 0, 1, 2):
            yy = clean[min(h - 1, max(0, y + dy))]
            if rows[yy].most_common(1)[0][0] == rows[clean[y]].most_common(1)[0][0]:
                c.update(rows[yy])
        n = sum(c.values()) / BAND
        (c1, n1), *rest = c.most_common()
        c2, n2 = rest[0] if rest else (c1, 0)
        p = n2 / (n1 + n2) if n2 else 0
        extra = [(k, m / (BAND * n)) for k, m in rest[1:] if k in texture]
        for x in range(T):
            col = c2 if BAYER[y % 4][x % 4] < p * 16 else c1
            for i, (k, share) in enumerate(extra):
                if _r(x, y, i) < share * 0.6:
                    col = k
            op[x, y] = col
    return out
