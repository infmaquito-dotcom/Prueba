// Las 10 escenas del video. Cada una usa los tiempos reales de la narración (CUE).

// ============================================================ 1. GANCHO
function escGancho(t) {
  const caida = 1.5;
  const shake = t > caida ? Math.sin(t * 70) * 16 * (1 - P(t, caida, 0.9)) : 0;
  g.save(); g.translate(shake, shake * 0.4);
  fondo(t, { cx: 1450, cy: 230, sc: 0.8 });
  txt('NAXXRAMAS', 960, 110, { size: 44, fam: 'Cinzel', w: 700, color: '#bfffe0', alpha: vis(t, 0.3, 3.0, 0.6), glow: 20, glowColor: '#6dffb0' });
  // el jefe cae
  const pf = P(t, caida, 1.3);
  jefe(960, 1080 + 420 * eIn(pf), 1.12, { alpha: 1 - sm(pf * 1.2), rot: -0.22 * eIn(pf), eyes: 1 - pf, t });
  g.restore();
  // destello
  const fl = t > caida ? Math.exp(-(t - caida) * 5) : 0;
  if (fl > 0.01) { g.fillStyle = `rgba(200,255,225,${0.7 * fl})`; g.fillRect(0, 0, W, H); }

  // columnas de luz y botín
  const items = ['hoja', 'anillo', 'capa', 'baculo'];
  const xs = [600, 840, 1080, 1320];
  const tomado = P(t, at('g1', 0.62), 0.8);   // un objeto se va con "otro"
  for (let i = 0; i < 4; i++) {
    const p = P(t, 1.8 + i * 0.18, 1.2);
    if (p <= 0) continue;
    const col = i % 2 ? '255,210,110' : '181,97,255';
    const gr = g.createLinearGradient(0, 1000, 0, 200);
    gr.addColorStop(0, `rgba(${col},${0.5 * p})`); gr.addColorStop(1, `rgba(${col},0)`);
    const bw = 70 + 20 * Math.sin(t * 3 + i);
    g.fillStyle = gr; g.fillRect(xs[i] - bw / 2, 1000 - 800 * eOut(p), bw, 800 * eOut(p));
    let x = xs[i], y = lerp(900, 470, eOut(p)) + Math.sin(t * 2 + i) * 10;
    let a = 1;
    if (i === 1 && tomado > 0) { x = lerp(x, 1480, eOut(tomado)); y = lerp(y, 700, eOut(tomado)); a = 1 - P(t, at('g1', 0.62) + 0.7, 0.3); }
    itemIcon(x, y, 110, ITEMS[items[i]][1], { glow: 0.8, border: i % 2 ? '#ff8000' : C.epic, alpha: a * clamp(p * 2) });
  }
  // "tú" y "otro"
  const pp = vis(t, at('g1', 0.4), ESC.gancho.fin, 0.5);
  hero(330, 1000, 1.25, 'mago', { name: 'Tú', alpha: pp, nameSize: 44 });
  hero(1590, 1000, 1.25, 'guerrero', { name: 'Otro', alpha: pp, glow: tomado, nameSize: 44 });
  const q = P(t, at('g1', 0.75), 0.5);
  if (q > 0) txt('?', 330 + Math.sin(t * 4) * 4, 690, { size: 150 * eBack(q), fam: 'Cinzel', w: 700, color: C.gold, glow: 30, glowColor: '#e8c46a', alpha: pp });
  if (q > 0) chip('¿Por qué él?', 330, 580, { size: 34, alpha: pp * P(t, at('g1', 0.85), 0.4) });
  // eso se acabó
  const k = P(t, at('g2', 0.35), 0.7);
  veil(0.6 * k);
  keyword('ESO SE ACABÓ', 960, 520, 118, k);
  veil(1 - P(t, 0, 1.0));
}

// ============================================================ 2. EL PROBLEMA
function escProblema(t) {
  fondo(t, { dim: 0.35, cx: 1600, cy: 200, sc: 0.6 });
  const clases = Object.keys(CLS);
  const p2 = P(t, at('p2', 0.25), 0.8);
  // 40 jugadores
  for (let i = 0; i < 40; i++) {
    const c = i % 10, r = Math.floor(i / 10);
    const x = 330 + c * 140 + (r % 2) * 40, y = 560 + r * 130;
    const p = P(t, at('p1', 0.02) + i * 0.035, 0.35);
    const cls = clases[Math.floor(hash(i + 4) * 9)];
    const nerv = P(t, at('p3', 0), 0.5);
    hero(x + Math.sin(t * 9 + i) * 3 * nerv, y, 0.5, cls, { alpha: eOut(p) * (1 - 0.6 * p2) });
  }
  keyword('40 JUGADORES', 520, 180, 76, P(t, at('p1', 0.2), 0.6), { alpha: 1 - 0.85 * p2 });
  // 3-4 objetos
  const pi = P(t, at('p1', 0.62), 0.6);
  ['hoja', 'anillo', 'capa'].forEach((k, i) => itemIcon(1260 + i * 150, 190, 110, ITEMS[k][1], { alpha: eOut(pi) * (1 - 0.85 * p2), glow: 0.6 }));
  txt('3 o 4 objetos', 1410, 305, { size: 40, w: 700, color: C.goldL, alpha: pi * (1 - 0.85 * p2) });
  txt('VS', 960, 185, { size: 60, fam: 'Cinzel', w: 700, color: C.dim, alpha: pi * (1 - 0.85 * p2) });

  // lento
  const pl = vis(t, at('p2', 0), at('p2', 0.45), 0.35);
  if (pl > 0) {
    reloj(960, 420, 1, t, pl);
    keyword('LENTO', 960, 620, 90, P(t, at('p2', 0.02), 0.5), { alpha: pl });
  }
  // chat con discusiones
  const pc = P(t, at('p2', 0.45), 0.5);
  if (pc > 0) {
    const nerv = P(t, at('p3', 0), 0.4);
    const sx = Math.sin(t * 40) * 5 * nerv;
    const x0 = 330 + sx, y0 = 390, w = 1260, h = 420;
    frame(x0, y0, w, h, { title: 'Chat de banda', alpha: eOut(pc) });
    const msgs = [
      [at('p2', 0.52), 'kharion', '¿Por qué se lo llevó él si yo saqué más?'],
      [at('p2', 0.68), 'lunaria', '¡Yo lo pedí primero!'],
      [at('p2', 0.84), 'sombrix', 'Él ya se llevó tres cosas...'],
      [at('p3', 0.05), 'brisa', '???'],
      [at('p3', 0.2), 'tukan', 'Así no se puede...'],
    ];
    msgs.forEach(([tm, who, m], i) => {
      const p = P(t, tm, 0.3);
      if (p <= 0) return;
      const [n, cls] = PJ[who];
      txtRich([['[Banda] ', C.orange, 700], [`[${n}]`, CLS[cls], 700], [': ' + m, C.orange, 500]], x0 + 50, y0 + 80 + i * 72, { size: 40, alpha: eOut(p) * pc });
    });
  }
  keyword('DESCONFIANZA', 960, 930, 96, P(t, at('p3', 0.3), 0.6), { tint: '#ff6a55' });
}
function reloj(x, y, s, t, a) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s); g.rotate(Math.sin(t * 1.5) * 0.08);
  g.strokeStyle = C.gold; g.lineWidth = 7; g.fillStyle = 'rgba(232,196,106,0.15)';
  g.beginPath(); g.moveTo(-60, -90); g.lineTo(60, -90); g.lineTo(8, 0); g.lineTo(60, 90); g.lineTo(-60, 90); g.lineTo(-8, 0); g.closePath(); g.fill(); g.stroke();
  const f = (t * 0.25) % 1;
  g.fillStyle = '#e8c46a';
  g.beginPath(); g.moveTo(-48 * (1 - f), -80 + 70 * f); g.lineTo(48 * (1 - f), -80 + 70 * f); g.lineTo(0, -6); g.closePath(); g.fill();
  g.beginPath(); g.moveTo(-50 * f, 84 - 60 * f); g.lineTo(50 * f, 84 - 60 * f); g.lineTo(55, 84); g.lineTo(-55, 84); g.closePath(); g.fill();
  g.fillRect(-2, 0, 4, 80);
  g.restore();
}

// ============================================================ 3. LA SOLUCIÓN
function escSolucion(t) {
  const e = ESC.solucion;
  fondo(t, { dim: 0.25, cx: 960, cy: 150, sc: 0.7 });
  const fl = Math.exp(-Math.max(0, t - (e.ini + 0.6)) * 4) * (t > e.ini + 0.6 ? 1 : 0);
  const pl = P(t, e.ini + 0.5, 1.0);
  const up = sm(P(t, at('s2', 0), 1.0));
  const y = lerp(360, 220, up), s = lerp(1.25, 0.7, up);
  selloAddon(960, y, s * eBack(pl), t, pl);
  const ty = lerp(620, 390, up);
  txt('SoftReserve335', 960, ty, { size: lerp(120, 76, up), fam: 'Cinzel', w: 700, color: C.gold, alpha: P(t, e.ini + 0.9, 0.8), glow: 30, glowColor: 'rgba(232,196,106,0.7)' });
  txt('Creado por la hermandad Pacto Oscuro', 960, ty + lerp(90, 62, up), { size: lerp(44, 34, up), w: 500, color: C.text, alpha: P(t, at('s1', 0.3), 0.8) });

  // carpeta -> juego
  const pf = vis(t, at('s2', 0.1), at('s3', 0), 0.5);
  if (pf > 0) {
    const mv = sm(P(t, at('s2', 0.28), 1.6));
    carpeta(lerp(600, 1290, mv), 640 - Math.sin(mv * Math.PI) * 80, 1, pf);
    txt('Carpeta del addon', 600, 760, { size: 34, w: 700, color: C.goldL, alpha: pf * (1 - mv) });
    pantallaJuego(1300, 640, 1, pf, P(t, at('s2', 0.28) + 1.6, 0.4));
    txt('Tu juego', 1300, 790, { size: 34, w: 700, color: C.goldL, alpha: pf });
    arrow(760, 640, 1110, 640, P(t, at('s2', 0.18), 0.6) * pf, 'rgba(232,196,106,0.6)', 6);
    chip('GRATIS', 820, 900, { size: 44, alpha: pf * P(t, at('s2', 0.82), 0.4), color: '#9dffb8', border: '#6dff8e' });
    chip('LEGAL', 1100, 900, { size: 44, alpha: pf * P(t, at('s2', 0.92), 0.4), color: '#9dffb8', border: '#6dff8e' });
  }
  // justo, transparente, obligatorio
  const w3 = [['JUSTO', 590, 0.0], ['TRANSPARENTE', 730, 0.22], ['OBLIGATORIO', 870, 0.62]];
  for (const [wd, yy, f] of w3) keyword(wd, 960, yy, 92, P(t, at('s3', f), 0.5));
  if (P(t, at('s3', 0.62), 0.5) > 0) txt('para todos en la raid', 960, 960, { size: 38, w: 700, color: C.text, alpha: P(t, at('s3', 0.8), 0.5) });
  if (fl > 0.01) { g.fillStyle = `rgba(255,235,190,${0.5 * fl})`; g.fillRect(0, 0, W, H); }
}
function carpeta(x, y, s, a) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s);
  g.shadowColor = 'rgba(232,196,106,0.6)'; g.shadowBlur = 30;
  g.fillStyle = '#b8892e'; rr(-80, -60, 70, 30, 8); g.fill();
  g.fillStyle = goldGrad(-50, 60); rr(-80, -45, 160, 110, 10); g.fill();
  g.shadowBlur = 0;
  g.fillStyle = 'rgba(60,30,10,0.35)'; rr(-80, -10, 160, 75, 8); g.fill();
  itemIcon(0, 20, 50, 'marca', { border: C.gold });
  g.restore();
}
function pantallaJuego(x, y, s, a, lleno) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s);
  rr(-150, -100, 300, 190, 12); g.fillStyle = '#0b0f14'; g.fill();
  g.lineWidth = 6; g.strokeStyle = goldGrad(-100, 90); g.stroke();
  g.save(); rr(-144, -94, 288, 178, 8); g.clip();
  const gr = g.createLinearGradient(0, -94, 0, 84); gr.addColorStop(0, '#1a1330'); gr.addColorStop(1, '#0c2220');
  g.fillStyle = gr; g.fillRect(-150, -100, 300, 200);
  g.scale(0.25, 0.25); necropolis(150, -260, 1, 0);
  g.restore();
  g.fillStyle = '#b8892e'; g.fillRect(-20, 90, 40, 26); g.fillRect(-60, 114, 120, 10);
  if (lleno > 0) {
    // mini ventana del addon dentro del juego
    g.globalAlpha *= lleno;
    rr(-110, -20, 120, 80, 6); g.fillStyle = 'rgba(13,10,22,0.95)'; g.fill(); g.lineWidth = 3; g.strokeStyle = C.gold; g.stroke();
    ['MS', 'OS', 'PASS'].forEach((k, i) => { rr(-100 + i * 36, 30, 30, 18, 4); g.fillStyle = BTN[k][0]; g.fill(); });
    checkmark(90, -40, 50, lleno);
  }
  g.restore();
}

// ============================================================ 4. ANTES DE LA RAID (web)
const LISTA_WEB = [['hoja', "Kel'Thuzad"], ['anillo', 'Sapphiron'], ['capa', 'Maexxna'], ['baculo', 'Loatheb'], ['escudo', 'Los Cuatro Jinetes']];
function navegador(x, y, w, h, t, o = {}) {
  const { url = '', page = 1, reservado = [0, 0, 0, 0, 0], hover = -1, alpha = 1 } = o;
  g.save(); g.globalAlpha *= alpha;
  g.shadowColor = 'rgba(0,0,0,0.8)'; g.shadowBlur = 40; g.shadowOffsetY = 12;
  rr(x, y, w, h, 14); g.fillStyle = '#16131d'; g.fill();
  g.shadowBlur = 0; g.shadowOffsetY = 0;
  g.lineWidth = 2; g.strokeStyle = '#3a3448'; g.stroke();
  g.fillStyle = '#231f2c'; rr(x, y, w, 70, [14, 14, 0, 0]); g.fill();
  ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(x + 32 + i * 28, y + 35, 9, 0, 7); g.fill(); });
  rr(x + 130, y + 15, w - 170, 40, 20); g.fillStyle = '#0f0d14'; g.fill();
  // candado
  g.strokeStyle = '#9ad5a9'; g.lineWidth = 3; g.beginPath(); g.arc(x + 160, y + 31, 7, Math.PI, 0); g.stroke();
  g.fillStyle = '#9ad5a9'; g.fillRect(x + 151, y + 31, 18, 13);
  txt(url, x + 185, y + 36, { size: 28, w: 500, color: '#e9e4f5', align: 'left', shadow: false });
  if (url.length > 0 && url.length < 22 && Math.floor(t * 3) % 2 === 0) {
    g.font = font(28, 'Alegreya Sans', 500);
    g.fillStyle = '#e9e4f5'; g.fillRect(x + 188 + g.measureText(url).width, y + 22, 2.5, 30);
  }
  if (page > 0) {
    g.save(); g.globalAlpha *= page;
    const gr = g.createLinearGradient(0, y + 70, 0, y + h);
    gr.addColorStop(0, '#1d1230'); gr.addColorStop(1, '#0e0a16');
    g.fillStyle = gr; rr(x, y + 70, w, h - 70, [0, 0, 14, 14]); g.fill();
    emblema(x + 80, y + 140, 0.28, t);
    txt('Pacto Oscuro', x + 140, y + 125, { size: 44, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
    txt('Reservas de botín', x + 140, y + 168, { size: 28, color: C.dim, align: 'left' });
    // pestañas
    [['Naxxramas', 1], ["Ahn'Qiraj", 0]].forEach(([n, on], i) => {
      const tx = x + w - 420 + i * 200;
      rr(tx, y + 110, 180, 52, 8); g.fillStyle = on ? '#3b2360' : '#1a1426'; g.fill();
      g.lineWidth = 2; g.strokeStyle = on ? C.gold : '#4a4060'; g.stroke();
      txt(n, tx + 90, y + 137, { size: 28, w: 700, color: on ? C.goldL : C.dim });
    });
    LISTA_WEB.forEach(([k, jefeN], i) => {
      const ry = y + 210 + i * 108;
      rr(x + 40, ry, w - 80, 94, 10); g.fillStyle = i % 2 ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.06)'; g.fill();
      if (reservado[i] > 0) { g.lineWidth = 2.5; g.strokeStyle = rgba('#e8c46a', reservado[i]); g.stroke(); }
      itemIcon(x + 95, ry + 47, 70, ITEMS[k][1]);
      txt(ITEMS[k][0], x + 150, ry + 34, { size: 36, w: 700, color: C.purple, align: 'left' });
      txt(jefeN, x + 150, ry + 70, { size: 26, color: C.dim, align: 'left' });
      const r = reservado[i];
      button(x + w - 320, ry + 17, 250, 60, r > 0.5 ? 'Reservado' : 'Reservar', { kind: r > 0.5 ? 'MS' : 'red', size: 30, hi: hover === i ? 0.6 : 0, press: r > 0 && r < 0.5 ? 1 : 0 });
      if (r > 0.5) checkmark(x + w - 365, ry + 47, 30, (r - 0.5) * 2, '#ffffff');
    });
    g.restore();
  }
  g.restore();
}
function escReserva(t) {
  const e = ESC.reserva;
  fondo(t, { dim: 0.45, cx: 1500, cy: 180, sc: 0.6 });
  const URL = 'softres.xdataplusx.com';
  const pw = P(t, e.ini + 0.2, 0.7);
  const nch = Math.floor(URL.length * P(t, e.ini + 0.6, 1.4));
  const page = P(t, e.ini + 2.1, 0.5);
  // clics de reserva
  const c1 = at('r2', 0.30), c2 = at('r2', 0.48);
  const res = [0, clamp((t - c1) / 0.25), clamp((t - c2) / 0.25), 0, 0];
  // encoger a la izquierda en r3
  const sh = sm(P(t, at('r3', 0), 1.0));
  const fuera = sm(P(t, at('r4', 0), 0.6));
  const bx = lerp(260, 60, sh), by = lerp(150, 200, sh), bs = lerp(1, 0.55, sh);
  g.save(); g.translate(bx, by); g.scale(bs, bs);
  navegador(0, 0, 1400, 780, t, { url: URL.slice(0, nch), page, reservado: res, alpha: eOut(pw) * (1 - fuera) });
  g.restore();
  // la dirección de la web, destacada mientras se nombra
  const pu = vis(t, at('r1', 0.5), at('r2', 0.05), 0.4);
  if (pu > 0) {
    g.save(); g.globalAlpha *= pu; g.shadowColor = 'rgba(232,196,106,0.9)'; g.shadowBlur = 30;
    g.lineWidth = 4; g.strokeStyle = C.gold; rr(260 + 130, 150 + 15, 1400 - 170, 40, 20); g.stroke(); g.restore();
    keyword('softres.xdataplusx.com', 960, 1000, 64, P(t, at('r1', 0.5), 0.5), { fam: 'Cinzel', w: 700, alpha: pu });
  }
  // cursor
  if (t < at('r3', 0.1)) {
    const a = vis(t, at('r2', 0.05), at('r3', 0.1), 0.3);
    const b1 = [260 + 1400 - 195, 150 + 210 + 1 * 108 + 47], b2 = [260 + 1400 - 195, 150 + 210 + 2 * 108 + 47];
    let cx = lerp(1300, b1[0], sm(P(t, at('r2', 0.08), c1 - at('r2', 0.08) - 0.1))), cy = lerp(900, b1[1], sm(P(t, at('r2', 0.08), c1 - at('r2', 0.08) - 0.1)));
    const m2 = sm(P(t, c1 + 0.2, c2 - c1 - 0.3));
    cx = lerp(cx, b2[0], m2); cy = lerp(cy, b2[1], m2);
    const press = Math.max(1 - Math.abs(t - c1) * 6, 1 - Math.abs(t - c2) * 6, 0);
    cursor(cx, cy, press, a);
  }
  // RESERVA
  const kr = vis(t, at('r2', 0.72), at('r3', 0.05), 0.35);
  if (kr > 0) { veil(0.45 * kr); keyword('RESERVA', 960, 520, 140, P(t, at('r2', 0.72), 0.5), { alpha: kr }); txt('«si cae esto, lo pido yo»  ·  SR', 960, 650, { size: 44, w: 700, color: C.goldL, alpha: kr }); }

  // r3: el maestro despojador carga las reservas en el addon
  const pa = vis(t, at('r3', 0.15), at('r4', 0.05), 0.5);
  if (pa > 0) {
    arrow(860, 520, 1010, 520, P(t, at('r3', 0.2), 0.6) * pa, C.gold, 9);
    frame(1060, 230, 760, 560, { title: 'SoftReserve335', alpha: pa });
    txt('Reservas cargadas', 1440, 300, { size: 36, w: 700, color: C.goldL, alpha: pa });
    const filas = [['veltra', 'anillo'], ['lunaria', 'anillo'], ['sombrix', 'capa'], ['brisa', 'baculo']];
    filas.forEach(([who, it], i) => {
      const p = P(t, at('r3', 0.35) + i * 0.3, 0.3) * pa;
      const ry = 370 + i * 90;
      itemIcon(1130, ry, 56, ITEMS[it][1], { alpha: p });
      txt(PJ[who][0], 1180, ry - 14, { size: 32, w: 700, color: CLS[PJ[who][1]], align: 'left', alpha: p });
      txt(ITEMS[it][0], 1180, ry + 20, { size: 26, color: C.purple, align: 'left', alpha: p });
      chip('SR', 1750, ry, { size: 26, alpha: p, color: C.goldL });
    });
    heroPJ('morgrath', 1440, 1010, 0.62, { alpha: pa, nameSize: 26, sub: 'Maestro despojador', glow: 0.5 });
  }
  // r4: cae un objeto reservado: solo tiran quienes lo reservaron
  const pr = vis(t, at('r4', 0.0), e.fin, 0.5);
  if (pr > 0) {
    itemIcon(960, 250, 120, 'anillo', { glow: 0.9, alpha: pr, border: C.epic });
    txt('Anillo de la Escarcha Eterna', 960, 350, { size: 42, w: 700, color: C.purple, alpha: pr });
    const filas = [['veltra', 1, 45], ['lunaria', 1, 81], ['kharion', 0], ['sombrix', 0]];
    filas.forEach(([who, sr, d], i) => {
      const x = 390 + i * 380;
      const p = P(t, at('r4', 0.1) + i * 0.12, 0.35) * pr;
      heroPJ(who, x, 700, 0.9, { alpha: p, gray: sr ? 0 : P(t, at('r4', 0.45), 0.4), glow: sr ? 0.6 : 0 });
      if (sr) {
        chip('RESERVÓ', x, 760, { size: 28, alpha: p, color: C.goldL });
        const n = rollNum(t, at('r4', 0.5) + i * 0.15, 0.8, d, i);
        if (n !== null) txt('Dado: ' + n, x, 830, { size: 40, fam: 'Cinzel', w: 700, color: C.gold, alpha: p });
      } else {
        txt('no reservó · no tira', x, 770, { size: 30, w: 700, color: '#9a93a8', alpha: p * P(t, at('r4', 0.45), 0.4) });
      }
    });
    keyword('SOLO TIRAN QUIENES RESERVARON', 960, 960, 58, P(t, at('r4', 0.55), 0.5), { alpha: pr });
  }
}

// ============================================================ 5. CAE UN OBJETO
function avisoBotin(x, y, t, o = {}) {
  const { alpha = 1, hi = {}, press = {}, timer = 1, count = null, nota = '', dado = null, lista = 0, listaPress = 0, s = 1, noReserva = 0 } = o;
  if (alpha <= 0) return;
  g.save(); g.translate(x, y); g.scale(s, s);
  const w = 820, h = 560;
  frame(-w / 2, -h / 2, w, h, { title: '¡Botín!', alpha });
  g.globalAlpha *= alpha;
  itemIcon(-w / 2 + 110, -150, 110, 'espada', { glow: 0.6 });
  txt('Hoja del Nigromante', -w / 2 + 190, -180, { size: 46, w: 700, color: C.purple, align: 'left' });
  txt("Kel'Thuzad · Naxxramas", -w / 2 + 190, -128, { size: 30, color: C.dim, align: 'left' });
  if (noReserva > 0) chip('Nadie la reservó', -w / 2 + 330, -60, { size: 28, alpha: noReserva, color: C.goldL });
  button(w / 2 - 190, -250, 150, 50, 'Ver lista', { kind: 'gold', size: 26, hi: lista, press: listaPress });
  const bw = 220, gap = 30, bx0 = -(bw * 3 + gap * 2) / 2;
  ['MS', 'OS', 'PASS'].forEach((k, i) => button(bx0 + i * (bw + gap), 10, bw, 96, k, { kind: k, size: 46, hi: hi[k] || 0, press: press[k] || 0, dimmed: (press.MS && k !== 'MS') ? 1 : 0 }));
  // cuenta atrás
  rr(-340, 160, 680, 34, 17); g.fillStyle = '#0a0710'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#6a5a3a'; g.stroke();
  const col = timer > 0.35 ? '#e8c46a' : (Math.floor(t * 6) % 2 ? '#ff5a4f' : '#ff9a4f');
  if (timer > 0) { rr(-336, 164, 672 * timer, 26, 13); g.fillStyle = col; g.fill(); }
  txt(count !== null ? `Tiempo: ${count} s` : 'Tiempo', 0, 225, { size: 30, w: 700, color: count !== null ? col : C.dim });
  if (dado !== null) txt(`Tu dado: ${dado}`, 0, -40, { size: 52, fam: 'Cinzel', w: 700, color: C.gold, glow: 20, glowColor: 'rgba(232,196,106,0.7)' });
  if (nota) txt(nota, 0, -40, { size: 32, color: C.text });
  g.restore();
}
function escObjeto(t) {
  const e = ESC.objeto;
  fondo(t, { dim: 0.3, cx: 1500, cy: 200, sc: 0.6 });
  // el jefe caído y el objeto que brilla
  const pBoss = 1 - P(t, at('o1', 0.55), 0.6);
  if (pBoss > 0) {
    cuerpo(960, 930, 1.3, t, pBoss);
    const pi = P(t, at('o1', 0.2), 0.8);
    itemIcon(960, lerp(900, 520, eOut(pi)), 140, 'espada', { glow: 1, alpha: pi * pBoss });
    txt('¡Cae un objeto!', 960, 330, { size: 56, fam: 'Cinzel', w: 700, color: C.gold, alpha: pi * pBoss });
  }
  const pa = P(t, at('o1', 0.55), 0.5);
  // posición del aviso: centrado; a la izquierda mientras explicamos MS/OS/PASS
  const lado = sm(P(t, at('o2', 0.15), 0.7)) * (1 - sm(P(t, at('o5', 0), 0.7)));
  const ax = lerp(960, 560, lado), ay = 560;
  const hi = {
    MS: vis(t, at('o2', 0.25), at('o3', 0), 0.3),
    OS: vis(t, at('o3', 0.0), at('o4', 0), 0.3),
    PASS: vis(t, at('o4', 0.0), at('o5', 0), 0.3),
  };
  const clic = at('o5', 0.5);
  const press = { MS: t > clic ? 1 : 0 };
  if (t > clic - 1.2 && t < clic) hi.MS = P(t, clic - 1.2, 0.5);
  const dT = at('o5', 0.72);
  const n = rollNum(t, dT, 0.9, 87, 3);
  // cuenta atrás en o6
  const t6 = at('o6', 0);
  let timer = 1, count = null;
  if (t > t6) { const k = Math.min(6, Math.floor((t - t6) / 0.6)); count = Math.max(1, 6 - k); timer = clamp(1 - (t - t6) / 4.2, 0.05, 1); }
  avisoBotin(ax, ay, t, { alpha: eOut(pa), hi, press, timer, count, dado: n, noReserva: P(t, at('o2', 0.02), 0.4) * (1 - P(t, at('o5', 0), 0.3)), s: lerp(1, 0.9, lado) });
  // dado girando
  if (t > dT && t < dT + 1.6) dado(ax + 520, ay - 60, 1.1, (t - dT) * 9 * (1 - P(t, dT, 1.0)) + 0.3, { alpha: vis(t, dT, dT + 1.6, 0.2) });
  // cursor que pulsa MS
  const cp = vis(t, clic - 1.3, clic + 1.0, 0.3);
  if (cp > 0) {
    const bx = 960 - 250, by = 560 + 58;
    const m = sm(P(t, clic - 1.3, 1.1));
    cursor(lerp(1300, bx, m), lerp(900, by, m), Math.max(0, 1 - Math.abs(t - clic) * 5), cp);
  }
  // panel explicativo
  const expl = [
    ['MS', 'Necesidad principal', ['Sirve para el papel principal', 'de tu personaje.', 'Tiene prioridad.'], at('o2', 0.25), at('o3', 0), '#6dff8e'],
    ['OS', 'Necesidad secundaria', ['Te sirve para un papel', 'secundario o de reserva.', 'Va después de MS.'], at('o3', 0), at('o4', 0), '#7fb2ff'],
    ['PASS', 'No lo quieres', ['Pasar también se registra.', 'No es quedarse callado.'], at('o4', 0), at('o5', 0), '#c9c3d6'],
  ];
  for (const [k, t1, lines, a, b, col] of expl) {
    const v = vis(t, a, b, 0.35);
    if (v <= 0) continue;
    const x = 1440;
    keyword(k, x, 330, 150, P(t, a, 0.5), { alpha: v, tint: col });
    txt(t1, x, 450, { size: 50, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v });
    lines.forEach((l, i) => txt(l, x, 530 + i * 56, { size: 40, color: C.text, alpha: v * P(t, a + 0.4 + i * 0.25, 0.4) }));
  }
  // explicación de dado y cuenta atrás
  txt('El addon tira el dado por ti', 960, 180, { size: 46, w: 700, color: C.goldL, alpha: vis(t, dT, t6 + 0.2, 0.4) });
  keyword('CUENTA ATRÁS', 960, 170, 72, P(t, t6 + 0.1, 0.5), { tint: '#ffb35a' });
}

// ============================================================ 6. QUIÉN GANA
function reglaOrden(x, y, s, t, o = {}) {
  const { p = [1, 1, 1], hl = -1, alpha = 1 } = o;
  const pasos = [['1', 'Reservas y MS, antes que OS'], ['2', 'Gana quien lleve menos +1'], ['3', 'Al final, decide el dado']];
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  pasos.forEach(([nn, l], i) => {
    const a = eOut(p[i]);
    if (a <= 0) return;
    const yy = i * 150;
    g.save(); g.globalAlpha *= a; g.translate(lerp(-80, 0, a), yy);
    const on = hl === i;
    rr(-560, -58, 1120, 116, 16);
    g.fillStyle = on ? 'rgba(80,50,15,0.95)' : 'rgba(18,12,30,0.92)'; g.fill();
    g.lineWidth = on ? 5 : 3; g.strokeStyle = on ? C.goldL : C.gold2; g.stroke();
    if (on) { g.shadowColor = 'rgba(255,215,110,0.8)'; g.shadowBlur = 30; g.stroke(); g.shadowBlur = 0; }
    g.beginPath(); g.arc(-480, 0, 42, 0, 7); g.fillStyle = goldGrad(-42, 42); g.fill();
    txt(nn, -480, 3, { size: 52, fam: 'Cinzel', w: 700, color: '#2a1805', shadow: false });
    txt(l, -410, 2, { size: 52, w: 700, color: C.text, align: 'left' });
    g.restore();
  });
  g.restore();
}
function cartaTirada(x, y, who, dado, mas1, t, o = {}) {
  const { alpha = 1, win = 0, lose = 0, tRoll = 0, tMas = 0 } = o;
  if (alpha <= 0) return;
  const [n, cls] = PJ[who];
  g.save(); g.globalAlpha *= alpha * (1 - 0.45 * lose);
  frame(x - 280, y - 260, 560, 540, { glow: win });
  hero(x, y + 60, 1.2, cls, { name: n, nameSize: 44, glow: 0.4 + win });
  const d = rollNum(t, tRoll, 0.9, dado, dado);
  txt('Dado', x - 130, y + 140, { size: 34, color: C.dim });
  txt(d === null ? '—' : String(d), x - 130, y + 205, { size: 84, fam: 'Cinzel', w: 700, color: C.goldL });
  txt('+1', x + 130, y + 140, { size: 34, color: C.dim });
  const pm = P(t, tMas, 0.4);
  txt(pm > 0 ? String(mas1) : '—', x + 130, y + 205, { size: 84 * (pm > 0 ? lerp(1.4, 1, eOut(pm)) : 1), fam: 'Cinzel', w: 700, color: mas1 === 0 ? '#6dff8e' : '#ff9a6a' });
  g.restore();
  if (win > 0) keyword('GANA', x, y - 300, 90, win);
}
function listaTiradas(x, y, t, o = {}) {
  const { alpha = 1, sc = 1, hlCol = -1, hlPass = 0, pie = 0 } = o;
  if (alpha <= 0) return;
  const w = 1240, h = 820;
  g.save(); g.translate(x, y); g.scale(sc, sc); g.translate(-w / 2, -h / 2);
  frame(0, 0, w, h, { title: 'Hoja del Nigromante — Tiradas', alpha, titleSize: 32 });
  g.globalAlpha *= alpha;
  const cols = [['Nombre', 90, 'left'], ['Dado', 640, 'center'], ['+1', 840, 'center'], ['Tipo', 1060, 'center']];
  cols.forEach(([c, cx, al], i) => {
    if (hlCol === i) { rr(cx - (al === 'left' ? 30 : 110), 60, al === 'left' ? 420 : 220, 640, 12); g.fillStyle = 'rgba(232,196,106,0.14)'; g.fill(); g.lineWidth = 2.5; g.strokeStyle = 'rgba(232,196,106,0.7)'; g.stroke(); }
    txt(c, cx, 100, { size: 38, fam: 'Cinzel', w: 700, color: C.gold, align: al });
  });
  g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(50, 130, w - 100, 2);
  const filas = [
    ['veltra', 12, 0, 'MS'], ['lunaria', 77, 1, 'MS'], ['kharion', 99, 2, 'MS'],
    ['sombrix', 95, 0, 'OS'], ['brisa', 64, 0, 'OS'], ['ramaz', 58, 1, 'OS'],
    ['aurelio', null, 0, 'PASS'], ['tukan', null, 1, 'PASS'],
  ];
  filas.forEach(([who, d, m, tipo], i) => {
    const ry = 175 + i * 66;
    if (i === 0) { rr(40, ry - 30, w - 80, 60, 8); g.fillStyle = 'rgba(109,255,142,0.12)'; g.fill(); }
    if (tipo === 'PASS' && hlPass > 0) { rr(40, ry - 30, w - 80, 60, 8); g.fillStyle = `rgba(200,195,214,${0.15 * hlPass})`; g.fill(); }
    const [n, cls] = PJ[who];
    txt(n, 90, ry, { size: 40, w: 700, color: CLS[cls], align: 'left' });
    if (i === 0) txt('← gana', 330, ry, { size: 32, w: 700, color: '#6dff8e', align: 'left' });
    txt(d === null ? '—' : String(d), 640, ry, { size: 40, w: 700, color: C.text });
    txt(String(m), 840, ry, { size: 40, w: 700, color: C.text });
    const tc = { MS: '#6dff8e', OS: '#7fb2ff', PASS: '#c9c3d6', SR: C.gold }[tipo];
    chip(tipo, 1060, ry, { size: 28, color: tc, border: tc });
  });
  // pie: la regla del orden
  g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(50, 712, w - 100, 2);
  txt('Orden: Reservas y MS antes que OS  ›  menos +1  ›  dado más alto', w / 2, 760, { size: 34, w: 700, color: pie > 0 ? C.goldL : C.dim, glow: pie ? 20 * pie : 0, glowColor: 'rgba(232,196,106,0.8)' });
  g.restore();
}
function escGana(t) {
  const e = ESC.gana;
  fondo(t, { dim: 0.45, cx: 1600, cy: 180, sc: 0.55 });
  // w1: el +1
  const v1 = vis(t, e.ini + 0.3, at('w2', 0.05), 0.4);
  if (v1 > 0) {
    txt('¿Y quién gana?', 960, 150, { size: 60, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v1 });
    keyword('+1', 960, 400, 220, P(t, at('w1', 0.18), 0.5), { alpha: v1 });
    const pg = P(t, at('w1', 0.5), 0.8);
    heroPJ('tukan', 960, 950, 1.1, { alpha: v1 * P(t, at('w1', 0.45), 0.4), glow: pg });
    if (pg > 0 && pg < 1) itemIcon(lerp(1500, 960, eOut(pg)), lerp(500, 720, eOut(pg)), 90, 'espada', { alpha: v1 * (1 - pg * 0.6) });
    chip('gana por MS', 960, 1010, { size: 30, alpha: v1 * P(t, at('w1', 0.6), 0.4) });
    const pb = P(t, at('w1', 0.8), 0.4);
    if (pb > 0) txt('+1', 1080, 700 - 30 * eOut(pb), { size: 90 * eBack(pb), fam: 'Cinzel Decorative', w: 900, color: '#ff9a6a', glow: 30, glowColor: '#ff9a6a', alpha: v1 });
  }
  // w2: menos +1 = prioridad; por reserva no suma
  const v2 = vis(t, at('w2', 0), at('w3', 0.02), 0.4);
  if (v2 > 0) {
    const a1 = vis(t, at('w2', 0), at('w2', 0.62), 0.3);
    if (a1 > 0) {
      heroPJ('sombrix', 640, 800, 1.2, { alpha: a1, gray: P(t, at('w2', 0.2), 0.4) * 0.6 });
      heroPJ('ramaz', 1280, 800, 1.2, { alpha: a1, glow: P(t, at('w2', 0.2), 0.4) });
      txt('+1: 2', 640, 890, { size: 54, fam: 'Cinzel', w: 700, color: '#ff9a6a', alpha: a1 });
      txt('+1: 0', 1280, 890, { size: 54, fam: 'Cinzel', w: 700, color: '#6dff8e', alpha: a1 });
      keyword('PRIORIDAD', 1280, 330, 76, P(t, at('w2', 0.18), 0.5), { alpha: a1 });
      arrow(1280, 390, 1280, 520, P(t, at('w2', 0.2), 0.4) * a1, C.gold, 8);
      txt('Así el botín se reparte entre todos', 960, 160, { size: 48, w: 700, color: C.goldL, alpha: a1 * P(t, at('w2', 0.35), 0.5) });
    }
    const a2 = vis(t, at('w2', 0.62), at('w3', 0.02), 0.3);
    if (a2 > 0) {
      heroPJ('brisa', 960, 820, 1.25, { alpha: a2, glow: 0.7 });
      chip('gana por RESERVA', 960, 880, { size: 34, alpha: a2 });
      keyword('RESERVA  =  NO SUMA +1', 960, 250, 70, P(t, at('w2', 0.66), 0.5), { alpha: a2 });
      txt('+1', 1100, 560, { size: 90, fam: 'Cinzel Decorative', w: 900, color: '#ff9a6a', alpha: a2 * 0.8 });
      cross(1100, 560, 110, P(t, at('w2', 0.78), 0.4));
    }
  }
  // w3: la regla del orden
  const v3 = vis(t, at('w3', 0), at('w6', 0.02), 0.4);
  if (v3 > 0) {
    const comp = sm(P(t, at('w4', 0), 0.8));
    txt('LA REGLA DEL ORDEN', 960, lerp(210, 70, comp), { size: lerp(70, 40, comp), fam: 'Cinzel', w: 700, color: C.gold, alpha: v3, glow: 20, glowColor: 'rgba(232,196,106,0.6)' });
    const hl = t > at('w5', 0) ? 1 : -1;
    const alphaR = v3 * (1 - comp * 0.0);
    reglaOrden(lerp(960, 960, comp), lerp(400, 135, comp), lerp(1, 0.45, comp), t, {
      p: [P(t, at('w3', 0.12), 0.5), P(t, at('w3', 0.5), 0.5), P(t, at('w3', 0.79), 0.5)], hl, alpha: alphaR
    });
    if (comp > 0) {
      g.save(); g.translate(0, 0);
      // la regla compacta ocupa 3 líneas pequeñas; las cartas debajo
      g.restore();
    }
  }
  // w4-w5: el ejemplo
  const v4 = vis(t, at('w4', 0), at('w6', 0.02), 0.4);
  if (v4 > 0) {
    const win = P(t, at('w5', 0), 0.6);
    const yC = 700;
    cartaTirada(560, yC, 'kharion', 99, 2, t, { alpha: v4, tRoll: at('w4', 0.1), tMas: at('w4', 0.33), lose: win });
    cartaTirada(1360, yC, 'veltra', 12, 0, t, { alpha: v4, tRoll: at('w4', 0.58), tMas: at('w4', 0.85), win });
    txt('No es un robo: llevaba menos +1', 960, 1030, { size: 46, w: 700, color: C.goldL, alpha: v4 * P(t, at('w5', 0.3), 0.5) });
  }
  // w6-w7: la lista transparente
  const v6 = vis(t, at('w6', 0), e.fin, 0.4);
  if (v6 > 0) {
    const clic = at('w6', 0.55);
    const op = sm(P(t, clic + 0.1, 0.7));
    avisoBotin(960, 560, t, { alpha: v6 * (1 - op), lista: P(t, at('w6', 0.2), 0.4), listaPress: Math.max(0, 1 - Math.abs(t - clic) * 5), dado: 12 });
    const bx = 960 + 410 - 115, by = 560 - 280 + 25;
    const m = sm(P(t, at('w6', 0.15), clic - at('w6', 0.15) - 0.1));
    cursor(lerp(1500, bx, m), lerp(900, by, m), Math.max(0, 1 - Math.abs(t - clic) * 5), v6 * (1 - op));
    chip('La misma lista que ve el maestro despojador', 960, 150, { size: 36, alpha: v6 * P(t, at('w6', 0.25), 0.5) * (1 - P(t, at('w7', 0), 0.4)) });
    if (op > 0) {
      const f = at('w7', 0);
      const hlCol = t < f ? -1 : t < at('w7', 0.1) ? 0 : t < at('w7', 0.18) ? 1 : t < at('w7', 0.26) ? 2 : t < at('w7', 0.38) ? 3 : -1;
      listaTiradas(960, 555, t, { alpha: v6 * op, sc: lerp(0.3, 1, eOut(op)), hlCol, hlPass: vis(t, at('w7', 0.38), at('w7', 0.52), 0.2), pie: vis(t, at('w7', 0.5), e.fin, 0.3) });
      const k = P(t, at('w7', 0.78), 0.5);
      if (k > 0) { veil(0.4 * k); keyword('NADA QUEDA OCULTO', 960, 540, 84, k); }
    }
  }
}

// ============================================================ 7. RECIBIR EL OBJETO
function escRecibir(t) {
  const e = ESC.recibir;
  fondo(t, { dim: 0.2, cx: 1500, cy: 200, sc: 0.6 });
  // la raid en semicírculo
  const raid = ['kharion', 'lunaria', 'sombrix', 'aurelio', 'thorgan', 'brisa', 'ramaz', 'tukan'];
  const v1 = vis(t, e.ini + 0.2, at('e2', 0.1), 0.5);
  if (v1 > 0) {
    raid.forEach((k, i) => heroPJ(k, 250 + i * 205, 1000 - Math.abs(i - 3.5) * 22, 0.75, { alpha: v1 * 0.9, nameSize: 26 }));
    heroPJ('veltra', 960, 1040, 0.95, { alpha: v1, glow: 1, nameSize: 32 });
    const pb = P(t, at('e1', 0.0), 0.6);
    g.save(); g.globalAlpha *= v1;
    g.translate(960, 330); g.scale(lerp(1.3, 1, eOut(pb)), lerp(1.3, 1, eOut(pb)));
    frame(-700, -180, 1400, 360, { alpha: clamp(pb * 2), glow: 1 });
    txtRich([['VELTRA', CLS.picaro, 800], [' gana', C.text, 800]], 0, -95, { size: 84, fam: 'Cinzel', align: 'center', alpha: clamp(pb * 2) });
    txt('Hoja del Nigromante', 0, 0, { size: 56, w: 700, color: C.purple, alpha: clamp(pb * 2) });
    txt('Dado 12  ·  MS  ·  llevaba menos +1', 0, 90, { size: 46, w: 700, color: C.goldL, alpha: P(t, at('e1', 0.55), 0.5) });
    g.restore();
    chip('Toda la raid lo ve', 960, 580, { size: 34, alpha: v1 * P(t, at('e1', 0.2), 0.4) });
  }
  // e2: acércate a quien reparte; diamante
  const v2 = vis(t, at('e2', 0), at('e3', 0.05), 0.5);
  if (v2 > 0) {
    const walk = sm(P(t, at('e2', 0.3), 3.0));
    heroPJ('veltra', lerp(520, 1000, walk), 900, 1.4, { alpha: v2, bob: Math.abs(Math.sin(t * 7)) * -8 * (walk > 0 && walk < 1 ? 1 : 0), nameSize: 40 });
    heroPJ('morgrath', 1360, 900, 1.4, { alpha: v2, sub: 'Maestro despojador', nameSize: 40 });
    const pd = P(t, at('e2', 0.5), 0.5);
    diamante(1360, 540, 1.3 * eBack(pd), t, v2 * pd);
    txt('mientras te deba algo', 1360, 460, { size: 32, w: 700, color: C.goldL, alpha: v2 * P(t, at('e2', 0.72), 0.5) });
    frame(360, 110, 1200, 170, { title: 'SoftReserve335', alpha: v2 * P(t, at('e2', 0.05), 0.5) });
    txtRich([['Acércate a ', C.text, 700], ['Morgrath', CLS.paladin, 800], [' para recibir tu objeto', C.text, 700]], 960, 205, { size: 46, align: 'center', alpha: v2 * P(t, at('e2', 0.1), 0.5) });
  }
  // e3: directo a la bolsa
  const v3 = vis(t, at('e3', 0), e.fin, 0.5);
  if (v3 > 0) {
    g.save(); g.globalAlpha *= v3;
    cuerpo(470, 690, 0.9, t);
    txt('Cuerpo del jefe', 470, 760, { size: 36, w: 700, color: C.goldL });
    cofre(470, 930, 1, P(t, at('e3', 0.3), 0.6));
    txt('o el cofre', 470, 1030, { size: 36, w: 700, color: C.goldL });
    // bolsa
    frame(1080, 380, 560, 560, { title: 'Bolsa' });
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
      rr(1130 + c * 120, 440 + r * 120, 100, 100, 8); g.fillStyle = 'rgba(0,0,0,0.55)'; g.fill();
      g.lineWidth = 2; g.strokeStyle = '#4a4060'; g.stroke();
    }
    const fly = P(t, at('e3', 0.45), 0.9);
    if (fly > 0) {
      const x = lerp(470, 1180, eOut(fly)), y = lerp(640, 490, eOut(fly)) - Math.sin(fly * Math.PI) * 180;
      itemIcon(x, y, lerp(90, 100, fly), 'espada', { glow: fly >= 1 ? 0.6 + 0.3 * Math.sin(t * 4) : 1 });
    }
    g.restore();
    keyword('DIRECTO A TU BOLSA', 960, 190, 80, P(t, at('e3', 0.6), 0.5), { alpha: v3 });
  }
}

// ============================================================ 8. LAS MARCAS
const FILA0 = ['brisa', 'sombrix', 'lunaria', 'ramaz', 'tukan', 'kharion', 'aurelio'];
function escMarcas(t) {
  const e = ESC.marcas;
  fondo(t, { dim: 0.25, cx: 960, cy: 170, sc: 0.75 });
  // m1: marca -> pieza de armadura
  const v1 = vis(t, e.ini + 0.3, at('m2', 0.05), 0.5);
  if (v1 > 0) {
    txt('NAXXRAMAS', 960, 470, { size: 40, fam: 'Cinzel', w: 700, color: '#bfffe0', glow: 20, glowColor: '#6dffb0', alpha: v1 });
    itemIcon(700, 700, 180, 'marca', { glow: 1, border: C.epic, alpha: v1 * P(t, at('m1', 0.1), 0.5) });
    txt('Marca de conjunto', 700, 840, { size: 42, w: 700, color: C.purple, alpha: v1 * P(t, at('m1', 0.15), 0.5) });
    arrow(830, 700, 1080, 700, P(t, at('m1', 0.6), 0.6) * v1, C.gold, 9);
    itemIcon(1220, 700, 180, 'pechera', { glow: 0.8, border: C.epic, alpha: v1 * P(t, at('m1', 0.75), 0.5) });
    txt('Pieza de armadura', 1220, 840, { size: 42, w: 700, color: C.purple, alpha: v1 * P(t, at('m1', 0.8), 0.5) });
  }
  // m2-m4: la fila
  const vq = vis(t, at('m2', 0), at('m5', 0.02), 0.5);
  if (vq > 0) {
    keyword('TURNO', 960, 170, 110, P(t, at('m2', 0.18), 0.5), { alpha: vq * (1 - vis(t, at('m4', 0.15), at('m5', 0), 0.3)) });
    const px = i => 330 + i * 210, py = 860;
    // animación de m3: Brisa pasa al final
    const t3 = at('m3', 0);
    const give = P(t, t3, 0.8);           // la marca vuela a Brisa
    const move = sm(P(t, t3 + 1.0, 2.0)); // Brisa pasa al final, el resto avanza
    FILA0.forEach((k, i) => {
      let x, y = py, glow = 0;
      if (i === 0) {
        x = lerp(px(0), px(6), move); y = py - Math.sin(move * Math.PI) * 200; glow = give > 0 ? 1 : 0;
      } else x = lerp(px(i), px(i - 1), move);
      const pos = i === 0 ? (move > 0.5 ? 7 : 1) : (move > 0.5 ? i : i + 1);
      const ap = P(t, at('m2', 0) + i * 0.12, 0.4);
      const isS = k === 'sombrix';
      const keep = isS ? vis(t, at('m4', 0.3), at('m5', 0), 0.3) : 0;
      heroPJ(k, x, y, 0.95, { alpha: vq * ap, glow: Math.max(glow * (1 - move), keep), nameSize: 28 });
      // número de turno
      g.save(); g.globalAlpha *= vq * ap;
      g.beginPath(); g.arc(x, y - 250, 30, 0, 7); g.fillStyle = pos === 1 ? goldGrad(y - 280, y - 220) : '#2a1f3c'; g.fill();
      g.lineWidth = 3; g.strokeStyle = C.gold; g.stroke();
      g.restore();
      txt(String(pos), x, y - 248, { size: 36, fam: 'Cinzel', w: 700, color: pos === 1 ? '#2a1805' : C.goldL, alpha: vq * ap, shadow: pos !== 1 });
    });
    // sin dados
    const pd = vis(t, at('m2', 0.0), at('m2', 0.55), 0.3);
    if (pd > 0) { dado(1330, 170, 0.9, 0.3, { alpha: pd }); cross(1330, 170, 90, P(t, at('m2', 0.08), 0.4)); }
    chip('El orden depende de tu asistencia a las raids', 960, 330, { size: 36, alpha: vq * vis(t, at('m2', 0.55), at('m3', 0), 0.4) });
    // marca volando a Brisa
    if (give > 0 && give < 1) itemIcon(lerp(960, px(0), eOut(give)), lerp(420, 560, eOut(give)), 90, 'marca', { glow: 1, border: C.epic });
    if (give >= 1 && move < 1) itemIcon(lerp(px(0), px(6), move) + 60, py - 100 - Math.sin(move * Math.PI) * 200, 60, 'marca', { glow: 0.6, border: C.epic, alpha: 1 - P(t, t3 + 2.6, 0.5) });
    keyword('NADIE PIERDE SU LUGAR', 960, 330, 64, vis(t, at('m3', 0.55), at('m4', 0), 0.4) > 0 ? P(t, at('m3', 0.55), 0.5) : 0, { alpha: vis(t, at('m3', 0.55), at('m4', 0.02), 0.4) });
    // m4: ya tiene esa pieza
    const t4 = at('m4', 0);
    const ap4 = P(t, t4, 1.0);
    if (t > t4) {
      const vv = vis(t, t4, at('m5', 0), 0.3);
      const back = P(t, at('m4', 0.55), 0.8);
      const mx = lerp(960, px(0) + 90, eOut(ap4)), my = lerp(420, 600, eOut(ap4));
      itemIcon(lerp(mx, 960, eOut(back)), lerp(my, 420, eOut(back)), 90, 'marca', { glow: 1, border: C.epic, alpha: vv });
      const pw = vis(t, at('m4', 0.2), at('m5', 0), 0.3);
      if (pw > 0) {
        frame(660, 220, 900, 200, { title: 'Aviso', alpha: pw });
        txt('!', 740, 320, { size: 110, fam: 'Cinzel', w: 700, color: '#ffcc4d', alpha: pw, glow: 20, glowColor: '#ffcc4d' });
        txtRich([['Sombrix', CLS.brujo, 800], [' ya tiene esta pieza', C.text, 700]], 1130, 300, { size: 46, align: 'center', alpha: pw });
        txt('Se avisa antes de entregarla', 1130, 360, { size: 34, color: C.dim, alpha: pw });
      }
      chip('Conserva su turno para la próxima', px(0), 1020, { size: 32, alpha: vis(t, at('m4', 0.62), at('m5', 0), 0.3), color: C.goldL });
    }
  }
  // m5: los alts
  const v5 = vis(t, at('m5', 0), e.fin, 0.5);
  if (v5 > 0) {
    const intento = P(t, at('m5', 0.55), 0.5), vuelta = P(t, at('m5', 0.72), 0.5);
    heroPJ('lunaria', 760, 850, 1.3, { alpha: v5, tag: 'PRINCIPAL', nameSize: 40, glow: 0.4 });
    hero(1180 - 170 * eOut(intento) * (1 - eOut(vuelta)), 850, 1.1, 'druida', { name: 'Lunaverde', alpha: v5, tag: 'ALT', nameSize: 36 });
    cross(1030, 640, 120, P(t, at('m5', 0.72), 0.4));
    keyword('UN ALT NUNCA PASA POR DELANTE', 960, 200, 58, P(t, at('m5', 0.5), 0.5), { alpha: v5 });
    txt('del principal', 960, 290, { size: 48, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v5 * P(t, at('m5', 0.6), 0.5) });
    txt('El addon sabe quién es el personaje secundario', 960, 1035, { size: 36, w: 500, color: C.text, alpha: v5 * P(t, at('m5', 0.3), 0.5) });
  }
}

// ============================================================ 9. ASISTENCIA
function escAsistencia(t) {
  const e = ESC.asistencia;
  fondo(t, { dim: 0.35, cx: 1500, cy: 200, sc: 0.6 });
  const jefes = ["Anub'Rekhan", 'Gran viuda Faerlina', 'Maexxna', 'Noth el Pesteador', 'Heigan el Impuro', 'Loatheb'];
  const mv = sm(P(t, at('a2', 0), 1.0));
  const fx = lerp(560, 330, mv);
  const v = vis(t, e.ini + 0.2, e.fin, 0.4);
  frame(fx - 380, 200, 760, 700, { title: 'Asistencia', alpha: v });
  jefes.forEach((j, i) => {
    const y = 300 + i * 95;
    const p = P(t, at('a1', 0.05) + i * 0.45, 0.4);
    txt(j, fx - 320, y, { size: 38, w: 700, color: C.text, align: 'left', alpha: v });
    checkmark(fx + 290, y, 46, p);
    if (p > 0.5) txt('derrotado', fx + 230, y, { size: 26, w: 500, color: '#9dffb8', align: 'right', alpha: v * p });
  });
  txt('Se anota quién estuvo presente', fx, 862, { size: 32, w: 700, color: C.goldL, alpha: v * P(t, at('a1', 0.4), 0.5) });
  // se sube a la web
  const pw = P(t, at('a2', 0.05), 0.6);
  if (pw > 0) {
    arrow(760, 550, 1020, 550, pw, C.gold, 9);
    g.save(); g.globalAlpha *= v * pw;
    rr(1060, 330, 620, 400, 14); g.fillStyle = '#16131d'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#3a3448'; g.stroke();
    g.fillStyle = '#231f2c'; rr(1060, 330, 620, 56, [14, 14, 0, 0]); g.fill();
    txt('softres.xdataplusx.com', 1370, 358, { size: 28, color: '#e9e4f5' });
    g.restore();
    chip('HISTORIAL', 1370, 480, { size: 44, alpha: v * P(t, at('a2', 0.25), 0.4) });
    chip('TURNO', 1370, 600, { size: 44, alpha: v * P(t, at('a2', 0.32), 0.4) });
  }
  // menos de 10 personas
  const p10 = P(t, at('a2', 0.56), 0.5);
  if (p10 > 0) {
    veil(0.55 * p10);
    frame(360, 380, 1200, 420, { alpha: p10, glow: 0.3 });
    const cl = ['guerrero', 'mago', 'sacerdote', 'picaro', 'cazador', 'brujo', 'druida'];
    cl.forEach((c, i) => hero(560 + i * 135, 700, 0.6, c, { alpha: p10 }));
    keyword('MENOS DE 10 PERSONAS', 960, 470, 66, p10, { tint: '#ff8a70' });
    txt('en el grupo: no cuenta', 960, 750, { size: 46, w: 700, color: C.text, alpha: P(t, at('a2', 0.7), 0.4) });
    cross(1500, 610, 90, P(t, at('a2', 0.8), 0.4));
  }
}

// ============================================================ 10. CIERRE
function escCierre(t) {
  const e = ESC.cierre;
  const fin = at('c4', 0) - 0.4;
  fondo(t, { dim: t < fin ? 0.4 : lerp(0.4, 0, P(t, fin, 1.5)), cx: 960, cy: lerp(160, 230, P(t, fin, 2)), sc: lerp(0.6, 0.9, sm(P(t, fin, 3))) });
  // c1: sin el addon
  const v1 = vis(t, e.ini + 0.2, at('c2', 0.02), 0.4);
  if (v1 > 0) {
    keyword('OBLIGATORIO', 960, 150, 90, P(t, e.ini + 0.3, 0.5), { alpha: v1 });
    txt('Sin el addon:', 960, 270, { size: 50, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v1 });
    const filas = [['No ves los avisos', 0.14], ['No puedes tirar desde los botones', 0.33], ['Tu asistencia no queda registrada', 0.55]];
    filas.forEach(([s, f], i) => {
      const p = P(t, at('c1', f), 0.4);
      const y = 390 + i * 120;
      cross(470, y, 60, p);
      txt(s, 540, y, { size: 52, w: 700, color: C.text, align: 'left', alpha: v1 * p });
    });
    keyword('PIERDES TU LUGAR EN LA FILA', 960, 800, 64, P(t, at('c1', 0.8), 0.5), { tint: '#ff8a70', alpha: v1 });
  }
  // c2: fallos corregidos
  const v2 = vis(t, at('c2', 0), at('c3', 0.02), 0.4);
  if (v2 > 0) {
    frame(360, 380, 1200, 300, { alpha: v2, glow: 0.4 });
    checkmark(520, 530, 110, P(t, at('c2', 0.1), 0.6));
    txt('Los fallos que reportó la hermandad', 1030, 490, { size: 50, w: 700, color: C.text, alpha: v2 });
    txt('ya se corrigieron', 1030, 570, { size: 56, fam: 'Cinzel', w: 700, color: C.gold, alpha: v2 * P(t, at('c2', 0.45), 0.4) });
  }
  // c3: los tres pasos
  const v3 = vis(t, at('c3', 0), fin + 0.3, 0.4);
  if (v3 > 0) {
    const pasos = [['1', 'Instala el addon', 0.0], ['2', 'Reserva en la web', 0.3], ['3', 'Nos vemos en Naxxramas', 0.6]];
    pasos.forEach(([n, s, f], i) => {
      const p = P(t, at('c3', f), 0.45);
      const y = 380 + i * 170;
      g.save(); g.globalAlpha *= v3 * eOut(p); g.translate(lerp(-60, 0, eOut(p)), 0);
      g.beginPath(); g.arc(560, y, 52, 0, 7); g.fillStyle = goldGrad(y - 52, y + 52); g.fill();
      txt(n, 560, y + 3, { size: 62, fam: 'Cinzel', w: 700, color: '#2a1805', shadow: false });
      txt(s, 650, y, { size: 66, fam: 'Cinzel', w: 700, color: C.goldL, align: 'left' });
      g.restore();
    });
  }
  // c4: logo
  const pl = P(t, fin, 1.2);
  if (pl > 0) {
    const gr = g.createRadialGradient(960, 460, 20, 960, 460, 520);
    gr.addColorStop(0, `rgba(160,80,255,${0.28 * pl})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(0, 0, W, H);
    emblema(960, 440, 1.25 * lerp(0.85, 1, eOut(pl)), t, pl);
    keyword('PACTO OSCURO', 960, 760, 120, P(t, fin + 0.4, 0.9));
    txt('SoftReserve335   ·   softres.xdataplusx.com', 960, 870, { size: 36, w: 700, color: C.text, alpha: P(t, fin + 1.4, 0.8) });
  }
  veil(P(t, TL.duracion - 1.6, 1.5));
}

// ============================================================ motor
const ESCENAS = { gancho: escGancho, problema: escProblema, solucion: escSolucion, reserva: escReserva, objeto: escObjeto, gana: escGana, recibir: escRecibir, marcas: escMarcas, asistencia: escAsistencia, cierre: escCierre };
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  const es = TL.escenas;
  let e = es.find(x => t >= x.ini && t < x.fin) || es[es.length - 1];
  ESCENAS[e.id](t);
  // fundido entre escenas
  const d = 0.35;
  let a = 0;
  if (e !== es[0]) a = Math.max(a, 1 - clamp((t - e.ini) / d));
  if (e !== es[es.length - 1]) a = Math.max(a, 1 - clamp((e.fin - t) / d));
  veil(a);
}
window.draw = draw;
window.initTL = initTL;
window.listo = () => Promise.all([
  document.fonts.load('700 40px "Cinzel"'), document.fonts.load('400 40px "Cinzel"'),
  document.fonts.load('900 40px "Cinzel Decorative"'), document.fonts.load('700 40px "Libre Baskerville"'),
  document.fonts.load('500 40px "Alegreya Sans"'), document.fonts.load('700 40px "Alegreya Sans"'),
  document.fonts.load('800 40px "Alegreya Sans"'), document.fonts.load('400 40px "Alegreya Sans"'),
]).then(() => document.fonts.ready);
