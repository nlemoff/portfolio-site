"""R5-House scene compositor.

Zones (top to bottom): top (sky + roof), room, garage, base (basement + bedrock).
Two compositions: D (desktop, 352 art px wide) and M (phone, 180 art px wide).
Each zone is drawn per mode (day = golden hour, night) into palette indices,
then lit with a light field (moon / desk lamp / monitor, plus golden-hour sun)
and ordered-dithered between light tiers.

compose(zone, layout, mode) -> Z with .c (Canvas), .light (Light), .ov (overlays), .tx (text boxes)
"""
import math
import random
import numpy as np
from px import Canvas, Light, grid, C, T, BAYER, FONT35, FONT34
import sprites as S

D_W, M_W = 352, 180


class Z:
    def __init__(self, w, h, mode, amb):
        self.c = Canvas(w, h)
        self.light = Light(w, h, amb)
        self.mode = mode
        self.ov = []      # dicts: id, x, y, w, h (sprite overlays / buttons)
        self.tx = []      # dicts: id, x, y, w, h (text boxes)
        self.w, self.h = w, h

    def o(self, id, x, y, w, h, **kw):
        d = dict(id=id, x=x, y=y, w=w, h=h); d.update(kw); self.ov.append(d)

    def t(self, id, x, y, w, h):
        self.tx.append(dict(id=id, x=x, y=y, w=w, h=h))


def rnd(seed):
    return random.Random(seed)


# ====================================================================== shared textures
def band_sky(c, y0, y1, x0, x1, stops):
    """stops: list of (y, color). Bands between stops are ordered-dithered, never smooth."""
    for y in range(y0, y1):
        # find segment
        for i in range(len(stops) - 1):
            ya, ca = stops[i]; yb, cb = stops[i + 1]
            if ya <= y < yb:
                t = (y - ya) / max(1, (yb - ya))
                # hard band for first 55%, dither the rest
                lvl = 0 if t < .45 else (t - .45) / .55
                for x in range(x0, x1):
                    c.px(x, y, cb if BAYER[y % 4][x % 4] < lvl else ca)
                break
        else:
            for x in range(x0, x1):
                c.px(x, y, stops[-1][1])


def earth(c, x0, y0, w, h, seed, top='w1'):
    r = rnd(seed)
    c.rect(x0, y0, w, h, 'w0')
    for yy in range(y0, y0 + h):
        for xx in range(x0, x0 + w):
            v = (xx * 13 + yy * 7 + (xx * yy) % 5) % 23
            if v == 0:
                c.px(xx, yy, 'w1')
            elif v == 7 and yy % 3 == 0:
                c.px(xx, yy, 'k0')
    # strata lines
    for sy in range(y0 + 9, y0 + h, 23):
        off = r.randint(0, 6)
        for xx in range(x0, x0 + w):
            yy = sy + int(1.5 * math.sin((xx + off) / 5))
            c.px(xx, yy, 'w1')
    # pebbles
    for _ in range(max(1, w * h // 90)):
        px, py = r.randint(x0 + 1, x0 + w - 3), r.randint(y0 + 1, y0 + h - 3)
        c.rect(px, py, 2, 1, 's1'); c.px(px, py, 's2')
    # roots
    for _ in range(max(0, w * h // 900)):
        px, py = r.randint(x0, x0 + w - 1), r.randint(y0, y0 + h - 1)
        for k in range(r.randint(4, 9)):
            c.px(px + k // 2 * r.choice((-1, 1)) // 2, py + k, 'w2')


def wall_cut(c, x, y, w, h):
    """a wall in cross-section: ink outline, studs and insulation hatch"""
    c.rect(x, y, w, h, 'w1')
    for yy in range(y, y + h):
        for xx in range(x + 1, x + w - 1):
            if (xx + yy) % 4 == 0:
                c.px(xx, yy, 'w0')
    c.rect(x, y, 1, h, 'k0'); c.rect(x + w - 1, y, 1, h, 'k0')


def slab(c, x, y, w, h):
    """floor/ceiling slab in cross-section: joists"""
    c.rect(x, y, w, h, 'w1')
    c.rect(x, y, w, 1, 'k0'); c.rect(x, y + h - 1, w, 1, 'k0')
    for xx in range(x, x + w, 12):
        c.rect(xx, y + 1, 4, h - 2, 'w2'); c.rect(xx, y + 1, 1, h - 2, 'k0')
        c.rect(xx + 4, y + 1, 1, h - 2, 'w0')


def wallpaper(c, x, y, w, h, base='n3', stripe='n2', dot='g2'):
    c.rect(x, y, w, h, base)
    for xx in range(x, x + w):
        if (xx - x) % 10 == 0:
            c.rect(xx, y, 1, h, stripe)
    for yy in range(y + 3, y + h, 8):
        for xx in range(x + 5, x + w, 10):
            o = 0 if ((yy - y) // 8) % 2 == 0 else 0
            c.px(xx + o, yy, dot)


def floorboards(c, x, y, w, h):
    c.rect(x, y, w, h, 'w3')
    c.rect(x, y, w, 1, 'w4')
    for xx in range(x, x + w):
        if (xx - x) % 23 == 0:
            c.rect(xx, y + 1, 1, h - 1, 'w2')
    c.rect(x, y + h - 1, w, 1, 'w2')


def ao(z, x, y, w, h, amt=.6, soft=2):
    z.light.shade(x, y, w, h, amt, soft)


# ====================================================================== sky + roof
def _bayer8():
    b = [[0]]
    for _ in range(3):
        n = len(b)
        nb = [[0] * (2 * n) for _ in range(2 * n)]
        for y in range(n):
            for x in range(n):
                v = 4 * b[y][x]
                nb[y][x] = v; nb[y][x + n] = v + 2; nb[y + n][x] = v + 3; nb[y + n][x + n] = v + 1
        b = nb
    return [[(v + .5) / 64 for v in row] for row in b]


B8 = _bayer8()


def ramp_sky(c, y0, y1, x0, x1, stops):
    """one continuous ordered-dither ramp: every row between two stops mixes them, no flat slabs"""
    for y in range(y0, y1):
        for i in range(len(stops) - 1):
            ya, ca = stops[i]; yb, cb = stops[i + 1]
            if ya <= y < yb:
                lvl = (y - ya) / max(1, (yb - ya))
                for x in range(x0, x1):
                    c.px(x, y, cb if B8[y % 8][x % 8] < lvl else ca)
                break
        else:
            for x in range(x0, x1):
                c.px(x, y, stops[-1][1])


def draw_sky(z, x0, x1, H, mode, horizon):
    c = z.c
    # hero copy sits in the upper ~45% of the sky: keep it over the deep blues
    if mode == 'night':
        stops = [(0, 'n1'), (int(horizon * .62), 'n2'), (horizon, 'n3')]
    else:
        stops = [(0, 'n3'), (int(horizon * .50), 'n4'), (int(horizon * .72), 'n5'), (int(horizon * .83), 'p3'),
                 (int(horizon * .93), 'o3'), (horizon, 'g4')]
    ramp_sky(c, 0, H, x0, x1, stops)
    c.em[0:H, x0:x1] = True


def stars(z, x0, x1, y1, seed, avoid=None, n=60):
    r = rnd(seed)
    for _ in range(n):
        x, y = r.randint(x0, x1 - 1), r.randint(2, y1)
        if avoid and avoid[0] <= x <= avoid[2] and avoid[1] <= y <= avoid[3]:
            continue
        col = r.choice(['n5', 'n5', 'n6', 'c1', 'g4'])
        z.c.px(x, y, col, em=True)
        if r.random() < .12:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                z.c.px(x + dx, y + dy, 'n4', em=True)


def ring(z, cx, cy, rx, ry, mode, ymax, x0=0, x1=None):
    """the thin lit ring arcing low across the sky"""
    c = z.c
    x1 = x1 or c.w
    cols = (['n6', 'c0', 'n5', 'n3'] if mode == 'night' else ['c1', 'c0', 'p3', 'V'.lower() and 'p2'])
    for x in range(x0, x1):
        t = (x - cx) / rx
        if abs(t) >= 1:
            continue
        y = cy - ry * math.sqrt(1 - t * t)
        yi = int(round(y))
        if yi > ymax:
            continue
        # thickness grows slightly toward the near (left) side for perspective
        th = 2 if x > cx else 3
        for k in range(th):
            col = cols[min(k, len(cols) - 1)] if k < th - 1 else cols[3]
            # shadowed segment on the far right
            if mode == 'night' and x > cx + rx * .62:
                col = 'n4' if k == 0 else 'n3'
            c.px(x, yi + k, col, em=True)
        if (x * 5) % 17 == 0 and mode == 'night':
            c.px(x, yi + th, 'n4', em=True)


def ridges(z, x0, x1, base, layers, seed):
    """rolling far ridges: list of (yTop, amp, color, freq)"""
    r = rnd(seed)
    for (yt, amp, col, fq, hl) in layers:
        ph = r.random() * 6
        ph2 = r.random() * 6
        for x in range(x0, x1):
            y = yt + amp * math.sin(x * fq + ph) + amp * .45 * math.sin(x * fq * 2.7 + ph2)
            yi = int(round(y))
            z.c.rect(x, yi, 1, base - yi, col)
            if hl:
                z.c.px(x, yi, hl)


def hills_oak(z, x0, x1, ytop, base, mode, seed):
    """Oakland hills: nearer, darker, tree bumps and window lights at night"""
    r = rnd(seed)
    c = z.c
    ph = r.random() * 6
    tops = {}
    for x in range(x0, x1):
        y = ytop + 6 * math.sin(x / 23 + ph) + 3 * math.sin(x / 9 + 1.3)
        # tree bumps
        if (x // 3) % 5 == 0:
            y -= 1
        yi = int(round(y))
        tops[x] = yi
        c.rect(x, yi, 1, base - yi, 'e1' if mode == 'night' else 'v')
        c.px(x, yi, 'e2' if mode == 'night' else 'p2')
    for x in range(x0, x1, 4):
        ty = tops[x]
        if r.random() < .5:
            c.rect(x, ty - 2, 3, 2, 'e1' if mode == 'night' else 'v')
            c.px(x + 1, ty - 3, 'e1' if mode == 'night' else 'v')
    if mode == 'night':
        for _ in range((x1 - x0) // 4):
            x = r.randint(x0, x1 - 1)
            y = r.randint(tops[x] + 3, base - 1)
            c.px(x, y, r.choice(['g4', 'g3', 'o3']), em=True)
    return tops


def crane(z, x, base, mode, flip=False, s=1.0):
    """Port of Oakland container crane: four legs, a boxy house, boom raised high"""
    c = z.c
    ink = 'k0' if mode == 'night' else 'p1'
    body = 'n2' if mode == 'night' else 'p2'
    lh = int(24 * s); span = int(20 * s); top = base - lh
    for lx in (x, x + span):
        c.rect(lx, top, 2, lh, ink)              # leg
        c.line(lx + 2, top + 2, lx + 5, top + 8, ink)
    c.rect(x, top + lh // 2, span + 2, 1, ink)
    c.line(x + 1, top + lh // 2, x + span, base - 2, ink)
    # main girder (long, sticks out over the water to the left)
    gl = x - int(16 * s); gr = x + span + int(8 * s)
    c.rect(gl, top - 3, gr - gl, 3, ink)
    c.rect(gl, top - 3, gr - gl, 1, body)
    # machinery house
    c.rect(x + 2, top - 9, span - 2, 6, body); c.frame(x + 2, top - 9, span - 2, 6, ink)
    c.rect(x + 4, top - 7, 3, 2, 'n1' if mode == 'night' else 'p1')
    # A-frame apex
    ax = x + span // 2
    c.line(x + 3, top - 9, ax, top - int(20 * s), ink); c.line(x + span - 1, top - 9, ax, top - int(20 * s), ink)
    # raised boom over the water
    bx, by = gl + 2, top - 3
    ex, ey = gl - int(4 * s), top - int(34 * s)
    c.line(bx, by, ex, ey, ink); c.line(bx + 1, by, ex + 1, ey, ink); c.line(bx + 2, by, ex + 2, ey + 1, ink)
    c.line(ax, top - int(20 * s), ex + 1, ey, ink)
    if mode == 'night':
        c.px(ex + 1, ey - 1, 'r3', em=True); c.px(ax, top - int(20 * s) - 1, 'r3', em=True)
        c.px(x + 5, top - 6, 'g4', em=True)


def mailbox(c, x, y):
    """mailbox on a post, number on its side"""
    c.rect(x, y + 2, 18, 9, 'n3')
    c.rect(x + 1, y, 16, 2, 'n3')
    c.rect(x + 1, y + 1, 16, 1, 'n4')
    c.frame(x, y + 2, 18, 9, 'k0')
    c.rect(x + 1, y - 1, 16, 1, 'k0'); c.px(x, y + 1, 'k0'); c.px(x + 17, y + 1, 'k0')
    c.rect(x + 1, y + 8, 16, 2, 'n2')
    c.text(x + 2, y + 3, '1701', 'c0')
    # flag (up)
    c.rect(x + 18, y - 3, 1, 9, 'k0'); c.rect(x + 19, y - 3, 3, 3, 'r3'); c.rect(x + 19, y, 3, 1, 'k0')
    # post
    c.rect(x + 7, y + 11, 4, 16, 'w2'); c.rect(x + 7, y + 11, 1, 16, 'k0'); c.rect(x + 10, y + 11, 1, 16, 'k0'); c.rect(x + 8, y + 11, 1, 16, 'w3')


def chimney(c, x, y, w, h):
    c.rect(x, y, w, h, 'r2')
    for yy in range(y, y + h):
        if (yy - y) % 3 == 2:
            c.rect(x, yy, w, 1, 'w1')
        else:
            off = 0 if ((yy - y) // 3) % 2 == 0 else 3
            for xx in range(x + off, x + w, 6):
                c.px(xx, yy, 'w1')
    c.rect(x + w - 2, y, 1, h, 'r3')
    c.rect(x - 1, y - 3, w + 2, 3, 's2'); c.rect(x - 1, y - 3, w + 2, 1, 's3')
    c.frame(x - 1, y - 3, w + 2, h + 3, 'k0')
    c.rect(x + 2, y - 4, w - 4, 1, 'k0')


def antenna(c, x, y0, y1):
    c.rect(x, y1, 1, y0 - y1, 's2')
    c.rect(x + 1, y1, 1, y0 - y1, 'k0')
    for i, (yy, hw) in enumerate([(y1 + 4, 10), (y1 + 9, 8), (y1 + 14, 6), (y1 + 19, 4)]):
        c.rect(x - hw, yy, hw * 2 + 2, 1, 's3'); c.rect(x - hw, yy + 1, hw * 2 + 2, 1, 'k0')
        c.px(x - hw, yy - 1, 's2'); c.px(x + hw + 1, yy - 1, 's2')


def roof(z, xl, xr, peak, yeave, mode, chim_x, ant_x):
    c = z.c
    px_, py_ = peak
    # shingles in a triangle
    for y in range(py_, yeave + 1):
        t = (y - py_) / (yeave - py_)
        a = int(round(px_ - (px_ - xl) * t)); b = int(round(px_ + (xr - px_) * t))
        row = (y - py_) // 4
        for x in range(a, b + 1):
            off = 0 if row % 2 == 0 else 4
            col = 'n2'
            if (y - py_) % 4 == 3:
                col = 'n1'
            elif (x + off) % 8 == 0:
                col = 'n1'
            elif (y - py_) % 4 == 0:
                col = 'n3'
            c.px(x, y, col)
        c.px(a, y, 'k0'); c.px(b, y, 'k0')
        c.px(a + 1, y, 'c2'); c.px(b - 1, y, 'c2')
    # bargeboards (trim) along the slopes
    c.line(px_, py_ - 1, xl - 2, yeave + 1, 'c1'); c.line(px_, py_ - 2, xl - 3, yeave + 1, 'k0')
    c.line(px_, py_ - 1, xr + 2, yeave + 1, 'c1'); c.line(px_, py_ - 2, xr + 3, yeave + 1, 'k0')
    # round attic vent
    vx, vy = px_, py_ + int((yeave - py_) * .5)
    c.disc(vx, vy, 7, 'k0'); c.disc(vx, vy, 6, 'c1'); c.disc(vx, vy, 5, 'n1')
    for k in range(-4, 5, 2):
        c.rect(vx - 4, vy + k, 9, 1, 'n2')
    if mode == 'night':
        c.disc(vx, vy, 3, 'g2', em=True)
        for k in range(-2, 3, 2):
            c.rect(vx - 3, vy + k, 7, 1, 'g1', em=True)
    # fascia board under the eave
    c.rect(xl - 3, yeave + 1, xr - xl + 7, 3, 'c1'); c.rect(xl - 3, yeave + 4, xr - xl + 7, 1, 'k0')
    c.rect(xl - 3, yeave + 1, xr - xl + 7, 1, 'c0')


def compose_top(L, mode):
    """sky + skyline + roof. L = 'D' or 'M'"""
    if L == 'D':
        W, H = D_W, 252
    else:
        W, H = M_W, 270
    z = Z(W, H, mode, 2.0)  # sky is emissive anyway; roof lit as day/night via ambient
    if mode == 'night':
        z.light = Light(W, H, 0.55)
    c = z.c
    if L == 'D':
        horizon = 196
        draw_sky(z, 0, W, H, mode, horizon)
        if mode == 'night':
            stars(z, 0, W, 190, 11, avoid=(10, 10, 214, 120), n=90)
            stars(z, 10, 214, 120, 12, n=10)
            # moon (light source): upper right
            c.disc(236, 34, 10, 'n6', em=True); c.disc(236, 34, 9, 'c0', em=True)
            for (mx, my, mr) in ((232, 31, 2), (240, 38, 1.5), (238, 28, 1)):
                c.disc(mx, my, mr, 'n6', em=True)
            c.disc(231, 38, 1, 'n5', em=True)
        else:
            # two suns setting behind the hills (left, above the lake)
            c.disc(62, 168, 11, 'o3', em=True); c.disc(62, 168, 9, 'g4', em=True); c.disc(62, 168, 6, 'c0', em=True)
            c.disc(96, 176, 6, 'o2', em=True); c.disc(96, 176, 5, 'o3', em=True); c.disc(96, 176, 3, 'g4', em=True)
            # thin cloud streaks
            for (cx, cy, cw) in ((150, 150, 60), (176, 140, 34), (24, 132, 40), (260, 160, 70)):
                c.rect(cx, cy, cw, 1, 'p3', em=True); c.rect(cx + 6, cy + 1, cw - 14, 1, 'p2', em=True)
        ring(z, 170, 430, 390, 284, mode, 206)
        # far WV ridges (rolling, blue)
        far = 'n2' if mode == 'night' else 'n4'
        far2 = 'n3' if mode == 'night' else 'n5'
        ridges(z, 0, W, 230, [(176, 4, far2, .045, 'n4' if mode == 'night' else 'n6'), (184, 4, far, .06, None)], 5)
        tops = hills_oak(z, 0, W, 196, 230, mode, 7)
        # Lake Merritt: a dark oval with its ring of lights at night
        lx, ly, lrx, lry = 40, 214, 30, 5
        c.ellipse(lx, ly, lrx + 2, lry + 2, 'e1' if mode == 'night' else 'v')
        c.ellipse(lx, ly, lrx, lry, 'n1' if mode == 'night' else 'p3', em=True)
        if mode == 'day':
            c.rect(lx - 18, ly - 1, 30, 1, 'g4', em=True); c.rect(lx - 10, ly + 1, 18, 1, 'o3', em=True)
        else:
            c.rect(lx - 14, ly, 24, 1, 'n2', em=True)
            for a in range(0, 360, 14):
                x = lx + (lrx + 1.5) * math.cos(math.radians(a)); y = ly + (lry + 1.5) * math.sin(math.radians(a))
                c.px(int(round(x)), int(round(y)), 'g4' if a % 28 == 0 else 'c1', em=True)
                # reflections
                if 20 < a < 160 and a % 28 == 0:
                    c.px(int(round(x)), int(round(y)) - 2, 'g2', em=True)
        # bay + port cranes on the right
        c.rect(196, 222, W - 196, 8, 'n2' if mode == 'night' else 'p3', em=True)
        if mode == 'day':
            for x in range(200, W, 7):
                c.rect(x, 224 + (x // 7) % 3, 3, 1, 'g4', em=True)
        for (cx_, s_) in ((226, 1.0), (274, 1.15), (318, 1.0)):
            crane(z, cx_, 224, mode, s=s_)
        # roof
        roof(z, 30, 320, (176, 178), 236, mode, 238, 104)
        chimney(c, 236, 190, 13, 20)
        antenna(c, 104, 214, 158)
        # house top band under the eave (siding stub) and walls start
        c.rect(30, 241, 292, 11, 'n2')
        for xx in range(30, 322, 3):
            c.px(xx, 243, 'n1')
        c.rect(30, 241, 292, 1, 'k0')
        slab(c, 36, 246, 288, 6)
        # street on the right (house sits on a hill: street at roof level)
        c.rect(322, 238, W - 322, 3, 's2'); c.rect(322, 238, W - 322, 1, 's3')
        c.rect(322, 241, W - 322, 11, 'w0')
        earth(c, 322, 241, W - 322, 11, 3)
        mailbox(c, 328, 214)
        # left column: looking down the hill at the flatlands
        c.rect(0, 238, 30, 14, 'e1' if mode == 'night' else 'v')
        if mode == 'night':
            for (xx, yy) in ((4, 243), (11, 247), (19, 241), (25, 249), (8, 250)):
                c.px(xx, yy, 'g4', em=True)
        # overlays
        z.o('planet', 270, 18, 40, 40)
        z.o('raven', 234, 174, 16, 13)
        z.o('eagle', 99, 145, 13, 13)
        z.o('smoke', 237, 156, 10, 30)
        z.o('dragon', 8, 8, 336, 150)
        z.t('hero', 14, 14, 200, 112)
        z.o('mailbox', 326, 210, 24, 32)
        # light: sky/skyline emissive; roof lit
        if mode == 'night':
            z.light.pool(236, 34, 240, 200, 0.9)  # moonlight on the roof's right
        else:
            z.light.pool(62, 168, 260, 120, 0.7)
    else:
        horizon = 214
        draw_sky(z, 0, W, H, mode, horizon)
        if mode == 'night':
            stars(z, 0, W, 210, 21, avoid=(6, 6, 174, 150), n=46)
            c.disc(150, 168, 7, 'n6', em=True); c.disc(150, 168, 6, 'c0', em=True); c.disc(148, 166, 1.5, 'n6', em=True)
        else:
            c.disc(40, 196, 9, 'o3', em=True); c.disc(40, 196, 7, 'g4', em=True); c.disc(40, 196, 4, 'c0', em=True)
            c.disc(64, 202, 5, 'o2', em=True); c.disc(64, 202, 4, 'o3', em=True)
        ring(z, 90, 420, 200, 236, mode, 220)
        far = 'n2' if mode == 'night' else 'n4'
        far2 = 'n3' if mode == 'night' else 'n5'
        ridges(z, 0, W, 248, [(198, 3, far2, .07, 'n4' if mode == 'night' else 'n6'), (205, 3, far, .09, None)], 5)
        hills_oak(z, 0, W, 214, 248, mode, 8)
        lx, ly = 22, 232
        c.ellipse(lx, ly, 18, 4, 'e1' if mode == 'night' else 'v')
        c.ellipse(lx, ly, 16, 3, 'n1' if mode == 'night' else 'p3', em=True)
        if mode == 'night':
            for a in range(0, 360, 20):
                x = lx + 17 * math.cos(math.radians(a)); y = ly + 4 * math.sin(math.radians(a))
                c.px(int(round(x)), int(round(y)), 'g4' if a % 40 == 0 else 'c1', em=True)
        c.rect(110, 238, W - 110, 6, 'n2' if mode == 'night' else 'p3', em=True)
        for (cx_, s_) in ((120, .7), (150, .8)):
            crane(z, cx_, 240, mode, s=s_)
        roof(z, 14, 156, (85, 196), 252, mode, 120, 44)
        chimney(c, 118, 214, 10, 22)
        antenna(c, 44, 222, 184)
        c.rect(14, 257, 146, 13, 'n2')
        for xx in range(14, 160, 3):
            c.px(xx, 259, 'n1')
        slab(c, 18, 264, 144, 6)
        c.rect(158, 256, W - 158, 3, 's2'); c.rect(158, 256, W - 158, 1, 's3')
        earth(c, 158, 259, W - 158, 11, 3)
        mailbox(c, 159, 232)
        c.rect(0, 256, 14, 14, 'e1' if mode == 'night' else 'v')
        z.o('planet', 134, 150, 40, 40)
        z.o('raven', 116, 198, 16, 13)
        z.o('eagle', 39, 171, 13, 13)
        z.o('smoke', 119, 180, 10, 30)
        z.o('dragon', 0, 120, 180, 100)
        z.t('hero', 8, 10, 164, 136)
        if mode == 'night':
            z.light.pool(150, 168, 150, 120, 0.9)
        else:
            z.light.pool(40, 196, 160, 100, 0.7)
    return z


# ====================================================================== room objects
def parchment(c0, X, Y, w, h, seed):
    r = rnd(seed)
    c = Canvas(w + 2, h + 2); x, y = 1, 1
    c.rect(x, y, w, h, 'c1')
    # torn edges
    for xx in range(x, x + w):
        for k in range(r.choice((0, 0, 1, 1, 2))):
            c.px(xx, y + k, T)
        for k in range(r.choice((0, 0, 1, 2))):
            c.px(xx, y + h - 1 - k, T)
    for yy in range(y, y + h):
        for k in range(r.choice((0, 0, 1, 2))):
            c.px(x + k, yy, T)
        for k in range(r.choice((0, 1, 1, 2))):
            c.px(x + w - 1 - k, yy, T)
    # aged edges: c2 ring inside
    m = c.a[y:y + h, x:x + w] != T
    edge = np.zeros_like(m)
    edge[1:, :] |= ~m[:-1, :]; edge[:-1, :] |= ~m[1:, :]; edge[:, 1:] |= ~m[:, :-1]; edge[:, :-1] |= ~m[:, 1:]
    edge &= m
    for (yy, xx) in zip(*np.where(edge)):
        c.px(x + xx, y + yy, 'w3')
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if c.a[yy, xx] == C('c1'):
                dx = min(xx - x, x + w - 1 - xx); dy = min(yy - y, y + h - 1 - yy)
                d = min(dx, dy)
                if d < 4 and BAYER[yy % 4][xx % 4] < (4 - d) / 6:
                    c.px(xx, yy, 'c2')
    c.outline('k0')
    c0.blit(c, X - 1, Y - 1)


def pin(c, x, y, col='r3'):
    c.px(x, y, col); c.px(x + 1, y, 'k0'); c.px(x, y + 1, 'k0'); c.px(x - 1, y, 'k0'); c.px(x, y - 1, 'k0')


def mountain(c, mx, my, hh):
    """fantasy-map mountain: lit left face, dithered shadow face, ink outline, snowcap"""
    for k in range(hh):
        for xx in range(mx - k, mx + k + 1):
            if xx < mx:
                col = 'c1'
            elif xx == mx:
                col = 'w3'
            else:
                col = 'w3' if (xx + my + k) % 2 == 0 else 'c2'
            c.px(xx, my + k, col)
        c.px(mx - k - 1, my + k, 'w1'); c.px(mx + k + 1, my + k, 'w1')
    c.px(mx, my - 1, 'w1')
    c.px(mx, my, 'c0'); c.px(mx - 1, my + 1, 'c0'); c.px(mx + 1, my + 1, 'c0')
    c.rect(mx - hh, my + hh, 2 * hh + 1, 1, 'w2')


def draw_map(z, x, y, w, h, ill_h, seed=4):
    """old-world map of the road from West Virginia to Oakland. The art sits in the top ill_h rows;
    the job list (live text) fills the parchment below it. Returns the banner rect."""
    c = z.c
    parchment(c, x, y, w, h, seed)
    r = rnd(seed + 11)
    fx0, fy0, fx1, fy1 = x + 4, y + 4, x + w - 5, y + ill_h
    # double-rule frame around the illustration with corner knots
    c.frame(fx0, fy0, fx1 - fx0, fy1 - fy0, 'w2'); c.frame(fx0 + 2, fy0 + 2, fx1 - fx0 - 4, fy1 - fy0 - 4, 'w3')
    for (kx, ky) in ((fx0, fy0), (fx1 - 3, fy0), (fx0, fy1 - 3), (fx1 - 3, fy1 - 3)):
        c.rect(kx, ky, 3, 3, 'w2'); c.px(kx + 1, ky + 1, 'r2')
    ax0, ay0, ax1, ay1 = fx0 + 3, fy0 + 3, fx1 - 3, fy1 - 3
    aw, ah = ax1 - ax0, ay1 - ay0
    # sea + the Bay on the left
    coast = {}
    for yy in range(ay0, ay1):
        t = (yy - ay0) / ah
        cx = ax0 + int(aw * .17 + 4 * math.sin(yy / 4.0) + 2 * math.sin(yy / 1.9))
        if .42 < t < .62:
            cx += int(7 * math.sin((t - .42) / .2 * math.pi))     # the Bay cuts inland
        coast[yy] = cx
        for xx in range(ax0, cx):
            c.px(xx, yy, 'n5' if (xx * 3 + yy * 5) % 7 else 'n4')
        c.px(cx, yy, 'n3'); c.px(cx + 1, yy, 'w3')
    for (wx, wy) in ((ax0 + 3, ay0 + 6), (ax0 + 8, ay0 + 14), (ax0 + 2, ay0 + 22), (ax0 + 6, ay0 + ah - 7)):
        c.px(wx, wy, 'n3'); c.px(wx + 1, wy - 1, 'n3'); c.px(wx + 2, wy, 'n3'); c.px(wx + 3, wy - 1, 'n3')
    # Oakland: a few roofs and a crane on the east shore of the Bay
    oy = ay0 + int(ah * .52)
    ox = coast[oy] + 3
    for k in range(3):
        hx = ox + k * 4
        c.rect(hx, oy, 3, 2, 'w2'); c.px(hx + 1, oy - 1, 'r2')
    c.rect(ox - 1, oy - 7, 1, 7, 'k0'); c.rect(ox + 2, oy - 7, 1, 7, 'k0'); c.rect(ox - 4, oy - 8, 9, 1, 'k0'); c.line(ox - 4, oy - 8, ox - 6, oy - 13, 'k0')
    # river winding out of the mountains to the Bay
    for i in range(70):
        t = i / 69
        rx_ = ox + 10 + t * aw * .45
        ry_ = oy + 3 + 5 * math.sin(t * 7) * (1 - t * .5) - t * 6
        c.px(int(rx_), int(ry_), 'n4')
    # mountains across the middle, bigger toward the west
    peaks = []
    for i in range(40):
        mx = int(ax0 + aw * (.32 + .40 * r.random()))
        my = int(ay0 + 3 + (ah - 14) * r.random())
        if all(abs(mx - px_) > 8 or abs(my - py_) > 6 for px_, py_ in peaks):
            peaks.append((mx, my))
    for (mx, my) in sorted(peaks, key=lambda p: p[1])[:16]:
        mountain(c, mx, my, r.choice((4, 5, 6, 7)))
    # forests (little round trees) and grass tufts
    for i in range(16):
        tx = int(ax0 + aw * (.30 + .45 * r.random())); ty = int(ay0 + 3 + (ah - 6) * r.random())
        c.px(tx, ty, 'e2'); c.px(tx + 1, ty, 'e2'); c.px(tx, ty - 1, 'e3'); c.px(tx, ty + 1, 'w2')
    # West Virginia: layered rolling ridges on the right
    for k in range(5):
        base = ay0 + 6 + k * ((ah - 12) // 5)
        for xx in range(int(ax0 + aw * .74), ax1 - 1):
            yy = base + int(2 * math.sin(xx / 3.2 + k * 1.3))
            c.px(xx, yy, 'n3' if k % 2 == 0 else 'w2')
            if (xx + k) % 5 == 0:
                c.px(xx, yy + 1, 'w3')
    # cabin + star where the road starts
    hx, hy = ax1 - 12, ay1 - 9
    c.rect(hx, hy, 6, 4, 'w2'); c.rect(hx - 1, hy - 1, 8, 1, 'r2'); c.rect(hx, hy - 2, 6, 1, 'r2'); c.rect(hx + 1, hy - 3, 4, 1, 'r2'); c.px(hx + 2, hy + 2, 'k0'); c.px(hx + 4, hy - 4, 's2')
    # dashed route WV -> Oakland, six stops
    pts = []
    n = 200
    sx, sy = hx - 2, hy + 2
    ex, ey = ox + 12, oy + 1
    for i in range(n + 1):
        t = i / n
        xx = sx + (ex - sx) * t
        yy = sy + (ey - sy) * t - (ah * .16) * math.sin(t * math.pi * 2.0) * (1 - t * .3)
        yy = max(ay0 + 4, min(ay1 - 5, yy))
        pts.append((int(round(xx)), int(round(yy))))
    for i, (xx, yy) in enumerate(pts):
        if (i // 3) % 2 == 0:
            c.px(xx, yy, 'r2')
    for t in (.18, .34, .5, .64, .78, .92):
        xx, yy = pts[int(t * n)]
        c.rect(xx - 1, yy - 1, 3, 3, 'r3'); c.frame(xx - 2, yy - 2, 5, 5, 'k0'); c.px(xx, yy, 'c0')
    c.rect(ex - 1, ey - 1, 3, 3, 'g3'); c.frame(ex - 2, ey - 2, 5, 5, 'k0')   # you are here
    # compass rose (top right)
    cx, cy = ax1 - 9, ay0 + 8
    for k in range(1, 6):
        c.px(cx, cy - k, 'w1' if k < 5 else 'r2'); c.px(cx, cy + k, 'w2'); c.px(cx - k, cy, 'w2'); c.px(cx + k, cy, 'w2')
    for k in (1, 2):
        for (dx, dy) in ((k, k), (-k, k), (k, -k), (-k, -k)):
            c.px(cx + dx, cy + dy, 'w3')
    c.px(cx, cy, 'r2'); c.px(cx - 1, cy - 6, 'w1'); c.px(cx + 1, cy - 6, 'w1'); c.px(cx, cy - 7, 'w1')
    # ribbon banner for the heading (live text sits on it)
    bw, bh = 40, 9
    bx, by = ax0 + int(aw * .30), ay0 + 1
    c.rect(bx - 4, by + 2, 4, bh, 'w3'); c.rect(bx + bw, by + 2, 4, bh, 'w3')
    for (ex_, d) in ((bx - 4, -1), (bx + bw + 3, 1)):
        c.px(ex_ + (1 if d < 0 else -1) * 0, by + 2 + bh // 2, 'c1')
    c.rect(bx, by, bw, bh, 'c1'); c.rect(bx, by + bh - 1, bw, 1, 'c2')
    c.frame(bx - 1, by - 1, bw + 2, bh + 2, 'w1')
    c.rect(bx - 5, by + 1, 1, bh + 2, 'w1'); c.rect(bx + bw + 4, by + 1, 1, bh + 2, 'w1')
    c.rect(bx - 5, by + bh + 2, 5, 1, 'w1'); c.rect(bx + bw, by + bh + 2, 5, 1, 'w1')
    pin(c, x + 3, y + 2); pin(c, x + w - 4, y + 2)
    z.o('map', x, y, w, h)
    return (bx, by, bw, bh)


def paper(c, x, y, w, h, kind='print', seed=0):
    col, sh = ('c0', 'c1') if kind != 'flyer' else ('g4', 'o3')
    c.rect(x + 1, y + 1, w, h, 'k0')          # drop onto cork
    c.rect(x, y, w, h, col)
    c.rect(x + w - 1, y, 1, h, sh); c.rect(x, y + h - 1, w, 1, sh)
    c.frame(x - 1, y - 1, w + 2, h + 2, 'k0')
    # folded corner
    c.px(x + w - 1, y, 'k0'); c.px(x + w - 2, y, sh); c.px(x + w - 1, y + 1, sh)
    if kind == 'flyer':
        # tear-off tabs
        for xx in range(x + 1, x + w - 1, 4):
            c.rect(xx + 3, y + h - 7, 1, 7, 'o3')
        c.rect(x, y + h - 8, w, 1, 'o3')
        for xx in range(x + 2, x + w - 2, 4):
            c.rect(xx, y + h - 6, 1, 4, 'k0')
        # one tab torn off
        c.rect(x + 5, y + h - 7, 3, 7, 'k0')
    pin(c, x + w // 2, y + 1, 'r3' if kind != 'flyer' else 'n4')


def draw_corkboard(z, x, y, w, h, papers):
    c = z.c
    c.rect(x, y, w, h, 'w2'); c.frame(x, y, w, h, 'k0')
    c.rect(x + 1, y + 1, w - 2, 1, 'w3'); c.rect(x + 1, y + 1, 1, h - 2, 'w3')
    c.rect(x + 3, y + 3, w - 6, h - 6, 'w4')
    for yy in range(y + 3, y + h - 3):
        for xx in range(x + 3, x + w - 3):
            v = (xx * 31 + yy * 17 + (xx * yy) % 7) % 13
            if v < 2:
                c.px(xx, yy, 'w3')
            elif v == 5:
                c.px(xx, yy, 'c2')
    c.frame(x + 3, y + 3, w - 6, h - 6, 'w1')
    # stray pins + a ticket stub
    pin(c, x + w - 9, y + h - 9, 'g3'); pin(c, x + 7, y + h - 8, 'n4')
    for (pid, px_, py_, pw, ph, kind) in papers:
        paper(c, px_, py_, pw, ph, kind)
        z.t(pid, px_, py_ + 2, pw, ph - 2 - (8 if kind == 'flyer' else 0))


def sash(c, x, y, h):
    """merit-badge sash pinned beside the corkboard: a long green loop covered in round badges"""
    cols = ['r3', 'g3', 'n4', 'c0', 'o2', 'e3', 'p3', 'n5', 'r2', 'g4']
    c.rect(x, y, 10, h, 'e2')
    c.rect(x, y, 1, h, 'k0'); c.rect(x + 9, y, 1, h, 'k0'); c.rect(x + 4, y + 3, 2, h - 3, 'e1')
    c.rect(x + 8, y, 1, h, 'e3')
    # pointed bottom fold
    for k in range(5):
        c.rect(x + k, y + h + k, 10 - 2 * k, 1, 'e2'); c.px(x + k, y + h + k, 'k0'); c.px(x + 9 - k, y + h + k, 'k0')
    c.rect(x + 4, y + h + 5, 2, 1, 'k0')
    i = 0
    for yy in range(y + 4, y + h - 2, 5):
        for xx in (x + 1, x + 6):
            col = cols[i % len(cols)]; i += 1
            c.rect(xx, yy, 3, 3, col); c.px(xx, yy, 'e1'); c.px(xx + 2, yy + 2, 'k0'); c.px(xx + 1, yy + 1, 'c0' if col != 'c0' else 'r2')
    pin(c, x + 5, y + 1, 'g3')


def window(z, x, y, w, h, mode, view_seed=3):
    c = z.c
    # view
    if mode == 'night':
        band_sky(c, y, y + h, x, x + w, [(y, 'n1'), (y + h * .6, 'n2'), (y + h, 'n3')])
        stars(z, x + 2, x + w - 2, y + h - 12, view_seed, n=10)
        c.disc(x + w - 12, y + 10, 5, 'c0', em=True); c.disc(x + w - 10, y + 9, 4, 'n2', em=True)
    else:
        band_sky(c, y, y + h, x, x + w, [(y, 'n5'), (y + h * .4, 'p3'), (y + h * .8, 'o3'), (y + h, 'g4')])
    c.em[y:y + h, x:x + w] = True
    hcol = 'n1' if mode == 'night' else 'p1'
    for xx in range(x, x + w):
        top = y + h - 8 - int(3 * math.sin(xx / 7) + 2 * math.sin(xx / 3))
        c.rect(xx, top, 1, y + h - top, hcol, em=True)
        if mode == 'night' and (xx * 7) % 11 == 0:
            c.px(xx, top + 3, 'g4', em=True)
    # frame + mullions
    c.frame(x - 3, y - 3, w + 6, h + 6, 'k0')
    c.rect(x - 2, y - 2, w + 4, 2, 'c1'); c.rect(x - 2, y + h, w + 4, 2, 'c2')
    c.rect(x - 2, y - 2, 2, h + 4, 'c1'); c.rect(x + w, y - 2, 2, h + 4, 'c2')
    c.rect(x + w // 2 - 1, y, 2, h, 'c1'); c.rect(x + w // 2, y, 1, h, 'c2')
    c.rect(x, y + h // 2 - 1, w, 2, 'c1'); c.rect(x, y + h // 2, w, 1, 'c2')
    # sill
    c.rect(x - 5, y + h + 2, w + 10, 3, 'c1'); c.rect(x - 5, y + h + 4, w + 10, 1, 'c2'); c.frame(x - 6, y + h + 2, w + 12, 4, 'k0')
    # curtain on the left
    for yy in range(y - 6, y + h + 2):
        cw = 7 if yy < y + h - 12 else 7 + (yy - (y + h - 12)) // 3
        for xx in range(x - 6, x - 6 + cw):
            col = 'r2' if (xx - x) % 3 else 'r1'
            c.px(xx, yy, col)
        c.px(x - 6 + cw, yy, 'k0')
    c.rect(x - 9, y - 7, w + 18, 2, 's2'); c.rect(x - 9, y - 7, w + 18, 1, 's3'); c.px(x - 10, y - 7, 'k0'); c.px(x + w + 9, y - 7, 'k0')


def shelf(c, x, y, w):
    c.rect(x, y, w, 3, 'w3'); c.rect(x, y, w, 1, 'w4'); c.rect(x, y + 3, w, 1, 'k0'); c.rect(x - 1, y, 1, 4, 'k0'); c.rect(x + w, y, 1, 4, 'k0')
    for bx in (x + 6, x + w - 9):
        c.rect(bx, y + 4, 3, 1, 's2'); c.rect(bx, y + 4, 1, 4, 's2'); c.px(bx + 1, y + 5, 's2'); c.line(bx, y + 8, bx + 3, y + 5, 'k0')


def door(z, x, y, w, h):
    """door frame + dark stairwell behind; the sliding panel is an overlay"""
    c = z.c
    c.rect(x - 4, y - 4, w + 8, h + 4, 'c1'); c.frame(x - 5, y - 5, w + 10, h + 5, 'k0')
    c.rect(x - 4, y - 4, w + 8, 1, 'c0'); c.rect(x + w + 2, y - 3, 2, h + 3, 'c2')
    c.rect(x, y, w, h, 'n1')
    # stairs going down into the dark
    for i in range(7):
        sx = x + 2 + i * 5; sy = y + h - 2 - 0 + 0
        c.rect(x + 2, y + 30 + i * 8, w - 4 - i * 4, 1, 'n2')
    c.rect(x + w - 6, y + 10, 1, h - 12, 'n2')  # handrail
    c.frame(x, y, w, h, 'k0')
    z.o('door', x, y, w, h)


def coat_rail(c, x, y, w):
    c.rect(x, y, w, 4, 'w3'); c.rect(x, y, w, 1, 'w4'); c.frame(x - 1, y - 1, w + 2, 6, 'k0')
    for px_ in (x + 9, x + 29):
        c.rect(px_, y + 1, 2, 2, 'g2'); c.px(px_ + 1, y + 1, 'g4')


def cd_tower(z, x, y, h):
    c = z.c
    w = 13
    c.rect(x, y, w, h, 'w1'); c.frame(x, y, w, h, 'k0'); c.rect(x + 1, y + 1, 1, h - 2, 'w2')
    # spines: album colorways, no names (pairs of colors per CD)
    spines = [('k0', 'c0'), ('s3', 'c0'), ('r3', 'k0'), ('o2', 'r2'), ('p3', 'c0'), ('n4', 'g3'), ('e3', 'k0'),
              ('c0', 'r2'), ('k0', 'r3'), ('g3', 'k0'), ('r2', 'c1'), ('n2', 'n5'), ('s2', 'o3'), ('c1', 'k0'),
              ('p2', 'n1'), ('o3', 'k0'), ('k0', 'g4'), ('n3', 'c0'), ('r3', 'c0'), ('s3', 'k0')]
    yy = y + 2
    gap_y = None
    i = 0
    while yy + 2 < y + h - 2:
        if i == 8:
            gap_y = yy; yy += 9; i += 1
            continue
        a, b = spines[i % len(spines)]
        c.rect(x + 2, yy, w - 4, 2, a)
        c.rect(x + 2 + (i * 3) % 5 + 1, yy, 2, 2, b)
        c.rect(x + 2, yy + 2, w - 4, 1, 'k0')
        yy += 3; i += 1
    if gap_y:
        c.rect(x + 2, gap_y, w - 4, 9, 'k0')
    z.o('orb3', x + 2, gap_y, 9, 9)


def rug(c, x, y, w):
    c.rect(x + 2, y, w - 4, 3, 'r2'); c.rect(x, y + 1, w, 2, 'r2')
    for xx in range(x + 3, x + w - 3, 4):
        c.px(xx, y + 1, 'g3')
    c.rect(x + 2, y, w - 4, 1, 'r3'); c.rect(x, y + 3, w, 1, 'r1')
    for xx in range(x - 2, x + w + 2, 2):
        c.px(xx, y + 3, 'c1')


def chair(c, x, y_floor):
    """wooden desk chair, side view, facing right"""
    sy = y_floor - 36
    c.rect(x, y_floor - 60, 3, 60, 'w2'); c.rect(x + 1, y_floor - 60, 1, 60, 'w3')
    c.frame(x - 1, y_floor - 61, 5, 62, 'k0')
    c.rect(x, sy, 24, 4, 'w3'); c.rect(x, sy, 24, 1, 'w4'); c.frame(x - 1, sy - 1, 26, 6, 'k0')
    c.rect(x + 20, sy + 4, 3, 36 - 4, 'w2'); c.frame(x + 19, sy + 4, 5, 36 - 4, 'k0')
    c.rect(x + 3, sy + 16, 18, 2, 'w2'); c.frame(x + 2, sy + 15, 20, 4, 'k0')
    for k in (8, 16, 24):
        c.rect(x + 3, y_floor - 70 + k, 0, 0, 'w2')


def desk(c, x, y, w, floor):
    c.rect(x, y, w, 5, 'w3'); c.rect(x, y, w, 1, 'w4'); c.frame(x - 1, y - 1, w + 2, 7, 'k0')
    # left leg panel
    c.rect(x + 2, y + 5, 4, floor - y - 5, 'w2'); c.frame(x + 1, y + 5, 6, floor - y - 5, 'k0')
    # drawers on the right
    dx = x + w - 28
    c.rect(dx, y + 5, 27, floor - y - 5, 'w2'); c.frame(dx - 1, y + 5, 29, floor - y - 5, 'k0')
    for i, dy in enumerate(range(y + 7, floor - 4, 11)):
        c.frame(dx + 2, dy, 23, 9, 'w1'); c.rect(dx + 11, dy + 4, 5, 1, 'g3'); c.rect(dx + 3, dy + 1, 21, 1, 'w3')


def monitor(z, x, y, w, h, mode):
    c = z.c
    c.rect(x, y, w, h, 's1'); c.frame(x, y, w, h, 'k0')
    c.rect(x + 1, y + 1, w - 2, 1, 's2'); c.rect(x + 1, y + h - 2, w - 2, 1, 'k0')
    sx, sy, sw, sh = x + 3, y + 3, w - 6, h - 7
    c.rect(sx, sy, sw, sh, 'n1', em=True)
    for yy in range(sy, sy + sh):
        for xx in range(sx, sx + sw):
            if (xx - yy) % 12 < 5:
                c.px(xx, yy, 'n2', em=True)
    c.rect(sx, sy, sw, 1, 'n3', em=True)
    c.px(x + w - 5, y + h - 3, 't2', em=True)
    # stand
    c.rect(x + w // 2 - 4, y + h, 8, 6, 's1'); c.frame(x + w // 2 - 5, y + h, 10, 6, 'k0')
    c.rect(x + w // 2 - 10, y + h + 5, 20, 2, 's1'); c.frame(x + w // 2 - 11, y + h + 5, 22, 3, 'k0')
    z.t('projects', sx, sy, sw, sh)
    return sx, sy, sw, sh


def lamp(c, x, y_desk, mode):
    """architect lamp on the right end of the desk, shade pointing down-left"""
    c.rect(x, y_desk - 3, 12, 3, 's1'); c.frame(x - 1, y_desk - 4, 14, 4, 'k0'); c.rect(x, y_desk - 3, 12, 1, 's2')
    c.line(x + 7, y_desk - 4, x + 9, y_desk - 26, 'k0'); c.line(x + 6, y_desk - 4, x + 8, y_desk - 26, 's3')
    c.line(x + 9, y_desk - 26, x - 2, y_desk - 40, 'k0'); c.line(x + 8, y_desk - 26, x - 3, y_desk - 40, 's3')
    c.disc(x + 8, y_desk - 26, 1.5, 'k0')
    # shade (cone pointing down-left)
    sx, sy = x - 10, y_desk - 46
    shade = grid([
        "....KKKK...",
        "...KGGGGK..",
        "..KGYGGhK..",
        ".KGYGGGhK..",
        "KGGGGGhhK..",
        "KhhhhhhK...",
        ".KYYYYK....",
    ], em_chars='Y' if mode == 'night' else '')
    c.blit(shade, sx, sy)


def pc_tower(c, x, y, h):
    c.rect(x, y, 14, h, 's1'); c.frame(x, y, 14, h, 'k0'); c.rect(x + 1, y + 1, 12, 1, 's2')
    c.rect(x + 3, y + 4, 8, 2, 'k0'); c.rect(x + 3, y + 8, 8, 2, 'k0')
    c.px(x + 10, y + h - 5, 't2', em=True); c.px(x + 11, y + h - 5, 'g4', em=True)
    for yy in range(y + 13, y + h - 7, 2):
        c.rect(x + 3, yy, 8, 1, 's2')


def cables(c, pts, col='k0'):
    for i in range(len(pts) - 1):
        c.line(*pts[i], *pts[i + 1], col)


def keyboard(c, x, y, w):
    c.rect(x, y, w, 3, 's1'); c.frame(x - 1, y - 1, w + 2, 4, 'k0')
    for xx in range(x + 1, x + w - 1, 2):
        c.px(xx, y, 's3')
    c.rect(x + w + 4, y, 5, 2, 's1'); c.frame(x + w + 3, y - 1, 7, 4, 'k0')  # mouse


def outlet(c, x, y):
    c.rect(x, y, 5, 7, 'c1'); c.frame(x - 1, y - 1, 7, 9, 'k0'); c.px(x + 1, y + 2, 'k0'); c.px(x + 3, y + 2, 'k0'); c.px(x + 1, y + 4, 'k0'); c.px(x + 3, y + 4, 'k0')


def blit_named(z, name, x, y, flip=False):
    g = name if isinstance(name, Canvas) else grid(getattr(S, name) if not callable(getattr(S, name)) else getattr(S, name)())
    z.c.blit(g, x, y, flip)
    return g


def finish_light(z, x0, x1, mode, papers):
    """keep light inside the house; papers get one solid tier so text on them reads"""
    amb_out = 2.0 if mode == 'day' else 0.0
    f = z.light.f
    f[:, :x0] = amb_out
    f[:, x1:] = amb_out
    for (x, y, w, h) in papers:
        z.light.set(x, y, w, h, 2.0 if mode == 'day' else 1.0)


# ====================================================================== room
def compose_room(L, mode):
    if L == 'D':
        return room_D(mode)
    return room_M(mode)


def room_shell(z, x0, x1, H, floor, mode, wains=40):
    c = z.c
    W = z.w
    wallpaper(c, x0, 6, x1 - x0, floor - 6)
    # wainscot
    wy = floor - wains
    c.rect(x0, wy, x1 - x0, wains, 'w2')
    for xx in range(x0 + 4, x1 - 20, 26):
        c.frame(xx, wy + 6, 20, wains - 12, 'w1'); c.rect(xx + 1, wy + 7, 18, 1, 'w3')
    c.rect(x0, wy - 2, x1 - x0, 3, 'w3'); c.rect(x0, wy - 2, x1 - x0, 1, 'w4'); c.rect(x0, wy + 1, x1 - x0, 1, 'k0')
    # baseboard
    c.rect(x0, floor - 3, x1 - x0, 3, 'c2'); c.rect(x0, floor - 3, x1 - x0, 1, 'c1')
    floorboards(c, x0, floor, x1 - x0, 4)
    # ceiling + crown
    slab(c, x0 - 6, 0, x1 - x0 + 12, 4)
    c.rect(x0, 4, x1 - x0, 2, 'c1'); c.rect(x0, 6, x1 - x0, 1, 'c2')


def room_D(mode):
    W, H = D_W, 300
    floor = 292
    z = Z(W, H, mode, 2.0 if mode == 'day' else 0.25)
    c = z.c
    x0, x1 = 42, 318
    # outside columns
    c.rect(0, 0, 36, H, 'e1' if mode == 'night' else 'p1')
    r = rnd(9)
    for yy in range(0, H, 1):
        for xx in range(0, 36):
            if (xx * 3 + yy * 5) % 37 == 0:
                c.px(xx, yy, 'n1' if mode == 'night' else 'p2')
    if mode == 'night':
        for _ in range(26):
            c.px(r.randint(1, 34), r.randint(2, H - 2), r.choice(['g4', 'g3', 'o3', 'c1']), em=True)
    else:
        for _ in range(18):
            c.px(r.randint(1, 34), r.randint(2, H - 2), 'p3')
    earth(c, 324, 0, W - 324, H, 31)
    oak_trunk(c, 6, 40, H, mode)
    oak_canopy(c, 16, 26, 16, 16, mode, 3)
    c.line(12, 120, 30, 104, 'w1' if mode == 'day' else 'w0'); c.line(12, 121, 30, 105, 'k0')
    wall_cut(c, 36, 0, 6, H)
    wall_cut(c, 318, 0, 6, H)
    room_shell(z, x0, x1, H, floor, mode)
    slab(c, 36, floor + 4, 288, H - floor - 4)
    # ---------------- upper wall: map, sash, corkboard
    b = draw_map(z, 46, 10, 144, 110, 60)
    z.t('worktitle', *b)
    z.t('work', 54, 72, 130, 44)
    sash(c, 194, 14, 82)
    draw_corkboard(z, 208, 12, 106, 100, [
        ('w1', 214, 18, 46, 40, 'print'),
        ('w2', 264, 18, 44, 46, 'print'),
        ('w3', 214, 68, 94, 38, 'print'),
    ])
    # ---------------- mid wall: window (moon) and the shelf
    window(z, 226, 126, 70, 44, mode)
    shelf(c, 46, 160, 124)
    for i, hh in enumerate((19, 17, 18)):
        b = grid(S.BOOK[:hh - 2] + S.BOOK[-2:]) if hh < 19 else grid(S.BOOK)
        c.blit(b, 50 + i * 5, 160 - b.h)
    c.blit(grid(S.BEAR), 66, 160 - 14)
    for i in range(6):
        c.blit(grid(S.TROPHY), 79 + i * 8, 160 - 13)
    z.o('fuzz', 128, 153, 9, 7)
    z.o('hilt', 140, 155, 16, 5)
    c.blit(grid(S.PLANT), 158, 151)
    # ---------------- floor: door, coats, CD tower, rug + corgi, hoodie, chair + towel, desk
    door(z, 50, 204, 34, 88)
    coat_rail(c, 90, 176, 40)
    c.blit(grid(S.ROBE), 91, 176)
    c.blit(grid(S.JACKET), 111, 176)
    cd_tower(z, 134, 236, 56)
    rug(c, 150, 288, 56)
    z.o('corgi', 156, 276, 33, 14)
    z.o('orb2', 166, 281, 9, 9)
    chair(c, 200, floor)
    z.o('towel', 194, 231, 16, 30)
    c.blit(grid(S.HOODIE), 184, 283)
    desk(c, 226, 250, 90, floor)
    pc_tower(c, 240, 262, 30)
    sx, sy, sw, sh = monitor(z, 208, 174, 94, 68, mode)
    lamp(c, 304, 250, mode)
    keyboard(c, 244, 247, 34)
    c.blit(grid(S.MUG), 230, 243)
    c.blit(grid(S.PENCUP), 283, 235)
    c.blit(grid(S.CAPSJAR), 292, 240)
    z.o('bobble', 220, 233, 10, 15)
    z.o('hearth', 300, 243, 9, 7)
    z.o('steam', 230, 230, 8, 12)
    outlet(c, 316 - 8, 270)
    cables(c, [(266, 249), (268, 258), (262, 268), (255, 276), (254, 290), (268, 291), (306, 291), (309, 276)])
    cables(c, [(305, 249), (306, 262), (309, 272)], 's1')
    # ---------------- light
    if mode == 'night':
        z.light.pool(292, 242, 86, 64, 2.7, core=.7)      # desk lamp
        z.light.pool(255, 222, 80, 62, 1.25, core=1.2)     # monitor glow
        z.light.shaft([(226, 126), (296, 126), (226, floor), (150, floor)], .95, soft=4)  # moon
        z.light.pool(180, 120, 160, 120, .35)
    else:
        z.light.shaft([(226, 126), (296, 126), (218, floor), (140, floor)], .85, soft=4)
        z.light.shade(x0, 200, 40, 92, .5, soft=10)
    ao(z, 228, 255, 88, 37, .6)
    ao(z, 46, 160, 124, 6, .5)
    ao(z, x0, 6, x1 - x0, 8, .4)
    finish_light(z, x0, x1, mode, [(48, 12, 140, 106), (208, 12, 106, 100)])
    return z




# ====================================================================== garage objects
def block_wall(c, x, y, w, h):
    c.rect(x, y, w, h, 's2')
    for yy in range(y, y + h):
        r_ = (yy - y) // 6
        if (yy - y) % 6 == 5:
            c.rect(x, yy, w, 1, 's1')
        else:
            off = 0 if r_ % 2 == 0 else 8
            for xx in range(x + off, x + w, 16):
                c.px(xx, yy, 's1')
        if (yy - y) % 6 == 0:
            for xx in range(x, x + w):
                if (xx * 7 + yy) % 9 == 0:
                    c.px(xx, yy, 's3')


def stairs(c, x_top, y_top, n, rise, run, w_side='left'):
    """steep stairs from the room door: stepped profile, solid side stringer, balusters + rail"""
    xe = x_top + n * run
    ye = y_top + n * rise
    for x in range(x_top, xe + 1):
        k = min(n - 1, (x - x_top) // run)
        yp = y_top + (k + 1) * rise - 2                      # top of this tread
        yb = int(y_top + (x - x_top) * rise / run) + 12      # underside of the stringer
        yb = max(yb, yp + 3)
        for y in range(yp, min(yb, ye + 1)):
            col = 'w2'
            if y - yp < 2:
                col = 'w4' if y == yp else 'w3'             # tread nosing
            elif (x - x_top) % run == 0:
                col = 'w1'                                    # riser line
            elif yb - y <= 2:
                col = 'w1'
            c.px(x, y, col)
        c.px(x, min(yb, ye + 1), 'k0')
        c.px(x, yp - 1, 'k0')
    for k in range(n):
        tx = x_top + k * run
        c.rect(tx, y_top + k * rise, 1, rise, 'k0')           # riser edge
        c.rect(tx + 2, y_top + (k + 1) * rise - 20, 1, 18, 's2')  # baluster
    c.line(x_top + 2, y_top - 18 + rise, xe + 2, ye - 20, 'w3')
    c.line(x_top + 2, y_top - 17 + rise, xe + 2, ye - 19, 'k0')
    c.rect(xe + 1, ye - 22, 3, 22, 'w2'); c.frame(xe, ye - 23, 5, 23, 'k0'); c.rect(xe, ye - 25, 5, 2, 'w3')


def pegboard(c, x, y, w, h):
    c.rect(x, y, w, h, 'w4'); c.frame(x - 1, y - 1, w + 2, h + 2, 'k0')
    for yy in range(y + 2, y + h - 1, 4):
        for xx in range(x + 2, x + w - 1, 4):
            c.px(xx, yy, 'w3')
    # hammer
    c.rect(x + 5, y + 5, 2, 14, 'w2'); c.rect(x + 3, y + 4, 7, 3, 's2'); c.rect(x + 3, y + 4, 7, 1, 's3'); c.frame(x + 2, y + 3, 9, 5, 'k0')
    # wrench
    c.rect(x + 15, y + 6, 2, 16, 's3'); c.rect(x + 14, y + 4, 4, 3, 's3'); c.px(x + 15, y + 4, 'w4'); c.rect(x + 14, y + 21, 4, 2, 's3')
    # saw
    c.poly([(x + 24, y + 4), (x + 40, y + 4), (x + 40, y + 9), (x + 24, y + 16)], 's3')
    for xx in range(x + 25, x + 40, 2):
        c.px(xx, y + 4 + (xx - x - 24) * 12 // 16 + 1, 's2')
    c.rect(x + 40, y + 3, 5, 8, 'r2'); c.frame(x + 40, y + 3, 5, 8, 'k0'); c.rect(x + 41, y + 5, 3, 4, 'w4')
    # pliers + tape
    c.line(x + 6, y + h - 14, x + 9, y + h - 4, 'r3'); c.line(x + 10, y + h - 14, x + 8, y + h - 4, 'r3'); c.disc(x + 8, y + h - 14, 1.5, 's3')
    c.disc(x + 30, y + h - 9, 4, 'g3'); c.disc(x + 30, y + h - 9, 2, 'k0'); c.rect(x + 34, y + h - 7, 3, 1, 's3')
    c.rect(x + 20, y + h - 18, 3, 12, 'g3'); c.rect(x + 20, y + h - 6, 3, 2, 's2')  # screwdriver


def workbench(c, x, y, w, floor):
    c.rect(x, y, w, 5, 'w3'); c.rect(x, y, w, 1, 'w4'); c.frame(x - 1, y - 1, w + 2, 7, 'k0')
    for lx in (x + 2, x + w - 6):
        c.rect(lx, y + 5, 4, floor - y - 5, 'w2'); c.frame(lx - 1, y + 5, 6, floor - y - 5, 'k0')
    c.rect(x + 1, floor - 14, w - 2, 3, 'w2'); c.frame(x, floor - 15, w, 5, 'k0')
    # paint cans + a toolbox on the lower shelf
    for i, col in enumerate(('n4', 'r3', 'c0')):
        cx = x + 8 + i * 9
        c.rect(cx, floor - 24, 7, 9, 's3'); c.rect(cx, floor - 21, 7, 4, col); c.frame(cx - 1, floor - 25, 9, 11, 'k0'); c.rect(cx, floor - 24, 7, 1, 's2')
    c.rect(x + w - 22, floor - 23, 16, 8, 'r2'); c.rect(x + w - 22, floor - 23, 16, 2, 'r3'); c.frame(x + w - 23, floor - 24, 18, 10, 'k0'); c.rect(x + w - 17, floor - 26, 6, 2, 'k0')
    # vise
    c.rect(x - 4, y - 6, 8, 6, 's2'); c.frame(x - 5, y - 7, 10, 8, 'k0'); c.rect(x - 4, y - 6, 8, 1, 's3'); c.rect(x - 7, y - 3, 3, 1, 's3')


def plate_wv(c, x, y):
    c.rect(x, y, 24, 12, 'n3'); c.frame(x - 1, y - 1, 26, 14, 'k0')
    c.frame(x, y, 24, 12, 'g3')
    c.rect(x + 1, y + 1, 22, 2, 'g3')
    # gold ridge silhouette + embossed serial blocks
    for xx in range(x + 2, x + 22):
        hh = 2 + int(1.5 * math.sin(xx / 2.2)) + (1 if xx % 5 == 0 else 0)
        c.rect(xx, y + 10 - hh, 1, hh, 'g2')
    for bx in (x + 3, x + 7, x + 11, x + 15, x + 19):
        c.rect(bx, y + 4, 2, 3, 'c0')
    c.px(x + 2, y + 2, 'k0'); c.px(x + 21, y + 2, 'k0')


def spray_a(c, x, y, mode):
    """spray-painted A with an arrow, overspray speckles and drips"""
    col, dark = 'o2', 'o1'
    pts = []
    A = [
        "....XXX....",
        "...XXXXX...",
        "...XX.XX...",
        "..XXX.XXX..",
        "..XX...XX..",
        ".XXX...XXX.",
        ".XXXXXXXXX.",
        ".XXXXXXXXX.",
        "XXX.....XXX",
        "XX.......XX",
        "XX.......XX",
    ]
    for yy, row in enumerate(A):
        for xx, ch in enumerate(row):
            if ch == 'X':
                c.rect(x + xx * 2, y + yy * 2, 2, 2, col)
    r = rnd(77)
    for _ in range(40):
        sx, sy = x + r.randint(-3, 24), y + r.randint(-3, 24)
        if c.get(sx, sy) != C(col):
            c.px(sx, sy, dark)
    for dx in (1, 17, 19):
        c.rect(x + dx, y + 22, 1, r.randint(3, 7), col)
    # arrow pointing right
    ay = y + 30
    c.rect(x, ay, 22, 2, col)
    for k in range(5):
        c.rect(x + 20 + k, ay - 4 + k, 1, 10 - 2 * k, col)
    c.rect(x + 6, ay + 2, 1, 4, col)


def nose_cone(c, x, y):
    """Formula Electric nose cone hung on wires, race number on a roundel"""
    c.line(x + 6, y - 10, x + 6, y, 's2'); c.line(x + 34, y - 10, x + 30, y + 2, 's2')
    pts = [(x, y + 6), (x + 6, y + 1), (x + 40, y), (x + 44, y + 4), (x + 44, y + 13), (x + 2, y + 13)]
    c.poly(pts, 'c0')
    c.poly([(x + 2, y + 9), (x + 44, y + 8), (x + 44, y + 11), (x + 3, y + 12)], 'n3')
    c.rect(x + 10, y + 7, 34, 1, 'g3')
    c.disc(x + 26, y + 6, 4, 'c0'); c.disc(x + 26, y + 6, 4.5, 'k0'); c.disc(x + 26, y + 6, 3.6, 'c0')
    c.text(x + 23, y + 4, '12', 'k0') if False else None
    from px import FONT34
    c.text(x + 23, y + 4, '12', 'k0', font=FONT34)
    c.rect(x + 6, y + 2, 20, 1, 'c1')
    # outline
    tmp = Canvas(48, 16)
    c.line(x, y + 6, x + 6, y + 1, 'k0'); c.line(x + 6, y + 1, x + 40, y, 'k0'); c.line(x + 40, y, x + 44, y + 4, 'k0')
    c.rect(x + 44, y + 4, 1, 10, 'k0'); c.rect(x + 2, y + 13, 43, 1, 'k0'); c.line(x, y + 6, x + 2, y + 13, 'k0')


def garage_door(z, x, y, w, h, mode):
    """sectional roll-up garage door: horizontal ribbed sections, top window row, side tracks,
    header, handle, light leaking in under the bottom seal"""
    c = z.c
    # header + side tracks
    c.rect(x - 7, y - 7, w + 14, 5, 'w2'); c.rect(x - 7, y - 7, w + 14, 1, 'w3'); c.frame(x - 8, y - 8, w + 16, 7, 'k0')
    for tx in (x - 5, x + w + 1):
        c.rect(tx, y - 2, 4, h + 2, 's2'); c.rect(tx + 1, y - 2, 2, h + 2, 's1'); c.frame(tx - 1, y - 2, 6, h + 2, 'k0')
        for ry in range(y + 6, y + h, 14):
            c.px(tx + 1, ry, 's3'); c.px(tx + 2, ry, 's3')  # roller
    sec = h // 4
    for k in range(4):
        sy = y + k * sec
        sh = sec if k < 3 else h - 3 * sec
        c.rect(x, sy, w, sh, 'c1')
        for ry in range(sy + 3, sy + sh - 1, 3):
            c.rect(x, ry, w, 1, 'c2')                       # ribs
        c.rect(x, sy, w, 1, 'k0'); c.rect(x, sy + 1, w, 1, 'c0')  # joint + highlight
        c.rect(x, sy + sh - 1, w, 1, 's3')
        for hx in (x + 2, x + w // 2 - 1, x + w - 4):        # hinges at the joints
            if k > 0:
                c.rect(hx, sy - 1, 3, 3, 's2'); c.px(hx + 1, sy, 's1')
    # top section: a row of little windows
    nwin = max(3, w // 22)
    ww = (w - 8 - (nwin - 1) * 4) // nwin
    for i in range(nwin):
        wx = x + 4 + i * (ww + 4)
        c.rect(wx, y + 5, ww, 6, 'k0')
        if mode == 'night':
            c.rect(wx + 1, y + 6, ww - 2, 4, 'n2', em=True); c.px(wx + 2 + i % 3, y + 7, 'n5', em=True)
        else:
            c.rect(wx + 1, y + 6, ww - 2, 2, 'p3', em=True); c.rect(wx + 1, y + 8, ww - 2, 2, 'o3', em=True)
    # handle + lock on the bottom section
    hy = y + h - sec // 2 - 1
    c.rect(x + w // 2 - 6, hy, 12, 2, 's1'); c.rect(x + w // 2 - 6, hy, 12, 1, 's3'); c.frame(x + w // 2 - 7, hy - 1, 14, 4, 'k0')
    c.disc(x + w - 9, hy, 1.5, 's3'); c.px(x + w - 9, hy, 'k0')
    # bottom seal + light leaking under the door
    c.rect(x, y + h - 2, w, 2, 'k0')
    leak = 'g4' if mode == 'day' else 'n5'
    c.rect(x + 2, y + h - 1, w - 4, 1, leak, em=True)
    c.frame(x - 1, y - 1, w + 2, h + 1, 'k0')
    return y + h


def sticker(c, cx, cy, w, h, ang, col, seed=0, art=None):
    """die-cut vinyl sticker: white border, slight rotation, a worn corner peeling up"""
    r = rnd(seed)
    a = math.radians(ang)
    ca_, sa_ = math.cos(a), math.sin(a)

    def corners(ww, hh):
        out = []
        for (dx, dy) in ((-ww / 2, -hh / 2), (ww / 2, -hh / 2), (ww / 2, hh / 2), (-ww / 2, hh / 2)):
            out.append((cx + dx * ca_ - dy * sa_, cy + dx * sa_ + dy * ca_))
        return out
    c.poly(corners(w + 4, h + 4), 'k0')
    c.poly(corners(w + 2, h + 2), 'c0')
    c.poly(corners(w, h), col)
    # worn edge: a few nicks in the white border
    pts = corners(w + 2, h + 2)
    for _ in range(4):
        k = r.randint(0, 3); t = r.random()
        (ax, ay), (bx, by) = pts[k], pts[(k + 1) % 4]
        c.px(int(ax + (bx - ax) * t), int(ay + (by - ay) * t), 's3')
    # peeling corner (top right) showing the backing
    tx, ty = [int(round(v)) for v in pts[1]]
    c.px(tx - 1, ty, 'c2'); c.px(tx - 1, ty + 1, 'c2'); c.px(tx - 2, ty + 1, 'c2'); c.px(tx, ty, 's3'); c.px(tx, ty + 1, 'k0')
    # scuffs on the face
    for _ in range(2):
        px_, py_ = cx + r.randint(-w // 2 + 2, w // 2 - 2), cy + r.randint(-h // 2 + 2, h // 2 - 2)
        c.px(int(px_), int(py_), 's2' if col != 'k0' else 's1')


def yard(z, x0, x1, floor, H, mode, steps_x):
    c = z.c
    # backdrop already filled; grass + fence + ground cut
    for xx in range(x0, x1, 4):
        c.rect(xx, floor - 22, 3, 22, 'w2' if mode == 'day' else 'w1'); c.px(xx + 1, floor - 23, 'w2'); c.rect(xx, floor - 22, 1, 22, 'k0')
    c.rect(x0, floor - 16, x1 - x0, 2, 'w3')
    c.rect(x0, floor, x1 - x0, 2, 'e3'); c.rect(x0, floor + 2, x1 - x0, 2, 'e2')
    for xx in range(x0, x1, 2):
        c.px(xx, floor - 1, 'e3' if xx % 4 else 'e2')
    earth(c, x0, floor + 4, x1 - x0, H - floor - 4, 41)
    # steps up to the side door
    for i in range(3):
        c.rect(steps_x + i * 0, floor - 4 * (i + 1), x1 - steps_x - i * 3, 4, 's2')
        c.rect(steps_x + i * 0, floor - 4 * (i + 1), x1 - steps_x - i * 3, 1, 's3')
        c.frame(steps_x + i * 0 - 1, floor - 4 * (i + 1) - 1, x1 - steps_x - i * 3 + 1, 5, 'k0')


def oak_trunk(c, x0, y0, y1, mode):
    bark, dark, lite = ('w1', 'w0', 'w2') if mode == 'day' else ('w0', 'k0', 'w1')
    for y in range(y0, y1):
        wob = int(1.2 * math.sin(y / 9))
        c.rect(x0 + wob, y, 9, 1, bark)
        c.px(x0 + wob, y, 'k0'); c.px(x0 + wob + 8, y, 'k0')
        if y % 5 == 0:
            c.px(x0 + wob + 3, y, dark)
        if y % 7 == 2:
            c.px(x0 + wob + 6, y, lite)


def oak_canopy(c, cx, cy, rx, ry, mode, seed):
    r = rnd(seed)
    a, b, hi = ('e1', 'e2', 'e3') if mode == 'day' else ('k0', 'e1', 'e2')
    blobs = [(cx + r.randint(-rx, rx), cy + r.randint(-ry, ry), r.randint(5, 9)) for _ in range(14)]
    for (bx, by, br) in blobs:
        c.disc(bx, by, br + 1, 'k0')
    for (bx, by, br) in blobs:
        c.disc(bx, by, br, a)
    for (bx, by, br) in blobs:
        c.disc(bx + 1, by - 1, br - 2, b)
        c.px(bx + 2, by - br + 2, hi); c.px(bx + 3, by - br + 3, hi)


def compose_garage(L, mode):
    return garage_D(mode) if L == 'D' else garage_M(mode)


def garage_D(mode):
    W, H = D_W, 212
    floor = 196
    z = Z(W, H, mode, 1.9 if mode == 'day' else 0.45)
    c = z.c
    x0, x1 = 42, 318
    c.rect(0, 0, 36, H, 'e1' if mode == 'night' else 'p1')
    if mode == 'night':
        r = rnd(5)
        for _ in range(12):
            c.px(r.randint(1, 34), r.randint(2, 150), r.choice(['g4', 'c1', 'o3']), em=True)
    oak_trunk(c, 6, 0, floor - 22, mode)
    yard(z, 0, 36, floor, H, mode, 24)
    oak_trunk(c, 6, floor - 23, floor, mode)
    c.rect(3, floor - 2, 15, 2, 'w1'); c.px(2, floor - 1, 'k0'); c.px(18, floor - 1, 'k0')
    c.blit(grid(S.HAY), 1, floor - 12)
    z.o('pumpkin', 24, floor - 12 - 10, 10, 10)
    earth(c, 324, 0, W - 324, H, 32)
    wall_cut(c, 36, 0, 6, floor)
    wall_cut(c, 318, 0, 6, floor)
    block_wall(c, x0, 0, x1 - x0, floor)
    # floor slab
    c.rect(36, floor, 288, H - floor, 's1'); c.rect(36, floor, 288, 1, 's3'); c.rect(36, floor + 1, 288, 1, 's2')
    c.ellipse(226, floor + 5, 10, 2, 'k0'); c.rect(36, H - 1, 288, 1, 'k0')
    # high window (moon)
    window_small(z, 112, 14, 40, 16, mode)
    # stairs down from the door above
    stairs(c, 42, 0, 12, 16, 5)
    # under-stairs storage: stacked boxes and a folded lawn chair
    for (bx, by, bw, bh) in ((44, 176, 16, 20), (44, 160, 13, 16), (61, 182, 14, 14)):
        c.rect(bx, by, bw, bh, 'w4'); c.rect(bx, by, bw, 2, 'c2'); c.rect(bx + bw // 2 - 1, by, 2, bh, 'c2')
        c.rect(bx + bw - 1, by, 1, bh, 'w3'); c.frame(bx - 1, by - 1, bw + 2, bh + 1, 'k0')
    c.line(78, 196, 84, 168, 's3'); c.line(84, 196, 78, 168, 's3'); c.rect(77, 170, 9, 2, 'g3')
    # wall: guitar, plate, spray A
    c.rect(116, 64, 2, 3, 's2')
    c.blit(S.guitar(), 110, 66)
    plate_wv(c, 132, 80)
    spray_a(c, 162, 54, mode)
    # drum kit (pieces are overlays); a rug under it
    c.rect(104, floor - 3, 92, 3, 'r1'); c.rect(104, floor - 3, 92, 1, 'r2')
    for xx in range(106, 194, 6):
        c.px(xx, floor - 2, 'g2')
    kit = S.drum_kit()
    kx, ky = 106, floor - 50
    hw, _, _ = kit['hw']; c.blit(hw, kx, ky)
    for k in ['crash', 'ride', 'hihat', 'tom1', 'tom2', 'kick', 'snare', 'floortom']:
        cv, px_, py_ = kit[k]
        z.o('kit-' + k, kx + px_, ky + py_, cv.w, cv.h)
    z.o('orb5', kx + 40, ky + 30, 9, 9)
    # shelf above the door: taped box, ship in a bottle, the little tv, paint cans
    sy = 40
    c.rect(202, sy, 112, 3, 'w3'); c.rect(202, sy, 112, 1, 'w4'); c.frame(201, sy - 1, 114, 5, 'k0')
    for i, bx in enumerate((206, 254, 300)):
        z.o('bracket%d' % i, bx, sy + 4, 8, 7)
    z.o('orb6', 218, sy - 11, 9, 9)
    z.o('box', 206, sy - 22, 28, 22)
    c.blit(grid(S.SHIPBOTTLE), 238, sy - 14)
    c.blit(grid(S.TV_SMALL), 266, sy - 14)
    z.o('tvsun', 269, sy - 8, 8, 4)
    for i, col in enumerate(('n3', 'e3', 'r3')):
        cx = 284 + i * 9
        c.rect(cx, sy - 10, 7, 10, 's3'); c.rect(cx, sy - 7, 7, 4, col); c.frame(cx - 1, sy - 11, 9, 12, 'k0'); c.rect(cx, sy - 10, 7, 1, 's2')
    # nose cone + a small pegboard between the shelf and the door header
    nose_cone(c, 206, 58)
    pegboard(c, 262, 52, 48, 34)
    # the roll-up door with link stickers stuck on it
    garage_door(z, 210, 96, 102, floor - 96, mode)
    for (sid, cx_, cy_, sw, sh, ang, col, sd) in (('lk-x', 228, 136, 13, 11, -7, 'k0', 3),
                                                  ('lk-li', 268, 128, 34, 11, 4, 'n3', 4),
                                                  ('lk-gh', 252, 152, 32, 11, -3, 'k0', 5)):
        sticker(c, cx_, cy_, sw, sh, ang, col, sd)
        z.t(sid, cx_ - sw // 2, cy_ - sh // 2, sw, sh)
    # light leaking under the door onto the floor
    for xx in range(214, 310):
        if BAYER[0][xx % 4] < .5:
            c.px(xx, floor, 'g4' if mode == 'day' else 'n5', em=True)
        if BAYER[1][xx % 4] < .25:
            c.px(xx, floor + 1, 'g3' if mode == 'day' else 'n4', em=True)
    # clutter: extension cord on a nail, cooler, sneakers, broom
    c.px(146, 104, 's2')
    for k in range(3):
        c.ellipse(146, 113 + k, 6 - k, 7 - k, 'o2')
    c.disc(146, 114, 3, 's2'); c.disc(146, 114, 2, 's2')
    c.line(150, 120, 152, 134, 'o2'); c.line(152, 134, 149, 140, 'o1')
    c.rect(184, 184, 20, 12, 'n4'); c.rect(184, 184, 20, 4, 'c0'); c.frame(183, 183, 22, 14, 'k0'); c.rect(189, 181, 10, 2, 's2'); c.rect(185, 191, 18, 1, 'n3')
    c.line(201, 150, 199, 182, 'w4'); c.poly([(195, 180), (203, 180), (204, 184), (194, 184)], 'g2')
    # light: moon through the high window, light under the door, the tv's glow
    if mode == 'night':
        z.light.shaft([(112, 14), (152, 14), (128, floor), (80, floor)], 1.35, soft=4)
        z.light.pool(150, 120, 150, 100, .6)
        z.light.pool(262, 196, 70, 22, 1.2)
        z.light.pool(273, 34, 30, 22, .9)
    else:
        z.light.shaft([(112, 14), (152, 14), (128, floor), (80, floor)], .8, soft=4)
        z.light.shade(x0, 0, x1 - x0, 20, .5, soft=8)
    ao(z, 42, 150, 40, 46, .35)
    finish_light(z, x0, x1, mode, [(214, 120, 96, 44)])
    return z


def window_small(z, x, y, w, h, mode):
    c = z.c
    if mode == 'night':
        c.rect(x, y, w, h, 'n2', em=True); c.rect(x, y + h - 5, w, 5, 'n1', em=True)
        c.px(x + 5, y + 3, 'c1', em=True); c.px(x + 30, y + 5, 'n5', em=True)
    else:
        c.rect(x, y, w, h // 2, 'p3', em=True); c.rect(x, y + h // 2, w, h - h // 2, 'o3', em=True)
    c.frame(x - 2, y - 2, w + 4, h + 4, 'k0'); c.frame(x - 1, y - 1, w + 2, h + 2, 'c1')
    c.rect(x + w // 2, y, 1, h, 'c1')




# ====================================================================== basement
def stone_wall(c, x, y, w, h, seed):
    r = rnd(seed)
    c.rect(x, y, w, h, 's1')
    yy = y
    while yy < y + h:
        bh = r.choice((6, 7, 8))
        xx = x - r.randint(0, 8)
        while xx < x + w:
            bw = r.choice((10, 12, 14, 16))
            col = r.choice(('s2', 's2', 's1', 'n2'))
            for py in range(yy + 1, min(y + h, yy + bh)):
                for px_ in range(max(x, xx + 1), min(x + w, xx + bw)):
                    c.px(px_, py, col)
            for px_ in range(max(x, xx + 1), min(x + w, xx + bw)):
                c.px(px_, yy + 1, 's3' if col == 's2' else 's2')
            xx += bw
        yy += bh


def big_crt(z, x, y, w, h, mode):
    """the arcade CRT that holds the game window"""
    c = z.c
    c.rect(x + 2, y, w - 4, h, 's1'); c.rect(x, y + 2, w, h - 4, 's1')
    c.rect(x + 2, y + 1, w - 4, 1, 's2'); c.rect(x + 1, y + 2, 1, h - 4, 's2')
    for (px_, py_) in ((x + 1, y + 1), (x + w - 2, y + 1), (x + 1, y + h - 2), (x + w - 2, y + h - 2)):
        c.px(px_, py_, 'k0')
    c.rect(x + 2, y - 1, w - 4, 1, 'k0'); c.rect(x + 2, y + h, w - 4, 1, 'k0'); c.rect(x - 1, y + 2, 1, h - 4, 'k0'); c.rect(x + w, y + 2, 1, h - 4, 'k0')
    c.px(x, y + 1, 'k0'); c.px(x + 1, y, 'k0'); c.px(x + w - 1, y + 1, 'k0'); c.px(x + w - 2, y, 'k0')
    c.px(x, y + h - 2, 'k0'); c.px(x + 1, y + h - 1, 'k0'); c.px(x + w - 1, y + h - 2, 'k0'); c.px(x + w - 2, y + h - 1, 'k0')
    # screen bezel
    sx, sy, sw, sh = x + 8, y + 7, w - 16, h - 26
    c.rect(sx - 3, sy - 3, sw + 6, sh + 6, 'k0')
    c.rect(sx, sy, sw, sh, 'n1', em=True)
    # grille + knobs + led
    gy = y + h - 15
    for xx in range(x + 10, x + 70, 3):
        c.rect(xx, gy, 2, 8, 'k0')
    for kx in (x + w - 30, x + w - 20):
        c.disc(kx, gy + 4, 3, 'k0'); c.disc(kx, gy + 4, 2, 's2'); c.px(kx, gy + 3, 's3')
    c.px(x + w - 10, gy + 4, 'r3', em=True)
    return sx, sy, sw, sh


def small_crt(c, x, y, mode, seed):
    c.rect(x, y, 26, 21, 's2'); c.frame(x - 1, y - 1, 28, 23, 'k0'); c.rect(x, y, 26, 1, 's3')
    c.rect(x + 3, y + 3, 16, 13, 'k0')
    c.rect(x + 4, y + 4, 14, 11, 'u', em=True)
    # split screen, four quadrants
    c.rect(x + 11, y + 4, 1, 11, 'n1', em=True); c.rect(x + 4, y + 9, 14, 1, 'n1', em=True)
    r = rnd(seed)
    for (qx, qy) in ((x + 4, y + 4), (x + 12, y + 4), (x + 4, y + 10), (x + 12, y + 10)):
        c.rect(qx, qy + 3, 7, 2, 'e2', em=True)
        c.px(qx + r.randint(1, 5), qy + r.randint(0, 2), 'N', em=True)
        c.px(qx + 3, qy + 2, 'c0', em=True)
    for yy in range(y + 4, y + 15, 2):
        c.rect(x + 4, yy, 14, 1, 'n2', em=True) if False else None
    c.rect(x + 21, y + 4, 3, 1, 'k0'); c.rect(x + 21, y + 6, 3, 1, 'k0'); c.disc(x + 22, y + 13, 1.5, 'k0')
    c.rect(x + 4, y + 21, 18, 2, 's1')


def console(c, x, y):
    c.rect(x, y, 14, 6, 'c0'); c.frame(x - 1, y - 1, 16, 8, 'k0'); c.rect(x, y + 4, 14, 2, 's3')
    c.px(x + 11, y + 2, 'e3', em=True)


def controller(c, x, y, col='k0'):
    g = grid(["..KKKKK..", ".K9999 9K".replace(' ', '9'), "K99KK99R9K", "K9KKK9GTK", ".KK...KK."]) if False else None
    c.rect(x + 1, y, 8, 3, 's3'); c.rect(x, y + 1, 10, 3, 's3'); c.frame(x - 1, y, 12, 5, 'k0')
    c.px(x + 2, y + 2, 'k0'); c.px(x + 7, y + 1, 'r3'); c.px(x + 8, y + 2, 'e3')


def beanbag(c, x, y, w, h, col, sh, hl):
    c.ellipse(x + w / 2, y + h * .6, w / 2, h * .45, sh)
    c.ellipse(x + w / 2, y + h * .55, w / 2 - 1, h * .42, col)
    c.ellipse(x + w * .4, y + h * .45, w * .28, h * .22, hl)
    c.rect(x + 2, y + h - 2, w - 4, 2, sh)
    tmp = Canvas(1, 1)
    # outline by scanning the region
    m = (c.a[y:y + h + 1, x:x + w + 1] != T)


def score_card(c, x, y, w, h):
    """index card: ruled lines, red margin, tape on the top corners"""
    c.rect(x + 1, y + 1, w, h, 'k0')
    c.rect(x, y, w, h, 'c0'); c.frame(x - 1, y - 1, w + 2, h + 2, 'k0')
    for ry in range(y + 7, y + h - 1, 6):
        c.rect(x + 1, ry, w - 2, 1, 'n6')
    c.rect(x + 4, y, 1, h, 'p3')
    c.rect(x + w - 1, y, 1, h, 'c1'); c.rect(x, y + h - 1, w, 1, 'c1')
    for tx in (x - 3, x + w - 7):
        for k in range(4):
            c.rect(tx + k, y - 3 + k, 7, 1, 'c2' if k % 2 else 'c1')


def headset(c, x, y):
    """over-ear headset hanging by its band, mic boom, cable"""
    for k, col in ((0, 'k0'), (1, 's2'), (2, 's1')):
        c.line(x + 1, y + 9 - k + 1, x + 3, y + 2 + k, col); c.line(x + 3, y + 2 + k, x + 11, y + 2 + k, col); c.line(x + 11, y + 2 + k, x + 13, y + 9 - k + 1, col)
    c.rect(x + 4, y + 2, 7, 1, 's3')
    for cx in (x - 1, x + 11):
        c.rect(cx, y + 9, 5, 8, 's1'); c.rect(cx + 1, y + 10, 1, 6, 's2'); c.rect(cx + 3, y + 10, 1, 6, 'r2'); c.frame(cx - 1, y + 8, 7, 10, 'k0')
    c.line(x + 15, y + 16, x + 19, y + 21, 'k0'); c.rect(x + 19, y + 21, 2, 2, 's2')
    c.line(x + 1, y + 18, x + 2, y + 30, 'k0'); c.line(x + 2, y + 30, x + 7, y + 34, 'k0')


def lava_lamp(c, x, y, mode):
    c.poly([(x + 1, y + 6), (x + 9, y + 6), (x + 10, y + 14), (x, y + 14)], 'r1')
    blob = 'o2'
    c.poly([(x + 2, y + 2), (x + 8, y + 2), (x + 9, y + 14), (x + 1, y + 14)], 'r2', em=True)
    c.disc(x + 4, y + 10, 2, blob, em=True); c.disc(x + 6, y + 5, 1.5, blob, em=True); c.px(x + 5, y + 13, 'o3', em=True)
    c.rect(x + 2, y, 6, 2, 's1'); c.rect(x, y + 14, 10, 6, 's1'); c.rect(x + 1, y + 14, 8, 1, 's2')
    c.frame(x - 1, y + 13, 12, 8, 'k0'); c.rect(x + 2, y - 1, 6, 1, 'k0')
    c.line(x + 1, y + 2, x - 1, y + 14, 'k0'); c.line(x + 8, y + 2, x + 10, y + 14, 'k0')


def compose_base(L, mode):
    return base_D(mode) if L == 'D' else base_M(mode)


def base_D(mode):
    W, H = D_W, 290
    floor = 248
    z = Z(W, H, mode, 0.5 if mode == 'day' else 0.25)
    c = z.c
    x0, x1 = 42, 318
    earth(c, 0, 0, 36, H, 51)
    earth(c, 324, 0, W - 324, H, 52)
    wall_cut(c, 36, 0, 6, floor + 6)
    wall_cut(c, 318, 0, 6, floor + 6)
    stone_wall(c, x0, 0, x1 - x0, floor, 3)
    # ceiling joists + pipes + duct
    slab(c, 36, 0, 288, 5)
    c.rect(x0, 8, x1 - x0, 2, 'o1'); c.rect(x0, 8, x1 - x0, 1, 'o2'); c.rect(x0, 10, x1 - x0, 1, 'k0')
    c.rect(x0 + 120, 12, 120, 7, 's2'); c.rect(x0 + 120, 12, 120, 1, 's3'); c.frame(x0 + 119, 11, 122, 9, 'k0')
    for xx in range(x0 + 130, x0 + 240, 22):
        c.rect(xx, 12, 1, 7, 's1')
    # floor
    c.rect(36, floor, 288, 6, 's1'); c.rect(36, floor, 288, 1, 's2')
    # bedrock / footer band
    c.rect(0, floor + 6, W, H - floor - 6, 'k0')
    r = rnd(8)
    for yy in range(floor + 6, H):
        for xx in range(0, W):
            v = (xx * 5 + yy * 11 + (xx * yy) % 7) % 29
            if v == 0:
                c.px(xx, yy, 'n1')
            elif v == 3 and yy % 2:
                c.px(xx, yy, 's1')
    for _ in range(30):
        bx, by = r.randint(0, W - 8), r.randint(floor + 8, H - 5)
        c.rect(bx, by, r.randint(4, 9), 2, 'n1'); c.px(bx, by, 's1')
    # arcade CRT on a low stand
    sx, sy, sw, sh = big_crt(z, 50, 20, 188, 176, mode)
    z.t('game', sx, sy, sw, sh)
    c.rect(54, 199, 180, 4, 'w3'); c.rect(54, 199, 180, 1, 'w4'); c.frame(53, 198, 182, 6, 'k0')
    c.rect(58, 203, 4, floor - 203, 'w2'); c.rect(226, 203, 4, floor - 203, 'w2')
    c.frame(57, 203, 6, floor - 203, 'k0'); c.frame(225, 203, 6, floor - 203, 'k0')
    console(c, 70, 206)
    # LAN night: four CRTs daisy-chained on the floor
    for i, cx in enumerate((66, 98, 130, 162)):
        small_crt(c, cx, floor - 24, mode, i)
        console(c, cx + 6, floor - 2) if False else None
    cables(c, [(92, floor - 6), (96, floor - 2), (98, floor - 6)])
    cables(c, [(124, floor - 6), (128, floor - 1), (130, floor - 6)])
    cables(c, [(156, floor - 6), (160, floor - 1), (162, floor - 6)])
    cables(c, [(188, floor - 8), (196, floor - 1), (230, floor - 1), (236, 200)])
    for (cx, cy) in ((100, floor - 3), (150, floor - 2), (186, floor - 4)):
        controller(c, cx, cy)
    # LAN night leftovers: pizza boxes, cans, a power strip
    for k in range(4):
        by = floor - 4 - k * 4
        c.rect(198 - k % 2, by, 28, 4, 'c2'); c.rect(198 - k % 2, by, 28, 1, 'c1'); c.frame(197 - k % 2, by - 1, 30, 5, 'k0')
    c.rect(202, floor - 16, 10, 2, 'r2')
    for (cx_, col) in ((230, 'r3'), (186, 'n4'), (96, 'e3'), (242, 'r3')):
        c.rect(cx_, floor - 5, 3, 5, col); c.rect(cx_, floor - 5, 3, 1, 's3'); c.frame(cx_ - 1, floor - 6, 5, 7, 'k0')
    c.rect(70, floor - 3, 16, 3, 'c1'); c.frame(69, floor - 4, 18, 5, 'k0')
    for xx in range(72, 86, 3):
        c.px(xx, floor - 2, 'k0')
    # high-score card taped to the wall (text is live HTML on it)
    score_card(c, 246, 30, 64, 27)
    z.t('scores', 248, 31, 61, 25)
    z.o('orb7', 300, 52, 9, 9)
    # headsets + a controller hanging on hooks
    c.rect(248, 70, 48, 3, 'w3'); c.rect(248, 70, 48, 1, 'w4'); c.frame(247, 69, 50, 5, 'k0')
    for hx in (250, 270):
        c.rect(hx + 6, 73, 2, 3, 's2')
        headset(c, hx, 74)
    c.line(292, 73, 292, 84, 'k0'); controller(c, 287, 85)
    # shelf: game cases (colors only) + a lava lamp
    c.rect(244, 112, 60, 3, 'w3'); c.rect(244, 112, 60, 1, 'w4'); c.frame(243, 111, 62, 5, 'k0')
    xx = 246
    for col in ('e2', 'n3', 'k0', 'e2', 'c0', 'n4', 'e3', 'k0', 'r2', 'e2', 'g3'):
        hh = 12 if col not in ('c0', 'g3') else 10
        c.rect(xx, 111 - hh, 3, hh, col); c.rect(xx + 3, 111 - hh, 1, hh, 'k0'); xx += 4
    lava_lamp(c, 294, 92, mode)
    # beanbags, water heater, power strip with the LAN cables
    c.rect(300, 150, 14, floor - 150, 's3'); c.frame(299, 149, 16, floor - 149, 'k0'); c.rect(301, 150, 2, floor - 150, 'c0')
    c.rect(300, 150, 14, 3, 's2'); c.rect(305, 140, 3, 10, 'o1')
    outlet(c, 286, 206)
    c.rect(258, floor - 3, 20, 3, 'c1'); c.frame(257, floor - 4, 22, 5, 'k0')
    for xx in range(260, 277, 4):
        c.px(xx, floor - 2, 'k0')
    c.px(276, floor - 3, 'r3', em=True)
    cables(c, [(278, floor - 2), (284, floor - 6), (288, 216)])
    cables(c, [(258, floor - 2), (244, floor - 1), (236, floor - 3), (214, floor - 1), (190, floor - 3)])
    cables(c, [(262, floor - 4), (250, floor - 10), (240, floor - 8)], 's1')
    # folded LAN-party table leaning on the wall
    tp = [(250, 132), (282, 128), (290, 230), (258, 234)]
    c.poly([(p[0] + 1, p[1] + 1) for p in tp], 'k0')
    c.poly(tp, 'c2')
    c.poly([(253, 136), (279, 132), (286, 226), (260, 230)], 'w4')
    c.line(250, 132, 282, 128, 'c1'); c.line(250, 132, 258, 234, 'k0'); c.line(282, 128, 290, 230, 'k0')
    for (ax, ay, bx, by) in ((258, 150, 284, 222), (283, 146, 262, 224)):
        c.line(ax, ay, bx, by, 's2')
    c.rect(262, 175, 18, 2, 's2')
    beanbag(c, 226, floor - 18, 34, 18, 'g3', 'g2', 'g4')
    beanbag(c, 262, floor - 16, 30, 16, 'n3', 'n2', 'n4')
    controller(c, 240, floor - 20)
    z.t('footer', 40, floor + 10, W - 80, H - floor - 14)
    # light: CRT glow
    z.light.pool(144, 120, 150, 120, 1.7, core=.8)
    for cx in (79, 111, 143, 175):
        z.light.pool(cx, floor - 10, 26, 18, .9)
    z.light.pool(298, 102, 30, 26, 1.0)
    z.light.pool(270, 200, 70, 50, .5)
    z.light.f[floor + 6:, :] = 2.0
    finish_light(z, x0, x1, mode, [(244, 28, 68, 31)])
    z.light.f[floor + 6:, :] = 2.0
    return z




# ====================================================================== phone compositions
MX0, MX1 = 16, 164


def m_columns(z, H, mode, ground=None):
    c = z.c
    c.rect(0, 0, 12, H, 'e1' if mode == 'night' else 'p1')
    if mode == 'night':
        r = rnd(H)
        for _ in range(H // 30):
            c.px(r.randint(1, 10), r.randint(2, H - 2), r.choice(['g4', 'c1', 'o3']), em=True)
    earth(c, 168, 0, 12, H, H + 1)
    wall_cut(c, 12, 0, 4, H)
    wall_cut(c, 164, 0, 4, H)


def room_M(mode):
    W, H = M_W, 692
    z = Z(W, H, mode, 2.0 if mode == 'day' else 0.25)
    c = z.c
    m_columns(z, H, mode)
    f1, f2 = 398, 680
    # study
    room_shell(z, MX0, MX1, f1, f1, mode, wains=34)
    slab(c, 12, f1 + 4, 156, 10)
    # hall
    sub = Canvas(W, H)
    z2 = Z(W, f2 + 12 - (f1 + 14), mode, 0)
    room_shell(z2, MX0, MX1, z2.h, f2 - (f1 + 14), mode, wains=34)
    c.blit(z2.c, 0, f1 + 14)
    slab(c, 12, f2 + 4, 156, H - f2 - 4)
    # study wall: corkboard with stacked papers
    draw_corkboard(z, 18, 12, 144, 160, [
        ('w1', 24, 18, 132, 33, 'print'),
        ('w2', 24, 55, 132, 33, 'print'),
        ('w3', 24, 92, 132, 44, 'print'),
    ])
    sash(c, 112, 137, 30)
    window(z, 118, 192, 40, 32, mode)
    shelf(c, 20, 214, 86)
    for i in range(3):
        c.blit(grid(S.BOOK), 22 + i * 5, 214 - 19)
    c.blit(grid(S.BEAR), 38, 214 - 14)
    for i in range(6):
        c.blit(grid(S.TROPHY), 50 + i * 8, 214 - 13)
    shelf(c, 20, 234, 60)
    z.o('fuzz', 24, 227, 9, 7)
    z.o('hilt', 38, 229, 16, 5)
    c.blit(grid(S.PLANT), 62, 225)
    # desk + monitor (projects as stacked rows)
    chair(c, 20, f1)
    z.o('towel', 14, f1 - 61, 16, 30)
    desk(c, 46, f1 - 42, 116, f1)
    pc_tower(c, 60, f1 - 30, 30)
    monitor(z, 40, 244, 122, 104, mode)
    lamp(c, 148, f1 - 42, mode)
    keyboard(c, 76, f1 - 45, 34)
    c.blit(grid(S.MUG), 52, f1 - 49)
    c.blit(grid(S.PENCUP), 118, f1 - 57)
    c.blit(grid(S.CAPSJAR), 128, f1 - 52)
    z.o('bobble', 64, f1 - 59, 10, 15)
    z.o('hearth', 138, f1 - 49, 9, 7)
    z.o('steam', 52, f1 - 62, 8, 12)
    # hall: map, door, coats, CD tower, rug + corgi
    hy = f1 + 14
    b = draw_map(z, 20, hy + 6, 140, 158, 52, seed=6)
    z.t('worktitle', *b)
    z.t('work', 25, hy + 60, 132, 102)
    door(z, 22, f2 - 88, 34, 88)
    coat_rail(c, 62, f2 - 108, 40)
    c.blit(grid(S.ROBE), 63, f2 - 108)
    c.blit(grid(S.JACKET), 83, f2 - 108)
    cd_tower(z, 146, f2 - 56, 56)
    rug(c, 84, f2 - 4, 58)
    z.o('corgi', 96, f2 - 16, 33, 14)
    z.o('orb2', 106, f2 - 11, 9, 9)
    c.blit(grid(S.HOODIE), 60, f2 - 9)
    if mode == 'night':
        z.light.pool(136, f1 - 10, 60, 50, 2.7, core=.7)
        z.light.pool(100, 300, 80, 66, 1.25, core=1.2)
        z.light.shaft([(118, 192), (158, 192), (110, f1), (60, f1)], .95, soft=3)
        z.light.pool(90, 470, 120, 110, .35)
    else:
        z.light.shaft([(118, 192), (158, 192), (104, f1), (56, f1)], .8, soft=3)
        z.light.shade(MX0, f2 - 90, 40, 90, .4, soft=8)
    ao(z, 46, f1 - 36, 116, 36, .6)
    finish_light(z, MX0, MX1, mode, [(18, 12, 144, 160), (20, hy + 6, 140, 158)])
    z.light.f[f1:f1 + 14, :] = 2.0 if mode == 'day' else 0.6
    return z


def garage_M(mode):
    W, H = M_W, 214
    floor = 200
    z = Z(W, H, mode, 1.9 if mode == 'day' else 0.45)
    c = z.c
    m_columns(z, H, mode)
    block_wall(c, MX0, 0, MX1 - MX0, floor)
    c.rect(12, floor, 156, H - floor, 's1'); c.rect(12, floor, 156, 1, 's3'); c.rect(12, H - 1, 156, 1, 'k0')
    window_small(z, 128, 14, 30, 12, mode)
    # shelf: taped box, ship in a bottle, tv, brackets
    sy = 44
    c.rect(18, sy, 102, 3, 'w3'); c.rect(18, sy, 102, 1, 'w4'); c.frame(17, sy - 1, 104, 5, 'k0')
    for i, bx in enumerate((22, 62, 108)):
        z.o('bracket%d' % i, bx, sy + 4, 8, 7)
    z.o('orb6', 32, sy - 11, 9, 9)
    z.o('box', 20, sy - 22, 28, 22)
    c.blit(grid(S.SHIPBOTTLE), 52, sy - 14)
    c.blit(grid(S.TV_SMALL), 82, sy - 14)
    z.o('tvsun', 85, sy - 8, 8, 4)
    nose_cone(c, 20, 62)
    spray_a(c, 74, 54, mode)
    c.rect(108, 54, 2, 3, 's2')
    c.blit(S.guitar(), 102, 56)
    plate_wv(c, 126, 60)
    # roll-up door across the back wall; the kit stands in front of it
    garage_door(z, 22, 106, 136, floor - 106, mode)
    for (sid, cx_, cy_, sw, sh, ang, col, sd) in (('lk-x', 120, 124, 13, 11, -7, 'k0', 3),
                                                  ('lk-li', 138, 142, 34, 11, 4, 'n3', 4),
                                                  ('lk-gh', 132, 160, 32, 11, -3, 'k0', 5)):
        sticker(c, cx_, cy_, sw, sh, ang, col, sd)
        z.t(sid, cx_ - sw // 2, cy_ - sh // 2, sw, sh)
    for xx in range(26, 154):
        if BAYER[0][xx % 4] < .5:
            c.px(xx, floor, 'g4' if mode == 'day' else 'n5', em=True)
    c.rect(18, floor - 3, 92, 3, 'r1')
    kit = S.drum_kit()
    kx, ky = 20, floor - 50
    hw, _, _ = kit['hw']; c.blit(hw, kx, ky)
    for k in ['crash', 'ride', 'hihat', 'tom1', 'tom2', 'kick', 'snare', 'floortom']:
        cv, px_, py_ = kit[k]
        z.o('kit-' + k, kx + px_, ky + py_, cv.w, cv.h)
    z.o('orb5', kx + 40, ky + 30, 9, 9)
    z.o('pumpkin', 150, floor - 10, 10, 10)
    if mode == 'night':
        z.light.shaft([(128, 14), (158, 14), (120, 106), (90, 106)], 1.2, soft=4)
        z.light.pool(90, 196, 80, 20, 1.1)
        z.light.pool(90, 40, 30, 20, .9)
        z.light.pool(90, 120, 100, 80, .5)
    else:
        z.light.shaft([(128, 14), (158, 14), (120, 106), (90, 106)], .8, soft=4)
    finish_light(z, MX0, MX1, mode, [(108, 114, 56, 54)])
    return z


def base_M(mode):
    W, H = M_W, 352
    floor = 300
    z = Z(W, H, mode, 0.5 if mode == 'day' else 0.25)
    c = z.c
    earth(c, 0, 0, 12, H, 61); earth(c, 168, 0, 12, H, 62)
    wall_cut(c, 12, 0, 4, floor + 6); wall_cut(c, 164, 0, 4, floor + 6)
    stone_wall(c, MX0, 0, MX1 - MX0, floor, 4)
    slab(c, 12, 0, 156, 5)
    c.rect(MX0, 8, MX1 - MX0, 2, 'o1'); c.rect(MX0, 8, MX1 - MX0, 1, 'o2')
    c.rect(12, floor, 156, 6, 's1'); c.rect(12, floor, 156, 1, 's2')
    c.rect(0, floor + 6, W, H - floor - 6, 'k0')
    for yy in range(floor + 6, H):
        for xx in range(0, W):
            if (xx * 5 + yy * 11 + (xx * yy) % 7) % 29 == 0:
                c.px(xx, yy, 'n1')
    sx, sy, sw, sh = big_crt(z, 18, 16, 144, 150, mode)
    z.t('game', sx, sy, sw, sh)
    c.rect(22, 169, 136, 4, 'w3'); c.frame(21, 168, 138, 6, 'k0')
    c.rect(26, 173, 4, 8, 'w2'); c.rect(150, 173, 4, 8, 'w2')
    # scoreboard
    score_card(c, 30, 188, 104, 42)
    z.t('scores', 33, 190, 99, 39)
    z.o('orb7', 138, 214, 9, 9)
    c.rect(140, 196, 20, 3, 'w3'); c.frame(139, 195, 22, 5, 'k0')
    lava_lamp(c, 145, 176, mode)
    headset(c, 142, 204) if False else None
    for i, cx in enumerate((20, 50, 80, 110)):
        small_crt(c, cx, floor - 24, mode, i)
    cables(c, [(46, floor - 6), (49, floor - 1), (50, floor - 6)])
    cables(c, [(76, floor - 6), (79, floor - 1), (80, floor - 6)])
    cables(c, [(106, floor - 6), (109, floor - 1), (110, floor - 6)])
    beanbag(c, 138, floor - 16, 24, 16, 'g3', 'g2', 'g4')
    controller(c, 60, floor - 3)
    z.t('footer', 8, floor + 10, W - 16, H - floor - 14)
    z.light.pool(90, 90, 110, 100, 1.7, core=.8)
    for cx in (33, 63, 93, 123):
        z.light.pool(cx, floor - 10, 24, 16, .9)
    z.light.pool(150, 186, 24, 20, 1.0)
    finish_light(z, MX0, MX1, mode, [(28, 186, 108, 46)])
    z.light.f[floor + 6:, :] = 2.0
    return z
