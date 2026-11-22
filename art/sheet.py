import sys
from px import Canvas, grid
import sprites as S
from PIL import Image
items = []
items += [('cs', f) for f in S.corgi_sleep_frames()]
items += [('cw', f) for f in S.corgi_walk_frames()]
items += [('sit', S.corgi_sit())]
items += [('raven', grid(r)) for r in S.RAVEN]
items += [('eagle', grid(r)) for r in S.EAGLE]
items += [('diver', grid(S.DIVER[0]))]
items += [('fuzz', grid(S.FUZZ[0])), ('hilt', grid(S.HILT)), ('hearth', grid(S.HEARTH)), ('trophy', grid(S.TROPHY)), ('book', grid(S.BOOK)), ('bear', grid(S.BEAR)), ('bobble', grid(S.BOBBLE)), ('caps', grid(S.CAPSJAR)), ('pencup', grid(S.PENCUP)), ('mug', grid(S.MUG)), ('plant', grid(S.PLANT)), ('pumpkin', grid(S.PUMPKIN)), ('hay', grid(S.HAY))]
items += [('orb%d'%i, S.orb(i)) for i in range(1,8)]
items += [('hit', grid(S.HITMARKER)), ('coin', grid(S.COIN[0])), ('bracket', grid(S.BRACKET)), ('p1', S.p1token())]
items += [('robe', grid(S.ROBE)), ('jacket', grid(S.JACKET)), ('hoodie', grid(S.HOODIE)), ('guitar', S.guitar()), ('ship', grid(S.SHIPBOTTLE)), ('tv', grid(S.TV_SMALL)), ('box', S.taped_box())]
kit = S.drum_kit(); kc = Canvas(88, 50)
for k in ['hw','crash','ride','hihat','tom1','tom2','kick','snare','floortom']:
    c,x,y = kit[k]; kc.blit(c,x,y)
items += [('kit', kc)]
extra = sys.argv[1:] 
Z = 6
W = 1400
x = y = 8; rowh = 0
pos = []
for name, c in items:
    if x + c.w*Z > W: x = 8; y += rowh + 12; rowh = 0
    pos.append((x, y, c)); x += c.w*Z + 12; rowh = max(rowh, c.h*Z)
H = y + rowh + 8
img = Image.new('RGBA', (W, H), (90, 100, 140, 255))
for x, y, c in pos:
    im = c.render().resize((c.w*Z, c.h*Z), Image.NEAREST)
    img.alpha_composite(im, (x, y))
img.save('/private/tmp/claude-501/-Users-nicholaslemoff-Desktop-portfolio-site/70643163-3e42-4ed4-80cd-7000e9d13ae6/scratchpad/r5work/sheet.png')
print(img.size)
