"""Generate the house markup, CSS and script for the site from layout.json.
python3 art/page.py  ->  src/generated/house.html, src/styles/house.css, src/scripts/house.js
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAY = json.load(open(os.path.join(HERE, 'layout.json')))
Z = LAY['zones']
A = LAY['atlas']
AW, AH = LAY['atlasSize']
ZONES = ['top', 'room', 'garage', 'base']


# ---------------------------------------------------------------- position helpers
def rect(zn, L, id, kind):
    d = Z[zn][L]['ov' if kind == 'ov' else 'tx']
    return d.get(id)


def P(zn, id, kind='ov', key=None, extra='', d=None, m=None):
    """style vars for an element placed in zone zn"""
    rd = d or rect(zn, 'D', id, kind)
    rm = m or rect(zn, 'M', id, kind)
    cls = []
    v = []
    if key:
        a = A[key]
        w = h = None
        v.append(f"--ax:{a['x']};--ay:{a['y']};--sw:{a['w']};--sh:{a['h']};--n:{a['n']}")
    if rd:
        v.append(f"--x:{rd[0]};--y:{rd[1]}")
        if not key:
            v.append(f"--w:{rd[2]};--h:{rd[3]}")
    else:
        cls.append('dn-d'); v.append('--x:0;--y:0')
    if rm:
        v.append(f"--mx:{rm[0]};--my:{rm[1]}")
        if not key:
            v.append(f"--mw:{rm[2]};--mh:{rm[3]}")
    else:
        cls.append('dn-m'); v.append('--mx:0;--my:0')
    if extra:
        v.append(extra)
    return ' '.join(cls), ';'.join(v)


def el(tag, zn, id, cls='', kind='ov', key=None, attrs='', inner='', extra='', d=None, m=None):
    c2, st = P(zn, id, kind, key, extra, d, m)
    classes = ' '.join(x for x in ['p', 'spr' if key else '', cls, c2] if x)
    return f'<{tag} class="{classes}" style="{st}"{(" " + attrs) if attrs else ""}>{inner}</{tag}>'


def S(key, cls='', attrs='', inner='', extra=''):
    """sprite not placed by layout (inside another element)"""
    a = A[key]
    return f'<span class="spr {cls}" style="--ax:{a["x"]};--ay:{a["y"]};--sw:{a["w"]};--sh:{a["h"]};--n:{a["n"]};{extra}"{(" " + attrs) if attrs else ""}>{inner}</span>'


def bgvars(zn):
    v = []
    for L in ('D', 'M'):
        for i, mode in enumerate(('day', 'night', 'gold'), 1):
            v.append(f"--{L.lower()}{i}:url(/house/R5-House-{zn}-{L}-{mode}.png)")
        for i, mode in enumerate(('day', 'night', 'gold'), 1):
            v.append(f"--{L.lower()}l{i}:url(/house/R5-House-{zn}-{L}-{mode}-eL.png)")
            v.append(f"--{L.lower()}r{i}:url(/house/R5-House-{zn}-{L}-{mode}-eR.png)")
    d, m = Z[zn]['D'], Z[zn]['M']
    v.append(f"--WD:{d['w']};--HD:{d['h']};--WM:{m['w']};--HM:{m['h']}")
    return ';'.join(v)


# ---------------------------------------------------------------- star twinkles
TW_D = [(30, 140), (226, 60), (318, 108), (180, 132), (150, 20), (330, 18), (260, 96)]
TW_M = [(20, 160), (160, 120), (100, 176), (60, 196), (170, 30)]


# ---------------------------------------------------------------- copy
WORK = [
    'Judgment Labs, Member of Technical Staff, 2026–',
    'FullProof, Founding Engineer, 2025–26',
    'Formula Electric at Berkeley, Simulations Lead, 2024–25',
    'NIST, Research Intern, 2024',
    'Berkeley Lab, ML Student Assistant, 2023–24',
    'Mojo Vision, Data Science Intern, 2023–24',
]
EMAIL = 'mailto:nlemoff@gmail.com'
XPOST = 'https://x.com/nlemoff/status/2109824932712784277'
LINKS = {'X': 'https://x.com/nlemoff', 'LinkedIn': 'https://www.linkedin.com/in/nicklemoff', 'GitHub': 'https://github.com/nlemoff'}
LOGO_KEY = {'Judgment Labs': 'judgment', 'FullProof': 'fullproof', 'Formula Electric at Berkeley': 'feb', 'NIST': 'nist', 'Berkeley Lab': 'berkeleylab', 'Mojo Vision': 'mojo'}
SFRB = 'https://github.com/nlemoff/SfRB'
EXT = 'target="_blank" rel="noopener"'


def work_split(s):
    a, b = s.split(', ', 1)
    return a, b


def build(dc=False):
    E = lambda x: x  # noqa
    ext = '' if dc else EXT
    # ------------------------------------------------ TOP
    tw = []
    for i in range(max(len(TW_D), len(TW_M))):
        d = list(TW_D[i]) + [5, 5] if i < len(TW_D) else None
        m = list(TW_M[i]) + [5, 5] if i < len(TW_M) else None
        tw.append(el('span', 'top', 'tw%d' % i, 'tw anim night-only', key='star', d=d, m=m,
                     extra=f'--fd:{260 + i * 70}ms;--dl:{-i * 0.7:.1f}s', attrs='aria-hidden="true"'))
    hero = el('div', 'top', 'hero', 'tb hero', kind='tx', inner=(
        '<h1>Nick Lemoff</h1>'
        '<p class="lede">I\'m at Judgment Labs.</p>'))
    planet_inner = (S('orb1', 'orb', attrs='data-orb="1" role="button" tabindex="0" aria-label="Orb"', extra='left:calc(24*var(--px));top:calc(2*var(--px))')
                    if not dc else S('orb1', 'orb', extra='left:calc(24*var(--px));top:calc(2*var(--px))'))
    top = f'''
<section class="zone" id="top" style="{bgvars('top')}" aria-label="Nick Lemoff">
 <div class="stage">
  {''.join(tw)}
  {el('span', 'top', 'dragon', 'dragon', key='dragon', attrs='aria-hidden="true"')}
  {el('div', 'top', 'planet', 'planet', key='planet', inner=planet_inner)}
  {el('span', 'top', 'smoke', 'smoke anim eve', key='smoke', extra='--fd:180ms', attrs='aria-hidden="true"')}
  {el('a', 'top', 'raven', 'raven anim', key='raven', extra='--fd:900ms', attrs=f'href="{EMAIL}" aria-label="Email"')}
  {el('span', 'top', 'eagle', 'eagle anim', key='eagle', extra='--fd:1400ms', attrs='aria-hidden="true"')}
  {hero}
 </div>
</section>'''

    # ------------------------------------------------ ROOM
    def job(w):
        co, rest = work_split(w)
        role, yrs = rest.rsplit(', ', 1)
        icon = S('logo-' + LOGO_KEY[co], 'logo', attrs='aria-hidden="true"')
        return (f'<li>{icon}'
                f'<span><b>{co}</b><span class="role">{role} · <span class="nw">{yrs}</span></span></span></li>')
    work = ''.join(job(w) for w in WORK)
    papers = {
        'w1': f'<a href="{XPOST}" {ext}>Aligning agent evals with your personal judgment</a> <span class="meta">(X, 2026)</span>',
        'w2': 'Finding undocumented oil and gas wells on historical maps <span class="meta">(AGU, 2024)</span>',
        'w3': 'Computed materials proposals depart from the structural memory of experimental discovery <span class="meta">(arXiv, 2026, co-author)</span>',
    }
    paper_html = ''.join(el('p', 'room', pid, 'tb paper', kind='tx', inner=html) for pid, html in papers.items())
    projects = el('div', 'room', 'projects', 'tb screen', kind='tx', inner=(
        '<h2>Projects</h2>'
        '<div class="ports" role="group" aria-label="Projects">'
        + ''.join(S('pt-' + k, 'port' + (' on' if i == 0 else ''), attrs=f'data-p="{i}"' + ('' if dc else f' role="button" tabindex="0" aria-label="{nm}"'))
                  for i, (k, nm) in enumerate((('evie', 'Evie'), ('sfrb', 'SfRB'), ('feb', 'FEBSim'))))
        + S('p1', 'p1tok', attrs='aria-hidden="true"')
        + '</div><ul class="plist">'
        '<li class="on" data-p="0"><b>Evie</b>: a real-time agent for depositions.</li>'
        f'<li data-p="1"><b><a href="{SFRB}" {ext}>SfRB</a></b>: a local-first resume builder.</li>'
        '<li data-p="2"><b>FEBSim</b>: lap-time sim for Berkeley\'s Formula Electric car.</li>'
        '</ul>'))
    writing_label = el('h2', 'room', 'wlabel', 'tb tape', kind='tx', inner='Writing', d=[236, 6, 46, 9], m=[66, 6, 46, 9])
    room = f'''
<section class="zone" id="room" style="{bgvars('room')}" aria-label="Work, projects and writing">
 <div class="stage">
  {el('h2', 'room', 'worktitle', 'tb banner', kind='tx', inner='Work')}
  {el('div', 'room', 'work', 'tb maptext t3', kind='tx', inner='<ul>' + work + '</ul>', extra='--x3:50;--y3:62;--w3:138;--h3:72')}
  {writing_label}
  {paper_html}
  {projects}
  <div class="p scan dn-m" style="--x:211;--y:177;--w:88;--h:61;--mx:0;--my:0" aria-hidden="true"></div>
  {el('span', 'room', 'door', 'doorway', inner=S('door', 'door').replace('<span ', '<button type="button" aria-label="Door" ', 1).replace('</span>', '</button>'))}
  {el('span', 'room', 'orb3', 'orb', key='orb3', attrs='data-orb="3" role="button" tabindex="0" aria-label="Orb"')}
  {el('span', 'room', 'orb2', 'orb', key='orb2', attrs='data-orb="2" role="button" tabindex="0" aria-label="Orb"')}
  {el('span', 'room', 'corgi', 'corgi anim', key='corgi', extra='--fd:900ms', attrs='aria-hidden="true"')}
  {el('span', 'room', 'towel', 'towel anim', key='towel', extra='--fd:420ms', attrs='aria-hidden="true"')}
  {el('span', 'room', 'bobble', 'bobble anim', key='bobble', extra='--fd:500ms', attrs='aria-hidden="true"')}
  {el('span', 'room', 'steam', 'steam anim morn', key='steam', extra='--fd:220ms', attrs='aria-hidden="true"')}
  {el('button', 'room', 'hearth', 'hearth', key='hearth', attrs='type="button" aria-label="Back to top"')}
  {el('button', 'room', 'fuzz', 'fuzz', key='fuzz', attrs='type="button" aria-label="Fuzzball"')}
  {el('span', 'room', 'hilt', 'hilt', key='hilt', attrs='tabindex="0" role="img" aria-label="Hilt"')}
 </div>
</section>'''

    # ------------------------------------------------ GARAGE
    DRUM_NAMES = {'crash': 'Crash cymbal', 'ride': 'Ride cymbal', 'hihat': 'Hi-hat', 'tom1': 'High tom', 'tom2': 'Mid tom', 'kick': 'Kick drum', 'snare': 'Snare drum', 'floortom': 'Floor tom'}
    kitmap = [('crash', 'Q'), ('ride', 'E'), ('hihat', 'A'), ('tom1', 'D'), ('tom2', 'F'), ('kick', 'B'), ('snare', 'S'), ('floortom', 'G')]
    kit = ''.join(el('button', 'garage', 'kit-' + k, 'drum', key='kit-' + k, attrs=f'type="button" data-drum="{k}" data-key="{key}" aria-label="{DRUM_NAMES[k]}" tabindex="-1"') for k, key in kitmap)
    brackets = ''.join(el('button', 'garage', 'bracket%d' % i, 'bracket', key='bracket', attrs='type="button" aria-label="Shelf bracket"') for i in range(3))
    stickers = ''.join(el('a', 'garage', sid, 'tb sticker s-' + sid, kind='tx', attrs=f'href="{href}" {ext}', inner=label, extra=f'--rot:{rot}deg')
                       for sid, label, href, rot in (('lk-x', 'X', LINKS['X'], -7), ('lk-li', 'LinkedIn', LINKS['LinkedIn'], 4), ('lk-gh', 'GitHub', LINKS['GitHub'], -3)))
    garage = f'''
<section class="zone" id="garage" style="{bgvars('garage')}" aria-label="Garage">
 <div class="stage">
  <div class="kit" tabindex="0" role="group" aria-label="Drum kit">{kit}</div>
  {el('span', 'garage', 'orb4', 'orb hide', key='orb4', d=[98, 186, 9, 9], m=[146, 190, 9, 9], attrs='data-orb="4" role="button" tabindex="0" aria-label="Orb"')}
  {el('span', 'garage', 'orb5', 'orb hide', key='orb5', attrs='data-orb="5" role="button" tabindex="0" aria-label="Orb"')}
  {el('span', 'garage', 'orb6', 'orb', key='orb6', attrs='data-orb="6" role="button" tabindex="0" aria-label="Orb"')}
  {el('button', 'garage', 'box', 'box', key='box', attrs='type="button" aria-label="Box"')}
  {brackets}
  {el('span', 'garage', 'tvsun', 'tvsun anim', key='tvsun', extra='--fd:300ms', attrs='aria-hidden="true"')}
  {el('span', 'garage', 'pumpkin', 'pumpkin', key='pumpkin', attrs='aria-hidden="true"')}
  {stickers}
 </div>
</section>'''

    # ------------------------------------------------ BASEMENT
    if dc:
        gamewin = el('div', 'base', 'game', 'tb gamewin', kind='tx', inner=(
            '<div class="gbar"><button class="gtab on" type="button" onClick="{{ tab0 }}">Time Trial</button>'
            '<button class="gtab" type="button" onClick="{{ tab1 }}">Aim Trainer</button>'
            '<button class="gtab" type="button" onClick="{{ tab2 }}">Ringfall</button>'
            '<button class="gfs" type="button">Full screen</button></div>'
            '<div class="gstage gtitle"><span class="gt-name">Time Trial</span><span class="gt-press" aria-hidden="true"></span></div>'))
    else:
        gamewin = el('div', 'base', 'game', 'tb gamewin', kind='tx', inner=(
            '<div class="gbar" role="toolbar" aria-label="Games">'
            '<button class="gtab" type="button" data-game="racing" aria-pressed="true">Time Trial</button>'
            '<button class="gtab" type="button" data-game="aim" aria-pressed="false">Aim Trainer</button>'
            '<button class="gtab" type="button" data-game="shooter" aria-pressed="false">Ringfall</button>'
            '<button class="gfs" type="button" id="gfs">Full screen</button></div>'
            '<div class="gstage"><iframe id="gframe" data-src="/games/racing/index.html" title="Time Trial" allow="fullscreen; autoplay; gamepad"></iframe></div>'))
    scores = el('div', 'base', 'scores', 'tb scores', kind='tx', inner=(
        '<table><tbody>'
        '<tr><th scope="row">Time Trial</th><td id="sc-racing">-:--.---</td></tr>'
        '<tr><th scope="row">Aim Trainer</th><td id="sc-aim">----</td></tr>'
        '<tr><th scope="row">Ringfall</th><td id="sc-shooter">--:--</td></tr>'
        '</tbody></table>'))
    dots = ''.join(f'<span class="dot" data-dot="{i}"></span>' for i in range(1, 8))
    footer = el('footer', 'base', 'footer', 'tb foot', kind='tx', inner=(
        f'<div class="dots" aria-hidden="true">{dots}</div>'
        '<h2 class="sr">Links</h2>'
        f'<p class="links"><a href="{EMAIL}">Email</a> · <a href="{LINKS["X"]}" {ext}>X</a> · <a href="{LINKS["LinkedIn"]}" {ext}>LinkedIn</a> · <a href="{LINKS["GitHub"]}" {ext}>GitHub</a></p>'))
    base = f'''
<section class="zone" id="base" style="{bgvars('base')}" aria-label="Basement">
 <div class="stage">
  {gamewin}
  <div class="p hum dn-m" style="--x:58;--y:27;--w:172;--h:143;--mx:0;--my:0" aria-hidden="true"></div>
  {scores}
  {el('span', 'base', 'orb7', 'orb hide', key='orb7', attrs='data-orb="7" role="button" tabindex="0" aria-label="Orb"')}
  {footer}
 </div>
</section>'''
    return top, room, garage, base


CSS = r'''
:root{
  --px:4px; --fs:16px;
  --k0:#0d0b1a; --n1:#161a3a; --n2:#222b5c; --n3:#33438a; --n4:#4f69b5; --n5:#86a2dc; --n6:#c4d4f2;
  --w0:#2a1a14; --w2:#70432a; --c0:#fffaf0; --c1:#efe2c0; --c2:#d4bc8e; --g2:#b5821a; --g3:#ffb612; --g4:#ffe08a; --r2:#9a2430; --r3:#d9483b; --s3:#a7abbe;
  --atlas:url(/house/R5-House-atlas-day.png);
  --ink-hero:var(--c0); --hero-sub:var(--c0); --hero-link:var(--c0);
  --paper:var(--k0); --paper-meta:#4a2c1c; --mapink:var(--w0);
  --page:#4f69b5; --paperbg:#fffaf0;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root{--atlas:url(/house/R5-House-atlas-night.png); --ink-hero:var(--g3); --hero-sub:var(--c1); --hero-link:var(--g4); --paper-meta:#3b3c4c; --page:#161a3a; --paperbg:#efe2c0; color-scheme:dark}
}
html.gold{--atlas:url(/house/R5-House-atlas-gold.png); --ink-hero:var(--g3); --hero-sub:var(--c1); --page:#0d0b1a}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--k0);color:var(--c1);font-family:"Pixelify Sans",system-ui,sans-serif;font-size:var(--fs);line-height:1.35;overflow-x:hidden;font-variant-ligatures:none}
.nw{white-space:nowrap}
h1,h2,p,ul,table{margin:0;padding:0}
h2{font-weight:600;font-size:inherit}
ul{list-style:none}
a{color:inherit;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:3px}
a:hover{text-decoration-style:dotted}
:focus-visible{outline:3px solid var(--g3);outline-offset:2px}
button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:pointer}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* ------------ zones: pixel stage centred, edges extended with the art's own edge column */
.zone{position:relative;display:flex;justify-content:center;overflow:hidden}
.zone::before,.zone::after{content:"";position:absolute;top:0;bottom:0;width:50%;background-size:calc(var(--px)*64) 100%;background-repeat:repeat-x;image-rendering:pixelated}
.zone::before{background-position:right top}
.zone::before{left:0;background-image:var(--dl1)}
.zone::after{right:0;background-image:var(--dr1)}
.stage{position:relative;z-index:1;flex:none;width:calc(var(--WD)*var(--px));height:calc(var(--HD)*var(--px));background:var(--d1) 0 0/100% 100% no-repeat;image-rendering:pixelated}
@media (prefers-color-scheme:dark){
  .zone::before{background-image:var(--dl2)} .zone::after{background-image:var(--dr2)}
  .stage{background-image:var(--d2)}
}
html.gold .stage{background-image:var(--d3)}
html.gold .zone::before{background-image:var(--dl3)} html.gold .zone::after{background-image:var(--dr3)}

/* ------------ positioned things (art units) */
.p{position:absolute;left:calc(var(--x)*var(--px));top:calc(var(--y)*var(--px))}
.p:not(.spr){width:calc(var(--w)*var(--px));height:calc(var(--h)*var(--px))}
.dn-d{display:none !important}
.spr{position:absolute;display:block;width:calc(var(--sw)*var(--px));height:calc(var(--sh)*var(--px));background-image:var(--atlas);background-repeat:no-repeat;
  background-size:calc(%AW%*var(--px)) calc(%AH%*var(--px));background-position:calc(var(--ax)*var(--px)*-1) calc(var(--ay)*var(--px)*-1);image-rendering:pixelated}
.anim{animation:play calc(var(--n)*var(--fd,250ms)) steps(var(--n)) infinite;animation-delay:var(--dl,0s)}
@keyframes play{from{background-position-x:calc(var(--ax)*var(--px)*-1)}to{background-position-x:calc((var(--ax) + var(--sw)*var(--n))*var(--px)*-1)}}

/* ------------ hero */
.hero h1{font-size:calc(var(--px)*24);line-height:.95;font-weight:700;color:var(--ink-hero);letter-spacing:-.01em;text-shadow:var(--px) var(--px) 0 var(--k0);margin-bottom:calc(var(--px)*4)}
.hero p{font-size:calc(var(--px)*6.5);line-height:1.3;color:var(--hero-sub);text-shadow:calc(var(--px)*.5) calc(var(--px)*.5) 0 var(--k0);max-width:34ch}
.hero p+p{margin-top:calc(var(--px)*2.5)}
.hero p.lede{font-weight:600}
.hero a{color:var(--hero-link)}

/* ------------ map (work) */
.maptext{color:var(--mapink);font-size:calc(var(--fs)*1.12);line-height:1.2}
.banner{display:flex;align-items:center;justify-content:center;color:#4e1420;font-weight:700;font-size:calc(var(--fs)*1.1);line-height:1;margin:0}
.maptext ul{height:100%;display:flex;flex-direction:column;justify-content:space-between}
.maptext li{display:flex;align-items:center;gap:calc(var(--px)*3)}
.maptext .logo{position:relative;flex:none}
.maptext b{display:block;font-weight:600;line-height:1.1}
.maptext .role{display:block;font-size:.86em;line-height:1.15;color:var(--paper-meta)}
/* corkboard */
.tape{display:flex;align-items:center;justify-content:center;background:var(--c1);color:var(--w0);font-size:var(--fs);line-height:1;box-shadow:0 calc(var(--px)*.5) 0 var(--c2)}
.paper{padding:calc(var(--px)*1.5) calc(var(--px)*2);color:var(--paper);font-size:var(--fs);line-height:1.22;overflow:hidden}
.paper a{color:var(--paper)}
.meta{display:block;margin-top:calc(var(--px)*.75);color:var(--paper-meta)}
/* monitor (projects) */
.screen{padding:calc(var(--px)*1.5) calc(var(--px)*2.5);color:var(--c1);font-size:var(--fs);line-height:1.2}
.screen h2{color:var(--g3);font-size:var(--fs);line-height:1;margin-bottom:calc(var(--px)*1.5)}
.ports{position:relative;display:flex;gap:calc(var(--px)*3);margin-bottom:calc(var(--px)*2)}
.ports .spr.port{position:relative;flex:none;outline:calc(var(--px)*.75) solid var(--k0);cursor:pointer}
.ports .spr.port.on{outline-color:var(--g3)}
.ports .spr.port:focus-visible{outline:calc(var(--px)*1) solid var(--g4);outline-offset:calc(var(--px)*.5)}
.p1tok{left:0;top:calc(var(--px)*9);margin-left:calc(var(--px)*10);transition:left .18s steps(4)}
.plist li{padding:calc(var(--px)*.5) 0;color:var(--n6)}
.plist li.on{color:var(--c0)}
.plist li.on b{color:var(--g3)}
.plist a{color:inherit}
.scan{pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 calc(var(--px)*2),rgba(13,11,26,.18) calc(var(--px)*2) calc(var(--px)*2.5));animation:flick 4.2s steps(1) infinite}
@keyframes flick{0%,100%{opacity:1}47%{opacity:.6}48%{opacity:1}83%{opacity:.8}84%{opacity:1}}

/* ------------ garage */
.kit{position:absolute;inset:0;pointer-events:none;outline:none}
.kit .drum{pointer-events:auto}
.kit:focus-visible .drum::after,.kit.live .drum::after{content:attr(data-key);position:absolute;left:50%;top:-1.1em;transform:translateX(-50%);font-size:calc(var(--px)*3);line-height:1;color:var(--g4);background:var(--k0);padding:1px 3px}
.drum.hit{transform:translateY(var(--px))}
.sticker{display:flex;align-items:center;justify-content:center;font-size:var(--fs);font-weight:600;line-height:1;text-decoration:none;transform:rotate(var(--rot,0deg))}
.s-lk-x,.s-lk-li,.s-lk-gh{color:#fffaf0}
.sticker:hover{text-decoration:underline}
.box.shake{animation:shake .32s steps(4)}
@keyframes shake{25%{transform:translateX(var(--px))}50%{transform:translateX(calc(var(--px)*-1))}75%{transform:translateX(var(--px))}}
.box.nudged{transform:translateX(calc(var(--px)*5))}
.orb.out{z-index:6;transform:translate(calc(var(--px)*-3),calc(var(--px)*-12));transition:transform .3s steps(4)}
.bracket.bump{animation:bump .2s steps(2)}
@keyframes bump{50%{transform:translateY(calc(var(--px)*-2))}}
.coin{pointer-events:none;animation:coin .6s steps(6) forwards}
.coin.spin{animation:play .32s steps(4) infinite, coin .6s steps(6) forwards}
@keyframes coin{0%{transform:translateY(0)}60%{transform:translateY(calc(var(--px)*-14))}100%{transform:translateY(calc(var(--px)*-12));opacity:0}}
.tvsun,.pumpkin,.dragon,.smoke.eve,.steam.morn{display:none}
html.gameday .tvsun{display:block}
html.gameday .towel{--fd:110ms !important}
html.halloween .pumpkin{display:block}
html.evening .smoke.eve{display:block}
html.morning .steam.morn{display:block}
html.gold .dragon{display:block;animation:uncoil 2.4s steps(24) both}
@keyframes uncoil{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.night-only{display:none}
@media (prefers-color-scheme:dark){.night-only{display:block}}
html.gold .night-only{display:block}

@media (pointer:coarse){.orb::before,.hearth::before,.fuzz::before,.bracket::before{content:"";position:absolute;inset:-10px}}

/* ------------ room interactions */
.doorway{overflow:hidden}
.doorway .door{position:absolute;left:0;top:0;transition:transform .5s steps(8)}
.door.open{transform:translateX(-100%)}
.hilt.hum{animation:hum .09s steps(2) infinite}
@keyframes hum{50%{transform:translate(calc(var(--px)*.5),calc(var(--px)*-.5))}}
.hearth.swirl{animation:swirl .7s steps(7)}
@keyframes swirl{50%{transform:translateY(calc(var(--px)*-3))}}
.ring{position:fixed;z-index:60;pointer-events:none;border:var(--px) solid var(--n5);outline:var(--px) solid var(--n3);animation:ringout .7s steps(7) forwards}
@keyframes ringout{from{transform:scale(.2);opacity:1}to{transform:scale(3);opacity:0}}
.corgi.walk{--n:4;--fd:110ms}
.corgi.flip{transform:scaleX(-1)}
.orb{cursor:pointer}
.orb.hide,.orb.got{display:none}
.fz{position:absolute;z-index:3;pointer-events:none}
.fz.drop{animation:drop .4s steps(5)}
@keyframes drop{from{transform:translateY(calc(var(--px)*-10))}}

/* ------------ basement */
.gamewin{display:flex;flex-direction:column;background:#c0c0c0;border:var(--px) solid var(--k0);color:var(--k0);font-size:calc(var(--fs)*.85)}
.gbar{display:flex;flex-wrap:wrap;gap:3px;padding:3px;background:#d4d0c8;border-bottom:2px solid #808080}
.gtab,.gfs{font-family:Verdana,Tahoma,sans-serif;font-size:11px;font-weight:700;line-height:1;padding:5px 9px;background:#d4d0c8;color:#000;border:2px solid;border-color:#fff #404040 #404040 #fff}
.gtab[aria-pressed="true"],.gtab.on{background:var(--g3);border-color:#404040 #fff #fff #404040}
.gfs{margin-left:auto}
.gstage{position:relative;flex:1;background:#000}
.gstage iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.hum{pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 calc(var(--px)*1),rgba(69,196,180,.07) calc(var(--px)*1) calc(var(--px)*2));animation:humroll 6s steps(36) infinite;mix-blend-mode:screen}
@keyframes humroll{from{background-position-y:0}to{background-position-y:calc(var(--px)*36)}}
.scores{padding:0 calc(var(--px)*2) 0 calc(var(--px)*3.5);display:flex;align-items:center;font-size:var(--fs)}
.scores table{width:100%;border-collapse:collapse}
.scores th{text-align:left;font-weight:500;color:#222b5c}
.scores td{text-align:right;color:#9a2430;font-weight:700}
.scores tr{display:flex;justify-content:space-between;gap:8px;line-height:1.2;padding:calc(var(--px)*.4) 0}
.scores tbody{display:block}
.foot{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:calc(var(--px)*2.5);color:var(--c1)}
.dots{display:flex;gap:calc(var(--px)*2)}
.dot{width:calc(var(--px)*3);height:calc(var(--px)*3);border:calc(var(--px)*.75) solid var(--s3);display:block}
.dot.on{background:#f08a24;border-color:#f08a24}
.links{font-size:calc(var(--fs)*1.1)}
.links a{color:var(--c1)}

/* ------------ fixed bits */
.snd{position:fixed;z-index:70;top:12px;right:12px;width:40px;height:40px;display:grid;place-items:center;background:var(--k0);border:3px solid var(--c1)}
.snd svg{width:24px;height:24px;shape-rendering:crispEdges}
.snd[aria-pressed="false"] .wave{display:none}
.snd[aria-pressed="true"] .mute{display:none}
.hitm{position:fixed;z-index:80;pointer-events:none;width:36px;height:36px;margin:-18px 0 0 -18px;animation:hit .22s steps(2) forwards}
@keyframes hit{to{opacity:0}}
.flick{position:fixed;inset:0;z-index:65;pointer-events:none;background:#0d0b1a;animation:flickr 1.1s steps(1) forwards}
@keyframes flickr{0%{opacity:.85}12%{opacity:0}22%{opacity:.7}30%{opacity:0}48%{opacity:.9}60%{opacity:0}100%{opacity:0}}
.diver{position:absolute;z-index:40;pointer-events:none}
.snow{position:fixed;inset:0;z-index:30;pointer-events:none;overflow:hidden}
.snow i{position:absolute;top:-8px;width:var(--px);height:var(--px);background:#fffaf0;animation:fall linear infinite}
@keyframes fall{to{transform:translateY(110vh)}}

/* ------------ scale tiers: one integer pixel scale per tier */
@media (max-width:1424px){:root{--px:3px;--fs:15px}}
@media (min-width:1073px) and (max-width:1424px){
  /* 3x art, text kept at 15px: the longest note takes the board's width, the map list gets a little more parchment */
  .p.t3{left:calc(var(--x3)*var(--px));top:calc(var(--y3)*var(--px));width:calc(var(--w3)*var(--px));height:calc(var(--h3)*var(--px))}
  .paper.t3{background:var(--paperbg);box-shadow:0 0 0 var(--px) #0d0b1a,var(--px) var(--px) 0 var(--px) #0d0b1a}
  .maptext{font-size:var(--fs)}
  .screen{padding:var(--px) calc(var(--px)*2);line-height:1.12}
  .screen h2{margin-bottom:var(--px)} .ports{margin-bottom:var(--px)} .plist li{padding:0}
}
@media (max-width:1072px){
  :root{--px:4px;--fs:19px}
  .stage{width:calc(var(--WM)*var(--px));height:calc(var(--HM)*var(--px));background-image:var(--m1)}
  .zone::before{background-image:var(--ml1)} .zone::after{background-image:var(--mr1)}
  .p{left:calc(var(--mx)*var(--px));top:calc(var(--my)*var(--px))}
  .p:not(.spr){width:calc(var(--mw,var(--w))*var(--px));height:calc(var(--mh,var(--h))*var(--px))}
  .dn-d{display:block !important} .dn-m{display:none !important}
  .hero h1{font-size:calc(var(--px)*22)}
  .hero p{font-size:calc(var(--px)*8.5)}
  .maptext{font-size:var(--fs)}
  .paper{font-size:var(--fs)}
}
@media (max-width:1072px) and (prefers-color-scheme:dark){
  .stage{background-image:var(--m2)}
  .zone::before{background-image:var(--ml2)} .zone::after{background-image:var(--mr2)}
}
@media (max-width:1072px){html.gold .stage{background-image:var(--m3)} html.gold .zone::before{background-image:var(--ml3)} html.gold .zone::after{background-image:var(--mr3)}}
@media (max-width:1072px){:root{--px:3px;--fs:17px}}
@media (max-width:1072px) and (min-width:760px){:root{--px:4px;--fs:19px}}
@media (max-width:559px){:root{--px:2px;--fs:15px}}
@media (max-width:559px){.gtab,.gfs{font-size:10px;padding:4px 6px} .screen{line-height:1.12} .plist li{padding:0}}

@media (prefers-reduced-motion:reduce){
  .anim,.scan,.hum,.hilt.hum,.dragon{animation:none !important}
  .door,.p1tok{transition:none}
}
'''

JS = r'''
(function(){
"use strict";
var CFG = %CFG%;
var root = document.documentElement;
var RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
var isM = function(){ return matchMedia('(max-width:1072px)').matches; };
var pxv = function(){ return parseFloat(getComputedStyle(root).getPropertyValue('--px')) || 4; };
var $ = function(s, r){ return (r||document).querySelector(s); };
var $$ = function(s, r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); };
function ls(k, v){ try{ if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); }catch(e){ return null; } }

/* ---------------- date / time (with ?date=YYYY-MM-DD&time=HH:MM override) */
var q = new URLSearchParams(location.search);
var now = new Date();
if (q.get('date')){ var d = q.get('date').split('-').map(Number); if (d.length === 3) now = new Date(d[0], d[1]-1, d[2], now.getHours(), now.getMinutes()); }
if (q.get('time')){ var t = q.get('time').split(':').map(Number); now.setHours(t[0]||0, t[1]||0); }
var M = now.getMonth() + 1, D = now.getDate(), H = now.getHours(), DOW = now.getDay();
if (M === 12 || M <= 2) root.classList.add('winter');
if ((M === 10 && D >= 15) || (M === 11 && D === 1)) root.classList.add('halloween');
var season = (M >= 9) || (M === 1) || (M === 2 && D <= 15);
if (season && DOW === 0) root.classList.add('gameday');
if (H >= 5 && H < 11) root.classList.add('morning');
if (H >= 17 || H < 5) root.classList.add('evening');

/* ---------------- sound: off by default, one toggle */
var AC = null, soundOn = false, tone = null;
function ac(){ if (!AC){ try{ AC = new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} } return AC; }
function env(g, a, t){ var c = ac(); g.gain.setValueAtTime(0.0001, c.currentTime); g.gain.exponentialRampToValueAtTime(a, c.currentTime+0.005); g.gain.exponentialRampToValueAtTime(0.0001, c.currentTime+t); }
function osc(type, f0, f1, dur, vol){ if(!soundOn||!ac()) return; var c=AC, o=c.createOscillator(), g=c.createGain(); o.type=type; o.frequency.setValueAtTime(f0,c.currentTime); if(f1) o.frequency.exponentialRampToValueAtTime(f1,c.currentTime+dur); o.connect(g); g.connect(c.destination); env(g,vol,dur); o.start(); o.stop(c.currentTime+dur+.02); }
function noise(dur, vol, hp, lp){ if(!soundOn||!ac()) return; var c=AC, n=c.sampleRate*dur, b=c.createBuffer(1,n,c.sampleRate), d=b.getChannelData(0); for(var i=0;i<n;i++) d[i]=Math.random()*2-1; var s=c.createBufferSource(); s.buffer=b; var f=c.createBiquadFilter(); f.type=hp?'highpass':'lowpass'; f.frequency.value=hp||lp||1000; var g=c.createGain(); s.connect(f); f.connect(g); g.connect(c.destination); env(g,vol,dur); s.start(); }
var SFX = {
  tick: function(){ osc('square', 1900, 1500, .04, .05); },
  whoosh: function(){ if(!soundOn||!ac()) return; var c=AC,n=c.sampleRate*.45,b=c.createBuffer(1,n,c.sampleRate),d=b.getChannelData(0); for(var i=0;i<n;i++) d[i]=Math.random()*2-1; var s=c.createBufferSource(); s.buffer=b; var f=c.createBiquadFilter(); f.type='bandpass'; f.Q.value=1.4; f.frequency.setValueAtTime(300,c.currentTime); f.frequency.exponentialRampToValueAtTime(2400,c.currentTime+.4); var g=c.createGain(); s.connect(f); f.connect(g); g.connect(c.destination); env(g,.12,.45); s.start(); },
  coin: function(){ osc('square', 988, 0, .07, .05); setTimeout(function(){ osc('square', 1319, 0, .18, .05); }, 70); },
  coo: function(){ osc('sine', 520, 880, .12, .08); },
  thud: function(){ osc('sine', 120, 50, .14, .2); noise(.06, .05, 0, 400); },
  swirl: function(){ [523,659,784,1047,1319].forEach(function(f,i){ setTimeout(function(){ osc('triangle', f, 0, .2, .05); }, i*60); }); },
  orb: function(){ [784,988,1175].forEach(function(f,i){ setTimeout(function(){ osc('square', f, 0, .1, .04); }, i*80); }); },
  drum: function(k){ if(k==='kick') osc('sine',150,40,.22,.5); else if(k==='snare'){ noise(.16,.25,1200); osc('triangle',190,120,.08,.15); } else if(k==='hihat') noise(.05,.12,7000); else if(k==='crash'||k==='ride') noise(k==='crash'?.9:.5,.12,4500); else osc('sine',{tom1:240,tom2:190,floortom:120}[k]||180,60,.3,.35); }
};
var hum = null;
function humOn(){ if(!soundOn||!ac()||hum) return; var c=AC, o=c.createOscillator(), o2=c.createOscillator(), f=c.createBiquadFilter(), g=c.createGain(); o.type='sawtooth'; o.frequency.value=72; o2.type='sawtooth'; o2.frequency.value=73.5; f.type='lowpass'; f.frequency.value=380; o.connect(f); o2.connect(f); f.connect(g); g.connect(c.destination); g.gain.value=0; g.gain.linearRampToValueAtTime(.06,c.currentTime+.08); o.start(); o2.start(); hum={o:o,o2:o2,g:g}; }
function humOff(){ if(!hum) return; var c=AC, h=hum; hum=null; h.g.gain.linearRampToValueAtTime(0,c.currentTime+.1); setTimeout(function(){ h.o.stop(); h.o2.stop(); }, 150); }
function roomTone(on){ if(!ac()) return; if(on && !tone){ var c=AC, n=c.sampleRate*2, b=c.createBuffer(1,n,c.sampleRate), d=b.getChannelData(0), last=0; for(var i=0;i<n;i++){ last=(last+.02*(Math.random()*2-1))/1.02; d[i]=last*3; } var s=c.createBufferSource(); s.buffer=b; s.loop=true; var f=c.createBiquadFilter(); f.type='lowpass'; f.frequency.value=500; var g=c.createGain(); g.gain.value=.05; s.connect(f); f.connect(g); g.connect(c.destination); s.start(); tone={s:s,g:g}; } else if(!on && tone){ tone.s.stop(); tone=null; } }
var snd = $('#snd');
snd.addEventListener('click', function(){ soundOn = !soundOn; snd.setAttribute('aria-pressed', String(soundOn)); if (soundOn && ac() && AC.state === 'suspended') AC.resume(); roomTone(soundOn); });

/* ---------------- hitmarker on any link click */
document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('a');
  if (!a) return;
  var h = document.createElement('span');
  h.className = 'spr hitm';
  h.style.cssText = CFG.hit + ';left:' + e.clientX + 'px;top:' + e.clientY + 'px;--px:4px';
  document.body.appendChild(h); SFX.tick();
  setTimeout(function(){ h.remove(); }, 260);
}, true);

/* ---------------- hearthstone: swirl, then back to the top */
var hearth = $('.hearth');
hearth.addEventListener('click', function(){
  var r = hearth.getBoundingClientRect();
  var ring = document.createElement('span'); ring.className = 'ring';
  ring.style.cssText = 'left:' + (r.left - 20) + 'px;top:' + (r.top - 26) + 'px;width:' + (r.width + 40) + 'px;height:' + (r.height + 40) + 'px';
  document.body.appendChild(ring); hearth.classList.add('swirl'); SFX.swirl();
  setTimeout(function(){ ring.remove(); hearth.classList.remove('swirl'); window.scrollTo({top:0, behavior: RM ? 'auto' : 'smooth'}); var h1 = $('h1'); h1.tabIndex = -1; h1.focus({preventScroll:true}); }, RM ? 0 : 650);
});

/* ---------------- door 117 slides */
var door = $('.door');
function doorOpen(o){ if (o === door.classList.contains('open')) return; door.classList.toggle('open', o); if (o) SFX.whoosh(); }
var doorHoverT = 0;
door.addEventListener('mouseenter', function(){ doorHoverT = performance.now(); doorOpen(true); });
door.addEventListener('mouseleave', function(){ doorOpen(false); });
door.addEventListener('focus', function(){ doorOpen(true); });
door.addEventListener('blur', function(){ doorOpen(false); });
door.addEventListener('click', function(){ if (performance.now() - doorHoverT < 700) return; doorOpen(!door.classList.contains('open')); });

/* ---------------- fuzzballs multiply and spill downstairs */
var fuzzN = 0;
$('.fuzz').addEventListener('click', function(){
  var spot = CFG.spill[Math.min(fuzzN, CFG.spill.length - 1)];
  fuzzN++;
  var f = document.createElement('span');
  f.className = 'p spr fz fuzz anim drop';
  f.setAttribute('aria-hidden', 'true');
  var jit = fuzzN >= CFG.spill.length ? (fuzzN % 5) * 3 : 0;
  f.style.cssText = CFG.fuzz + ';--fd:' + (300 + fuzzN * 37 % 200) + 'ms;--x:' + (spot.x + jit) + ';--y:' + spot.y + ';--mx:' + (spot.mx + jit) + ';--my:' + spot.my;
  $('#' + spot.z + ' .stage').appendChild(f);
  SFX.coo();
  if (fuzzN === CFG.orb4at) showOrb(4);
});

/* ---------------- taped box: the tape holds */
var box = $('.box'), boxN = 0;
box.addEventListener('click', function(){
  boxN++; box.classList.remove('shake'); void box.offsetWidth; box.classList.add('shake'); SFX.thud();
  if (boxN >= 3 && !box.classList.contains('nudged')){ box.classList.add('nudged'); var o6 = $('[data-orb="6"]'); if (o6){ o6.classList.add('out'); o6.tabIndex = 0; } }
});

/* ---------------- shelf brackets pop coins */
$$('.bracket').forEach(function(b){
  b.addEventListener('click', function(){
    b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); SFX.coin();
    var c = document.createElement('span');
    c.className = 'p spr coin spin';
    var s = getComputedStyle(b);
    c.style.cssText = CFG.coin + ';--x:' + (parseFloat(s.getPropertyValue('--x')) + 1) + ';--y:' + (parseFloat(s.getPropertyValue('--y')) - 13) + ';--mx:' + (parseFloat(s.getPropertyValue('--mx')) + 1) + ';--my:' + (parseFloat(s.getPropertyValue('--my')) - 13);
    b.parentNode.appendChild(c); setTimeout(function(){ c.remove(); }, 700);
  });
});

/* ---------------- hilt hums on hover */
var hilt = $('.hilt');
['mouseenter','focus'].forEach(function(ev){ hilt.addEventListener(ev, function(){ hilt.classList.add('hum'); humOn(); }); });
['mouseleave','blur'].forEach(function(ev){ hilt.addEventListener(ev, function(){ hilt.classList.remove('hum'); humOff(); }); });
hilt.addEventListener('click', function(){ hilt.classList.add('hum'); humOn(); clearTimeout(hilt._t); hilt._t = setTimeout(function(){ hilt.classList.remove('hum'); humOff(); }, 1500); });

/* ---------------- projects: drop the P1 token */
var ports = $$('.port'), plist = $$('.plist li'), tok = $('.p1tok');
function pick(i){ ports.forEach(function(p, k){ p.classList.toggle('on', k === i); }); plist.forEach(function(l, k){ l.classList.toggle('on', k === i); }); tok.style.left = ports[i].offsetLeft + 'px'; }
ports.forEach(function(p, i){ p.addEventListener('click', function(){ pick(i); SFX.tick(); }); p.addEventListener('mouseenter', function(){ pick(i); }); p.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); pick(i); } }); });
plist.forEach(function(l, i){ l.addEventListener('mouseenter', function(){ pick(i); }); });
requestAnimationFrame(function(){ pick(0); });

/* ---------------- corgi: wakes near the cursor, trots after it, goes back to sleep */
var corgi = $('.corgi'), cg = {state:'sleep', x:null, t:0, lastNear:0};
function cgL(){ return isM() ? CFG.corgi.M : CFG.corgi.D; }
function cgSet(state){
  cg.state = state;
  var key = state === 'sleep' ? CFG.sp.corgi : (state === 'sit' ? CFG.sp.corgisit : CFG.sp.corgiwalk);
  corgi.style.cssText = key + ';--fd:' + (state === 'walk' ? '110ms' : '900ms') + ';--x:' + Math.round(cg.x) + ';--y:' + (state === 'sleep' ? cgL().y : cgL().wy) + ';--mx:' + Math.round(cg.x) + ';--my:' + (state === 'sleep' ? cgL().y : cgL().wy);
  corgi.classList.toggle('walk', state === 'walk');
  if (state !== 'sleep') showOrb(2);
}
var target = null, lapQ = [];
document.addEventListener('pointermove', function(e){
  if (lapQ.length) return;
  var r = corgi.getBoundingClientRect();
  var near = Math.abs(e.clientX - (r.left + r.width/2)) < 150 && Math.abs(e.clientY - (r.top + r.height/2)) < 120;
  if (near){ cg.lastNear = performance.now(); if (cg.state === 'sleep'){ if (cg.x === null) cg.x = cgL().home; cgSet('sit'); cg.t = performance.now(); } }
  if (cg.state !== 'sleep' && Math.abs(e.clientY - (r.top + r.height/2)) < 260){
    var st = corgi.parentNode.getBoundingClientRect();
    target = (e.clientX - st.left) / pxv() - 16;
  }
});
function clampX(x){ var L = cgL(); return Math.max(L.min, Math.min(L.max, x)); }
function tick(ts){
  if (cg.x === null) cg.x = cgL().home;
  if (lapQ.length){ target = lapQ[0]; if (Math.abs(cg.x - target) < 2){ lapQ.shift(); if (!lapQ.length){ target = null; cgSet('sleep'); } } }
  if (cg.state !== 'sleep'){
    if (!lapQ.length && performance.now() - cg.lastNear > 4500){ target = cgL().home; if (Math.abs(cg.x - target) < 2){ cg.x = cgL().home; cgSet('sleep'); target = null; } }
    if (target !== null && !(RM && !lapQ.length)){
      var tx = clampX(target), dx = tx - cg.x;
      if (Math.abs(dx) > 2){ if (cg.state !== 'walk') cgSet('walk'); cg.x += Math.sign(dx) * Math.min(Math.abs(dx), lapQ.length ? 1.6 : 0.9); corgi.classList.toggle('flip', dx < 0); corgi.style.setProperty('--x', Math.round(cg.x)); corgi.style.setProperty('--mx', Math.round(cg.x)); }
      else if (cg.state === 'walk' && !lapQ.length){ cgSet('sit'); }
    }
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
corgi.parentNode.addEventListener('click', function(e){ if (e.target !== corgi) return; if (cg.x === null) cg.x = cgL().home; if (cg.state === 'sleep') cgSet('sit'); cg.lastNear = performance.now(); target = cg.x + (cg.x > cgL().home + 20 ? -40 : 40); });

/* ---------------- drum kit: keyboard-playable only while the kit is focused or hovered */
var kit = $('.kit'), hits = 0, KEYS = {}, drums = $$('.drum');
drums.forEach(function(d){ KEYS[d.dataset.key.toLowerCase()] = d; });
function play(d){ d.classList.add('hit'); setTimeout(function(){ d.classList.remove('hit'); }, 90); SFX.drum(d.dataset.drum); hits++; if (hits === CFG.orb5at) showOrb(5); }
drums.forEach(function(d){ d.addEventListener('pointerdown', function(e){ e.preventDefault(); play(d); kit.focus({preventScroll:true}); }); });
kit.addEventListener('keydown', function(e){ if (e.metaKey || e.ctrlKey || e.altKey) return; var d = KEYS[e.key.toLowerCase()]; if (d){ e.preventDefault(); play(d); } });
var kitZone = $('#garage .stage');
function typing(a){ return a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.tagName === 'IFRAME' || a.tagName === 'SELECT' || a.isContentEditable); }
drums.forEach(function(d){ d.addEventListener('mouseenter', function(){ if (!typing(document.activeElement)){ kit.classList.add('live'); kit.focus({preventScroll:true}); } }); });
kit.addEventListener('blur', function(){ kit.classList.remove('live'); });
kitZone.addEventListener('mouseleave', function(){ if (document.activeElement === kit) kit.blur(); });

/* ---------------- orbs (7, persisted) */
var got = ls('r5.orbs') || [];
function dots(){ $$('.dot').forEach(function(d){ d.classList.toggle('on', got.indexOf(+d.dataset.dot) >= 0); }); }
function showOrb(n){ var o = $('[data-orb="' + n + '"]'); if (o && got.indexOf(n) < 0){ o.classList.remove('hide'); o.tabIndex = 0; } }
function collect(n){ if (got.indexOf(n) >= 0) return; got.push(n); ls('r5.orbs', got); var o = $('[data-orb="' + n + '"]'); if (o) o.classList.add('got'); SFX.orb(); dots(); if (got.length === 7){ root.classList.add('gold'); ls('r5.gold', true); } }
$$('[data-orb]').forEach(function(o){ var n = +o.dataset.orb; if (got.indexOf(n) >= 0) o.classList.add('got');
  if (o.classList.contains('hide') || n === 2 || n === 6) o.tabIndex = -1;
  o.addEventListener('click', function(e){ e.stopPropagation(); collect(n); });
  o.addEventListener('keydown', function(e){ if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); collect(n); } }); });
dots();
if (ls('r5.gold') || got.length >= 7) root.classList.add('gold');

/* ---------------- konami: lights flicker, corgi does a lap */
var KON = ['arrowup','arrowup','arrowdown','arrowdown','arrowleft','arrowright','arrowleft','arrowright','b','a'], ki = 0;
document.addEventListener('keydown', function(e){
  var tg = e.target; if (tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.isContentEditable)) return;
  if (kit.contains(tg) || tg === kit) { ki = 0; return; }
  var k = e.key.toLowerCase();
  ki = (k === KON[ki]) ? ki + 1 : (k === KON[0] ? (ki === 2 ? 2 : 1) : 0);
  if (ki === KON.length){ ki = 0; if (!RM){ var f = document.createElement('div'); f.className = 'flick'; document.body.appendChild(f); setTimeout(function(){ f.remove(); }, 1200); }
    var L = cgL(); if (cg.x === null) cg.x = L.home; cgSet('walk'); cg.lastNear = performance.now() + 8000; lapQ = [L.max, L.min, L.home]; }
});

/* ---------------- fast scroll past the roof: a hooded figure dives into the hay */
var lastY = scrollY, lastT = performance.now(), diving = false, roofEdge = 0;
function measureRoof(){ var t = $('#top'); roofEdge = t.offsetTop + t.offsetHeight * .9; }
measureRoof(); addEventListener('resize', measureRoof);
addEventListener('scroll', function(){
  var y = scrollY, t = performance.now(), v = (y - lastY) / Math.max(1, t - lastT);
  var line = y + innerHeight * .35;
  if (!diving && !RM && !isM() && v > 2.2 && lastY + innerHeight * .35 < roofEdge && line >= roofEdge) dive();
  lastY = y; lastT = t;
}, {passive:true});
function dive(){
  diving = true;
  var P = pxv(), eagle = $('.eagle').getBoundingClientRect(), top = $('#top .stage'), gar = $('#garage .stage');
  var tr = top.getBoundingClientRect(), gr = gar.getBoundingClientRect();
  var x0 = eagle.left - 2 * P + scrollX, y0 = eagle.top - 12 * P + scrollY;
  var x1 = gr.left + CFG.hay.x * P + scrollX, y1 = gr.top + CFG.hay.y * P + scrollY;
  var d = document.createElement('span'); d.className = 'spr diver'; d.style.cssText = CFG.sp.diver + ';--px:' + P + 'px;left:0;top:0';
  document.body.appendChild(d);
  var mid = {x: tr.left + 14 * P + scrollX, y: tr.top + (CFG.eave) * P + scrollY};
  var anim = d.animate([
    {transform:'translate(' + x0 + 'px,' + y0 + 'px) rotate(0deg)'},
    {transform:'translate(' + mid.x + 'px,' + (mid.y - 30) + 'px) rotate(0deg)', offset:.25},
    {transform:'translate(' + (x1 - 7*P) + 'px,' + (y1 - 14*P) + 'px) rotate(0deg)'}
  ], {duration: 1100, easing: 'steps(22)'});
  anim.onfinish = function(){ d.remove(); var p = document.createElement('span'); p.className = 'spr anim'; p.style.cssText = CFG.sp.puff + ';--px:' + P + 'px;--fd:120ms;position:absolute;left:' + (x1 - 10*P) + 'px;top:' + (y1 - 10*P) + 'px;z-index:40;animation-iteration-count:1';
    document.body.appendChild(p); SFX.thud(); setTimeout(function(){ p.remove(); }, 400); setTimeout(function(){ diving = false; }, 6000); };
}

/* ---------------- snow (Dec-Feb) */
if (root.classList.contains('winter') && !RM){
  var sn = document.createElement('div'); sn.className = 'snow'; sn.setAttribute('aria-hidden','true');
  for (var i = 0; i < 70; i++){ var f = document.createElement('i'); f.style.left = (Math.random()*100) + 'vw'; f.style.animationDuration = (7 + Math.random()*8) + 's'; f.style.animationDelay = (-Math.random()*15) + 's'; f.style.animationTimingFunction = 'steps(' + (60 + (i % 40)) + ')'; sn.appendChild(f); }
  document.body.appendChild(sn);
}

/* ---------------- games: tabs, full screen, scores */
var frame = $('#gframe'), want = frame.dataset.src, loaded = false;
function load(){ if (!loaded){ loaded = true; frame.src = want; } }
$$('.gtab').forEach(function(b){ b.addEventListener('click', function(){ $$('.gtab').forEach(function(x){ x.setAttribute('aria-pressed', String(x === b)); }); want = '/games/' + b.dataset.game + '/index.html'; frame.title = b.textContent; loaded = false; load(); }); });
if ('IntersectionObserver' in window){
  new IntersectionObserver(function(es){ if (es[0].isIntersecting) load(); }, {rootMargin:'400px 0px'}).observe(frame);
  new IntersectionObserver(function(es){ if (!es[0].isIntersecting && loaded && frame.contentWindow) frame.contentWindow.postMessage('nl:pause', location.origin); }, {threshold:0}).observe(frame);
} else load();
$('#gfs').addEventListener('click', function(){ load();
  var go = frame.requestFullscreen || frame.webkitRequestFullscreen;
  if (go) go.call(frame); else window.open(want, '_blank', 'noopener');
});
function fmtLap(s){ if (s == null) return '-:--.---'; var m = Math.floor(s/60); return m + ':' + (s - m*60).toFixed(3).padStart(6, '0'); }
var base0 = null;
function readScores(){
  var r = ls('nl-racing-ampere-v1'), a = ls('range06.best'), s = ls('ringfall.best');
  var lap = r && r.bestLap, aim = a ? Math.max.apply(null, [0].concat(Object.keys(a).map(function(k){ return +a[k] || 0; }))) : 0, ring = s && s.time;
  $('#sc-racing').textContent = fmtLap(lap);
  $('#sc-aim').textContent = aim ? String(Math.round(aim)) : '----';
  $('#sc-shooter').textContent = ring ? (String(Math.floor(ring/60)).padStart(2,'0') + ':' + (ring%60).toFixed(2).padStart(5,'0')) : '--:--';
  var sig = JSON.stringify([lap, aim, ring, r && r.laps]);
  if (base0 === null) base0 = sig; else if (sig !== base0) showOrb(7);
}
readScores(); setInterval(readScores, 2500);
})();
'''


def cfg():
    zr, zg, zt = Z['room'], Z['garage'], Z['top']
    def spv(k):
        a = A[k]; return f"--ax:{a['x']};--ay:{a['y']};--sw:{a['w']};--sh:{a['h']};--n:{a['n']}"
    cd, cm = zr['D']['ov']['corgi'], zr['M']['ov']['corgi']
    spill = []
    for i in range(9):   # off the shelf and onto the floor by the door (never in front of the trophies)
        spill.append(dict(z='room', x=90 + i * 6, y=285 - (i % 2), mx=58 + i * 6, my=673 - (i % 2)))
    for i in range(6):   # down the garage stairs
        spill.append(dict(z='garage', x=44 + (i + 5) * 5, y=(i + 6) * 16 - 2 - 7, mx=112 + i * 7, my=193))
    spill.append(dict(z='garage', x=104, y=189, mx=150, my=193))
    return json.dumps(dict(
        corgi=dict(D=dict(y=cd[1], wy=cd[1] - 2, home=cd[0], min=92, max=288), M=dict(y=cm[1], wy=cm[1] - 2, home=cm[0], min=60, max=130)),
        spill=spill, orb4at=12, orb5at=16,
        fuzz=spv('fuzz'), coin=spv('coin'), hit=spv('hit'),
        sp=dict(corgi=spv('corgi'), corgisit=spv('corgisit'), corgiwalk=spv('corgiwalk'), diver=spv('diver'), puff=spv('puff')),
        hay=dict(x=14, y=186), eave=236,
    ))


SPEAKER = ('<svg viewBox="0 0 12 12" aria-hidden="true"><g fill="#efe2c0"><rect x="1" y="4" width="2" height="4"/><rect x="3" y="3" width="1" height="6"/><rect x="4" y="2" width="1" height="8"/><rect x="5" y="1" width="1" height="10"/></g>'
           '<g class="wave" fill="#ffb612"><rect x="7" y="5" width="1" height="2"/><rect x="8" y="3" width="1" height="1"/><rect x="8" y="8" width="1" height="1"/><rect x="9" y="4" width="1" height="4"/><rect x="10" y="2" width="1" height="2"/><rect x="10" y="8" width="1" height="2"/><rect x="11" y="4" width="1" height="4"/></g>'
           '<g class="mute" fill="#d9483b"><rect x="7" y="4" width="1" height="1"/><rect x="8" y="5" width="1" height="1"/><rect x="9" y="6" width="1" height="1"/><rect x="10" y="7" width="1" height="1"/><rect x="10" y="4" width="1" height="1"/><rect x="9" y="5" width="1" height="1"/><rect x="8" y="6" width="1" height="1"/><rect x="7" y="7" width="1" height="1"/></g></svg>')

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet">'


def standalone():
    top, room, garage, base = build(dc=False)
    css = CSS.replace('%AW%', str(AW)).replace('%AH%', str(AH))
    js = JS.replace('%CFG%', cfg())
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nick Lemoff</title>
<meta name="description" content="Nick Lemoff, Member of Technical Staff at Judgment Labs. I work on agent evals.">
<meta name="color-scheme" content="light dark">
{FONT}
<style>{css}</style>
</head>
<body>
<button class="snd" id="snd" type="button" aria-label="Sound" aria-pressed="false">{SPEAKER}</button>
<main>
{top}
{room}
{garage}
{base}
</main>
<script>{js}</script>
</body>
</html>
'''


DC_LOGIC = """class Component extends DCLogic {
  constructor(props) {
    super(props);
    this.state = { tab: 0 };
  }
  renderVals() {
    const names = ['Time Trial', 'Aim Trainer', 'Ringfall'];
    const t = this.state.tab;
    return {
      title: names[t],
      p0: t === 0 ? 'true' : 'false',
      p1: t === 1 ? 'true' : 'false',
      p2: t === 2 ? 'true' : 'false',
      tab0: () => this.setState({ tab: 0 }),
      tab1: () => this.setState({ tab: 1 }),
      tab2: () => this.setState({ tab: 2 })
    };
  }
}"""


def dc_doc(height):
    top, room, garage, base = build(dc=True)
    css = CSS.replace('%AW%', str(AW)).replace('%AH%', str(AH))
    css += """
.gtitle{display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;gap:10px;padding:6% 7%;background:#0d0b1a url(/house/R5-House-title.png) center/cover no-repeat;image-rendering:pixelated}
.gt-name{font-family:"Pixelify Sans",sans-serif;font-weight:700;font-size:calc(var(--px)*13);line-height:1;color:#ffb612;text-shadow:4px 4px 0 #0d0b1a}
.gt-press{width:calc(var(--px)*4);height:calc(var(--px)*5);background:#ffb612;clip-path:polygon(0 0,100% 50%,0 100%);animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:.35}}
.gtab[aria-pressed="true"]{background:#ffb612;border-color:#404040 #fff #fff #404040}
"""
    gam = '<span class="gt-name">Time Trial</span>'
    base = base.replace('<button class="gtab on" type="button" onClick="{{ tab0 }}">', '<button class="gtab" type="button" aria-pressed="{{ p0 }}" onClick="{{ tab0 }}">')
    base = base.replace('<button class="gtab" type="button" onClick="{{ tab1 }}">', '<button class="gtab" type="button" aria-pressed="{{ p1 }}" onClick="{{ tab1 }}">')
    base = base.replace('<button class="gtab" type="button" onClick="{{ tab2 }}">', '<button class="gtab" type="button" aria-pressed="{{ p2 }}" onClick="{{ tab2 }}">')
    base = base.replace(gam, '<span class="gt-name">{{ title }}</span>')
    # the DC root carries the page ground; sound toggle is a static button
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Nick Lemoff</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<style>{css}</style>
</helmet>
<div class="r5root" style="font-family: 'Pixelify Sans', system-ui, sans-serif; background: #0d0b1a; color: #efe2c0; min-height: 100vh; position: relative">
<button class="snd" type="button" aria-label="Sound" aria-pressed="false">{SPEAKER}</button>
<main>
{top}
{room}
{garage}
{base}
</main>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{height}}}}}'>
{DC_LOGIC}
</script>
</body>
</html>
"""


def site():
    """the three pieces src/pages/index.astro stitches together"""
    top, room, garage, base = build(dc=False)
    css = CSS.replace('%AW%', str(AW)).replace('%AH%', str(AH))
    js = JS.replace('%CFG%', cfg())
    html = f'''<button class="snd" id="snd" type="button" aria-label="Sound" aria-pressed="false">{SPEAKER}</button>
<main>
{top}
{room}
{garage}
{base}
</main>
'''
    return html, css, js


if __name__ == '__main__':
    root = os.path.join(HERE, '..', 'src')
    html, css, js = site()
    for rel, body in (('generated/house.html', html), ('styles/house.css', css), ('scripts/house.js', js)):
        out = os.path.join(root, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w').write(body)
        print('wrote', os.path.relpath(out))
