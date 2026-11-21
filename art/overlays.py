"""Overlay sprites (animated / interactive). Each returns a list of frames."""
import math
from px import Canvas, grid, C, T
import sprites as S


def planet():
    c = Canvas(40, 40)
    cx, cy, r = 20, 25, 12
    c.disc(cx, cy, r + 1, 'k0')
    c.disc(cx, cy, r, 'w2')
    for y in range(40):
        for x in range(40):
            if c.get(x, y) == C('w2'):
                d = math.hypot(x - cx + .5, y - cy + .5)
                if y < cy - 3 + int(2 * math.sin(x / 2.5)):
                    c.px(x, y, 'e2')
                    if x - cx > 2 and d > r - 3:
                        c.px(x, y, 'e3')
                elif x - cx > 4 and d > r - 3:
                    c.px(x, y, 'w3')
                elif x - cx < -4 and d > r - 3:
                    c.px(x, y, 'w1')
                if (x * 7 + y * 3) % 13 == 0 and y > cy:
                    c.px(x, y, 's2')
    c.px(cx + 6, cy - 6, 'L'); c.px(cx + 7, cy - 5, 'L')
    # little house (left, on top)
    hx, hy = 11, 9
    c.rect(hx, hy + 4, 7, 5, 'c0'); c.rect(hx + 5, hy + 4, 2, 5, 'c1')
    for k in range(4):
        c.rect(hx - 1 + k, hy + 3 - k, 9 - 2 * k, 1, 'r2')
    c.rect(hx + 1, hy + 6, 2, 2, 'g4', em=True); c.rect(hx + 4, hy + 6, 2, 3, 'w2')
    c.px(hx + 6, hy, 's2'); c.px(hx + 6, hy - 1, 's3')
    # tree (right)
    tx, ty = 27, 6
    c.rect(tx, ty + 6, 2, 6, 'w1')
    c.disc(tx + 1, ty + 3, 5, 'e2'); c.disc(tx + 2, ty + 2, 3, 'e3'); c.px(tx + 3, ty, 'L')
    c.outline('k0')
    return [c]


TOWEL = [
    "..KKKKKKKKKK....",
    ".KYGGGGGGGhhK...",
    ".KYGGGGGGGhhhK..",
    ".KYGGGGGGhKhhK..",
    ".KYGGGGGGhKhhK..",
    ".KGGGGGGGhKhhK..",
    ".KYGGGGGGhKKKK..",
    ".KYGGGGGGhK.....",
    ".KGGGGGGGhK.....",
    ".KYGGGGGGhK.....",
    ".KYGGGGGGhK.....",
    ".KGGGGGGGhK.....",
    ".KYGGGGGGhK.....",
    ".KKKKKKKKKK.....",
    ".KKKKKKKKKK.....",
    ".KYGGGGGGhK.....",
    ".KYGGGGGGhK.....",
    ".KGGGGGGGhK.....",
    ".KYGGGGGGhK.....",
    ".KGGGGGGGhK.....",
    ".KhGhGhGhhK.....",
    "..K.K.K.K.......",
]


def towel(sway=0):
    rows = []
    for y, r in enumerate(TOWEL):
        if y >= 12 and sway:
            r = (r[1:] + '.') if sway < 0 else ('.' + r)[:16]
        rows.append(r)
    return grid(rows + ['.' * 16] * (30 - len(rows)))


def towel_frames():
    return [towel(0), towel(0), towel(1), towel(1), towel(0), towel(-1)]


def smoke_frames(n=6, w=10, h=30, cols=('s3', 'c1')):
    frames = []
    for f in range(n):
        c = Canvas(w, h)
        for i in range(4):
            y = h - 3 - ((f * 5 + i * 8) % (h - 2))
            rr = 1 + (h - y) / 12
            x = w / 2 + 2 * math.sin((y + f) / 5)
            c.disc(x, y, rr, cols[0]); c.disc(x - .5, y - .5, max(.6, rr - 1), cols[1])
        frames.append(c)
    return frames


def steam_frames():
    frames = []
    for f in range(4):
        c = Canvas(8, 12)
        for i in range(3):
            y = 11 - ((f * 3 + i * 4) % 12)
            x = 3 + int(1.5 * math.sin((y + f * 2) / 2))
            c.px(x, y, 'c0' if y > 5 else 's3')
            if y % 3 == 0:
                c.px(x + 1, y, 's3')
        frames.append(c)
    return frames


def tvsun_frames():
    out = []
    for f in range(2):
        c = Canvas(8, 4, 'e2')
        c.rect(0, 0, 8, 1, 'e3')
        c.px(2 + f, 2, 'g3'); c.px(5 - f, 1, 'k0'); c.px(6, 3, 'g3'); c.px(3, 3, 'c0')
        c.em[:, :] = True
        out.append(c)
    return out


def pumpkin():
    g = grid(S.PUMPKIN)
    # carved face (glows at night)
    for (x, y) in ((3, 4), (6, 4), (3, 6), (4, 7), (5, 7), (6, 6)):
        g.px(x, y, 'g4', em=True)
    return [g]


def bobble_frames():
    a = grid(S.BOBBLE)
    b = Canvas(a.w, a.h)
    # head bobs one pixel
    for y in range(a.h):
        for x in range(a.w):
            v = a.a[y, x]
            if v != T:
                ny = y - 1 if y < 7 else y
                b.a[ny, x] = v
    for x in range(a.w):
        if b.a[6, x] == T and a.a[7, x] != T:
            pass
    return [a, a, b, a]


def door_panel():
    c = Canvas(34, 88)
    c.rect(0, 0, 34, 88, 'w3')
    c.rect(0, 0, 34, 1, 'w4'); c.rect(33, 0, 1, 88, 'w2'); c.rect(0, 0, 1, 88, 'w4')
    for (px_, py_, pw, ph) in ((4, 5, 26, 30), (4, 41, 26, 40)):
        c.rect(px_, py_, pw, ph, 'w2'); c.rect(px_ + 1, py_ + 1, pw - 2, ph - 2, 'w3')
        c.rect(px_, py_, pw, 1, 'w1'); c.rect(px_, py_, 1, ph, 'w1'); c.rect(px_ + pw - 1, py_, 1, ph, 'w4'); c.rect(px_, py_ + ph - 1, pw, 1, 'w4')
    # number plate 117
    c.rect(9, 14, 16, 9, 'g3'); c.frame(8, 13, 18, 11, 'k0'); c.rect(9, 14, 16, 1, 'g4'); c.rect(9, 22, 16, 1, 'g2')
    c.text(11, 16, '117', 'k0')
    # handle
    c.rect(4, 44, 2, 10, 'g2'); c.rect(4, 44, 1, 10, 'g4'); c.frame(3, 43, 4, 12, 'k0')
    c.frame(0, 0, 34, 88, 'k0')
    return [c]


def dragon(W=336, H=150):
    """a long dragon made of stars, uncoiling across the sky"""
    c = Canvas(W, H)
    pts = []
    for i in range(420):
        t = i / 419
        x = 6 + t * (W - 60)
        y = H * .55 + 38 * math.sin(t * math.pi * 2.6 + .4) * (0.5 + .5 * t) - 18 * t
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        w_ = 1.5 + 4 * math.sin(math.pi * min(1, i / 419 * 1.05))
        if i % 9 == 0:
            for side in (-1, 1):
                nx = x + side * 0; ny = y + side * w_
                c.px(int(nx), int(ny), 'g4', em=True)
        if i % 18 == 4:
            c.px(int(x), int(y), 'c0', em=True)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c.px(int(x) + dx, int(y) + dy, 'g3', em=True)
        if i % 26 == 13 and i < 380:
            # dorsal spines
            c.px(int(x), int(y - w_ - 3), 'g3', em=True)
    # head at the end
    hx, hy = pts[-1]
    hx, hy = int(hx), int(hy)
    head = [
        "...Y.....Y..........",
        "....Y...Y...........",
        ".....Y.Y............",
        "....YYYYYY..........",
        "...Y......YY........",
        "..Y...W.....YY......",
        "..Y...........YYYY..",
        "..Y..............Y..",
        "...Y....YYYYYYYYY...",
        "....Y..Y............",
        ".....YY..Y.Y.Y......",
        "......YYYYYYYY......",
    ]
    for y, row in enumerate(head):
        for x, ch in enumerate(row):
            if ch == 'Y':
                c.px(hx - 3 + x, hy - 7 + y, 'g4', em=True)
            elif ch == 'W':
                c.px(hx - 3 + x, hy - 7 + y, 'c0', em=True)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    c.px(hx - 3 + x + dx, hy - 7 + y + dy, 'g3', em=True)
    # whiskers trailing back from the snout
    for k in range(14):
        c.px(hx + 14 - k // 2 + k, hy + 1 + int(2.5 * math.sin(k / 2)), 'g3', em=True) if k % 2 == 0 else None
    # claws (two small star clusters along the body)
    for t in (.3, .62):
        x, y = pts[int(t * 419)]
        for k in range(4):
            c.px(int(x) - 2 + k * 2, int(y) + 9 + (k % 2), 'g4', em=True)
    return [c]


def portrait(kind):
    c = Canvas(18, 18)
    if kind == 'evie':
        c.rect(0, 0, 18, 18, 'n3')
        mic = grid([
            "..KKKKK..",
            ".K9W9W9K.",
            "K9W9W9W9K",
            "K8989898K",
            "K9898989K",
            ".K89898K.",
            "..KGGGK..",
            "...K7K...",
            "...K7K...",
            "...K7K...",
            "..KK7KK..",
            ".KKKKKKK.",
        ])
        c.blit(mic, 5, 3)
        for x, h in ((1, 2), (2, 5), (3, 3), (14, 3), (15, 6), (16, 2)):
            c.rect(x, 8 - h // 2, 1, h, 'N')
    elif kind == 'sfrb':
        c.rect(0, 0, 18, 18, 'e2')
        c.rect(4, 2, 10, 14, 'c0'); c.frame(3, 1, 12, 16, 'k0')
        c.rect(5, 3, 3, 3, 'n4'); c.rect(9, 3, 4, 1, 'k0'); c.rect(9, 5, 3, 1, 's2')
        for y in range(8, 15, 2):
            c.rect(5, y, 8 - (y % 3), 1, 's2')
        c.rect(5, 7, 8, 1, 'r3')
    else:
        c.rect(0, 0, 18, 18, 'r2')
        c.rect(0, 13, 18, 5, 's1'); c.rect(0, 15, 18, 1, 'g3')
        car = [
            "............KK..",
            "....KKKK....KyK.",
            "..KKWWWnKKKKKKK.",
            "KKWWWWWWWWW3WWKK",
            "K33333333333333K",
            ".KK7KK.....KK7K.",
            "..K9K.......K9K.",
        ]
        g = grid(car); c.blit(g, 1, 7)
    c.em[:, :] = True
    return [c]


def puff_frames():
    out = []
    for f in range(3):
        c = Canvas(20, 12)
        for i in range(10):
            a = i * 36 + f * 7
            r = 3 + f * 3
            x = 10 + r * math.cos(math.radians(a)); y = 8 - abs(r * .8 * math.sin(math.radians(a)))
            c.rect(int(x), int(y), 2, 1, 'g3' if i % 2 else 'g4')
        out.append(c)
    return out


def corgi_walk():
    return S.corgi_walk_frames()


ALL = {
    'planet': planet, 'towel': towel_frames, 'smoke': smoke_frames, 'steam': steam_frames,
    'tvsun': tvsun_frames, 'pumpkin': pumpkin, 'bobble': bobble_frames, 'door': door_panel,
    'dragon': dragon,
    'raven': lambda: [grid(f) for f in S.RAVEN], 'eagle': lambda: [grid(f) for f in S.EAGLE],
    'fuzz': lambda: [grid(f) for f in S.FUZZ], 'hilt': lambda: [grid(S.HILT)], 'hearth': lambda: [grid(S.HEARTH, em_chars='56W')],
    'corgi': S.corgi_sleep_frames, 'corgiwalk': corgi_walk, 'corgisit': lambda: [S.corgi_sit()],
    'box': lambda: [S.taped_box()], 'bracket': lambda: [grid(S.BRACKET)], 'coin': lambda: [grid(f) for f in S.COIN],
    'hit': lambda: [grid(S.HITMARKER)], 'diver': lambda: [grid(S.DIVER[0])], 'puff': puff_frames,
    'p1': lambda: [S.p1token()], 'pt-evie': lambda: portrait('evie'), 'pt-sfrb': lambda: portrait('sfrb'), 'pt-feb': lambda: portrait('feb'),
    'star': lambda: [grid(f) for f in S.STAR],
}
for i in range(1, 8):
    ALL['orb%d' % i] = (lambda i=i: [S.orb(i)])
for k in ['crash', 'ride', 'hihat', 'tom1', 'tom2', 'kick', 'snare', 'floortom']:
    ALL['kit-' + k] = (lambda k=k: [S.drum_kit()[k][0]])


def title_racing():
    """still title screen for the artboard's CRT: a hill track at golden hour"""
    import scene as SC
    from px import Canvas, grid
    W, H = 160, 100
    c = Canvas(W, H)
    SC.band_sky(c, 0, 62, 0, W, [(0, 'n4'), (20, 'p3'), (40, 'o3'), (62, 'g4')])
    c.disc(118, 52, 9, 'g4'); c.disc(118, 52, 6, 'c0')
    for x in range(W):
        y = 50 + int(4 * math.sin(x / 13) + 2 * math.sin(x / 5))
        c.rect(x, y, 1, H - y, 'p1')
    for x in range(W):
        y = 58 + int(3 * math.sin(x / 17 + 2))
        c.rect(x, y, 1, H - y, 'e2'); c.px(x, y, 'e3')
    # track: a wide S curve with kerbs
    for y in range(62, H):
        t = (y - 62) / (H - 62)
        cx = 80 + 40 * math.sin(t * 3.2 + .3)
        w = 6 + 50 * t
        a, b = int(cx - w / 2), int(cx + w / 2)
        c.rect(a, y, b - a, 1, 's1')
        for k in (a - 2, b):
            c.rect(k, y, 2, 1, 'r3' if (y // 3) % 2 else 'c0')
        if y % 6 < 3 and t > .2:
            c.px(int(cx), y, 'c1')
    # trees
    for (tx, ty) in ((14, 66), (30, 72), (140, 70), (150, 80), (8, 84)):
        c.rect(tx, ty, 2, 4, 'w1'); c.disc(tx + 1, ty - 2, 3, 'e1'); c.px(tx + 2, ty - 3, 'e2')
    car = grid([
        "............KK..",
        "....KKKK....KyK.",
        "..KKWWWnKKKKKKK.",
        "KKWWWWWWWWW3WWKK",
        "K33333333333333K",
        ".KK7KK.....KK7K.",
        "..K9K.......K9K.",
    ])
    c.blit(car, 70, 84)
    return c
