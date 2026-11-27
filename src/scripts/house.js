
(function(){
"use strict";
var CFG = {"corgi": {"D": {"y": 276, "wy": 274, "home": 156, "min": 92, "max": 288}, "M": {"y": 664, "wy": 662, "home": 96, "min": 60, "max": 130}}, "spill": [{"z": "room", "x": 90, "y": 285, "mx": 58, "my": 673}, {"z": "room", "x": 96, "y": 284, "mx": 64, "my": 672}, {"z": "room", "x": 102, "y": 285, "mx": 70, "my": 673}, {"z": "room", "x": 108, "y": 284, "mx": 76, "my": 672}, {"z": "room", "x": 114, "y": 285, "mx": 82, "my": 673}, {"z": "room", "x": 120, "y": 284, "mx": 88, "my": 672}, {"z": "room", "x": 126, "y": 285, "mx": 94, "my": 673}, {"z": "room", "x": 132, "y": 284, "mx": 100, "my": 672}, {"z": "room", "x": 138, "y": 285, "mx": 106, "my": 673}, {"z": "garage", "x": 69, "y": 87, "mx": 112, "my": 193}, {"z": "garage", "x": 74, "y": 103, "mx": 119, "my": 193}, {"z": "garage", "x": 79, "y": 119, "mx": 126, "my": 193}, {"z": "garage", "x": 84, "y": 135, "mx": 133, "my": 193}, {"z": "garage", "x": 89, "y": 151, "mx": 140, "my": 193}, {"z": "garage", "x": 94, "y": 167, "mx": 147, "my": 193}, {"z": "garage", "x": 104, "y": 189, "mx": 150, "my": 193}], "orb4at": 12, "orb5at": 16, "fuzz": "--ax:0;--ay:240;--sw:9;--sh:7;--n:2", "coin": "--ax:311;--ay:240;--sw:6;--sh:8;--n:4", "hit": "--ax:336;--ay:240;--sw:9;--sh:9;--n:1", "sp": {"corgi": "--ax:47;--ay:240;--sw:33;--sh:14;--n:2", "corgisit": "--ax:251;--ay:240;--sw:21;--sh:15;--n:1", "corgiwalk": "--ax:114;--ay:240;--sw:34;--sh:16;--n:4", "diver": "--ax:346;--ay:240;--sw:14;--sh:14;--n:1", "puff": "--ax:0;--ay:263;--sw:20;--sh:12;--n:3"}, "hay": {"x": 14, "y": 186}, "eave": 236};
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
// ?v=<deploy time>: the games are cached for up to 10 min, and a refresh of the page doesn't refetch an iframe, so
// without it a new deploy can take a while to show up inside the house
function load(){ if (!loaded){ loaded = true; frame.src = want + '?v=' + (document.documentElement.dataset.build || ''); } }
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
