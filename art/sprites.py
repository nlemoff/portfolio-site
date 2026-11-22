"""Hand-drawn sprites for R5-House (character grids + small procedural helpers).
Legend: see px.LEGEND. K = ink outline. Light comes from upper right (moon/window)
and the desk lamp, so most objects carry their highlight on the right/top.
"""
from px import Canvas, grid, strip, C, T
import numpy as np

# ------------------------------------------------------------------ corgi
CORGI_SLEEP = [
    "........................K...K....",
    ".......................KoK.KUK...",
    ".......................KooKKOUK..",
    "........KKKKKKKKKKKKKKKKOOOOOOK..",
    "......KKOOOOOOOOOOOOOOOOOOOOOOOK.",
    ".....KUUUUUOOOOOOOOOOOOOOOOKKOOOK",
    "....KUOOOOOOOOOOOOOOOOOOOOOOOOWWK",
    "...KWUOOOOOOOOOOOOOOOOOOOOOOWWWWK",
    "..KWWOOOOOOOOOOOOOOOOOOOOOOWWWKKK",
    "..KWWOOOOOOOoooooooooOOOOOWWWWK..",
    ".KWWWOOOoooooooooooooooOOWWWWWWK.",
    ".KWWWWoooPPPPPPPPPPPPPPWWWWWWWWWK",
    "..KPPPPPPPKKKKKKKKKKKKKPPPPPPPPK.",
    "...KKKKKKK............KKKKKKKKK..",
]

CORGI_STAND = [  # facing right, 4 leg frames built below
    "........................K..K......",
    ".......................KoKKUK.....",
    ".......................KooKOUK....",
    ".......................KOOOOOOK...",
    "..KK...................KOOOOKOOK..",
    ".KWWK..................KOOOOOOWWKK",
    ".KWUOKKKKKKKKKKKKKKKKKKOOOOOWWWWWK",
    "..KUOOOOOOOOOOOOOOOOOOOOOOWWWWKKK.",
    "..KOOOOOOOOOOOOOOOOOOOOOOOWWWK....",
    "..KOOOOOOOOOOOOOOOOOOOOOOWWWWK....",
    "..KWOOOooooooooooooooOOOWWWWWK....",
    "..KWWWoooPPPPPPPPPPPPPPPWWWWK.....",
    "...KWWPPKKKKKKKKKKKKKKKPPWWK......",
]
LEGS = [  # 4-frame walk cycle under the body (rows 13-15), x offsets for back & front legs
    ["...KWK.KWK.............KWK.KWK...", "...KWK.KWK.............KWK.KWK...", "...KK..KK..............KK..KK...."],
    ["....KWKKWK..............KWKKWK...", "....KWKKWK..............KWKKWK...", "....KK.KK................KK.KK..."],
    [".....KWWK................KWWK....", ".....KWWK................KWWK....", ".....KKKK................KKKK...."],
    ["....KWKKWK..............KWKKWK...", "...KWK..KWK............KWK..KWK..", "...KK....KK............KK....KK.."],
]
CORGI_SIT = [
    "..............K..K..",
    ".............KoKKUK.",
    ".............KooKOUK",
    ".............KOOOOOK",
    ".............KOOKOOK",
    ".............KOOOOWWK",
    "......KKKKKKKKOOOWWWK",
    "....KKOOOOOOOOOOWWKK.",
    "...KUOOOOOOOOOOOWWK..",
    "..KUOOOOOOOOOOOWWWK..",
    "..KOOOOOOOOOOOOWWWK..",
    ".KWOOOOooooooOOWWWK..",
    ".KWWOoooooooooOWWWK..",
    ".KWWWPPPPPPPPPWKWWK..",
    "..KKKKKKKKKKKKKKKKK..",
]


def corgi_sleep_frames():
    a = grid(CORGI_SLEEP)
    b = a.copy()
    # breathe: raise the back by one pixel between x=7..21
    for x in range(7, 22):
        col = b.a[:, x]
        ys = np.where(col != T)[0]
        if len(ys) == 0:
            continue
        top = ys[0]
        if top >= 1:
            b.a[top - 1, x] = C('k0')
            b.a[top, x] = b.a[top + 2, x] if top + 2 < b.h else b.a[top, x]
    return [a, b]


def corgi_walk_frames():
    frames = []
    for legs in LEGS:
        g = grid(CORGI_STAND + legs)
        frames.append(g)
    return frames


def corgi_sit():
    return grid(CORGI_SIT)


# ------------------------------------------------------------------ birds
RAVEN = [
    [
        ".....KKKK.......",
        "....K1255K......",
        "...K11K925K.....",
        "KKKK111K225K....",
        "K877K111122K....",
        ".KKKK1111222K...",
        "....K11111235K..",
        "....K111112345K.",
        ".....K111112335K",
        "......K1111122K.",
        ".......KK11112K.",
        ".........K911K..",
        "........KK.KK...",
    ],
    [
        "................",
        ".....KKKK.......",
        "....K1221K......",
        "..KK11K921K.....",
        "KK77K11K221K....",
        ".KKK1111122K....",
        "....K1111222K...",
        "....K11111232K..",
        ".....K111112332K",
        "......K1111122K.",
        ".......KK11112K.",
        ".........K911K..",
        "........KK.KK...",
    ],
]

EAGLE = [
    [
        "....KKK......",
        "...KWWWK.....",
        "..KWWKWWK....",
        "KGGWWWWWK....",
        ".KKKWWWWK....",
        "...KcWWccK...",
        "..KccbcccbK..",
        "..Kcbcccbcc K",
        "..KbccbccbcK.",
        "...KbcbcbcbK.",
        "....KbcbbbK..",
        ".....KbbbbbK.",
        "....KGKKGKKK.",
    ],
    [
        "....KKK......",
        "...KWWWK.....",
        "..KWWKWWK....",
        "KGGWWWWWK....",
        ".KKKWWWWK....",
        "..KcccWWcK...",
        ".KccbcccbcK..",
        "Kccbcccbccc K",
        ".KbccbccbcK..",
        "...KbcbcbcbK.",
        "....KbcbbbK..",
        ".....KbbbbbK.",
        "....KGKKGKKK.",
    ],
]

# hooded figure, swan dive (white robe, red sash)
DIVER = [
    [
        "......KK......",
        "......K9K.....",
        ".....KWWK.....",
        ".....KW9K.....",
        ".....KWWK.....",
        "....KRTRK.....",
        "KKK.KWWWK.KKK.",
        "K9WKWWWWWKWW9K",
        ".KKKWW9WWKKKK.",
        "....KWWWK.....",
        "....KW1WK.....",
        "....K9W9K.....",
        ".....K9K......",
        "......K.......",
    ],
]

# ------------------------------------------------------------------ small objects
FUZZ = [
    [
        "...e.d...",
        ".deddedd.",
        "edeeddede",
        "ddeddeddd",
        "cddcddcdd",
        ".cdccdcc.",
        "..c.c.c..",
    ],
    [
        "..d..e.d.",
        ".deddedd.",
        "dedeeddee",
        "ddeddeddd",
        "cddcddcdd",
        ".cdccdcc.",
        "..c.c.c..",
    ],
]

HILT = [
    "...............",
    "K9WW9K8K8K8K99KK",
    "K899K7K7K7K7T8KK",
    "K78877777777788K",
    ".KKKKKKKKKKKKKK.",
]
HILT = [
    ".KKKKKKKKKKKKKK.",
    "KWW99K8K8K8K99WK",
    "K9988K7K7K7KT89K",
    "K7887777777778 8K".replace(' ', '8'),
    ".KKKKKKKKKKKKKK.",
]

HEARTH = [
    "..KKKK..",
    ".K9889K.",
    "K98558 9K".replace(' ', ''),
    "K8565889K"[:8],
    "K8855887",
    ".K8888K.",
    "..KKKK..",
]
HEARTH = [
    "..KKKKK..",
    ".K99988K.",
    "K9986888K",
    "K886W688K",
    "K8886887K",
    ".K87787K.",
    "..KKKKK..",
]

TROPHY = [  # football on a tapered stand
    "...KK..",
    "..KYGK.",
    ".KYGhGK",
    ".KGhGhK",
    "KGhGhyK",
    ".KhGyK.",
    "..KhK..",
    "..KGK..",
    "..KGK..",
    ".KYGhK.",
    ".KGhyK.",
    "KYGGhyK",
    "KKKKKKK",
]

BOOK = [
    "KKKK",
    "KGGK",
    "KRTK",
    "KRTK",
    "KRRK",
    "KGGK",
    "KRTK",
    "KRTK",
    "KRTK",
    "KRTK",
    "KRTK",
    "KRTK",
    "KRTK",
    "KRRK",
    "KGGK",
    "KRTK",
    "KRRK",
    "KGGK",
    "KKKK",
]

BEAR = [
    ".KK...KK..",
    "KdcK.KdcK.",
    "KcKKKKKcK.",
    ".KcdddddK.",
    "KcdKddKddK",
    "KcddeeedcK",
    ".KcdeKedK.",
    "..KKcccKK.",
    ".KcdddddcK",
    "KcdcdddddcK",
    "KccdedeccK.",
    ".KcKKKKcK..",
    "KeeK..KeeK.",
    ".KK....KK..",
]

BOBBLE = [
    "..KKKK..",
    ".K1KG1K.",
    "K11G111K",
    "K1KG1918",
    "K11G9Q9K",
    ".KK9QK9K",
    "..KKKK..",
    "..K11K..",
    ".K1GG1K.",
    ".K1GG1K.",
    "..KGGK..",
    ".KGKKGK.",
    "KKKKKKKK",
    "KGGGGGGK",
    "KKKKKKKK",
]
BOBBLE = [
    "..KKKKK..",
    ".K11G11K.",
    "K111G1119K",
    "K111G1K98K",
    "K11KG9Q9K.",
    ".K119QQ9K.",
    "..KKKKKK..",
    "...K11K...",
    "..K1GG1K..",
    ".K11GG11K.",
    "..KGGGGK..",
    "..KGKKGK..",
    ".KKKKKKKK.",
    ".K1GGGG1K.",
    ".KKKKKKKK.",
]

CAPSJAR = [
    ".K8888K.",
    ".K9999K.",
    "K6....6K",
    "K6R9GW5K",
    "KG9TRG95",
    "K9WRG9R5",
    "KRG9WRG5",
    "KGTRG9W5",
    "K6R9GTRK",
    ".K5555K.",
]

PENCUP = [
    "..e....e..",
    "..dK..Ke..",
    "...d..d...",
    "...e..d.Y.",
    "...d.d..G.",
    "...e.d..G.",
    "....dd..G.",
    "....de.G..",
    "....ed.G..",
    "..KKKKKKK.",
    "..K89898K.",
    "..K98989K.",
    "..K89898K.",
    "..K98989K.",
    "..KKKKKKK.",
]

MUG = [
    ".KKKKK..",
    "KWWWWPK.",
    "KGGGGGKK",
    "KWWWWPK.K",
    "KWWWWPKK",
    "KPPPPQK.",
    ".KKKKK..",
]
MUG = [
    ".KKKKKK.",
    "KWWWWWPKK",
    "KGGGGGGK.K",
    "KWWWWWPK.K",
    "KWWWWWPKK.",
    "KPWWWPQK..",
    ".KKKKKK...",
]

PLANT = [
    "...J.L..",
    ".LJ.LJ..",
    "..LJJ.L.",
    ".JLJLJJ.",
    "..JJLJ..",
    ".KKKKKK.",
    ".KoOOoK.",
    "..KOOK..",
    "..KKKK..",
]

PUMPKIN = [
    "....Jj....",
    "....jJ....",
    ".KKKKKKKK.",
    "KoOUOOUOoK",
    "KOOGOOGOOK",
    "KOOOOOOOOK",
    "KOGOGGOGOK",
    "KoOGOGOOoK",
    ".KoooooooK",
    "..KKKKKK..",
]

HAY = [
    "..KKKKKKKKKKKKKKKKKKKKKK..",
    ".KYGYGGYGYGbGYGGYGYGYGGYK.",
    "KGYGhGYGhGGbGhGYGhGYGhGGYK",
    "KGhGYGhGYGhbYGhGYGhGYhGhGK",
    "KhGhGhGhGhGbhGhGhGhGhGhGhK",
    "KGYGhGYGhGYbhGYGhGYGhGYGhK",
    "KhGhGhGhGhGbGhGhGhGhGhGhGK",
    "KGhGYGhGYGhbYGhGYGhGYhGhGK",
    "KhGhGhGhGhGbhGhGhGhGhGhGyK",
    "KyhyhyhyhyhbhyhyhyhyhyhyyK",
    ".KyyyyyyyyybyyyyyyyyyyyyK.",
    "..KKKKKKKKKKKKKKKKKKKKKK..",
]

ORB_DOTS = {
    1: [(4, 4)], 2: [(3, 3), (5, 5)], 3: [(3, 3), (4, 4), (5, 5)], 4: [(3, 3), (5, 3), (3, 5), (5, 5)],
    5: [(3, 3), (5, 3), (4, 4), (3, 5), (5, 5)], 6: [(3, 2), (5, 2), (3, 4), (5, 4), (3, 6), (5, 6)],
    7: [(3, 2), (5, 2), (2, 4), (4, 4), (6, 4), (3, 6), (5, 6)],
}


def orb(n):
    c = Canvas(9, 9)
    c.disc(4.5, 4.5, 4.5, 'k0')
    c.disc(4.5, 4.5, 3.6, 'o2')
    c.px(2, 2, 'o3'); c.px(3, 2, 'o3'); c.px(2, 3, 'o3'); c.px(2, 5, 'o1'); c.px(5, 7, 'o1'); c.px(6, 6, 'o1'); c.px(4, 7, 'o1')
    for (x, y) in ORB_DOTS[n]:
        c.px(x, y, 'r2')
    c.px(6, 2, 'c0')
    return c


HITMARKER = [
    "K.......K",
    ".W.....W.",
    "..W...W..",
    ".........",
    ".........",
    ".........",
    "..W...W..",
    ".W.....W.",
    "K.......K",
]

COIN = [
    [".KKKK.", "KYGGhK", "KGYhGK", "KGYhGK", "KGYhGK", "KGYhGK", "KhGGyK", ".KKKK."],
    ["..KK..", ".KYGK.", ".KGhK.", ".KGhK.", ".KGhK.", ".KGhK.", ".KhyK.", "..KK.."],
    ["..K...", "..KK..", "..KK..", "..KK..", "..KK..", "..KK..", "..KK..", "..K..."],
    ["..KK..", ".KGhK.", ".KhGK.", ".KhGK.", ".KhGK.", ".KhGK.", ".KyhK.", "..KK.."],
]

BRACKET = [
    "KKKKKKKK",
    "K999998K",
    "K98KKKKK",
    "K98K....",
    "K98K....",
    "K8K.....",
    "KK......",
]

STAR = [
    [".....", ".....", "..Y..", ".....", "....."],
    [".....", "..Y..", ".YWY.", "..Y..", "....."],
    ["..Y..", "..Y..", "YYWYY", "..Y..", "..Y.."],
    [".....", "..Y..", ".YWY.", "..Y..", "....."],
]

P1TOKEN = [
    "..KKKKK..",
    ".KTTTTTK.",
    "KTWWTWTTK",
    "KTWTWWTTK",
    "KTWWTWTTK",
    "KTWTTWTTK",
    ".KTWTWWK.",
    "..KKKKK..",
]


def p1token():
    c = Canvas(11, 11)
    c.disc(5.5, 5.5, 5.5, 'k0')
    c.disc(5.5, 5.5, 4.6, 'r3')
    c.px(3, 2, 'p3'); c.px(2, 3, 'p3')
    c.text(2, 3, 'P', 'c0')
    c.text(6, 3, '1', 'c0')
    c.px(7, 9, 'r2'); c.px(8, 8, 'r2')
    return c


# ------------------------------------------------------------------ hanging clothes
ROBE = [  # white assassin coat on a hanger: folded hood, red cape on one shoulder, belt + red sash, split tails
    ".........KK.........",
    "........K..K........",
    "...........K........",
    ".....KKKKKKKKKK.....",
    "....KW99WWWW99WK....",
    "...KWW9WWWWWW9WWK...",
    "..KWWWW9KKKK9WWWWK..",
    ".KRRWWWWK11KWWWWWWK.",
    "KRRTRWWWK11KWWWW9WWK",
    "KRTTRWW9WK1KWW9WWW9K",
    "KRTTRW9WWK1KW9WWWW9K",
    "KRTTRW9WWK1KW9WWWW9K",
    "KRTTRW9WWK1KW9WWW9WK",
    "KRTTRW9WWK1KW9WWW9WK",
    "KRRTRW9WWK1KW9WWW9WK",
    "KKRRRW9WWK1KW9WWW9WK",
    ".KKRRWWWWK1KWWWWW9WK",
    ".KW9KbbbbbbbbbbbK9WK",
    ".KW9KTTTTTTTTTTRK9WK",
    ".KW9KRRRRTRRRRRrK9WK",
    ".KW9KbbbbbGbbbbbK9WK",
    ".K9WKWW9WK1KWW9WKW9K",
    ".KWWKWW9WKRKWW9WKWWK",
    ".KK9KWW9WKRKWW9WK9KK",
    "..KKKWW9WKTRKW9WKKK.",
    "....KWW9WKTRKW9WK...",
    "....KW9WWKTRKWW9K...",
    "....KW9WKRRTRKW9K...",
    "....KW9WKR..RKW9K...",
    "....KW9WKR..RKW9K...",
    "....KW9WKR..RKWW9K..",
    "...KWW9WK....KWW9K..",
    "...KW99WK....KW99K..",
    "...KWW9WK....KWW9K..",
    "...KTRTRK....KRTRK..",
    "...KKKKK......KKKK..",
]

JACKET = [  # black military jacket with white braid, on a hanger
    "........KK........",
    ".......K99K.......",
    ".........K........",
    "......KKKKKK......",
    "....KK9KK2K9KK....",
    "..KKYY1K22K1YYKK..",
    ".KYWYW1K11K1WYWYK.",
    ".KYKYK1KWWK1KYKYK.",
    ".K11111K1K11111 1K".replace(' ', '1'),
    ".K1111WWWKWWW1111K",
    ".K111W111K111W111K",
    ".K1111WWWKWWW1111K",
    ".K111K111K111K111K",
    ".K1111WWWKWWW1111K",
    ".K111W111K111W111K",
    ".K1111WWWKWWW1111K",
    ".K111K111K111K111K",
    ".K1111WWWKWWW1111K",
    ".K111W111K111W111K",
    ".K1211WWWKWWW1121K",
    ".K121K111K1112121K",
    ".K121K1W1K1W1K121K",
    ".K121K111K111K121K",
    ".K121K111K111K121K",
    ".K121K111K111K121K",
    ".K12KK1W1K1W1KK21K",
    ".K12KK111K111KK21K",
    ".KWWKK111K111KKWWK",
    ".KKKKK111K111KKKKK",
    ".....K111K111K....",
    ".....K1W1K1W1K....",
    ".....K111K111K....",
    ".....K112K211K....",
    ".....KKKKKKKKK....",
]

HOODIE = [  # dropped on the floor: hood (open, dark inside) on the left, sleeve flung right, pocket, drawstrings
    "..KKKKK...................",
    ".K34443K...KKKKKKKKKK.....",
    "K3422243KKK3444444443K....",
    "K342112433333333333344KKK.",
    "K3421124W3W3333333333334K.",
    ".K34224W33W333KKKKKK3343K.",
    "..KK444W33W33K222222K3KK..",
    ".K333334W33W3K222222K3K...",
    "K23333333W3W3KKKKKKKK33K..",
    ".KK22222222222222222222K..",
    "...KKKKKKKKKKKKKKKKKKKK...",
]

# ------------------------------------------------------------------ garage
GUITAR = [
    ".....KKK......",
    "....K999K.....",
    "....K9W9K.....",
    "....K999K.....",
    "....K9W9K.....",
    ".....KKK......",
    ".....KedK.....",
    ".....KedK.....",
    ".....KYdK.....",
    ".....KedK.....",
    ".....KedK.....",
    ".....KYdK.....",
    ".....KedK.....",
    ".....KedK.....",
    ".....KYdK.....",
    ".....KedK.....",
    ".....KedK.....",
    "..KK.KedK.KK..",
    ".KxxKKedKKxxK.",
    ".KxxxKedKxxxK.",
    ".KxxxxKKxxxxK.",
    "..KxxxWWWxxxK.",
    "..KxxxKKKxxK..",
    ".KxxxxxxxxxxK.",
    "KxxxxxWWWxxxxK",
    "KxxxxxKKKxxxxK",
    "KxxxxxxxxxxxxK",
    "KxxxxxK9KxxxxK",
    ".KxxxxxxxxxxK.",
    ".KxxxxxxxxxxK.",
    "..KxxxxxxxxK..",
    "...KKKKKKKK...",
]

SHIPBOTTLE = [
    "..........................",
    "......KKKKKKKKKKKKKKKK....",
    ".....K6.......5.....6K....",
    "....K6....K..PK..K...5KKKK",
    "...K5.....PK.PPK.PK..5KccK",
    "...K5....PPK.PPK.PPK.5KccK",
    "...K5....PPK.PPK.PPK.5KccK",
    "...K5..KKKKKKKKKKKKKK5KKKK",
    "...K5...KcccdccccdcK.5K...",
    "...K5....KKKKKKKKKK..5K...",
    "....K5555555555555555K....",
    ".....KKKKKKKKKKKKKKKKK....",
    "....KdK............KdK....",
    "...KKKKKKKKKKKKKKKKKKKK...",
]

TV_SMALL = [
    "....K....K....",
    ".....K..K.....",
    "......KK......",
    ".KKKKKKKKKKKK.",
    "K877777777778K",
    "K7KKKKKKKKKK7K",
    "K7K11111111K7K",
    "K7K11111111K7K",
    "K7K11111111K7K",
    "K7K11111111K7K",
    "K7KKKKKKKKKK7K",
    "K7777777798T7K",
    ".KKKKKKKKKKKK.",
    "..KK......KK..",
]

PLATE = None  # procedural


def taped_box():
    c = Canvas(28, 22)
    # trophy corner poking out of the top flap
    for y, row in enumerate([
        "..........KK",
        ".........KYGK",
        "........KYGhK",
        "........KGhK.",
    ]):
        for x, ch in enumerate(row):
            if ch != '.':
                c.px(x + 8, y, {'K': 'k0', 'Y': 'g4', 'G': 'g3', 'h': 'g2'}[ch])
    # box body
    c.rect(1, 4, 26, 17, 'w4')
    c.frame(0, 3, 28, 19, 'k0')
    c.rect(1, 4, 26, 3, 'w3')          # top flap shadow line
    c.rect(1, 4, 12, 2, 'c2')          # flap highlight
    c.rect(1, 18, 26, 3, 'w3')
    for y in range(8, 18):
        c.px(26, y, 'w3')
    # tape: across top and down the middle
    c.rect(1, 9, 26, 3, 'c2')
    c.rect(12, 4, 4, 17, 'c2')
    c.rect(1, 9, 26, 1, 'c1'); c.rect(12, 4, 1, 17, 'c1')
    c.px(0, 10, 'c2'); c.px(27, 10, 'c2')
    # dust (dither speckles on the top)
    for x in range(1, 27, 2):
        c.px(x, 4, 's3' if x % 4 == 1 else 'c1')
    for x in (3, 7, 18, 22):
        c.px(x, 5, 's3')
    # a scrawl on the side
    c.line(4, 15, 9, 15, 'w2'); c.line(18, 15, 23, 14, 'w2')
    return c


# ------------------------------------------------------------------ helpers for procedural props
def drum_kit():
    """returns dict of piece -> (canvas, x, y) within an 88x50 kit box"""
    P = {}

    def cymbal(w, tilt=0):
        c = Canvas(w, 4)
        c.rect(1, 1, w - 2, 2, 'g3')
        c.rect(0, 2, w, 1, 'g2')
        c.rect(1, 1, w // 3, 1, 'g4')
        c.rect(w // 2 - 1, 0, 3, 1, 'g2')
        c.rect(w // 2, 0, 1, 1, 'k0')
        c.rect(1, 3, w - 2, 1, 'k0')
        c.px(0, 2, 'k0'); c.px(w - 1, 2, 'k0')
        return c

    def tom(w, h, legs=False):
        c = Canvas(w, h + (8 if legs else 0))
        # top head (ellipse) + shell
        c.rect(1, 2, w - 2, h - 3, 'n3')
        c.ellipse(w / 2, 2.5, w / 2 - .5, 2.2, 'c1')
        c.rect(2, 2, w - 4, 1, 'c0')
        # hoops
        c.rect(0, 4, w, 1, 's3'); c.rect(0, h - 2, w, 1, 's3')
        # shell shading: sparkle
        for x in range(1, w - 1):
            for y in range(5, h - 2):
                if x < 3:
                    c.px(x, y, 'n2')
                elif x > w - 4:
                    c.px(x, y, 'n4')
                if (x * 7 + y * 3) % 11 == 0:
                    c.px(x, y, 'n5')
        # lugs
        for x in range(3, w - 2, 4):
            c.rect(x, 6, 1, h - 9, 's2')
        c.outline('k0')
        if legs:
            c.line(2, h, 0, h + 7, 's2'); c.line(w - 3, h, w - 1, h + 7, 's2')
            c.line(w // 2, h, w // 2, h + 7, 's3')
        return c

    def outlined(c):
        c2 = Canvas(c.w + 2, c.h + 2)
        c2.blit(c, 1, 1)
        c2.outline('k0')
        return c2

    # stands (baked separately as 'hw')
    hw = Canvas(88, 50)
    # hi-hat stand (left)
    hw.rect(9, 14, 1, 33, 's3'); hw.line(9, 44, 4, 48, 's2'); hw.line(9, 44, 14, 48, 's2'); hw.rect(8, 44, 3, 1, 's2')
    # crash boom (left high)
    hw.line(20, 10, 22, 30, 's2'); hw.line(22, 30, 22, 47, 's3'); hw.line(22, 44, 18, 48, 's2'); hw.line(22, 44, 26, 48, 's2')
    # ride boom (right high)
    hw.line(70, 9, 67, 30, 's2'); hw.line(67, 30, 67, 36, 's3')
    # snare stand
    hw.line(24, 36, 20, 48, 's2'); hw.line(24, 36, 28, 48, 's2'); hw.rect(24, 32, 1, 5, 's3')
    # throne (behind the kick, peeks out)
    hw.rect(40, 22, 10, 3, 'k0'); hw.rect(41, 22, 8, 2, 's1')
    # pedal + spurs
    hw.rect(42, 46, 4, 2, 's2'); hw.line(31, 44, 28, 48, 's3'); hw.line(57, 44, 60, 48, 's3')
    P['hw'] = (hw, 0, 0)

    P['crash'] = (cymbal(18), 12, 8)
    P['ride'] = (cymbal(20), 60, 7)
    P['hihat'] = (None, 0, 12)
    hh = Canvas(16, 6)
    top = cymbal(16); hh.blit(top, 0, 0); hh.blit(top, 0, 3)
    P['hihat'] = (hh, 2, 12)
    P['tom1'] = (tom(11, 9), 33, 14)
    P['tom2'] = (tom(11, 9), 45, 14)
    # kick drum front view: circle
    k = Canvas(28, 28)
    k.disc(14, 14, 14, 'k0'); k.disc(14, 14, 13, 's3'); k.disc(14, 14, 12, 'k0'); k.disc(14, 14, 11, 'c1')
    k.disc(14, 14, 8, 'c0'); k.disc(14, 14, 7, 'c1')
    # gold ring + port hole
    for a in range(0, 360, 6):
        import math
        x = 14 + 9.5 * math.cos(math.radians(a)); y = 14 + 9.5 * math.sin(math.radians(a))
        k.px(int(x), int(y), 'g3')
    k.disc(18.5, 18.5, 2.2, 'k0')
    k.rect(3, 13, 1, 3, 's2'); k.rect(24, 13, 1, 3, 's2'); k.rect(13, 2, 3, 1, 's2'); k.rect(13, 25, 3, 1, 's2')
    P['kick'] = (k, 30, 21)
    sn = Canvas(16, 9)
    sn.rect(1, 2, 14, 5, 's3'); sn.ellipse(8, 2.5, 7.5, 2, 'c0'); sn.rect(1, 4, 14, 1, 's2'); sn.rect(1, 6, 14, 1, 's2')
    for x in range(2, 15, 3):
        sn.rect(x, 4, 1, 3, 's1')
    sn.rect(12, 3, 2, 3, 'c0')
    sn.outline('k0')
    P['snare'] = (outlined(sn) if False else sn, 17, 27)
    ft = tom(16, 18, legs=True)
    # setlist taped to the floor tom: tempos only
    from px import FONT34
    paper = Canvas(13, 17)
    paper.rect(0, 0, 13, 17, 'c0'); paper.frame(0, 0, 13, 17, 'k0')
    paper.rect(4, 0, 5, 1, 'c2')  # tape
    paper.rect(1, 16, 11, 1, 'c2')
    for i, t in enumerate(['170', '182', '96', '148']):
        paper.text(2 if len(t) == 3 else 4, 2 + i * 5 - (0), t, 'k0' if t != '182' else 'r2', font=FONT34) if i < 3 else paper.text(2, 2 + i * 5 - 1, t, 'k0', font=FONT34)
    ft.blit(paper, 2, 5)
    P['floortom'] = (ft, 60, 24)
    return P


def stick_figure_placeholder():
    return grid(["K"])


def guitar():
    """striped body: red base, white + black diagonal stripes"""
    g = Canvas(14, len(GUITAR))
    for y, row in enumerate(GUITAR):
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            if ch == 'x':
                k = (x * 2 + y * 3) % 13
                col = 'k0' if k in (0, 1) else ('c0' if k in (6, 7) else ('r3' if (x + y) % 5 else 'r2'))
                g.px(x, y, col)
            else:
                from px import LEGEND
                g.px(x, y, LEGEND[ch])
    return g


# ------------------------------------------------------------------ work logos (pixel takes on each mark)
LOGO_W, LOGO_H = 15, 11
LOGOS = {
    'judgment': [  # two posts with feet kicked outward
        "....TT.TT....",
        "....TT.TT....",
        "....TT.TT....",
        "....TT.TT....",
        "....TT.TT....",
        "....TT.TT....",
        "....T...T....",
        "TTTTT...TTTTT",
        "TTTT.....TTTT",
    ],
    'fullproof': [  # the fingerprint O
        "...OOOOO...",
        ".OOOOOOOOO.",
        ".OO.....OO.",
        "OO..ooo..OO",
        "OO.o...o.OO",
        "OO.o.o.o.OO",
        "OO.o.o.o.OO",
        "OO...o.o.OO",
        ".OO....oOO.",
        ".OOOOOOOOO.",
        "...OOOOO...",
    ],
    'feb': [  # one slanted slab, blue over gold
        "....4444.",
        "...4444..",
        "..4444...",
        ".4444GGGG",
        "4444GGGGh",
        "...GGGGh.",
        "..GGGGh..",
        ".hhhhh...",
    ],
    'nist': [
        "K..K.K..KKK.KKK",
        "KK.K.K.K.....K.",
        "KK.K.K.K.....K.",
        "K.KK.K..KK...K.",
        "K.KK.K....K..K.",
        "K..K.K....K..K.",
        "K..K.K.KKK...K.",
    ],
    'berkeleylab': [  # the dome and the tower, on navy
        ".222222222222.",
        "22222222222WW2",
        "2222WWWW222WW2",
        "222W2222W22WW2",
        "22W222222W2WW2",
        "2WWWWWWWWWWWW2",
        "2W2W2W2W2W2WW2",
        "2WWWWWWWWWWWW2",
        "22222222222222",
        ".222222222222.",
    ],
}


def _mojo():
    """two half rings: the upper one cyan, the lower one ink, offset so they make a wave"""
    import math
    from px import LEGEND
    c = Canvas(13, 8)
    for y in range(8):
        for x in range(13):
            for cx, cy, top, col in ((4.5, 4.0, True, 'n'), (8.5, 3.0, False, 'K')):
                d = math.hypot(x + .5 - cx, y + .5 - cy)
                if 2.6 <= d <= 4.6 and ((y + .5 <= cy) if top else (y + .5 >= cy)):
                    c.px(x, y, LEGEND[col])
    return c


def logo(name):
    m = _mojo() if name == 'mojo' else grid(LOGOS[name])
    out = Canvas(max(LOGO_W, m.w), LOGO_H)
    out.blit(m, (out.w - m.w) // 2, (LOGO_H - m.h) // 2)
    return out
