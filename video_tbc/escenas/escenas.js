// Las 14 escenas del video de TBC. Cada una usa los tiempos reales de la narración (CUE).

// ------------------------------------------------------------ datos de ejemplo
const CORE = [
  ['Thorgan', 'paladin', 'tanque'], ['Kharion', 'guerrero', 'tanque'], ['Ramaz', 'druida', 'tanque'],
  ['Aurelio', 'sacerdote', 'sanador'], ['Tukan', 'chaman', 'sanador'], ['Lumen', 'paladin', 'sanador'],
  ['Seren', 'druida', 'sanador'], ['Ilsa', 'sacerdote', 'sanador'], ['Nahui', 'chaman', 'sanador'],
  ['Veltra', 'picaro', 'dps'], ['Lunaria', 'mago', 'dps'], ['Sombrix', 'brujo', 'dps'], ['Brisa', 'cazador', 'dps'],
  ['Grimta', 'guerrero', 'dps'], ['Zefir', 'mago', 'dps'], ['Nyx', 'picaro', 'dps'], ['Oscuria', 'brujo', 'dps'],
  ['Kayra', 'cazador', 'dps'], ['Rumi', 'chaman', 'dps'], ['Dorn', 'guerrero', 'dps'], ['Selva', 'druida', 'dps'],
  ['Pyra', 'mago', 'dps'], ['Umbra', 'brujo', 'dps'], ['Tala', 'cazador', 'dps'], ['Vex', 'picaro', 'dps'],
];
const BUFFOS = [['sacerdote', 'Sacerdote', 'Entereza'], ['mago', 'Mago', 'Intelecto Arcano'], ['druida', 'Druida', 'Marca de lo Salvaje'],
  ['paladin', 'Paladín', 'Bendiciones'], ['chaman', 'Chamán', 'Tótems'], ['guerrero', 'Guerrero', 'Grito de batalla']];
const ITEM_TBC = 'Hoja de Terrallende';

// ============================================================ 1. GANCHO
function escGancho(t) {
  fondoTBC(t);
  const op = sm(P(t, 0.6, 2.6));
  const zoom = lerp(0.72, 0.8, sm(P(t, 0, 12)));
  portal(960, 900, zoom, op, t);
  const k = P(t, at('g1', 0.15), 0.7);
  keyword('LLEGA TBC', 960, 170, 120, k, { tint: '#8dff6a' });
  chip('3 de octubre', 960, 290, { size: 40, alpha: P(t, at('g1', 0.5), 0.5), color: C.goldL });
  const frases = [['Nueva expansión', 0.0], ['Nuevas bandas', 0.25], ['Una forma justa de repartir el botín', 0.55]];
  const pv = vis(t, at('g2', 0), ESC.gancho.fin, 0.4);
  if (pv > 0) {
    g.fillStyle = `rgba(0,0,0,${0.45 * pv})`; g.fillRect(0, 880, W, 200);
    frases.forEach(([s, f], i) => {
      const p = P(t, at('g2', f), 0.5);
      txt(s, [700, 1220, 960][i], i === 2 ? 1030 : 950, { size: i === 2 ? 44 : 48, fam: 'Cinzel', w: 700, color: i === 2 ? C.gold : C.goldL, alpha: p * pv, glow: i === 2 ? 20 : 0, glowColor: 'rgba(232,196,106,0.6)' });
    });
  }
  veil(1 - P(t, 0, 1.0));
}

// ============================================================ 2. EL PROBLEMA
function escProblema(t) {
  fondoTBC(t, { dim: 0.45 });
  const p2 = P(t, at('p2', 0.1), 0.6);
  for (let i = 0; i < 25; i++) {
    const c = i % 5, r = Math.floor(i / 5);
    const x = 170 + c * 120 + (r % 2) * 30, y = 430 + r * 120;
    const p = P(t, at('p1', 0.02) + i * 0.05, 0.35);
    hero(x + Math.sin(t * 9 + i) * 3 * P(t, at('p2', 0.2), 0.5), y, 0.45, CORE[i][1], { alpha: eOut(p) });
  }
  keyword('25 JUGADORES', 450, 180, 70, P(t, at('p1', 0.15), 0.6));
  const pi = P(t, at('p1', 0.6), 0.6);
  itemIcon(1350, 180, 110, 'espada', { alpha: pi, glow: 0.6 });
  itemIcon(1500, 180, 110, 'anillo', { alpha: pi, glow: 0.6 });
  txt('muy pocos objetos', 1425, 300, { size: 40, w: 700, color: C.goldL, alpha: pi });
  // chat con las dudas
  if (p2 > 0) {
    const x0 = 860, y0 = 400, w = 960, h = 380;
    frame(x0, y0, w, h, { title: 'Chat de banda', alpha: p2 });
    const msgs = [[at('p2', 0.3), 'Kharion', 'guerrero', '¿Por qué se lo llevó él?'],
      [at('p2', 0.52), 'Lunaria', 'mago', 'Yo vine a todas las raids.'],
      [at('p2', 0.72), 'Sombrix', 'brujo', 'Él ya tiene tres cosas...']];
    msgs.forEach(([tm, n, cls, m], i) => {
      const p = P(t, tm, 0.3);
      if (p > 0) txtRich([['[Banda] ', C.orange, 700], [`[${n}]`, CLS[cls], 700], [': ' + m, C.orange, 500]], x0 + 44, y0 + 80 + i * 80, { size: 40, alpha: eOut(p) * p2 });
    });
    const pl = P(t, at('p2', 0.05), 0.4) * (1 - P(t, at('p3', 0), 0.4));
    if (pl > 0) keyword('LENTO', 1340, y0 + h + 90, 70, P(t, at('p2', 0.05), 0.4), { alpha: pl, tint: '#ff8a70' });
  }
  const pj = P(t, at('p3', 0.4), 0.5);
  if (pj > 0) {
    veil(0.8 * pj);
    keyword('JUSTO · CLARO · VISIBLE', 960, 540, 84, pj);
    txt('para todos', 960, 650, { size: 46, w: 700, color: C.goldL, alpha: P(t, at('p3', 0.75), 0.4) });
  }
}

// ============================================================ 3. LAS TRES HERRAMIENTAS
function iconoWeb(x, y, s, t, a) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s);
  rr(-120, -85, 240, 170, 12); g.fillStyle = '#121017'; g.fill(); g.lineWidth = 3; g.strokeStyle = '#4a4458'; g.stroke();
  g.fillStyle = '#1d1a24'; rr(-120, -85, 240, 34, [12, 12, 0, 0]); g.fill();
  ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(-100 + i * 16, -68, 5, 0, 7); g.fill(); });
  g.fillStyle = '#221433'; g.fillRect(-120, -51, 240, 36);
  emblema(-96, -33, 0.08, t);
  for (let i = 0; i < 4; i++) { rr(-100, -2 + i * 20, 200 - i * 30, 10, 5); g.fillStyle = i ? '#3a3448' : C.gold; g.fill(); }
  g.restore();
}
function iconoTooltip(x, y, s, a) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s);
  rr(-120, -85, 240, 170, 8); g.fillStyle = 'rgba(8,10,28,0.96)'; g.fill(); g.lineWidth = 3; g.strokeStyle = '#8f8fa8'; g.stroke();
  rr(-100, -65, 130, 14, 7); g.fillStyle = '#b561ff'; g.fill();
  for (let i = 0; i < 3; i++) { rr(-100, -36 + i * 22, 150 - i * 20, 10, 5); g.fillStyle = '#dcdcdc'; g.fill(); }
  g.fillStyle = 'rgba(232,196,106,0.6)'; g.fillRect(-100, 36, 200, 2);
  rr(-100, 50, 120, 12, 6); g.fillStyle = C.gold; g.fill();
  txt('1', 80, 56, { size: 26, color: C.goldL, shadow: false });
  g.restore();
}
function escHerramientas(t) {
  fondoTBC(t, { dim: 0.5 });
  txt('Tres piezas que trabajan juntas', 960, 130, { size: 60, fam: 'Cinzel', w: 700, color: C.goldL, alpha: P(t, at('h1', 0), 0.6) });
  const inst = vis(t, at('h5', 0), at('h6', 0.02), 0.4);
  const cards = [
    ['h2', 'La página web', 'softres.xdataplusx.com', 'TE REGISTRA', 0.28],
    ['h3', 'SoftReserve335', 'Reparte el botín en el juego', 'REPARTE', 0.82],
    ['h4', 'BisTooltip', 'Te dice qué objetos son los mejores', 'TE GUÍA', 0.52],
  ];
  cards.forEach(([cue, tit, sub, rol, f], i) => {
    const p = P(t, at(cue, 0), 0.6);
    if (p <= 0) return;
    const x = 420 + i * 540, y = 520;
    const a = eOut(p) * (1 - inst);
    frame(x - 230, y - 230, 460, 440, { alpha: a, glow: P(t, at('h6', f), 0.4) * 0.8 });
    if (i === 0) iconoWeb(x, y - 70, 1, t, a);
    if (i === 1) selloAddon(x, y - 70, 0.75, t, a);
    if (i === 2) iconoTooltip(x, y - 70, 1, a);
    txt(tit, x, y + 80, { size: 42, fam: 'Cinzel', w: 700, color: C.gold, alpha: a });
    txt(sub, x, y + 135, { size: 28, color: C.text, alpha: a, maxW: 420 });
    const pr = P(t, at('h6', f), 0.4);
    if (pr > 0) keyword(rol, x, y + 300, 58, pr, { alpha: 1 - inst });
  });
  if (inst > 0) {
    const mv = sm(P(t, at('h5', 0.12), 1.6));
    txt('¿Qué es un addon?', 960, 300, { size: 54, fam: 'Cinzel', w: 700, color: C.goldL, alpha: inst });
    txt('Un pequeño programa que se instala dentro del juego', 960, 380, { size: 40, color: C.text, alpha: inst });
    carpeta(lerp(640, 1250, mv), 620 - Math.sin(mv * Math.PI) * 70, 1, inst);
    g.save(); g.globalAlpha *= inst;
    g.fillStyle = '#b8892e'; rr(1170, 560, 70, 26, 8); g.fill();
    rr(1170, 575, 170, 120, 10); g.fillStyle = 'rgba(184,137,46,0.35)'; g.fill(); g.lineWidth = 3; g.strokeStyle = C.gold; g.stroke();
    g.restore();
    txt('Carpeta de addons del juego', 1255, 740, { size: 32, w: 700, color: C.goldL, alpha: inst });
    txt('Se copia la carpeta', 640, 740, { size: 32, w: 700, color: C.goldL, alpha: inst * (1 - mv) });
    chip('GRATIS', 800, 880, { size: 44, alpha: inst * P(t, at('h5', 0.75), 0.4), color: '#9dffb8', border: '#6dff8e' });
    chip('PERMITIDO', 1120, 880, { size: 44, alpha: inst * P(t, at('h5', 0.85), 0.4), color: '#9dffb8', border: '#6dff8e' });
  }
}
function carpeta(x, y, s, a) {
  g.save(); g.globalAlpha *= a; g.translate(x, y); g.scale(s, s);
  g.shadowColor = 'rgba(232,196,106,0.6)'; g.shadowBlur = 30;
  g.fillStyle = '#b8892e'; rr(-80, -60, 70, 30, 8); g.fill();
  g.fillStyle = goldGrad(-50, 60); rr(-80, -45, 160, 110, 10); g.fill();
  g.shadowBlur = 0;
  g.fillStyle = 'rgba(60,30,10,0.35)'; rr(-80, -10, 160, 75, 8); g.fill();
  dado(0, 20, 0.45, 0.3);
  g.restore();
}

// ============================================================ 4. REGÍSTRATE EN LA WEB
const PERSONAJES = [
  { n: 'Veltra', cls: 'picaro', clase: 'Pícaro', spec: 'Combate', tipo: 'PRINCIPAL', prof: ['Alquimia', 'Herboristería'] },
  { n: 'Veltrix', cls: 'mago', clase: 'Mago', spec: 'Arcano', tipo: 'ALT', prof: ['Sastrería', 'Encantamiento'] },
  { n: 'Veltrana', cls: null, clase: '', spec: '', tipo: 'ALT', prof: [] },
];
function tarjetaPJ(x, y, w, pj, t, o = {}) {
  const { alpha = 1, alerta = 0, candado = 0, prof = 0 } = o;
  const h = 212;
  g.save(); g.globalAlpha *= alpha;
  rr(x, y, w, h, 12); g.fillStyle = '#1a1422'; g.fill();
  g.lineWidth = alerta ? 4 : 2; g.strokeStyle = alerta ? `rgba(255,90,79,${0.5 + 0.5 * Math.sin(t * 6)})` : (pj.tipo === 'PRINCIPAL' ? C.gold : '#3a3448'); g.stroke();
  const col = pj.cls ? CLS[pj.cls] : '#8a8494';
  hero(x + 80, y + 180, 0.58, pj.cls || 'sacerdote', { gray: pj.cls ? 0 : 1 });
  txt(pj.n, x + 160, y + 50, { size: 40, w: 800, color: col, align: 'left' });
  chip(pj.tipo, x + w - 20, y + 48, { size: 24, align: 'right', color: pj.tipo === 'PRINCIPAL' ? C.goldL : C.dim, border: pj.tipo === 'PRINCIPAL' ? C.gold : '#6d6578' });
  campo(x + 160, y + 82, 200, 'Clase', pj.clase, { vacio: !pj.clase, color: col });
  campo(x + 380, y + 82, 200, 'Spec', pj.spec, { vacio: !pj.spec });
  if (prof > 0) {
    txt('Profesiones:', x + 160, y + 186, { size: 24, w: 700, color: C.dim, align: 'left', alpha: prof });
    pj.prof.forEach((p, i) => chip(p, x + 320 + i * 170, y + 186, { size: 22, alpha: prof, align: 'left', color: '#cfe8ff', border: '#5a7aa8' }));
    if (!pj.prof.length) txt('—', x + 320, y + 186, { size: 26, color: C.dim, align: 'left', alpha: prof });
  }
  if (candado > 0) {
    g.save(); g.globalAlpha *= candado; g.translate(x + w - 60, y + 130);
    g.strokeStyle = C.gold; g.lineWidth = 5; g.beginPath(); g.arc(0, -8, 14, Math.PI, 0); g.stroke();
    g.fillStyle = goldGrad(-8, 22); rr(-20, -8, 40, 32, 5); g.fill();
    g.restore();
  }
  g.restore();
}
function escRegistro(t) {
  fondoTBC(t, { dim: 0.55 });
  const wx = 160, wy = 90, ww = 1600, wh = 900;
  const r2 = at('r2', 0), clicD = at('r2', 0.25);
  const logged = t > clicD + 0.4;
  const r3 = at('r3', 0), r5 = at('r5', 0);
  const tab = t > r5 ? 0 : -1;
  const final = P(t, at('r9', 0), 0.5);
  const prof = t > at('r8', 0.45) && t < at('r9', 0) ? 3 : tab;
  web(wx, wy, ww, wh, t, {
    tab: prof, usuario: logged ? ['Veltra', 'picaro'] : null, alpha: P(t, ESC.registro.ini + 0.2, 0.6) * (1 - 0.75 * final),
    discordHi: vis(t, clicD - 0.8, clicD + 0.3, 0.2), discordPress: Math.max(0, 1 - Math.abs(t - clicD) * 5),
    contenido: (x, y, w, h) => {
      if (t < r5) {
        // portada pública
        const gr = g.createLinearGradient(0, y, 0, y + 400); gr.addColorStop(0, '#2a1640'); gr.addColorStop(1, '#15101c');
        g.fillStyle = gr; g.fillRect(x, y, w, 400);
        emblema(x + 260, y + 210, 0.75, t);
        txt('Pacto Oscuro', x + 500, y + 150, { size: 80, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
        txt('Hermandad de WoW Perú', x + 505, y + 225, { size: 36, color: C.text, align: 'left' });
        [['Quiénes somos', 0], ['Cómo entrar', 1]].forEach(([s, i]) => {
          const bx = x + 120 + i * 720, by = y + 450;
          rr(bx, by, 640, 220, 12); g.fillStyle = '#1a1422'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#3a3448'; g.stroke();
          txt(s, bx + 32, by + 50, { size: 38, fam: 'Cinzel', w: 700, color: C.goldL, align: 'left' });
          for (let k = 0; k < 3; k++) { rr(bx + 32, by + 100 + k * 34, 560 - k * 90, 14, 7); g.fillStyle = '#3a3448'; g.fill(); }
        });
        chip('Portada pública', x + w - 180, y + 60, { size: 30, alpha: vis(t, at('r1', 0.4), r2, 0.3) });
      }
      if (logged && t < r5) {
        // tu personaje principal de TBC
        g.fillStyle = 'rgba(0,0,0,0.6)'; g.fillRect(x, y, w, h);
        const pm = P(t, r3 - 0.2, 0.5);
        const mx = x + w / 2 - 440, my = y + 60;
        frame(mx, my, 880, 600, { title: 'Tu personaje principal de TBC', alpha: pm, titleSize: 30 });
        const typed = (s, a) => s.slice(0, Math.floor(s.length * P(t, a, 0.6)));
        campo(mx + 60, my + 90, 760, 'Nombre', typed('Veltra', at('r3', 0.45)), { alpha: pm, foco: t > at('r3', 0.4) && t < at('r3', 0.6) ? 1 : 0, color: CLS.picaro });
        campo(mx + 60, my + 200, 360, 'Clase', t > at('r3', 0.62) ? 'Pícaro' : '', { alpha: pm, color: CLS.picaro });
        campo(mx + 460, my + 200, 360, 'Spec', t > at('r3', 0.8) ? 'Combate' : '', { alpha: pm });
        button(mx + 60, my + 340, 760, 70, 'Guardar', { kind: 'MS', size: 32, alpha: pm });
        const hiNo = vis(t, at('r4', 0.25), at('r4', 0.75), 0.3);
        button(mx + 60, my + 440, 760, 70, 'No voy a raidear en TBC', { kind: 'PASS', size: 30, alpha: pm, hi: hiNo });
        if (hiNo > 0) cursor(mx + 600, my + 485, 0, hiNo);
        chip('Respuesta válida', mx + 440, my + 560, { size: 30, alpha: P(t, at('r4', 0.35), 0.4) * pm, color: '#9dffb8', border: '#6dff8e' });
      }
      if (t >= r5) {
        // mis personajes
        txt('Mis personajes', x + 80, y + 70, { size: 48, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
        PERSONAJES.forEach((pj, i) => {
          const p = P(t, r5 + 0.3 + i * 0.35, 0.5);
          tarjetaPJ(x + 80, y + 115 + i * 228, 900, pj, t, {
            alpha: eOut(p),
            alerta: i === 2 ? vis(t, at('r6', 0.1), at('r7', 0.05), 0.3) : 0,
            candado: i === 0 ? P(t, at('r7', 0.1), 0.4) : 0,
            prof: i < 2 ? P(t, at('r8', 0.05) + i * 0.3, 0.4) : P(t, at('r8', 0.05) + 0.6, 0.4),
          });
        });
        // panel lateral con la explicación
        const lado = (s, a, b, col = C.text) => txt(s, x + 1260, y + 250, { size: 36, w: 700, color: col, alpha: vis(t, a, b, 0.3), maxW: 540 });
        lado('Tu principal y tus alts', at('r5', 0.4), at('r6', 0));
        if (vis(t, at('r6', 0.1), at('r7', 0), 0.3) > 0) {
          keyword('OBLIGATORIAS', x + 1260, y + 220, 50, P(t, at('r6', 0.05), 0.4), { alpha: vis(t, at('r6', 0.05), at('r7', 0), 0.3) });
          txt('Clase y spec', x + 1260, y + 300, { size: 36, w: 700, color: C.goldL, alpha: vis(t, at('r6', 0.05), at('r7', 0), 0.3) });
          txt('Sin ellas: apuntado,', x + 1260, y + 560, { size: 32, w: 700, color: '#ff9a8a', alpha: vis(t, at('r6', 0.4), at('r7', 0), 0.3) });
          txt('pero no existe para el reparto', x + 1260, y + 605, { size: 32, w: 700, color: '#ff9a8a', alpha: vis(t, at('r6', 0.4), at('r7', 0), 0.3) });
        }
        if (vis(t, at('r7', 0), at('r8', 0), 0.3) > 0) {
          const a = vis(t, at('r7', 0), at('r8', 0), 0.3);
          txt('Tu principal', x + 1260, y + 220, { size: 40, fam: 'Cinzel', w: 700, color: C.gold, alpha: a });
          txt('solo lo cambia un oficial', x + 1260, y + 280, { size: 34, w: 700, color: C.text, alpha: a });
          txt('Nadie se cuela en la fila', x + 1260, y + 360, { size: 32, color: C.dim, alpha: a * P(t, at('r7', 0.5), 0.4) });
        }
        if (vis(t, at('r8', 0), at('r8', 0.45), 0.3) > 0) {
          const a = vis(t, at('r8', 0), at('r8', 0.45), 0.3);
          txt('Profesiones', x + 1260, y + 220, { size: 40, fam: 'Cinzel', w: 700, color: C.gold, alpha: a });
          txt('debajo de cada personaje', x + 1260, y + 280, { size: 34, w: 700, color: C.text, alpha: a });
        }
      }
      if (prof === 3) {
        // pestaña Profesiones: la ve toda la hermandad
        g.fillStyle = 'rgba(12,10,16,0.97)'; g.fillRect(x, y, w, h);
        txt('Profesiones de la hermandad', x + 80, y + 70, { size: 46, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
        [['Alquimia', [['Veltra', 'picaro', 1], ['Aurelio', 'sacerdote', 0]]], ['Herrería', [['Kharion', 'guerrero', 1], ['Dorn', 'guerrero', 0]]],
          ['Joyería', [['Lunaria', 'mago', 1]]], ['Encantamiento', [['Veltrix', 'mago', 0], ['Oscuria', 'brujo', 1]]]].forEach(([pr, gente], i) => {
          const ry = y + 150 + i * 120;
          rr(x + 80, ry, w - 160, 100, 10); g.fillStyle = '#1a1422'; g.fill();
          txt(pr, x + 120, ry + 50, { size: 38, w: 800, color: '#cfe8ff', align: 'left' });
          gente.forEach(([n, c, max], k) => txtRich([[n, CLS[c], 700], [max ? '  ★ al máximo' : '', C.gold, 700]], x + 520 + k * 420, ry + 50, { size: 34 }));
        });
        txt('La ve toda la hermandad: sabes a quién pedirle algo', x + w / 2, y + 700, { size: 36, w: 700, color: C.goldL });
      }
    }
  });
  if (!logged && t > r2 - 0.2 && t < clicD + 0.5) cursor(lerp(1200, wx + ww - 180, sm(P(t, r2, clicD - r2 - 0.1))), lerp(800, wy + 60 + 42, sm(P(t, r2, clicD - r2 - 0.1))), Math.max(0, 1 - Math.abs(t - clicD) * 5));
  const pk = vis(t, ESC.registro.ini + 0.1, at('r1', 0.35), 0.4);
  if (pk > 0) { veil(0.7 * pk); chip('PASO 1', 960, 400, { size: 40, alpha: pk, color: C.goldL }); keyword('REGISTRO', 960, 520, 130, P(t, ESC.registro.ini + 0.2, 0.6), { alpha: pk }); }
  const rol = vis(t, at('r2', 0.45), r3 - 0.3, 0.3);
  if (rol > 0) chip('Lo que ves depende de tu rol en el Discord de la hermandad', 960, 1030, { size: 32, alpha: rol });
  const sin = vis(t, at('r4', 0.8), r5, 0.3);
  if (sin > 0) chip('Sin contestar, no se entra', 960, 1030, { size: 34, alpha: sin, color: '#ff9a8a', border: '#ff5a4f' });
  if (final > 0) {
    keyword('SIN REGISTRO NO HAY CORE', 960, 440, 76, final);
    keyword('SIN CORE NO HAY ROTACIÓN', 960, 590, 76, P(t, at('r9', 0.5), 0.5), { tint: '#ff9a6a' });
  }
}

// ============================================================ 5. LAS CORES
function formacion(x, y, t, o = {}) {
  const { alpha = 1, hlRol = null, oficial = 0 } = o;
  g.save(); g.globalAlpha *= alpha;
  for (let gi = 0; gi < 5; gi++) {
    const gx = x + gi * 196;
    txt('Grupo ' + (gi + 1), gx + 90, y, { size: 26, w: 700, color: C.dim });
    for (let k = 0; k < 5; k++) {
      const [n, cls, rol] = CORE[gi * 5 + k];
      const ry = y + 30 + k * 64;
      const on = hlRol && hlRol === rol;
      rr(gx, ry, 180, 56, 6);
      g.fillStyle = rgba(CLS[cls], on ? 0.4 : 0.18); g.fill();
      g.lineWidth = on ? 3 : 1.5; g.strokeStyle = on ? C.goldL : rgba(CLS[cls], 0.6); g.stroke();
      txt(n, gx + 12, ry + 29, { size: 26, w: 800, color: CLS[cls], align: 'left', shadow: false });
      if (rol !== 'dps') iconoRol(rol, gx + 152, ry + 28, 0.8);
    }
  }
  g.restore();
}
function escCores(t) {
  fondoTBC(t, { dim: 0.5 });
  const e = ESC.cores;
  // k1: dos cores
  const v1 = vis(t, e.ini + 0.3, at('k2', 0.02), 0.4);
  if (v1 > 0) {
    keyword('CORE', 960, 140, 110, P(t, at('k1', 0.02), 0.5), { alpha: v1 });
    txt('el equipo fijo de 25 que raidea junto cada semana', 960, 240, { size: 38, w: 700, color: C.text, alpha: v1 * P(t, at('k1', 0.15), 0.4) });
    [['Core 1', 'Horario A', 520], ['Core 2', 'Horario B', 1400]].forEach(([n, hs, cx], j) => {
      const p = P(t, at('k1', 0.45) + j * 0.3, 0.5) * v1;
      frame(cx - 330, 330, 660, 560, { title: n, alpha: p });
      for (let i = 0; i < 25; i++) hero(cx - 240 + (i % 5) * 120, 440 + Math.floor(i / 5) * 95, 0.36, CORE[(i + j * 7) % 25][1], { alpha: p });
      chip(hs, cx, 850, { size: 32, alpha: p * P(t, at('k1', 0.8), 0.4), color: C.goldL });
    });
    txt('=', 960, 610, { size: 120, fam: 'Cinzel', w: 700, color: C.gold, alpha: v1 * P(t, at('k1', 0.62), 0.4) });
    chip('Igual de competitivas · solo cambia el horario', 960, 990, { size: 34, alpha: v1 * P(t, at('k1', 0.66), 0.4) });
  }
  // k2-k3: la página Cores
  const v2 = vis(t, at('k2', 0), at('k4', 0.02), 0.4);
  if (v2 > 0) {
    web(80, 60, 1760, 960, t, {
      tab: 1, usuario: ['Veltra', 'picaro'], alpha: v2,
      contenido: (x, y, w, h) => {
        [['Core 1', 1], ['Core 2', 0]].forEach(([n, on], i) => {
          rr(x + 60 + i * 190, y + 30, 170, 50, 8); g.fillStyle = on ? '#3b2360' : '#1a1426'; g.fill();
          g.lineWidth = 2; g.strokeStyle = on ? C.gold : '#4a4060'; g.stroke();
          txt(n, x + 145 + i * 190, y + 56, { size: 28, w: 700, color: on ? C.goldL : C.dim });
        });
        const cnt = P(t, at('k2', 0.35), 0.4);
        [['tanque', 'Tanques', 3], ['sanador', 'Sanadores', 6], ['dps', 'DPS', 16]].forEach(([r, n, c], i) => {
          iconoRol(r, x + 520 + i * 250, y + 55, 0.9, cnt);
          txt(`${n}: ${c}`, x + 550 + i * 250, y + 56, { size: 30, w: 700, color: C.text, align: 'left', alpha: cnt });
        });
        const hl = t > at('k3', 0.35) ? (t < at('k3', 0.7) ? 'tanque' : 'sanador') : null;
        formacion(x + 60, y + 130, t, { alpha: P(t, at('k2', 0.05), 0.5), hlRol: t > at('k3', 0) ? hl : null });
        // buffos
        const pb = P(t, at('k2', 0.7), 0.5);
        g.save(); g.globalAlpha *= pb;
        rr(x + 1080, y + 110, 600, 440, 12); g.fillStyle = '#1a1422'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#3a3448'; g.stroke();
        txt('Buffos que aporta cada clase', x + 1110, y + 150, { size: 30, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
        BUFFOS.forEach(([c, n, b], i) => txtRich([[n + ': ', CLS[c], 800], [b, C.text, 500]], x + 1110, y + 210 + i * 56, { size: 30 }));
        g.restore();
        const po = P(t, at('k3', 0.05), 0.5);
        if (po > 0) {
          rr(x + 1080, y + 580, 600, 150, 12); g.fillStyle = 'rgba(80,50,15,0.9)'; g.globalAlpha = po; g.fill();
          g.lineWidth = 3; g.strokeStyle = C.gold; g.stroke(); g.globalAlpha = 1;
          txt('Lista oficial', x + 1380, y + 625, { size: 36, fam: 'Cinzel', w: 700, color: C.goldL, alpha: po });
          txt('la arma un oficial y marca tanques y sanadores', x + 1380, y + 680, { size: 26, w: 700, color: C.text, alpha: po });
        }
      }
    });
  }
  // k4-k5: el requisito
  const v4 = vis(t, at('k4', 0), e.fin, 0.4);
  if (v4 > 0) {
    txt('Para entrar en la rotación de marcas:', 960, 120, { size: 50, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v4 });
    const pasos = [['1', 'Entra con Discord', 0.42], ['2', 'Registra tu principal de TBC', 0.6], ['3', 'Completa «Mis personajes» con clase y spec', 0.75]];
    pasos.forEach(([n, s, f], i) => {
      const p = P(t, at('k4', f), 0.4) * v4;
      if (p <= 0) return;
      const y = 250 + i * 120;
      g.save(); g.globalAlpha *= p;
      rr(260, y - 45, 900, 90, 14); g.fillStyle = 'rgba(18,12,30,0.92)'; g.fill(); g.lineWidth = 3; g.strokeStyle = C.gold2; g.stroke();
      g.beginPath(); g.arc(320, y, 34, 0, 7); g.fillStyle = goldGrad(y - 34, y + 34); g.fill();
      txt(n, 320, y + 2, { size: 40, color: '#2a1805', shadow: false });
      txt(s, 380, y, { size: 38, w: 700, color: C.text, align: 'left' });
      g.restore();
    });
    const pc = P(t, at('k4', 0.2), 0.5) * v4;
    arrow(1190, 370, 1320, 370, pc, C.gold, 8);
    keyword('CORE', 1470, 370, 84, pc, { alpha: v4 });
    arrow(1470, 430, 1470, 560, pc, C.gold, 8);
    keyword('ROTACIÓN', 1470, 630, 72, P(t, at('k4', 0.05), 0.5), { alpha: v4, tint: '#8dff6a' });
    const p5 = P(t, at('k5', 0), 0.5);
    if (p5 > 0) {
      hero(700, 950, 0.9, 'mago', { name: '¿?', gray: 1, alpha: p5 });
      txt('Sin registro: el sistema no te ve', 1150, 860, { size: 42, w: 800, color: '#ff9a8a', alpha: p5 });
      txt('y no te toca turno', 1150, 920, { size: 42, w: 800, color: '#ff9a8a', alpha: P(t, at('k5', 0.5), 0.4) });
    }
  }
}

// ============================================================ 6. BISTOOLTIP
function escBis(t) {
  fondoTBC(t, { dim: 0.55 });
  const e = ESC.bistooltip;
  // b1: qué es BiS
  const v1 = vis(t, e.ini + 0.2, at('b2', 0.02), 0.4);
  if (v1 > 0) {
    chip('PASO 2 · BISTOOLTIP', 960, 150, { size: 40, alpha: v1 * P(t, at('b1', 0), 0.4), color: C.goldL });
    keyword('BiS', 960, 330, 200, P(t, at('b1', 0.3), 0.5), { alpha: v1, fam: 'Cinzel', w: 700 });
    txt('Best in Slot', 960, 480, { size: 60, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v1 * P(t, at('b1', 0.5), 0.4) });
    txt('el mejor objeto posible para cada parte de tu equipo', 960, 570, { size: 42, w: 700, color: C.text, alpha: v1 * P(t, at('b1', 0.65), 0.4) });
    ['pechera', 'capa', 'espada', 'anillo'].forEach((k, i) => itemIcon(660 + i * 200, 760, 110, k, { alpha: v1 * P(t, at('b1', 0.7) + i * 0.15, 0.4), border: C.gold, glow: 0.5 }));
  }
  // b2: pasar el ratón por un objeto
  const v2 = vis(t, at('b2', 0), at('b3', 0.02), 0.4);
  if (v2 > 0) {
    frame(200, 300, 560, 560, { title: 'Bolsa', alpha: v2 });
    g.save(); g.globalAlpha *= v2;
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
      rr(250 + c * 120, 360 + r * 120, 100, 100, 8); g.fillStyle = 'rgba(0,0,0,0.55)'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#4a4060'; g.stroke();
    }
    g.restore();
    itemIcon(300, 410, 90, 'espada', { alpha: v2, glow: P(t, at('b2', 0.15), 0.3) });
    itemIcon(420, 530, 90, 'anillo', { alpha: v2 });
    itemIcon(540, 410, 90, 'capa', { alpha: v2 });
    const m = sm(P(t, at('b2', 0.02), 0.8));
    cursor(lerp(700, 318, m), lerp(900, 428, m), 0, v2);
    const pt = P(t, at('b2', 0.15), 0.4) * v2;
    tooltipObjeto(820, 250, t, { alpha: pt, bis: P(t, at('b2', 0.35), 2.2) });
  }
  // b3-b4: minimapa y ventana
  const v3 = vis(t, at('b3', 0), at('b5', 0.02), 0.4);
  if (v3 > 0) {
    const clic = at('b3', 0.55);
    const abierta = P(t, clic + 0.1, 0.5);
    const [bx, by] = minimapa(1700, 220, 1, t, { alpha: v3, hi: vis(t, clic - 0.8, clic + 0.4, 0.2), press: Math.max(0, 1 - Math.abs(t - clic) * 5) });
    const m = sm(P(t, at('b3', 0.3), clic - at('b3', 0.3) - 0.1));
    cursor(lerp(1300, bx, m), lerp(700, by, m), Math.max(0, 1 - Math.abs(t - clic) * 5), v3 * (1 - abierta * 0.0));
    txt('clic izquierdo', bx - 60, by + 80, { size: 30, w: 700, color: C.goldL, alpha: v3 * vis(t, at('b3', 0.4), at('b4', 0), 0.3) });
    // chat con el comando
    const pc = P(t, at('b3', 0.75), 0.3);
    if (pc > 0) {
      g.save(); g.globalAlpha *= v3 * pc;
      rr(60, 900, 640, 70, 8); g.fillStyle = 'rgba(0,0,0,0.7)'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#6d6578'; g.stroke();
      const cmd = '/bistooltip';
      txt('Decir: ' + cmd.slice(0, Math.floor(cmd.length * P(t, at('b3', 0.78), 0.8))), 90, 936, { size: 36, w: 700, color: '#fff', align: 'left', shadow: false });
      g.restore();
    }
    // ventana
    const hov = t > at('b4', 0.6) ? [5, 0] : null;
    if (abierta > 0) {
      ventanaBis(160, 120, t, { alpha: v3 * abierta, filas: P(t, clic + 0.3, 1.5), hover: hov });
      txt('Listas por clase, spec y fase', 650, 60, { size: 40, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v3 * P(t, clic + 0.6, 0.5) });
      const p6 = vis(t, at('b4', 0), at('b5', 0), 0.3);
      if (p6 > 0) {
        keyword('HASTA 6 OPCIONES', 1400, 560, 56, P(t, at('b4', 0.02), 0.4), { alpha: p6 });
        txt('por cada parte del equipo', 1400, 630, { size: 34, w: 700, color: C.text, alpha: p6 });
      }
      if (hov) {
        const ph = P(t, at('b4', 0.6), 0.3);
        const ix = 160 + 330, iy = 120 + 180 + 5 * 88;
        cursor(ix + 10, iy + 10, 0, ph * v3);
        g.save(); g.globalAlpha *= ph * v3;
        rr(ix + 60, iy - 150, 470, 130, 8); g.fillStyle = 'rgba(8,10,28,0.97)'; g.fill(); g.lineWidth = 3; g.strokeStyle = '#8f8fa8'; g.stroke();
        txt(ITEM_TBC, ix + 84, iy - 115, { size: 30, w: 700, color: '#b561ff', align: 'left', shadow: false });
        txt('Sale de: Guarida de Gruul', ix + 84, iy - 75, { size: 28, color: '#fff', align: 'left', shadow: false });
        txt('Jefe: Gruul', ix + 84, iy - 40, { size: 28, color: '#fff', align: 'left', shadow: false });
        g.restore();
      }
    }
  }
  // b5-b6: fuente The Burning Crusade y aviso
  const v5 = vis(t, at('b5', 0), e.fin, 0.4);
  if (v5 > 0) {
    const clic = at('b5', 0.3);
    const [bx, by] = minimapa(1500, 330, 1.2, t, { alpha: v5, hi: vis(t, clic - 0.6, clic + 0.3, 0.2), press: Math.max(0, 1 - Math.abs(t - clic) * 5) });
    cursor(bx, by, Math.max(0, 1 - Math.abs(t - clic) * 5), v5 * (1 - P(t, clic + 0.8, 0.3)));
    txt('clic derecho', bx, by + 80, { size: 30, w: 700, color: C.goldL, alpha: v5 * vis(t, at('b5', 0.1), at('b6', 0), 0.3) });
    const po = P(t, clic + 0.15, 0.4) * v5;
    frame(200, 250, 880, 330, { title: 'Opciones de BisTooltip', alpha: po, titleSize: 28 });
    g.save(); g.globalAlpha *= po;
    txt('Fuente', 260, 340, { size: 30, w: 700, color: C.dim, align: 'left' });
    rr(260, 370, 760, 70, 10); g.fillStyle = '#0c0a10'; g.fill();
    const elegido = t > at('b5', 0.72);
    g.lineWidth = elegido ? 4 : 2; g.strokeStyle = elegido ? '#8dff6a' : '#5a4a30'; g.stroke();
    txt(elegido ? 'The Burning Crusade' : '…', 290, 406, { size: 38, w: 800, color: elegido ? '#b8ff9a' : C.dim, align: 'left' });
    if (elegido) checkmark(975, 405, 40, P(t, at('b5', 0.72), 0.4));
    g.restore();
    const pr = P(t, at('b6', 0), 0.5);
    if (pr > 0) {
      frame(260, 720, 1400, 220, { alpha: pr, glow: 0.2 });
      txt('!', 350, 830, { size: 110, fam: 'Cinzel', w: 700, color: '#ffcc4d', alpha: pr, glow: 20, glowColor: '#ffcc4d' });
      txt('Las listas son una referencia', 1000, 800, { size: 50, fam: 'Cinzel', w: 700, color: C.goldL, alpha: pr });
      txt('El servidor puede cambiar estadísticas o botín', 1000, 870, { size: 36, w: 700, color: C.text, alpha: P(t, at('b6', 0.35), 0.4) });
    }
  }
}

// ============================================================ 7. RESERVA EN LA WEB
const LISTA_GRUUL = [['espada', ITEM_TBC, 1], ['anillo', 'Anillo del Rey Ogro', 0], ['capa', 'Capa de la Guarida', 0], ['pechera', 'Hombreras de Terrallende', 0]];
function escReserva(t) {
  fondoTBC(t, { dim: 0.55 });
  const e = ESC.reserva;
  // v1: el oficial comparte el enlace
  const v1 = vis(t, e.ini + 0.2, at('v2', 0.05), 0.4);
  if (v1 > 0) {
    chip('PASO 3', 960, 70, { size: 36, alpha: v1 * P(t, at('v1', 0), 0.4), color: C.goldL });
    keyword('RESERVA', 960, 190, 110, P(t, at('v1', 0.05), 0.5), { alpha: v1 });
    frame(460, 380, 1000, 300, { title: 'Mensaje de un oficial', alpha: v1 * P(t, at('v1', 0.4), 0.4), titleSize: 28 });
    g.save(); g.globalAlpha *= v1 * P(t, at('v1', 0.45), 0.4);
    heroPJ('morgrath', 560, 610, 0.55, { nameSize: 24 });
    txt('Reservas para la próxima banda:', 660, 490, { size: 36, w: 700, color: C.text, align: 'left' });
    rr(660, 540, 560, 64, 10); g.fillStyle = 'rgba(88,101,242,0.2)'; g.fill(); g.lineWidth = 2.5; g.strokeStyle = '#8a95ff'; g.stroke();
    txt('Enlace de la raid', 690, 573, { size: 34, w: 800, color: '#aab4ff', align: 'left' });
    g.restore();
  }
  // v2-v3: la página de reservas
  const v2 = vis(t, at('v2', 0), e.fin, 0.4);
  if (v2 > 0) {
    const sh = sm(P(t, at('v3', 0.55), 0.8));
    const clic = at('v2', 0.35);
    const res = t > clic;
    web(lerp(60, 40, sh), 60, lerp(1180, 1000, sh), 960, t, {
      tab: -1, sinTabs: true, usuario: ['Veltra', 'picaro'], alpha: v2, url: 'softres.xdataplusx.com',
      contenido: (x, y, w, h) => {
        txt('Reservas · Guarida de Gruul', x + 50, y + 60, { size: 42, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
        campo(x + 50, y + 110, 360, 'Tu personaje', 'Veltra', { color: CLS.picaro, foco: vis(t, at('v2', 0.05), at('v2', 0.25), 0.2) });
        txt(`Reservas: ${res ? 1 : 0} de 1`, x + w - 50, y + 150, { size: 32, w: 800, color: res ? '#9dffb8' : C.text, align: 'right' });
        LISTA_GRUUL.forEach(([k, n, rec], i) => {
          const ry = y + 250 + i * 110;
          rr(x + 50, ry, w - 100, 96, 10); g.fillStyle = i % 2 ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.06)'; g.fill();
          if (rec && res) { g.lineWidth = 3; g.strokeStyle = C.gold; g.stroke(); }
          itemIcon(x + 105, ry + 48, 70, k);
          txt(n, x + 160, ry + 36, { size: 32, w: 700, color: '#b561ff', align: 'left' });
          txt('Gruul', x + 160, ry + 72, { size: 24, color: C.dim, align: 'left' });
          const r = rec && res;
          button(x + w - 280, ry + 18, 220, 60, r ? 'Reservado' : 'Reservar', { kind: r ? 'MS' : 'red', size: 28, press: rec && Math.abs(t - clic) < 0.15 ? 1 : 0 });
        });
      }
    });
    // la recomendación de BisTooltip al lado
    const pb = P(t, at('v2', 0.0), 0.5) * (1 - sh);
    if (pb > 0) {
      frame(1300, 260, 560, 300, { title: 'BisTooltip', alpha: pb, titleSize: 28 });
      g.save(); g.globalAlpha *= pb;
      txt('Mano derecha · puesto 1', 1580, 340, { size: 30, w: 700, color: C.goldL });
      itemIcon(1400, 440, 80, 'espada', { border: C.gold, glow: 0.6 });
      txt(ITEM_TBC, 1460, 425, { size: 30, w: 700, color: '#b561ff', align: 'left' });
      txt('Guarida de Gruul · Gruul', 1460, 465, { size: 26, color: C.text, align: 'left' });
      g.restore();
      arrow(1300, 440, 1160, 400, P(t, at('v2', 0.12), 0.4) * pb, C.gold, 6);
    }
    const m = sm(P(t, at('v2', 0.12), clic - at('v2', 0.12) - 0.1));
    if (t < at('v3', 0.4)) cursor(lerp(1000, 1180 - 280 + 60 + 110, m), lerp(900, 60 + 145 + 250 + 48, m), Math.max(0, 1 - Math.abs(t - clic) * 5), v2);
    chip('Normalmente 1 por persona · el oficial decide cuántas', 640, 1040, { size: 30, alpha: vis(t, at('v2', 0.55), at('v3', 0.3), 0.3) });
    chip('Así no gastas tu reserva en algo que no te sirve', 640, 1040, { size: 30, alpha: vis(t, at('v3', 0.05), at('v3', 0.55), 0.3), color: C.goldL });
    if (sh > 0) {
      arrow(1060, 520, 1180, 520, sh, C.gold, 8);
      frame(1220, 300, 640, 440, { title: 'SoftReserve335', alpha: sh });
      txt('Reservas cargadas', 1540, 370, { size: 34, w: 700, color: C.goldL, alpha: sh });
      [['Veltra', 'picaro', 'espada', ITEM_TBC], ['Lunaria', 'mago', 'anillo', 'Anillo del Rey Ogro'], ['Grimta', 'guerrero', 'capa', 'Capa de la Guarida']].forEach(([n, c, k, it], i) => {
        const p = P(t, at('v3', 0.65) + i * 0.25, 0.3) * sh;
        itemIcon(1290, 450 + i * 90, 56, k, { alpha: p });
        txt(n, 1340, 436 + i * 90, { size: 30, w: 700, color: CLS[c], align: 'left', alpha: p });
        txt(it, 1340, 468 + i * 90, { size: 24, color: '#b561ff', align: 'left', alpha: p });
        chip('SR', 1800, 450 + i * 90, { size: 24, alpha: p, color: C.goldL });
      });
    }
  }
}

// ============================================================ 8. CAE UN OBJETO
function avisoBotin(x, y, t, o = {}) {
  const { alpha = 1, hi = {}, press = {}, timer = 1, count = null, dado = null, lista = 0, listaPress = 0, s = 1, nota = 0 } = o;
  if (alpha <= 0) return;
  g.save(); g.translate(x, y); g.scale(s, s);
  const w = 820, h = 560;
  frame(-w / 2, -h / 2, w, h, { title: '¡Botín!', alpha });
  g.globalAlpha *= alpha;
  itemIcon(-w / 2 + 110, -150, 110, 'espada', { glow: 0.6 });
  txt(ITEM_TBC, -w / 2 + 190, -180, { size: 46, w: 700, color: '#b561ff', align: 'left' });
  txt('Gruul · Guarida de Gruul', -w / 2 + 190, -128, { size: 30, color: C.dim, align: 'left' });
  if (nota > 0) chip('Nadie lo reservó', -w / 2 + 330, -60, { size: 28, alpha: nota, color: C.goldL });
  button(w / 2 - 190, -250, 150, 50, 'Ver lista', { kind: 'gold', size: 26, hi: lista, press: listaPress });
  const bw = 220, gap = 30, bx0 = -(bw * 3 + gap * 2) / 2;
  ['MS', 'OS', 'PASS'].forEach((k, i) => button(bx0 + i * (bw + gap), 10, bw, 96, k, { kind: k, size: 46, hi: hi[k] || 0, press: press[k] || 0, dimmed: (press.MS && k !== 'MS') ? 1 : 0 }));
  rr(-340, 160, 680, 34, 17); g.fillStyle = '#0a0710'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#6a5a3a'; g.stroke();
  const col = timer > 0.35 ? '#e8c46a' : (Math.floor(t * 6) % 2 ? '#ff5a4f' : '#ff9a4f');
  if (timer > 0) { rr(-336, 164, 672 * timer, 26, 13); g.fillStyle = col; g.fill(); }
  txt(count !== null ? `Tiempo: ${count} s` : 'Tiempo', 0, 225, { size: 30, w: 700, color: count !== null ? col : C.dim });
  if (dado !== null) txt(`Tu dado: ${dado}`, 0, -40, { size: 52, fam: 'Cinzel', w: 700, color: C.gold, glow: 20, glowColor: 'rgba(232,196,106,0.7)' });
  g.restore();
}
function escObjeto(t) {
  fondoTBC(t, { dim: 0.35 });
  const e = ESC.objeto;
  // o1: cae un objeto; obligatorio
  const v1 = vis(t, e.ini + 0.2, at('o2', 0.02), 0.4);
  if (v1 > 0) {
    cuerpo(960, 900, 1.4, t, v1);
    const pi = P(t, at('o1', 0.15), 0.8);
    itemIcon(960, lerp(880, 480, eOut(pi)), 150, 'espada', { glow: 1, alpha: pi * v1 });
    txt('¡Cae un objeto!', 960, 290, { size: 60, fam: 'Cinzel', w: 700, color: C.gold, alpha: pi * v1 });
    chip('SoftReserve335: obligatorio para todos los que van', 960, 1010, { size: 34, alpha: v1 * P(t, at('o1', 0.5), 0.4), color: C.goldL });
  }
  // o2: si alguien lo reservó
  const v2 = vis(t, at('o2', 0), at('o3', 0.02), 0.4);
  if (v2 > 0) {
    keyword('RESERVA', 960, 170, 100, P(t, at('o2', 0.02), 0.4), { alpha: v2 });
    [['veltra', 1, 45], ['lunaria', 1, 81], ['kharion', 0], ['sombrix', 0]].forEach(([who, sr, d], i) => {
      const x = 390 + i * 380, p = P(t, at('o2', 0.1) + i * 0.12, 0.35) * v2;
      heroPJ(who, x, 720, 1, { alpha: p, gray: sr ? 0 : P(t, at('o2', 0.45), 0.4), glow: sr ? 0.6 : 0 });
      if (sr) {
        chip('RESERVÓ', x, 780, { size: 28, alpha: p, color: C.goldL });
        const n = rollNum(t, at('o2', 0.55) + i * 0.15, 0.8, d, i);
        if (n !== null) txt('Dado: ' + n, x, 850, { size: 42, fam: 'Cinzel', w: 700, color: C.gold, alpha: p });
      } else txt('no reservó · no tira', x, 790, { size: 30, w: 700, color: '#9a93a8', alpha: p * P(t, at('o2', 0.45), 0.4) });
    });
  }
  // o3-o6: el aviso con MS / OS / PASS
  const v3 = vis(t, at('o3', 0), e.fin, 0.4);
  if (v3 > 0) {
    const lado = 1 - sm(P(t, at('o6', 0), 0.7));
    const ax = lerp(960, 560, lado), ay = 560;
    const hi = { MS: vis(t, at('o3', 0.2), at('o4', 0), 0.3), OS: vis(t, at('o4', 0), at('o5', 0), 0.3), PASS: vis(t, at('o5', 0), at('o6', 0), 0.3) };
    const clic = at('o6', 0.33), dT = at('o6', 0.42), t6 = at('o6', 0.7);
    if (t > clic - 1.0 && t < clic) hi.MS = P(t, clic - 1.0, 0.4);
    let timer = 1, count = null;
    if (t > t6) { const k = Math.min(5, Math.floor((t - t6) / 0.5)); count = Math.max(1, 6 - k); timer = clamp(1 - (t - t6) / 3.4, 0.05, 1); }
    avisoBotin(ax, ay, t, { alpha: v3, hi, press: { MS: t > clic ? 1 : 0 }, timer, count, dado: rollNum(t, dT, 0.9, 87, 3), nota: P(t, at('o3', 0.02), 0.4) * (1 - P(t, at('o6', 0), 0.3)), s: lerp(1, 0.9, lado) });
    if (t > dT && t < dT + 1.6) dado(ax + 520, ay - 60, 1.1, (t - dT) * 9 * (1 - P(t, dT, 1.0)) + 0.3, { alpha: vis(t, dT, dT + 1.6, 0.2) });
    const cp = vis(t, clic - 1.1, clic + 0.8, 0.3);
    if (cp > 0) { const m = sm(P(t, clic - 1.1, 0.9)); cursor(lerp(1300, 710, m), lerp(900, 618, m), Math.max(0, 1 - Math.abs(t - clic) * 5), cp); }
    const expl = [
      ['MS', 'Necesidad principal', ['Sirve para tu papel principal.', 'Tiene prioridad.'], at('o3', 0.2), at('o4', 0), '#6dff8e'],
      ['OS', 'Necesidad secundaria', ['Te sirve para un papel de reserva.', 'Va después de MS.'], at('o4', 0), at('o5', 0), '#7fb2ff'],
      ['PASS', 'No lo quieres', ['Pasar también queda registrado.'], at('o5', 0), at('o6', 0), '#c9c3d6'],
    ];
    for (const [k, t1, lines, a, b, col] of expl) {
      const v = vis(t, a, b, 0.35);
      if (v <= 0) continue;
      keyword(k, 1440, 330, 150, P(t, a, 0.5), { alpha: v, tint: col });
      txt(t1, 1440, 450, { size: 50, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v });
      lines.forEach((l, i) => txt(l, 1440, 530 + i * 56, { size: 40, color: C.text, alpha: v * P(t, a + 0.4 + i * 0.25, 0.4) }));
    }
    txt('El addon tira el dado por ti', 960, 170, { size: 46, w: 700, color: C.goldL, alpha: vis(t, dT, t6 + 0.1, 0.3) });
    keyword('CUENTA ATRÁS', 960, 170, 72, P(t, t6 + 0.05, 0.4), { tint: '#ffb35a' });
  }
}

// ============================================================ 9. QUIÉN GANA
function reglaOrden(x, y, s, t, o = {}) {
  const { p = [1, 1, 1], hl = -1, alpha = 1 } = o;
  const pasos = [['1', 'Reservas y MS, antes que OS'], ['2', 'Gana quien lleve menos +1'], ['3', 'Al final, decide el dado']];
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  pasos.forEach(([nn, l], i) => {
    const a = eOut(p[i]);
    if (a <= 0) return;
    g.save(); g.globalAlpha *= a; g.translate(lerp(-80, 0, a), i * 150);
    const on = hl === i;
    rr(-560, -58, 1120, 116, 16);
    g.fillStyle = on ? 'rgba(80,50,15,0.95)' : 'rgba(18,12,30,0.92)'; g.fill();
    g.lineWidth = on ? 5 : 3; g.strokeStyle = on ? C.goldL : C.gold2; g.stroke();
    g.beginPath(); g.arc(-480, 0, 42, 0, 7); g.fillStyle = goldGrad(-42, 42); g.fill();
    txt(nn, -480, 3, { size: 52, color: '#2a1805', shadow: false });
    txt(l, -410, 2, { size: 52, w: 700, color: C.text, align: 'left' });
    g.restore();
  });
  g.restore();
}
function cartaTirada(x, y, who, dadoN, mas1, t, o = {}) {
  const { alpha = 1, win = 0, lose = 0, tRoll = 0, tMas = 0 } = o;
  if (alpha <= 0) return;
  const [n, cls] = PJ[who];
  g.save(); g.globalAlpha *= alpha * (1 - 0.45 * lose);
  frame(x - 280, y - 260, 560, 540, { glow: win });
  hero(x, y + 60, 1.2, cls, { name: n, nameSize: 44, glow: 0.4 + win });
  const d = rollNum(t, tRoll, 0.9, dadoN, dadoN);
  txt('Dado', x - 130, y + 140, { size: 34, color: C.dim });
  txt(d === null ? '—' : String(d), x - 130, y + 205, { size: 84, color: C.goldL });
  txt('+1', x + 130, y + 140, { size: 34, color: C.dim });
  const pm = P(t, tMas, 0.4);
  txt(pm > 0 ? String(mas1) : '—', x + 130, y + 205, { size: 84 * (pm > 0 ? lerp(1.4, 1, eOut(pm)) : 1), color: mas1 === 0 ? '#6dff8e' : '#ff9a6a' });
  g.restore();
  if (win > 0) keyword('GANA', x, y - 300, 90, win);
}
function listaTiradas(x, y, t, o = {}) {
  const { alpha = 1, sc = 1, pie = 0 } = o;
  if (alpha <= 0) return;
  const w = 1240, h = 820;
  g.save(); g.translate(x, y); g.scale(sc, sc); g.translate(-w / 2, -h / 2);
  frame(0, 0, w, h, { title: ITEM_TBC + ' — Tiradas', alpha, titleSize: 32 });
  g.globalAlpha *= alpha;
  [['Nombre', 90, 'left'], ['Dado', 640, 'center'], ['+1', 840, 'center'], ['Tipo', 1060, 'center']].forEach(([c, cx, al]) => txt(c, cx, 100, { size: 38, fam: 'Cinzel', w: 700, color: C.gold, align: al }));
  g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(50, 130, w - 100, 2);
  const filas = [['veltra', 12, 0, 'MS'], ['lunaria', 77, 1, 'MS'], ['kharion', 99, 2, 'MS'], ['sombrix', 95, 0, 'OS'], ['brisa', 64, 0, 'OS'], ['ramaz', 58, 1, 'OS'], ['aurelio', null, 0, 'PASS'], ['tukan', null, 1, 'PASS']];
  filas.forEach(([who, d, m, tipo], i) => {
    const ry = 175 + i * 66;
    if (i === 0) { rr(40, ry - 30, w - 80, 60, 8); g.fillStyle = 'rgba(109,255,142,0.12)'; g.fill(); }
    const [n, cls] = PJ[who];
    txt(n, 90, ry, { size: 40, w: 700, color: CLS[cls], align: 'left' });
    if (i === 0) txt('← gana', 330, ry, { size: 32, w: 700, color: '#6dff8e', align: 'left' });
    txt(d === null ? '—' : String(d), 640, ry, { size: 40, w: 700, color: C.text });
    txt(String(m), 840, ry, { size: 40, w: 700, color: C.text });
    const tc = { MS: '#6dff8e', OS: '#7fb2ff', PASS: '#c9c3d6' }[tipo];
    chip(tipo, 1060, ry, { size: 28, color: tc, border: tc });
  });
  g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(50, 712, w - 100, 2);
  txt('Orden: Reservas y MS antes que OS  ›  menos +1  ›  dado más alto', w / 2, 760, { size: 34, w: 700, color: pie > 0 ? C.goldL : C.dim, glow: pie ? 20 * pie : 0, glowColor: 'rgba(232,196,106,0.8)' });
  g.restore();
}
function escGana(t) {
  const e = ESC.gana;
  fondoTBC(t, { dim: 0.5 });
  // w1: el +1
  const v1 = vis(t, e.ini + 0.3, at('w2', 0.02), 0.4);
  if (v1 > 0) {
    txt('¿Quién gana?', 960, 140, { size: 60, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v1 });
    keyword('+1', 960, 360, 200, P(t, at('w1', 0.2), 0.5), { alpha: v1 });
    txt('cada objeto ganado por MS', 960, 500, { size: 42, w: 700, color: C.text, alpha: v1 * P(t, at('w1', 0.3), 0.4) });
    const a2 = P(t, at('w1', 0.5), 0.4) * v1;
    heroPJ('sombrix', 660, 900, 1, { alpha: a2, gray: 0.6 * P(t, at('w1', 0.55), 0.4) });
    heroPJ('ramaz', 1260, 900, 1, { alpha: a2, glow: P(t, at('w1', 0.55), 0.4) });
    txt('+1: 2', 660, 980, { size: 50, color: '#ff9a6a', alpha: a2 });
    txt('+1: 0', 1260, 980, { size: 50, color: '#6dff8e', alpha: a2 });
    chip('PRIORIDAD', 1260, 610, { size: 36, alpha: P(t, at('w1', 0.62), 0.4) * v1 });
    chip('Ganar por RESERVA no suma +1', 960, 1045, { size: 30, alpha: P(t, at('w1', 0.85), 0.4) * v1 });
  }
  // w2-w4: regla y ejemplo
  const v2 = vis(t, at('w2', 0), at('w5', 0.02), 0.4);
  if (v2 > 0) {
    const comp = sm(P(t, at('w3', 0), 0.8));
    txt('LA REGLA DEL ORDEN', 960, lerp(210, 70, comp), { size: lerp(70, 40, comp), fam: 'Cinzel', w: 700, color: C.gold, alpha: v2, glow: 20, glowColor: 'rgba(232,196,106,0.6)' });
    reglaOrden(960, lerp(400, 135, comp), lerp(1, 0.45, comp), t, { p: [P(t, at('w2', 0.12), 0.5), P(t, at('w2', 0.52), 0.5), P(t, at('w2', 0.8), 0.5)], hl: t > at('w4', 0) ? 1 : -1, alpha: v2 });
    const v4 = P(t, at('w3', 0), 0.4) * v2;
    if (v4 > 0) {
      const win = P(t, at('w4', 0), 0.6);
      cartaTirada(560, 700, 'kharion', 99, 2, t, { alpha: v4, tRoll: at('w3', 0.05), tMas: at('w3', 0.35), lose: win });
      cartaTirada(1360, 700, 'veltra', 12, 0, t, { alpha: v4, tRoll: at('w3', 0.55), tMas: at('w3', 0.85), win });
      txt('No es un robo: llevaba menos +1', 960, 1030, { size: 46, w: 700, color: C.goldL, alpha: v4 * P(t, at('w4', 0.3), 0.5) });
    }
  }
  // w5: la lista transparente
  const v5 = vis(t, at('w5', 0), e.fin, 0.4);
  if (v5 > 0) {
    const clic = at('w5', 0.4);
    const op = sm(P(t, clic + 0.1, 0.7));
    avisoBotin(960, 560, t, { alpha: v5 * (1 - op), lista: P(t, at('w5', 0.1), 0.3), listaPress: Math.max(0, 1 - Math.abs(t - clic) * 5), dado: 12 });
    const m = sm(P(t, at('w5', 0.05), clic - at('w5', 0.05) - 0.1));
    cursor(lerp(1500, 1255, m), lerp(900, 305, m), Math.max(0, 1 - Math.abs(t - clic) * 5), v5 * (1 - op));
    if (op > 0) listaTiradas(960, 555, t, { alpha: v5 * op, sc: lerp(0.3, 1, eOut(op)), pie: P(t, at('w5', 0.8), 0.4) });
  }
}

// ============================================================ 10. RECIBIR EL OBJETO
function escRecibir(t) {
  const e = ESC.recibir;
  fondoTBC(t, { dim: 0.3 });
  const v1 = vis(t, e.ini + 0.2, at('e2', 0.05), 0.4);
  if (v1 > 0) {
    ['kharion', 'lunaria', 'sombrix', 'aurelio', 'thorgan', 'brisa', 'ramaz', 'tukan'].forEach((k, i) => heroPJ(k, 250 + i * 205, 1000 - Math.abs(i - 3.5) * 22, 0.75, { alpha: v1 * 0.9, nameSize: 26 }));
    heroPJ('veltra', 960, 1040, 0.95, { alpha: v1, glow: 1, nameSize: 32 });
    const pb = P(t, at('e1', 0), 0.6);
    g.save(); g.globalAlpha *= v1; g.translate(960, 330); g.scale(lerp(1.3, 1, eOut(pb)), lerp(1.3, 1, eOut(pb)));
    frame(-700, -180, 1400, 360, { alpha: clamp(pb * 2), glow: 1 });
    txtRich([['VELTRA', CLS.picaro, 800], [' gana', C.text, 800]], 0, -95, { size: 84, fam: 'Cinzel', align: 'center', alpha: clamp(pb * 2) });
    txt(ITEM_TBC, 0, 0, { size: 56, w: 700, color: '#b561ff', alpha: clamp(pb * 2) });
    txt('Dado 12  ·  MS  ·  llevaba menos +1', 0, 90, { size: 46, w: 700, color: C.goldL, alpha: P(t, at('e1', 0.45), 0.5) });
    g.restore();
    chip('Toda la banda lo ve', 960, 580, { size: 34, alpha: v1 * P(t, at('e1', 0.2), 0.4) });
  }
  const v2 = vis(t, at('e2', 0), at('e3', 0.05), 0.4);
  if (v2 > 0) {
    const walk = sm(P(t, at('e2', 0.2), 2.5));
    heroPJ('veltra', lerp(520, 1000, walk), 900, 1.4, { alpha: v2, nameSize: 40 });
    heroPJ('morgrath', 1360, 900, 1.4, { alpha: v2, sub: 'Maestro despojador', nameSize: 40 });
    const pd = P(t, at('e2', 0.55), 0.5);
    diamante(1360, 540, 1.3 * eBack(pd), t, v2 * pd);
    txt('mientras te deba algo', 1360, 460, { size: 32, w: 700, color: C.goldL, alpha: v2 * P(t, at('e2', 0.75), 0.4) });
    frame(360, 110, 1200, 170, { title: 'SoftReserve335', alpha: v2 * P(t, at('e2', 0.02), 0.4) });
    txtRich([['Acércate a ', C.text, 700], ['Morgrath', CLS.paladin, 800], [' para recibir tu objeto', C.text, 700]], 960, 205, { size: 46, align: 'center', alpha: v2 * P(t, at('e2', 0.08), 0.4) });
  }
  const v3 = vis(t, at('e3', 0), e.fin, 0.4);
  if (v3 > 0) {
    const hist = P(t, at('e3', 0.45), 0.6);
    g.save(); g.globalAlpha *= v3 * (1 - hist);
    cuerpo(430, 560, 0.9, t);
    txt('Cuerpo del jefe', 430, 630, { size: 36, w: 700, color: C.goldL });
    cofre(430, 820, 1, P(t, at('e3', 0.1), 0.6));
    txt('o el cofre', 430, 920, { size: 36, w: 700, color: C.goldL });
    frame(1080, 330, 560, 560, { title: 'Bolsa' });
    for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) { rr(1130 + c * 120, 390 + r * 120, 100, 100, 8); g.fillStyle = 'rgba(0,0,0,0.55)'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#4a4060'; g.stroke(); }
    const fly = P(t, at('e3', 0.2), 0.8);
    if (fly > 0) itemIcon(lerp(430, 1180, eOut(fly)), lerp(520, 440, eOut(fly)) - Math.sin(fly * Math.PI) * 180, 90, 'espada', { glow: 0.8 });
    g.restore();
    keyword('DIRECTO A TU BOLSA', 960, 180, 76, P(t, at('e3', 0.3), 0.5), { alpha: v3 * (1 - hist) });
    if (hist > 0) {
      web(160, 110, 1600, 860, t, {
        tab: -1, usuario: ['Veltra', 'picaro'], alpha: v3 * hist,
        contenido: (x, y, w, h) => {
          txt('Historial de Veltra', x + 60, y + 60, { size: 46, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
          [['Noche', 80], ['Objeto', 380], ['Tipo', 1000], ['Compitió contra', 1260]].forEach(([c, cx]) => txt(c, x + cx, y + 140, { size: 30, fam: 'Cinzel', w: 700, color: C.goldL, align: 'left' }));
          [['Noche 3', ITEM_TBC, 'MS', '7 jugadores'], ['Noche 2', 'Anillo del Rey Ogro', 'SR', '2 jugadores'], ['Noche 1', 'Capa de la Guarida', 'OS', '3 jugadores']].forEach((r, i) => {
            const ry = y + 210 + i * 90, p = P(t, at('e3', 0.55) + i * 0.15, 0.3);
            rr(x + 60, ry - 36, w - 120, 72, 8); g.fillStyle = i ? 'rgba(255,255,255,0.03)' : 'rgba(109,255,142,0.1)'; g.globalAlpha = p; g.fill(); g.globalAlpha = 1;
            txt(r[0], x + 80, ry, { size: 32, w: 700, color: C.text, align: 'left', alpha: p });
            txt(r[1], x + 380, ry, { size: 32, w: 700, color: '#b561ff', align: 'left', alpha: p });
            chip(r[2], x + 1040, ry, { size: 26, alpha: p, color: C.goldL });
            txt(r[3], x + 1260, ry, { size: 32, w: 700, color: C.text, align: 'left', alpha: p });
          });
          txt('Qué se llevó, cuándo y contra cuántos compitió', x + w / 2, y + 560, { size: 34, w: 700, color: C.goldL, alpha: P(t, at('e3', 0.8), 0.4) });
        }
      });
    }
  }
}

// ============================================================ 11. LA ROTACIÓN DE MARCAS
function tarjetaBanda(x, y, nombre, n, rot, t, o = {}) {
  const { alpha = 1, hl = 0 } = o;
  frame(x - 250, y - 150, 500, 300, { alpha, glow: hl });
  g.save(); g.globalAlpha *= alpha;
  txt(nombre, x, y - 70, { size: 46, fam: 'Cinzel', w: 700, color: C.goldL });
  txt(`${n} jugadores`, x, y - 10, { size: 34, w: 700, color: C.text });
  g.restore();
  if (rot === 1) chip('ROTACIÓN', x, y + 80, { size: 34, alpha, color: '#b8ff9a', border: '#8dff6a' });
  if (rot === 0) chip('SIN ROTACIÓN · SE RESERVA', x, y + 80, { size: 28, alpha, color: C.goldL });
}
function escRotacion(t) {
  const e = ESC.rotacion;
  fondoTBC(t, { dim: 0.4 });
  // m1: marcas
  const v1 = vis(t, e.ini + 0.3, at('m2', 0.02), 0.4);
  if (v1 > 0) {
    keyword('MARCAS DE CONJUNTO', 960, 200, 80, P(t, at('m1', 0.02), 0.5), { alpha: v1 });
    itemIcon(700, 580, 180, 'marca', { glow: 1, alpha: v1 * P(t, at('m1', 0.2), 0.4) });
    arrow(830, 580, 1080, 580, P(t, at('m1', 0.55), 0.5) * v1, C.gold, 9);
    itemIcon(1220, 580, 180, 'pechera', { glow: 0.8, alpha: v1 * P(t, at('m1', 0.7), 0.4) });
    txt('Marca', 700, 720, { size: 40, w: 700, color: '#b561ff', alpha: v1 });
    txt('Pieza de armadura de conjunto', 1220, 720, { size: 36, w: 700, color: '#b561ff', alpha: v1 * P(t, at('m1', 0.7), 0.4) });
  }
  // m2-m3: dónde hay rotación
  const v2 = vis(t, at('m2', 0), at('m4', 0.02), 0.4);
  if (v2 > 0) {
    keyword('ROTACIÓN', 960, 150, 110, P(t, at('m2', 0.05), 0.5), { alpha: v2, tint: '#8dff6a' });
    const kh = vis(t, at('m3', 0), at('m4', 0), 0.3);
    tarjetaBanda(420, 520, 'Karazhan', 10, t > at('m3', 0.1) ? 0 : -1, t, { alpha: v2 * P(t, at('m2', 0.1), 0.4) * (1 - 0.5 * (1 - kh) * P(t, at('m2', 0.3), 0.3)), hl: kh });
    tarjetaBanda(960, 520, 'Gruul', 25, t > at('m2', 0.4) ? 1 : -1, t, { alpha: v2 * P(t, at('m2', 0.2), 0.4), hl: vis(t, at('m2', 0.35), at('m3', 0), 0.3) });
    tarjetaBanda(1500, 520, 'Magtheridon', 25, t > at('m2', 0.5) ? 1 : -1, t, { alpha: v2 * P(t, at('m2', 0.3), 0.4), hl: vis(t, at('m2', 0.45), at('m3', 0), 0.3) });
    if (kh > 0) txt('En Karazhan: todo se reserva, y se tira MS antes que OS', 960, 820, { size: 42, w: 700, color: C.goldL, alpha: kh * P(t, at('m3', 0.3), 0.4) });
  }
  // m4-m8: la fila
  const vq = vis(t, at('m4', 0), e.fin, 0.4);
  if (vq > 0) {
    const tRonda = at('m6', 0.25);
    // fila base
    const fila = [['Thorgan', 'paladin', 'tanque'], ['Kharion', 'guerrero', 'tanque'], ['Aurelio', 'sacerdote', 'sanador'], ['Tukan', 'chaman', 'sanador'],
      ['Veltra', 'picaro', 'dps', 12], ['Lunaria', 'mago', 'dps', 11], ['Sombrix', 'brujo', 'dps', 10], ['Brisa', 'cazador', 'dps', 10], ['Zefir', 'mago', 'dps', 9]];
    const alt = vis(t, at('m8', 0), e.fin, 0.3);
    const px = i => 170 + i * 176;
    const segs = [['TANQUES', 0, 2, '#7fb2ff', 0.0], ['SANADORES', 2, 4, '#6dff8e', 0.35], ['DPS', 4, 9, '#ff7a6a', 0.62]];
    const t4 = at('m4', 0);
    segs.forEach(([n, a, b, col, f]) => {
      const p = P(t, at('m4', f), 0.4) * vq;
      if (p <= 0) return;
      g.save(); g.globalAlpha *= p;
      rr(px(a) - 80, 250, px(b - 1) - px(a) + 160, 620, 16); g.fillStyle = rgba(col, 0.08); g.fill(); g.lineWidth = 2.5; g.strokeStyle = rgba(col, 0.6); g.stroke();
      g.restore();
      txt(n, (px(a) + px(b - 1)) / 2, 295, { size: 34, fam: 'Cinzel', w: 700, color: col, alpha: p });
      for (let i = a; i < b; i++) {
        const [nm, cls, rol, asis] = fila[i];
        const pi = P(t, at('m4', f) + (i - a) * 0.1, 0.35) * vq;
        hero(px(i), 700, 0.85, cls, { name: nm, nameSize: 26, alpha: pi, glow: 0 });
        iconoRol(rol, px(i), 380, 0.9, pi);
        // asistencia de los dps
        if (asis !== undefined) {
          const pa = P(t, at('m5', 0.1), 0.4) * vq;
          txt('Asistencia', px(i), 760, { size: 22, w: 700, color: C.dim, alpha: pa });
          txt(String(asis), px(i), 800, { size: 40, color: asis === 10 ? C.goldL : C.text, alpha: pa });
        }
        // marca recibida (ronda)
        if (rol === 'tanque') {
          const got = i === 0 ? P(t, at('m6', 0.0), 0.3) : P(t, at('m6', 0.2), 0.3);
          const reset = P(t, tRonda + 0.6, 0.3);
          if (got > 0 && reset < 1) itemIcon(px(i) + 45, 470, 48, 'marca', { alpha: got * (1 - reset) * vq, border: C.epic });
        }
      }
    });
    // flechas de orden estricto
    const pf = P(t, at('m4', 0.8), 0.4) * vq * (1 - P(t, at('m5', 0), 0.3));
    arrow(px(1) + 90, 560, px(2) - 90, 560, pf, C.gold, 6);
    arrow(px(3) + 90, 560, px(4) - 90, 560, pf, C.gold, 6);
    chip('Orden estricto: nadie se salta el turno', 960, 950, { size: 34, alpha: vis(t, at('m4', 0.7), at('m5', 0), 0.3) });
    // m5: asistencia manda, empate -> dados
    const v5 = vis(t, at('m5', 0), at('m6', 0), 0.3);
    if (v5 > 0) {
      keyword('ASISTENCIA', 960, 150, 90, P(t, at('m5', 0.05), 0.4), { alpha: v5 });
      const pe = P(t, at('m5', 0.55), 0.4);
      if (pe > 0) {
        g.save(); g.globalAlpha *= v5 * pe; g.lineWidth = 4; g.strokeStyle = C.goldL; rr(px(6) - 80, 730, px(7) - px(6) + 160, 100, 12); g.stroke(); g.restore();
        dado(px(6) + 88, 870, 0.55, t * 6 * (1 - P(t, at('m5', 0.6), 1.2)) + 0.3, { alpha: v5 * pe });
        chip('Empate exacto: se tiran dados', (px(6) + px(7)) / 2, 950, { size: 30, alpha: v5 * pe });
      }
      chip('Premiamos a los más dedicados', 960, 1030, { size: 34, alpha: v5 * P(t, at('m5', 0.8), 0.4), color: C.goldL });
    }
    // m6: rondas
    const v6 = vis(t, at('m6', 0), at('m7', 0), 0.3);
    if (v6 > 0) {
      keyword('RONDAS', 960, 150, 90, P(t, at('m6', 0.02), 0.4), { alpha: v6 });
      chip('Nadie repite marca hasta que todos los de su grupo tengan una', 960, 950, { size: 32, alpha: v6 * P(t, at('m6', 0.1), 0.4) });
      const pr = P(t, tRonda, 0.4) * v6;
      txt(t < tRonda + 0.6 ? 'Ronda 1' : 'Ronda 2', (px(0) + px(1)) / 2, 1030, { size: 38, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v6 });
      if (pr > 0 && t < tRonda + 0.9) checkmark((px(0) + px(1)) / 2 + 120, 1030, 34, pr);
    }
    // m7: suplentes
    const v7 = vis(t, at('m7', 0), at('m8', 0), 0.3);
    if (v7 > 0) {
      veil(0.6 * v7);
      frame(360, 260, 1200, 520, { title: 'Suplentes', alpha: v7 });
      hero(560, 700, 1, 'druida', { name: 'Selva', tag: 'SUPLENTE', alpha: v7, nameSize: 30 });
      [['Semana 1', '1.ª raid con la core', 'aún no entra', 0.1, '#ff9a8a'], ['Semana 2', '2.ª raid con la core', 'entra en la rotación', 0.45, '#9dffb8']].forEach(([s, a, b, f, col], i) => {
        const p = P(t, at('m7', f), 0.4) * v7;
        txt(s, 760, 400 + i * 190, { size: 40, fam: 'Cinzel', w: 700, color: C.goldL, align: 'left', alpha: p });
        txt(a, 760, 450 + i * 190, { size: 34, w: 700, color: C.text, align: 'left', alpha: p });
        txt(b, 1150, 450 + i * 190, { size: 34, w: 800, color: col, align: 'left', alpha: p });
        if (i === 1) checkmark(1500, 640, 50, p); else cross(1500, 450, 40, p);
      });
    }
    // m8: alts al final
    if (alt > 0) {
      veil(0.35 * alt);
      hero(1740, 700, 0.85, 'mago', { name: 'Veltrix', tag: 'ALT', alpha: alt, nameSize: 26 });
      arrow(1740, 560, 1600, 560, P(t, at('m8', 0.55), 0.3) * alt, C.red, 6);
      cross(1660, 560, 60, P(t, at('m8', 0.62), 0.3));
      keyword('ALTS AL FINAL', 960, 150, 80, P(t, at('m8', 0.05), 0.4), { alpha: alt });
      chip('Marcados · nunca pasan por delante de un principal', 960, 950, { size: 32, alpha: alt * P(t, at('m8', 0.4), 0.4) });
    }
  }
}

// ============================================================ 12. LA ASISTENCIA
function escAsistencia(t) {
  const e = ESC.asistencia;
  fondoTBC(t, { dim: 0.45 });
  const v1 = vis(t, e.ini + 0.2, at('a2', 0.02), 0.4);
  if (v1 > 0) {
    keyword('ASISTENCIA', 960, 130, 100, P(t, at('a1', 0), 0.5), { alpha: v1 });
    frame(240, 280, 760, 500, { title: 'Jefes derrotados', alpha: v1 });
    ['Alto Rey Maulgar', 'Gruul', 'Magtheridon'].forEach((j, i) => {
      const y = 400 + i * 110, p = P(t, at('a1', 0.1) + i * 0.4, 0.4);
      txt(j, 300, y, { size: 40, w: 700, color: C.text, align: 'left', alpha: v1 });
      checkmark(900, y, 50, p);
    });
    txt('Se anota quién estuvo', 620, 730, { size: 34, w: 700, color: C.goldL, alpha: v1 * P(t, at('a1', 0.3), 0.4) });
    const pw = P(t, at('a1', 0.55), 0.5) * v1;
    arrow(1020, 530, 1180, 530, pw, C.gold, 8);
    iconoWeb(1450, 500, 1.4, t, pw);
    chip('Decide tu lugar en la rotación', 1450, 700, { size: 32, alpha: pw * P(t, at('a1', 0.75), 0.4), color: C.goldL });
  }
  const v2 = vis(t, at('a2', 0), at('a3', 0.02), 0.4);
  if (v2 > 0) {
    keyword('POR PERSONA', 960, 150, 90, P(t, at('a2', 0.02), 0.5), { alpha: v2 });
    hero(640, 720, 1.2, 'picaro', { name: 'Veltra', tag: 'PRINCIPAL', alpha: v2, nameSize: 36 });
    hero(1280, 720, 1.2, 'mago', { name: 'Veltrix', tag: 'ALT', alpha: v2, nameSize: 36, glow: P(t, at('a2', 0.2), 0.4) });
    txt('Hoy vino con su alt', 1280, 800, { size: 32, w: 700, color: C.text, alpha: v2 * P(t, at('a2', 0.2), 0.4) });
    arrow(1150, 900, 800, 900, P(t, at('a2', 0.45), 0.5) * v2, C.gold, 8);
    chip('La asistencia cuenta para la misma persona', 960, 980, { size: 34, alpha: v2 * P(t, at('a2', 0.55), 0.4), color: '#9dffb8', border: '#6dff8e' });
  }
  const v3 = vis(t, at('a3', 0), e.fin, 0.4);
  if (v3 > 0) {
    const prog = P(t, at('a3', 0.42), 0.5);
    chip('Solo cuentan las bandas de 25', 960, 380, { size: 44, alpha: v3 * P(t, at('a3', 0.02), 0.4) * (1 - prog) });
    chip('Menos de 10 en el grupo: no cuenta', 960, 500, { size: 44, alpha: v3 * P(t, at('a3', 0.18), 0.4) * (1 - prog), color: '#ff9a8a', border: '#ff5a4f' });
    if (prog > 0) {
      web(160, 90, 1600, 900, t, {
        tab: 2, usuario: ['Veltra', 'picaro'], alpha: v3 * prog,
        contenido: (x, y, w, h) => {
          [['Etapa actual', 0], ['TBC', 1]].forEach(([n, on], i) => {
            rr(x + 60 + i * 230, y + 30, 210, 50, 8); g.fillStyle = on ? '#3b2360' : '#1a1426'; g.fill();
            g.lineWidth = 2; g.strokeStyle = on ? C.gold : '#4a4060'; g.stroke();
            txt(n, x + 165 + i * 230, y + 56, { size: 28, w: 700, color: on ? C.goldL : C.dim });
          });
          [['Posición', 80], ['Jugador', 300], ['Papel', 680], ['Asistencia', 960], ['Por qué', 1220]].forEach(([c, cx]) => txt(c, x + cx, y + 140, { size: 30, fam: 'Cinzel', w: 700, color: C.goldL, align: 'left' }));
          [['1', 'Thorgan', 'paladin', 'tanque', 11, 'Tanque'], ['2', 'Kharion', 'guerrero', 'tanque', 10, 'Tanque'], ['3', 'Aurelio', 'sacerdote', 'sanador', 12, 'Sanador'], ['4', 'Veltra', 'picaro', 'dps', 12, 'DPS · más asistencia'], ['5', 'Lunaria', 'mago', 'dps', 11, 'DPS · asistencia']].forEach((r, i) => {
            const ry = y + 210 + i * 86, p = P(t, at('a3', 0.5) + i * 0.1, 0.3);
            txt(r[0], x + 100, ry, { size: 36, color: C.text, alpha: p });
            txt(r[1], x + 300, ry, { size: 34, w: 800, color: CLS[r[2]], align: 'left', alpha: p });
            iconoRol(r[3], x + 700, ry, 0.8, p);
            txt(String(r[4]), x + 1020, ry, { size: 36, color: C.text, alpha: p });
            txt(r[5], x + 1220, ry, { size: 30, w: 700, color: C.dim, align: 'left', alpha: p });
          });
          txt('Quién va primero, y por qué', x + w / 2, y + 700, { size: 36, w: 700, color: C.goldL, alpha: P(t, at('a3', 0.8), 0.4) });
        }
      });
    }
  }
}

// ============================================================ 13. RESUMEN
function escResumen(t) {
  const e = ESC.resumen;
  fondoTBC(t, { dim: 0.45 });
  const v = vis(t, e.ini + 0.2, at('s6', 0.02), 0.4);
  if (v > 0) {
    keyword('RESUMEN', 960, 120, 90, P(t, at('s1', 0), 0.5), { alpha: v });
    const items = [['s1', 'Entra a la web con Discord'], ['s2', 'Registra tu principal y «Mis personajes»'], ['s3', 'Pide tu lugar en una core'], ['s4', 'Instala SoftReserve335 (obligatorio) y BisTooltip'], ['s5', 'Reserva antes de cada banda']];
    items.forEach(([c, s], i) => {
      const p = P(t, at(c, 0.05), 0.4);
      const y = 280 + i * 140;
      g.save(); g.globalAlpha *= v * eOut(p); g.translate(lerp(-60, 0, eOut(p)), 0);
      rr(300, y - 55, 1320, 110, 16); g.fillStyle = 'rgba(18,12,30,0.92)'; g.fill(); g.lineWidth = 3; g.strokeStyle = C.gold2; g.stroke();
      g.restore();
      checkmark(380, y, 60, P(t, at(c, 0.3), 0.5));
      txt(s, 460, y, { size: 50, w: 700, color: C.text, align: 'left', alpha: v * p });
    });
  }
  const v6 = vis(t, at('s6', 0), e.fin, 0.4);
  if (v6 > 0) {
    txt('Sin SoftReserve335:', 960, 220, { size: 56, fam: 'Cinzel', w: 700, color: C.goldL, alpha: v6 });
    [['No ves los avisos', 0.12], ['No puedes tirar con los botones', 0.3], ['Tu asistencia no se registra', 0.5]].forEach(([s, f], i) => {
      const p = P(t, at('s6', f), 0.4), y = 360 + i * 120;
      cross(520, y, 60, p);
      txt(s, 590, y, { size: 52, w: 700, color: C.text, align: 'left', alpha: v6 * p });
    });
    keyword('PIERDES TU LUGAR EN LA ROTACIÓN', 960, 800, 60, P(t, at('s6', 0.72), 0.5), { tint: '#ff8a70', alpha: v6 });
  }
}

// ============================================================ 14. CIERRE
function escCierre(t) {
  const e = ESC.cierre;
  fondoTBC(t);
  portal(960, 1000, 1.05, 1, t);
  const p1 = vis(t, at('c1', 0), at('c2', 0) - 0.3, 0.4);
  txt('Regístrate · prepárate · nos vemos en TBC', 960, 150, { size: 56, fam: 'Cinzel', w: 700, color: C.goldL, alpha: p1, glow: 20, glowColor: 'rgba(232,196,106,0.6)' });
  const pl = P(t, at('c2', 0) - 0.4, 1.2);
  if (pl > 0) {
    veil(0.25 * pl);
    emblema(960, 400, 1.1 * lerp(0.85, 1, eOut(pl)), t, pl);
    keyword('PACTO OSCURO', 960, 700, 130, P(t, at('c2', 0) - 0.1, 0.9));
    txt('Nos vemos en TBC', 960, 820, { size: 48, fam: 'Cinzel', w: 700, color: '#b8ff9a', alpha: P(t, at('c2', 0) + 0.8, 0.8), glow: 20, glowColor: '#6dff8e' });
    txt('softres.xdataplusx.com  ·  SoftReserve335  ·  BisTooltip', 960, 900, { size: 32, w: 700, color: C.text, alpha: P(t, at('c2', 0) + 1.4, 0.8) });
  }
  veil(P(t, TL.duracion - 1.6, 1.5));
}

// ============================================================ motor
const ESCENAS = { gancho: escGancho, problema: escProblema, herramientas: escHerramientas, registro: escRegistro, cores: escCores, bistooltip: escBis, reserva: escReserva, objeto: escObjeto, gana: escGana, recibir: escRecibir, rotacion: escRotacion, asistencia: escAsistencia, resumen: escResumen, cierre: escCierre };
function draw(t) {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
  const es = TL.escenas;
  const e = es.find(x => t >= x.ini && t < x.fin) || es[es.length - 1];
  ESCENAS[e.id](t);
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
