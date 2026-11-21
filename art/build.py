"""Build every house image (public/house) and layout.json.
python3 art/build.py [outdir]
"""
import json, os, sys
import numpy as np
from px import Canvas, Light
import scene, overlays as O, margins

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'public', 'house')
os.makedirs(OUT, exist_ok=True)
ZONES = ['top', 'room', 'garage', 'base']
layout = {'zones': {}, 'atlas': {}}
lightref = {}   # (zone, mode) -> D light field for overlay lighting
placed = {}     # overlay id -> (zone, x, y) in D

for zn in ZONES:
    layout['zones'][zn] = {}
    for L in ('D', 'M'):
        info = None
        for mode in ('day', 'night'):
            z = getattr(scene, 'compose_' + zn)(L, mode)
            lf = z.light.get()
            z.c.render(light=lf).save(f'{OUT}/R5-House-{zn}-{L}-{mode}.png', optimize=True)
            if mode == 'night':
                g = z.c.render(light=lf, gold=True)
                g.save(f'{OUT}/R5-House-{zn}-{L}-gold.png', optimize=True)
                margins.tile(g, 'L').save(f'{OUT}/R5-House-{zn}-{L}-gold-eL.png', optimize=True)
                margins.tile(g, 'R').save(f'{OUT}/R5-House-{zn}-{L}-gold-eR.png', optimize=True)
            # repeating tiles for the page margins beyond the scene
            im = z.c.render(light=lf)
            margins.tile(im, 'L').save(f'{OUT}/R5-House-{zn}-{L}-{mode}-eL.png', optimize=True)
            margins.tile(im, 'R').save(f'{OUT}/R5-House-{zn}-{L}-{mode}-eR.png', optimize=True)
            if L == 'D':
                lightref[(zn, mode)] = z.light
                for o in z.ov:
                    placed.setdefault(o['id'], (zn, o['x'], o['y']))
            info = dict(w=z.w, h=z.h, ov={o['id']: [o['x'], o['y'], o['w'], o['h']] for o in z.ov},
                        tx={t['id']: [t['x'], t['y'], t['w'], t['h']] for t in z.tx})
        layout['zones'][zn][L] = info

# ---------------------------------------------------------------- atlas
LIT_AS = {'corgiwalk': 'corgi', 'corgisit': 'corgi', 'coin': 'bracket0', 'bracket': 'bracket0', 'hit': None, 'diver': None, 'puff': None,
          'star': None, 'orb1': None, 'orb2': None, 'orb3': None, 'orb4': None, 'orb5': None, 'orb6': None, 'orb7': None, 'p1': None, 'pt-evie': None, 'pt-sfrb': None, 'pt-feb': None, 'dragon': None, 'planet': None, 'smoke': None}
entries = []
for key, fn in O.ALL.items():
    frames = fn()
    entries.append((key, frames))
# shelf-pack
AW = 400
x = y = 0; rowh = 0
pos = {}
for key, frames in entries:
    w, h = frames[0].w * len(frames), frames[0].h
    if x + w > AW:
        x = 0; y += rowh + 1; rowh = 0
    pos[key] = (x, y); x += w + 1; rowh = max(rowh, h)
AH = y + rowh
for mode in ('day', 'night', 'gold'):
    atlas = Canvas(AW, AH)
    for key, frames in entries:
        ax, ay = pos[key]
        ref = LIT_AS.get(key, key)
        for i, f in enumerate(frames):
            lm = 'day' if mode == 'day' else 'night'
            if ref and ref in placed:
                zn, px_, py_ = placed[ref]
                sub = lightref[(zn, lm)].sub(px_, py_, f.w, f.h)
                if key == 'coin':
                    sub = np.maximum(sub, 2.0)
                im = f.render(light=sub, gold=(mode == 'gold'))
            else:
                im = f.render(gold=(mode == 'gold'))
            # paste rendered pixels back via a temp canvas trick: render directly into a PIL atlas instead
            entries_img = im
            if not hasattr(atlas, 'pil'):
                from PIL import Image
                atlas.pil = Image.new('RGBA', (AW, AH), (0, 0, 0, 0))
            atlas.pil.alpha_composite(entries_img, (ax + i * f.w, ay))
    atlas.pil.save(f'{OUT}/R5-House-atlas-{mode}.png', optimize=True)
for key, frames in entries:
    layout['atlas'][key] = dict(x=pos[key][0], y=pos[key][1], w=frames[0].w, h=frames[0].h, n=len(frames))
layout['atlasSize'] = [AW, AH]
json.dump(layout, open(os.path.join(os.path.dirname(__file__), 'layout.json'), 'w'), indent=1)
print('ok', AW, AH, len(os.listdir(OUT)))
