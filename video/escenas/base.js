// Utilidades de dibujo: fondo de Naxxramas, ventanas del addon, personajes, objetos.
const W = 1920, H = 1080;
const cv = document.getElementById('c');
const g = cv.getContext('2d');

let TL = null;
const CUE = {}, ESC = {};
function initTL(tl) {
  TL = tl;
  for (const e of tl.escenas) { ESC[e.id] = e; for (const c of e.cues) CUE[c.id] = c; }
}

// ---------------------------------------------------------------- tiempo
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const sm = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const eOut = x => { x = clamp(x); return 1 - Math.pow(1 - x, 3); };
const eIn = x => { x = clamp(x); return x * x * x; };
const eBack = x => { x = clamp(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const P = (t, a, d = 0.5) => clamp((t - a) / d);
const at = (id, f = 0) => { const c = CUE[id]; return c.ini + f * (c.fin - c.ini); };
// visible entre a y b, con entrada/salida suaves
const vis = (t, a, b, d = 0.4) => Math.min(sm((t - a) / d), sm((b - t) / d));
function hash(n) { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }

// ---------------------------------------------------------------- colores
const C = {
  gold: '#e8c46a', gold2: '#b8892e', goldL: '#fff1c2', purple: '#b561ff', epic: '#a335ee',
  green: '#6dffb0', text: '#f3ecdb', dim: '#a79fb6', red: '#ff5a4f', orange: '#ff8c1a',
  frame: 'rgba(13,10,22,0.94)'
};
const CLS = {
  guerrero: '#C69B6D', paladin: '#F48CBA', cazador: '#AAD372', picaro: '#FFF468', sacerdote: '#FFFFFF',
  chaman: '#0070DD', mago: '#3FC7EB', brujo: '#8788EE', druida: '#FF7C0A'
};
const PJ = {
  kharion: ['Kharion', 'guerrero'], veltra: ['Veltra', 'picaro'], lunaria: ['Lunaria', 'mago'],
  sombrix: ['Sombrix', 'brujo'], aurelio: ['Aurelio', 'sacerdote'], thorgan: ['Thorgan', 'paladin'],
  brisa: ['Brisa', 'cazador'], ramaz: ['Ramaz', 'druida'], tukan: ['Tukan', 'chaman'],
  morgrath: ['Morgrath', 'paladin']
};

// ---------------------------------------------------------------- texto
function font(size, fam = 'Alegreya Sans', w = 500) { return `${w} ${size}px "${fam}"`; }
// En Cinzel el "1" parece una "I": los textos con números usan Libre Baskerville
const NUM_SOLO = /^[\s\d+\-—:·,.]+$/;
function famNum(s, fam, w) {
  if (/\d/.test(s) && (fam.startsWith('Cinzel') || NUM_SOLO.test(s)) && s !== 'SoftReserve335') return ['Libre Baskerville', 700];
  return [fam, w];
}
function txt(s, x, y, o = {}) {
  let { size = 40, fam = 'Alegreya Sans', w = 500, color = C.text, align = 'center', base = 'middle',
    alpha = 1, glow = 0, glowColor = null, shadow = true, maxW = null } = o;
  if (alpha <= 0) return;
  [fam, w] = famNum(String(s), fam, w);
  g.save();
  g.globalAlpha *= alpha;
  g.font = font(size, fam, w);
  g.textAlign = align; g.textBaseline = base;
  if (glow) { g.shadowColor = glowColor || color; g.shadowBlur = glow; }
  else if (shadow) { g.shadowColor = 'rgba(0,0,0,0.9)'; g.shadowBlur = size * 0.18; g.shadowOffsetY = size * 0.05; }
  g.fillStyle = color;
  if (maxW) g.fillText(s, x, y, maxW); else g.fillText(s, x, y);
  g.restore();
}
// texto con varios colores en una línea: partes = [[texto, color, peso?], ...]
function txtRich(parts, x, y, o = {}) {
  const { size = 36, fam = 'Alegreya Sans', align = 'left', alpha = 1 } = o;
  g.save();
  let total = 0;
  const fw = p => famNum(p[0], fam, p[2] || 500);
  for (const p of parts) { g.font = font(size, ...fw(p)); total += g.measureText(p[0]).width; }
  let cx = align === 'center' ? x - total / 2 : align === 'right' ? x - total : x;
  for (const p of parts) {
    g.font = font(size, ...fw(p));
    txt(p[0], cx, y, { size, fam, w: p[2] || 500, color: p[1], align: 'left', alpha });
    cx += g.measureText(p[0]).width;
  }
  g.restore();
}
function goldGrad(y0, y1) {
  const gr = g.createLinearGradient(0, y0, 0, y1);
  gr.addColorStop(0, '#fff6d2'); gr.addColorStop(0.45, '#f0c865'); gr.addColorStop(0.55, '#d9a441'); gr.addColorStop(1, '#8a5a17');
  return gr;
}
// palabra clave grande y dorada
function keyword(s, x, y, size, p, o = {}) {
  if (p <= 0) return;
  let { tint = null, fam = 'Cinzel Decorative', w = 900, alpha = 1 } = o;
  [fam, w] = famNum(s, fam, w);
  const sc = lerp(1.5, 1, eOut(p));
  g.save();
  g.globalAlpha *= clamp(p * 2.2) * alpha;
  g.translate(x, y); g.scale(sc, sc);
  g.font = font(size, fam, w);
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.shadowColor = tint || 'rgba(255,200,90,0.8)'; g.shadowBlur = size * 0.5;
  g.lineWidth = size * 0.08; g.strokeStyle = 'rgba(20,10,5,0.95)';
  g.strokeText(s, 0, 0);
  g.shadowBlur = size * 0.35;
  if (tint) {
    const gr = g.createLinearGradient(0, -size / 2, 0, size / 2);
    gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.5, tint); gr.addColorStop(1, shade(tint, -0.45));
    g.fillStyle = gr;
  } else g.fillStyle = goldGrad(-size / 2, size / 2);
  g.fillText(s, 0, 0);
  // destello que cruza al aparecer
  if (p < 1) {
    g.globalCompositeOperation = 'lighter';
    g.globalAlpha = 0.5 * Math.sin(p * Math.PI);
    g.shadowBlur = 0;
    g.fillStyle = '#fff';
    g.fillText(s, 0, 0);
  }
  g.restore();
}
function shade(hex, k) {
  const n = parseInt(hex.slice(1), 16);
  let r = n >> 16, gg = (n >> 8) & 255, b = n & 255;
  const f = v => Math.round(k < 0 ? v * (1 + k) : v + (255 - v) * k);
  return `rgb(${f(r)},${f(gg)},${f(b)})`;
}
function rgba(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`;
}

// ---------------------------------------------------------------- fondo
const STARS = Array.from({ length: 160 }, (_, i) => [hash(i) * W, hash(i + 500) * H * 0.75, hash(i + 900)]);
function fondo(t, o = {}) {
  const { dim = 0, cx = 1340, cy = 300, sc = 1, mist = 1 } = o;
  let gr = g.createLinearGradient(0, 0, 0, H);
  gr.addColorStop(0, '#05040b'); gr.addColorStop(0.45, '#120d24'); gr.addColorStop(0.8, '#0d1d1c'); gr.addColorStop(1, '#070d0d');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  // estrellas
  for (const [x, y, k] of STARS) {
    const a = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(t * (0.6 + k * 1.7) + k * 40));
    g.fillStyle = `rgba(210,220,255,${a * 0.7})`;
    g.fillRect(x, y, 1.2 + k * 1.6, 1.2 + k * 1.6);
  }
  // resplandor verde de la necrópolis
  const bob = Math.sin(t * 0.35) * 10;
  const x0 = cx + Math.sin(t * 0.05) * 30, y0 = cy + bob;
  gr = g.createRadialGradient(x0, y0 + 40 * sc, 20, x0, y0 + 40 * sc, 620 * sc);
  gr.addColorStop(0, 'rgba(90,255,170,0.22)'); gr.addColorStop(0.4, 'rgba(60,160,140,0.09)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  necropolis(x0, y0, sc, t);
  // niebla
  for (let i = 0; i < 9; i++) {
    const s = 0.4 + hash(i + 70) * 0.6;
    const x = ((hash(i) * W * 1.6 + t * (8 + 14 * s)) % (W * 1.6)) - W * 0.3;
    const y = H * (0.55 + 0.45 * hash(i + 30));
    const r = 380 + 420 * s;
    const green = i % 3 !== 0;
    gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, green ? `rgba(120,210,180,${0.075 * mist})` : `rgba(140,90,200,${0.08 * mist})`);
    gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2);
  }
  // partículas que suben
  for (let i = 0; i < 70; i++) {
    const sp = 18 + hash(i + 3) * 40;
    const x = hash(i + 11) * W + Math.sin(t * 0.5 + i) * 20;
    const y = H + 40 - ((t * sp + hash(i + 7) * H * 1.2) % (H * 1.2));
    const a = 0.25 + 0.5 * hash(i + 19);
    g.fillStyle = i % 4 === 0 ? `rgba(200,150,255,${a})` : `rgba(130,255,190,${a})`;
    g.beginPath(); g.arc(x, y, 1.2 + hash(i + 23) * 2.2, 0, 7); g.fill();
  }
  // viñeta
  gr = g.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,0.75)');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (dim > 0) { g.fillStyle = `rgba(4,3,8,${dim})`; g.fillRect(0, 0, W, H); }
}
// ciudadela flotante (silueta propia, sin logotipos)
function necropolis(x, y, s, t) {
  g.save(); g.translate(x, y); g.scale(s, s);
  const body = '#161224', rim = 'rgba(120,255,190,0.55)';
  const capas = [[-300, 300, 0, 40], [-260, 260, 40, 95], [-210, 210, 95, 150], [-150, 150, 150, 205], [-90, 90, 205, 255], [-40, 40, 255, 300]];
  g.shadowColor = 'rgba(80,255,170,0.5)'; g.shadowBlur = 25;
  for (const [a, b, y0, y1] of capas) {
    g.beginPath();
    g.moveTo(a, y0); g.lineTo(b, y0); g.lineTo(b * 0.86, y1); g.lineTo(a * 0.86, y1); g.closePath();
    g.fillStyle = body; g.fill();
    g.shadowBlur = 0;
    g.strokeStyle = rim; g.lineWidth = 1.5; g.beginPath(); g.moveTo(a, y0); g.lineTo(b, y0); g.stroke();
  }
  // punta inferior
  g.beginPath(); g.moveTo(-34, 300); g.lineTo(34, 300); g.lineTo(0, 380); g.closePath(); g.fillStyle = body; g.fill();
  // agujas superiores
  const agujas = [[-250, 70], [-190, 110], [-120, 160], [-50, 120], [0, 210], [50, 130], [120, 170], [190, 100], [250, 80]];
  for (const [ax, h] of agujas) {
    g.beginPath(); g.moveTo(ax - 18, 2); g.lineTo(ax, -h); g.lineTo(ax + 18, 2); g.closePath();
    g.fillStyle = body; g.fill();
    g.fillStyle = `rgba(110,255,180,${0.5 + 0.4 * Math.sin(t * 2 + ax)})`;
    g.beginPath(); g.arc(ax, -h * 0.55, 3, 0, 7); g.fill();
  }
  // ventanas
  for (let r = 0; r < 5; r++) {
    const [a, b, y0, y1] = capas[r];
    const yy = (y0 + y1) / 2;
    for (let xx = a * 0.8; xx < b * 0.8; xx += 34) {
      const on = hash(xx * 3 + r * 17) > 0.35;
      if (!on) continue;
      const fl = 0.55 + 0.45 * Math.sin(t * 1.3 + xx + r * 5);
      g.fillStyle = `rgba(120,255,180,${0.35 + 0.5 * fl})`;
      g.fillRect(xx - 4, yy - 7, 8, 14);
    }
  }
  g.restore();
}
function veil(a) { if (a > 0) { g.fillStyle = `rgba(0,0,0,${clamp(a)})`; g.fillRect(0, 0, W, H); } }

// ---------------------------------------------------------------- ventanas del addon
function rr(x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function gem(x, y, s) {
  g.save(); g.translate(x, y); g.rotate(Math.PI / 4);
  g.fillStyle = goldGrad(-s, s); g.fillRect(-s, -s, s * 2, s * 2);
  g.fillStyle = '#5b2a86'; g.fillRect(-s * 0.45, -s * 0.45, s * 0.9, s * 0.9);
  g.restore();
}
function frame(x, y, w, h, o = {}) {
  const { title = null, alpha = 1, glow = 0, titleSize = 34 } = o;
  if (alpha <= 0) return;
  g.save();
  g.globalAlpha *= alpha;
  g.shadowColor = glow ? `rgba(232,196,106,${0.6 * glow})` : 'rgba(0,0,0,0.8)';
  g.shadowBlur = glow ? 40 : 34; g.shadowOffsetY = glow ? 0 : 10;
  rr(x, y, w, h, 12); g.fillStyle = C.frame; g.fill();
  g.shadowBlur = 0; g.shadowOffsetY = 0;
  let gr = g.createLinearGradient(0, y, 0, y + h);
  gr.addColorStop(0, 'rgba(110,70,170,0.20)'); gr.addColorStop(0.35, 'rgba(40,25,70,0.05)'); gr.addColorStop(1, 'rgba(0,0,0,0.2)');
  rr(x, y, w, h, 12); g.fillStyle = gr; g.fill();
  g.lineWidth = 5; g.strokeStyle = goldGrad(y, y + h); rr(x, y, w, h, 12); g.stroke();
  g.lineWidth = 1.5; g.strokeStyle = 'rgba(232,196,106,0.4)'; rr(x + 9, y + 9, w - 18, h - 18, 7); g.stroke();
  gem(x, y, 9); gem(x + w, y, 9); gem(x, y + h, 9); gem(x + w, y + h, 9);
  if (title) {
    g.font = font(titleSize, 'Cinzel', 700);
    const tw = Math.max(260, g.measureText(title).width + 90);
    const tx = x + w / 2 - tw / 2, ty = y - titleSize * 0.85;
    rr(tx, ty, tw, titleSize * 1.7, 10);
    gr = g.createLinearGradient(0, ty, 0, ty + titleSize * 1.7);
    gr.addColorStop(0, '#3a2352'); gr.addColorStop(1, '#170d24');
    g.fillStyle = gr; g.fill();
    g.lineWidth = 3; g.strokeStyle = goldGrad(ty, ty + titleSize * 1.7); g.stroke();
    txt(title, x + w / 2, ty + titleSize * 0.87, { size: titleSize, fam: 'Cinzel', w: 700, color: C.gold });
  }
  g.restore();
}
const BTN = { MS: ['#2f8a45', '#123d1d'], OS: ['#3569b8', '#132a52'], PASS: ['#6d6878', '#2a2731'], red: ['#9a2a24', '#3f0e0b'], gold: ['#b48a2e', '#4a3208'] };
function button(x, y, w, h, label, o = {}) {
  const { kind = 'red', hi = 0, press = 0, alpha = 1, size = 38, dimmed = 0 } = o;
  if (alpha <= 0) return;
  const [c1, c2] = BTN[kind];
  g.save(); g.globalAlpha *= alpha * (1 - 0.6 * dimmed);
  const sc = 1 + 0.07 * hi - 0.05 * press;
  g.translate(x + w / 2, y + h / 2); g.scale(sc, sc); g.translate(-w / 2, -h / 2);
  if (hi > 0) { g.shadowColor = `rgba(255,220,120,${0.9 * hi})`; g.shadowBlur = 40 * hi; }
  rr(0, 0, w, h, 10);
  const gr = g.createLinearGradient(0, 0, 0, h);
  gr.addColorStop(0, press ? c2 : shade(c1, 0.15)); gr.addColorStop(1, press ? c1 : c2);
  g.fillStyle = gr; g.fill(); g.shadowBlur = 0;
  g.lineWidth = 3 + 2 * hi; g.strokeStyle = goldGrad(0, h); g.stroke();
  // brillo superior
  rr(6, 5, w - 12, h * 0.38, 7); g.fillStyle = 'rgba(255,255,255,0.12)'; g.fill();
  txt(label, w / 2, h / 2 + 2, { size, fam: 'Cinzel', w: 700, color: hi > 0.3 ? '#fff6d2' : C.goldL });
  g.restore();
}
function chip(s, x, y, o = {}) {
  const { size = 30, color = C.text, bg = 'rgba(20,14,34,0.88)', border = C.gold, alpha = 1, align = 'center' } = o;
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha;
  g.font = font(size, ...famNum(s, 'Alegreya Sans', 700));
  const w = g.measureText(s).width + size * 1.4, h = size * 1.6;
  const x0 = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  rr(x0, y - h / 2, w, h, h / 2); g.fillStyle = bg; g.fill();
  g.lineWidth = 2.5; g.strokeStyle = border; g.stroke();
  txt(s, x0 + w / 2, y + 1, { size, w: 700, color });
  g.restore();
}
function cursor(x, y, press = 0, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y);
  const s = 1.25 - 0.15 * press; g.scale(s, s);
  if (press > 0) {
    g.strokeStyle = `rgba(255,230,150,${press})`; g.lineWidth = 3;
    g.beginPath(); g.arc(0, 0, 30 * (1.4 - press * 0.4), 0, 7); g.stroke();
  }
  g.beginPath(); g.moveTo(0, 0); g.lineTo(0, 42); g.lineTo(11, 32); g.lineTo(19, 50); g.lineTo(26, 46); g.lineTo(18, 29); g.lineTo(32, 29); g.closePath();
  g.fillStyle = goldGrad(0, 50); g.shadowColor = 'rgba(0,0,0,0.9)'; g.shadowBlur = 8; g.fill();
  g.shadowBlur = 0; g.lineWidth = 2; g.strokeStyle = '#2a1805'; g.stroke();
  g.restore();
}
function checkmark(x, y, s, p = 1, color = '#6dff8e') {
  if (p <= 0) return;
  g.save(); g.lineCap = 'round'; g.lineJoin = 'round'; g.lineWidth = s * 0.22; g.strokeStyle = color;
  g.shadowColor = color; g.shadowBlur = 12;
  g.beginPath();
  const a = [x - s * 0.45, y], b = [x - s * 0.1, y + s * 0.35], c = [x + s * 0.5, y - s * 0.4];
  const p1 = clamp(p * 2), p2 = clamp(p * 2 - 1);
  g.moveTo(...a); g.lineTo(lerp(a[0], b[0], p1), lerp(a[1], b[1], p1));
  if (p2 > 0) g.lineTo(lerp(b[0], c[0], p2), lerp(b[1], c[1], p2));
  g.stroke(); g.restore();
}
function cross(x, y, s, p = 1, color = C.red) {
  if (p <= 0) return;
  g.save(); g.lineCap = 'round'; g.lineWidth = s * 0.2; g.strokeStyle = color; g.shadowColor = color; g.shadowBlur = 14;
  const p1 = clamp(p * 2), p2 = clamp(p * 2 - 1);
  g.beginPath(); g.moveTo(x - s / 2, y - s / 2); g.lineTo(x - s / 2 + s * p1, y - s / 2 + s * p1);
  if (p2 > 0) { g.moveTo(x + s / 2, y - s / 2); g.lineTo(x + s / 2 - s * p2, y - s / 2 + s * p2); }
  g.stroke(); g.restore();
}
function arrow(x0, y0, x1, y1, p = 1, color = C.gold, wdt = 8) {
  if (p <= 0) return;
  const x = lerp(x0, x1, p), y = lerp(y0, y1, p), an = Math.atan2(y1 - y0, x1 - x0);
  g.save(); g.strokeStyle = color; g.fillStyle = color; g.lineWidth = wdt; g.lineCap = 'round';
  g.shadowColor = color; g.shadowBlur = 16;
  g.beginPath(); g.moveTo(x0, y0); g.lineTo(x - Math.cos(an) * wdt * 2, y - Math.sin(an) * wdt * 2); g.stroke();
  g.translate(x, y); g.rotate(an);
  g.beginPath(); g.moveTo(0, 0); g.lineTo(-wdt * 3.2, -wdt * 2.2); g.lineTo(-wdt * 3.2, wdt * 2.2); g.closePath(); g.fill();
  g.restore();
}

// ---------------------------------------------------------------- objetos
const ITEMS = {
  hoja: ['Hoja del Nigromante', 'espada'],
  anillo: ['Anillo de la Escarcha Eterna', 'anillo'],
  capa: ['Capa de la Necrópolis', 'capa'],
  baculo: ['Báculo del Vacío Frío', 'baculo'],
  escudo: ['Escudo del Caballero Caído', 'escudo'],
  marca: ['Marca de conjunto', 'marca'],
  pechera: ['Pieza de armadura', 'pechera']
};
function itemIcon(x, y, s, kind, o = {}) {
  const { alpha = 1, glow = 0, border = C.epic, rot = 0 } = o;
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.rotate(rot);
  const h = s / 2;
  if (glow > 0) { g.shadowColor = border; g.shadowBlur = 50 * glow; }
  rr(-h, -h, s, s, s * 0.1);
  const gr = g.createRadialGradient(0, -h * 0.3, 0, 0, 0, s * 0.8);
  gr.addColorStop(0, '#3b2d52'); gr.addColorStop(1, '#0e0a16');
  g.fillStyle = gr; g.fill(); g.shadowBlur = 0;
  g.save(); rr(-h, -h, s, s, s * 0.1); g.clip();
  g.scale(s / 100, s / 100);
  simbolo(kind);
  g.restore();
  g.lineWidth = Math.max(3, s * 0.06); g.strokeStyle = border; rr(-h, -h, s, s, s * 0.1); g.stroke();
  g.lineWidth = 1.5; g.strokeStyle = 'rgba(255,255,255,0.25)'; rr(-h + s * 0.07, -h + s * 0.07, s * 0.86, s * 0.86, s * 0.06); g.stroke();
  g.restore();
}
function simbolo(k) {
  const steel = () => { const gr = g.createLinearGradient(-10, 0, 10, 0); gr.addColorStop(0, '#9fb4c9'); gr.addColorStop(0.5, '#f4fbff'); gr.addColorStop(1, '#6f8599'); return gr; };
  g.lineJoin = 'round';
  if (k === 'espada') {
    g.rotate(-Math.PI / 4);
    g.shadowColor = '#7dffc0'; g.shadowBlur = 14;
    g.fillStyle = steel(); g.beginPath(); g.moveTo(-6, 18); g.lineTo(-6, -34); g.lineTo(0, -44); g.lineTo(6, -34); g.lineTo(6, 18); g.fill();
    g.shadowBlur = 0;
    g.fillStyle = '#6dffb0'; g.fillRect(-1.5, -30, 3, 44);
    g.fillStyle = goldGrad(16, 26); g.fillRect(-20, 16, 40, 8);
    g.fillStyle = '#4a2d18'; g.fillRect(-4, 24, 8, 16);
    g.fillStyle = C.gold; g.beginPath(); g.arc(0, 43, 5, 0, 7); g.fill();
  } else if (k === 'anillo') {
    g.lineWidth = 11; g.strokeStyle = goldGrad(-30, 30); g.beginPath(); g.ellipse(0, 8, 26, 22, 0, 0, 7); g.stroke();
    g.shadowColor = '#8fd8ff'; g.shadowBlur = 18; g.fillStyle = '#9fe6ff';
    g.beginPath(); g.moveTo(0, -30); g.lineTo(12, -16); g.lineTo(0, -4); g.lineTo(-12, -16); g.closePath(); g.fill();
  } else if (k === 'capa') {
    const gr = g.createLinearGradient(0, -36, 0, 40); gr.addColorStop(0, '#7a3cc0'); gr.addColorStop(1, '#2a0f45');
    g.fillStyle = gr; g.beginPath(); g.moveTo(-18, -34); g.lineTo(18, -34); g.lineTo(34, 38); g.quadraticCurveTo(0, 28, -34, 38); g.closePath(); g.fill();
    g.fillStyle = goldGrad(-40, -28); g.fillRect(-20, -38, 40, 8);
    g.strokeStyle = 'rgba(109,255,176,0.8)'; g.lineWidth = 2; g.beginPath(); g.moveTo(0, -28); g.lineTo(0, 30); g.stroke();
  } else if (k === 'baculo') {
    g.rotate(Math.PI / 5);
    g.fillStyle = '#5a3a22'; g.fillRect(-4, -20, 8, 64);
    g.shadowColor = '#b58cff'; g.shadowBlur = 20; g.fillStyle = '#c9a7ff';
    g.beginPath(); g.arc(0, -30, 12, 0, 7); g.fill();
    g.strokeStyle = goldGrad(-44, -16); g.lineWidth = 4; g.beginPath(); g.arc(0, -30, 16, Math.PI * 0.1, Math.PI * 0.9, true); g.stroke();
  } else if (k === 'escudo') {
    g.fillStyle = '#26324a'; g.beginPath(); g.moveTo(-30, -34); g.lineTo(30, -34); g.lineTo(30, 4); g.quadraticCurveTo(28, 30, 0, 42); g.quadraticCurveTo(-28, 30, -30, 4); g.closePath(); g.fill();
    g.lineWidth = 5; g.strokeStyle = goldGrad(-34, 42); g.stroke();
    g.fillStyle = '#6dffb0'; g.beginPath(); g.arc(0, 0, 9, 0, 7); g.fill();
  } else if (k === 'marca') {
    g.shadowColor = '#7dffc0'; g.shadowBlur = 22;
    g.fillStyle = goldGrad(-36, 36); g.beginPath();
    for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2 - Math.PI / 2; g.lineTo(Math.cos(a) * 36, Math.sin(a) * 36); }
    g.closePath(); g.fill(); g.shadowBlur = 0;
    g.fillStyle = '#1a2a24'; g.beginPath();
    for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2 - Math.PI / 2; g.lineTo(Math.cos(a) * 26, Math.sin(a) * 26); }
    g.closePath(); g.fill();
    g.fillStyle = '#6dffb0'; g.beginPath(); g.moveTo(0, -16); g.lineTo(13, 10); g.lineTo(-13, 10); g.closePath(); g.fill();
    g.fillStyle = '#1a2a24'; g.beginPath(); g.arc(0, 3, 4, 0, 7); g.fill();
  } else if (k === 'pechera') {
    const gr = g.createLinearGradient(0, -36, 0, 40); gr.addColorStop(0, '#9fb4c9'); gr.addColorStop(1, '#3d4c5c');
    g.fillStyle = gr; g.beginPath();
    g.moveTo(-34, -26); g.lineTo(-14, -34); g.quadraticCurveTo(0, -24, 14, -34); g.lineTo(34, -26); g.lineTo(28, -4); g.lineTo(22, 38); g.lineTo(-22, 38); g.lineTo(-28, -4); g.closePath(); g.fill();
    g.strokeStyle = C.gold; g.lineWidth = 3; g.stroke();
    g.fillStyle = '#6dffb0'; g.beginPath(); g.arc(0, 6, 7, 0, 7); g.fill();
  }
}
// cofre del botín
function cofre(x, y, s, open = 0) {
  g.save(); g.translate(x, y); g.scale(s, s);
  g.fillStyle = '#4a2d18'; rr(-60, -20, 120, 70, 8); g.fill();
  g.strokeStyle = C.gold; g.lineWidth = 5; g.stroke();
  g.save(); g.translate(0, -20); g.rotate(-0.6 * open);
  g.fillStyle = '#5c3a20'; g.beginPath(); g.moveTo(-60, 0); g.quadraticCurveTo(0, -46, 60, 0); g.closePath(); g.fill(); g.stroke();
  g.restore();
  g.fillStyle = C.gold; g.fillRect(-9, -8, 18, 22);
  if (open > 0) {
    const gr = g.createRadialGradient(0, -30, 0, 0, -30, 120);
    gr.addColorStop(0, `rgba(255,220,120,${0.6 * open})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(-140, -150, 280, 200);
  }
  g.restore();
}

// ---------------------------------------------------------------- personajes
// x,y = pies. Silueta encapuchada con el color de su clase.
function hero(x, y, s, cls, o = {}) {
  const { name = null, alpha = 1, glow = 0, tag = null, nameSize = 30, sub = null, gray = 0, bob = 0 } = o;
  if (alpha <= 0) return;
  const col = CLS[cls] || '#ccc';
  const c = gray ? '#888' : col;
  g.save(); g.globalAlpha *= alpha * (1 - 0.55 * gray);
  g.translate(x, y + bob); g.scale(s, s);
  // sombra en el suelo
  g.fillStyle = 'rgba(0,0,0,0.55)'; g.beginPath(); g.ellipse(0, 0, 52, 12, 0, 0, 7); g.fill();
  if (glow > 0) {
    const gr = g.createRadialGradient(0, -80, 10, 0, -80, 170);
    gr.addColorStop(0, rgba(col, 0.45 * glow)); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(-180, -260, 360, 300);
  }
  // capa / cuerpo
  const gr = g.createLinearGradient(0, -140, 0, 0);
  gr.addColorStop(0, '#2a2238'); gr.addColorStop(1, '#0d0a14');
  g.fillStyle = gr;
  g.beginPath();
  g.moveTo(-30, -118); g.quadraticCurveTo(-44, -60, -50, -2); g.quadraticCurveTo(0, 8, 50, -2); g.quadraticCurveTo(44, -60, 30, -118); g.closePath();
  g.fill();
  g.lineWidth = 3.5; g.strokeStyle = c; g.stroke();
  // franja frontal
  g.fillStyle = rgba(c.startsWith('#') ? c : '#888888', 0.85);
  g.beginPath(); g.moveTo(-6, -112); g.lineTo(6, -112); g.lineTo(10, -4); g.lineTo(-10, -4); g.closePath(); g.fill();
  // hombreras
  g.fillStyle = shade(c.startsWith('#') ? c : '#888888', -0.35);
  g.beginPath(); g.ellipse(-34, -114, 20, 12, -0.3, 0, 7); g.fill(); g.stroke();
  g.beginPath(); g.ellipse(34, -114, 20, 12, 0.3, 0, 7); g.fill(); g.stroke();
  // capucha y rostro
  g.fillStyle = '#1b1526';
  g.beginPath(); g.moveTo(-24, -118); g.quadraticCurveTo(-28, -160, 0, -176); g.quadraticCurveTo(28, -160, 24, -118); g.closePath(); g.fill();
  g.lineWidth = 3; g.strokeStyle = c; g.stroke();
  g.fillStyle = '#07050b'; g.beginPath(); g.ellipse(0, -136, 14, 16, 0, 0, 7); g.fill();
  g.fillStyle = gray ? '#999' : '#fff'; g.shadowColor = c; g.shadowBlur = 8;
  g.fillRect(-8, -140, 5, 3); g.fillRect(3, -140, 5, 3);
  g.shadowBlur = 0;
  g.restore();
  if (name) txt(name, x, y + bob - 190 * s - nameSize * 0.4, { size: nameSize, w: 700, color: gray ? '#999' : col, alpha: alpha * (1 - 0.5 * gray) });
  if (sub) txt(sub, x, y + bob + 30 * s + 8, { size: nameSize * 0.8, w: 500, color: C.dim, alpha });
  if (tag) chip(tag, x, y + bob - 190 * s - nameSize * 1.6, { size: nameSize * 0.7, alpha, color: C.goldL });
}
function heroPJ(key, x, y, s, o = {}) { const [n, c] = PJ[key]; hero(x, y, s, c, Object.assign({ name: n }, o)); }

// jefe gigante (silueta propia)
function jefe(x, y, s, o = {}) {
  const { alpha = 1, rot = 0, eyes = 1, t = 0 } = o;
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.rotate(rot); g.scale(s, s);
  const gr = g.createLinearGradient(0, -700, 0, 0);
  gr.addColorStop(0, '#2c2440'); gr.addColorStop(1, '#0a0810');
  g.fillStyle = gr;
  g.shadowColor = 'rgba(100,255,180,0.35)'; g.shadowBlur = 40;
  g.beginPath();
  g.moveTo(-230, 0); g.lineTo(-200, -300); g.lineTo(-330, -420); g.lineTo(-360, -250); g.lineTo(-400, -240); g.lineTo(-360, -470);
  g.lineTo(-210, -520); g.lineTo(-150, -560); g.lineTo(-90, -600); g.lineTo(-120, -700); g.lineTo(-40, -640);
  g.lineTo(0, -655); g.lineTo(40, -640); g.lineTo(120, -700); g.lineTo(90, -600); g.lineTo(150, -560); g.lineTo(210, -520);
  g.lineTo(360, -470); g.lineTo(400, -240); g.lineTo(360, -250); g.lineTo(330, -420); g.lineTo(200, -300); g.lineTo(230, 0);
  g.closePath(); g.fill();
  g.shadowBlur = 0;
  g.strokeStyle = 'rgba(120,255,190,0.5)'; g.lineWidth = 3; g.stroke();
  // runas del pecho
  g.strokeStyle = `rgba(110,255,180,${0.5 + 0.3 * Math.sin(t * 3)})`; g.lineWidth = 4;
  g.beginPath(); g.moveTo(-60, -420); g.lineTo(0, -360); g.lineTo(60, -420); g.moveTo(0, -360); g.lineTo(0, -260); g.stroke();
  // ojos
  g.fillStyle = `rgba(140,255,200,${eyes})`; g.shadowColor = '#6dffb0'; g.shadowBlur = 30 * eyes;
  g.beginPath(); g.ellipse(-36, -590, 16, 7, 0.25, 0, 7); g.fill();
  g.beginPath(); g.ellipse(36, -590, 16, 7, -0.25, 0, 7); g.fill();
  g.restore();
}

// cuerpo del jefe caído: un montículo oscuro con destellos de botín
function cuerpo(x, y, s, t, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  const gr = g.createRadialGradient(0, -20, 10, 0, -20, 220);
  gr.addColorStop(0, 'rgba(109,255,176,0.35)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = gr; g.fillRect(-240, -220, 480, 260);
  g.fillStyle = '#1c1628'; g.beginPath(); g.ellipse(0, 0, 170, 60, 0, Math.PI, 0); g.fill();
  g.strokeStyle = 'rgba(120,255,190,0.5)'; g.lineWidth = 3; g.stroke();
  // cuernos caídos
  g.fillStyle = '#1c1628';
  g.beginPath(); g.moveTo(-120, -20); g.lineTo(-190, -80); g.lineTo(-100, -40); g.closePath(); g.fill(); g.stroke();
  g.beginPath(); g.moveTo(110, -30); g.lineTo(200, -70); g.lineTo(130, -10); g.closePath(); g.fill(); g.stroke();
  for (let i = 0; i < 7; i++) {
    const a = 0.5 + 0.5 * Math.sin(t * 3 + i * 2.1);
    g.fillStyle = `rgba(255,230,150,${a})`;
    g.beginPath(); g.arc(-110 + i * 36, -30 - 20 * hash(i + 3), 3 + 2 * a, 0, 7); g.fill();
  }
  g.restore();
}

// dado (cubo con puntos que gira)
function dado(x, y, s, spin, o = {}) {
  const { alpha = 1 } = o;
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.rotate(spin); g.scale(s, s);
  g.shadowColor = 'rgba(0,0,0,0.8)'; g.shadowBlur = 16;
  rr(-40, -40, 80, 80, 14); g.fillStyle = '#f4ecd8'; g.fill(); g.shadowBlur = 0;
  g.lineWidth = 4; g.strokeStyle = C.gold2; g.stroke();
  g.fillStyle = '#7a1f1f';
  const face = Math.floor(Math.abs(spin * 3)) % 6 + 1;
  const pts = { 1: [[0, 0]], 2: [[-18, -18], [18, 18]], 3: [[-18, -18], [0, 0], [18, 18]], 4: [[-18, -18], [18, -18], [-18, 18], [18, 18]], 5: [[-18, -18], [18, -18], [0, 0], [-18, 18], [18, 18]], 6: [[-18, -20], [18, -20], [-18, 0], [18, 0], [-18, 20], [18, 20]] }[face];
  for (const [px, py] of pts) { g.beginPath(); g.arc(px, py, 7, 0, 7); g.fill(); }
  g.restore();
}
// número que gira como tirada 1-100 y se detiene en `final`
function rollNum(t, t0, dur, final, seed = 1) {
  if (t < t0) return null;
  if (t >= t0 + dur) return final;
  const k = Math.floor((t - t0) * 22);
  return 1 + Math.floor(hash(k * 7.3 + seed * 13) * 100);
}
// diamante flotante sobre quien reparte
function diamante(x, y, s, t, alpha = 1) {
  if (alpha <= 0) return;
  const b = Math.sin(t * 3) * 8;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y + b); g.scale(s, s);
  g.shadowColor = '#ffd76a'; g.shadowBlur = 35;
  g.beginPath(); g.moveTo(0, -34); g.lineTo(24, 0); g.lineTo(0, 34); g.lineTo(-24, 0); g.closePath();
  g.fillStyle = goldGrad(-34, 34); g.fill();
  g.shadowBlur = 0;
  g.fillStyle = 'rgba(255,255,255,0.6)'; g.beginPath(); g.moveTo(0, -34); g.lineTo(10, -6); g.lineTo(0, 0); g.lineTo(-10, -6); g.closePath(); g.fill();
  g.restore();
}
// emblema de la hermandad (diseño propio)
function emblema(x, y, s, t, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  // alas / púas
  g.fillStyle = '#1d1430';
  for (const d of [-1, 1]) {
    g.beginPath(); g.moveTo(d * 70, -70);
    for (let i = 0; i < 4; i++) { g.lineTo(d * (150 + i * 20), -110 + i * 55); g.lineTo(d * (95 + i * 8), -60 + i * 50); }
    g.lineTo(d * 70, 90); g.closePath(); g.fill();
    g.strokeStyle = 'rgba(232,196,106,0.7)'; g.lineWidth = 3; g.stroke();
  }
  // escudo
  g.shadowColor = 'rgba(181,97,255,0.8)'; g.shadowBlur = 50;
  g.beginPath(); g.moveTo(-100, -120); g.lineTo(100, -120); g.lineTo(100, 10); g.quadraticCurveTo(95, 100, 0, 150); g.quadraticCurveTo(-95, 100, -100, 10); g.closePath();
  const gr = g.createLinearGradient(0, -120, 0, 150); gr.addColorStop(0, '#3d1f63'); gr.addColorStop(1, '#12081f');
  g.fillStyle = gr; g.fill(); g.shadowBlur = 0;
  g.lineWidth = 9; g.strokeStyle = goldGrad(-120, 150); g.stroke();
  g.lineWidth = 2; g.strokeStyle = 'rgba(232,196,106,0.5)';
  g.beginPath(); g.moveTo(-82, -104); g.lineTo(82, -104); g.lineTo(82, 8); g.quadraticCurveTo(78, 86, 0, 128); g.quadraticCurveTo(-78, 86, -82, 8); g.closePath(); g.stroke();
  // luna eclipsada
  g.fillStyle = goldGrad(-60, 40); g.beginPath(); g.arc(0, -10, 50, 0, 7); g.fill();
  g.fillStyle = '#2a1545'; g.beginPath(); g.arc(18, -22, 44, 0, 7); g.fill();
  // ojo / gema
  g.shadowColor = '#6dffb0'; g.shadowBlur = 25 + 10 * Math.sin(t * 2);
  g.fillStyle = '#6dffb0'; g.beginPath(); g.moveTo(0, 50); g.lineTo(16, 74); g.lineTo(0, 98); g.lineTo(-16, 74); g.closePath(); g.fill();
  g.restore();
}
// sello del addon: dado dentro de un círculo dorado
function selloAddon(x, y, s, t, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  g.shadowColor = 'rgba(232,196,106,0.7)'; g.shadowBlur = 50;
  g.beginPath(); g.arc(0, 0, 120, 0, 7);
  const gr = g.createRadialGradient(0, -30, 10, 0, 0, 120); gr.addColorStop(0, '#4b2a77'); gr.addColorStop(1, '#140a22');
  g.fillStyle = gr; g.fill(); g.shadowBlur = 0;
  g.lineWidth = 10; g.strokeStyle = goldGrad(-120, 120); g.stroke();
  g.lineWidth = 2; g.strokeStyle = 'rgba(232,196,106,0.6)'; g.beginPath(); g.arc(0, 0, 100, 0, 7); g.stroke();
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2 + t * 0.2; gem(Math.cos(a) * 110, Math.sin(a) * 110, 4); }
  g.restore();
  dado(x, y, s * 1.1, 0.35 + Math.sin(t) * 0.05, { alpha });
}
