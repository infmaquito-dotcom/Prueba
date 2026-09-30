// Elementos propios del video de TBC: cielo de Terrallende, portal, página web,
// recuadro de información del juego y ventana de BisTooltip. Todo es diseño propio.

// ---------------------------------------------------------------- Terrallende
const ROCAS = Array.from({ length: 5 }, (_, i) => ({
  x: 160 + i * 400 + hash(i + 40) * 120, y: 170 + hash(i + 50) * 260, s: 0.5 + hash(i + 60) * 0.7, v: 4 + hash(i + 70) * 6
}));
function roca(x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s);
  g.fillStyle = '#1c0c0e';
  g.beginPath();
  g.moveTo(-120, 0); g.lineTo(-90, -28); g.lineTo(-30, -40); g.lineTo(40, -34); g.lineTo(110, -18); g.lineTo(130, 0);
  g.lineTo(80, 30); g.lineTo(40, 80); g.lineTo(10, 140); g.lineTo(-20, 90); g.lineTo(-70, 40); g.closePath();
  g.fill();
  g.strokeStyle = 'rgba(255,110,50,0.55)'; g.lineWidth = 2.5;
  g.beginPath(); g.moveTo(-120, 0); g.lineTo(-90, -28); g.lineTo(-30, -40); g.lineTo(40, -34); g.lineTo(110, -18); g.lineTo(130, 0); g.stroke();
  g.restore();
}
function fondoTBC(t, o = {}) {
  const { dim = 0, suelo = 1 } = o;
  let gr = g.createLinearGradient(0, 0, 0, H);
  gr.addColorStop(0, '#080307'); gr.addColorStop(0.35, '#240912'); gr.addColorStop(0.7, '#3a1210'); gr.addColorStop(1, '#100605');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  // nebulosas roja y verde vil
  const neb = [[380, 260, 520, 'rgba(255,70,40,0.16)'], [1500, 200, 600, 'rgba(120,255,90,0.12)'], [1100, 520, 480, 'rgba(255,120,40,0.12)'], [300, 700, 420, 'rgba(90,255,120,0.08)']];
  neb.forEach(([x, y, r, c], i) => {
    const xx = x + Math.sin(t * 0.07 + i) * 60, yy = y + Math.cos(t * 0.05 + i) * 30;
    gr = g.createRadialGradient(xx, yy, 0, xx, yy, r); gr.addColorStop(0, c); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(xx - r, yy - r, r * 2, r * 2);
  });
  for (const [x, y, k] of STARS.slice(0, 90)) {
    const a = 0.2 + 0.5 * (0.5 + 0.5 * Math.sin(t * (0.6 + k) + k * 30));
    g.fillStyle = `rgba(255,220,200,${a * 0.6})`; g.fillRect(x, y * 0.7, 1.5 + k, 1.5 + k);
  }
  // rocas flotantes
  for (const r of ROCAS) roca(((r.x + t * r.v) % (W + 400)) - 200, r.y + Math.sin(t * 0.3 + r.x) * 12, r.s);
  // suelo agrietado
  if (suelo > 0) {
    g.save(); g.globalAlpha *= suelo;
    g.fillStyle = '#140806';
    g.beginPath(); g.moveTo(0, H);
    for (let x = 0; x <= W; x += 60) g.lineTo(x, 900 + Math.sin(x * 0.013) * 22 + hash(x) * 26);
    g.lineTo(W, H); g.closePath(); g.fill();
    g.strokeStyle = 'rgba(255,120,40,0.6)'; g.lineWidth = 2; g.shadowColor = '#ff6a2a'; g.shadowBlur = 12;
    for (let i = 0; i < 9; i++) {
      const x0 = hash(i + 200) * W, y0 = 950 + hash(i + 210) * 110;
      g.beginPath(); g.moveTo(x0, y0);
      for (let k = 1; k < 5; k++) g.lineTo(x0 + k * 40 + hash(i * 9 + k) * 30 - 15, y0 + (hash(i * 7 + k) - 0.5) * 40);
      g.stroke();
    }
    g.restore();
  }
  // brasas y chispas viles
  for (let i = 0; i < 80; i++) {
    const sp = 20 + hash(i + 3) * 45;
    const x = hash(i + 11) * W + Math.sin(t * 0.6 + i) * 24;
    const y = H + 40 - ((t * sp + hash(i + 7) * H * 1.2) % (H * 1.2));
    const a = 0.3 + 0.5 * hash(i + 19);
    g.fillStyle = i % 3 === 0 ? `rgba(130,255,100,${a})` : `rgba(255,${120 + Math.floor(hash(i) * 80)},50,${a})`;
    g.beginPath(); g.arc(x, y, 1.2 + hash(i + 23) * 2.2, 0, 7); g.fill();
  }
  gr = g.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(0,0,0,0.75)');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  if (dim > 0) { g.fillStyle = `rgba(6,3,5,${dim})`; g.fillRect(0, 0, W, H); }
}

// portal de piedra con un vórtice verde y rojo (diseño propio)
function portal(x, y, s, open, t, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  // resplandor
  if (open > 0) {
    const gr = g.createRadialGradient(0, -260, 20, 0, -260, 620);
    gr.addColorStop(0, `rgba(120,255,100,${0.45 * open})`); gr.addColorStop(0.5, `rgba(255,80,40,${0.18 * open})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(-700, -900, 1400, 1100);
  }
  // vórtice
  g.save();
  g.beginPath(); g.rect(-190, -520, 380, 520); g.clip();
  g.fillStyle = '#050805'; g.fillRect(-190, -520, 380, 520);
  if (open > 0) {
    const cy = -260;
    let gr = g.createRadialGradient(0, cy, 0, 0, cy, 320 * open);
    gr.addColorStop(0, 'rgba(220,255,200,0.95)'); gr.addColorStop(0.25, 'rgba(110,255,90,0.85)'); gr.addColorStop(0.65, 'rgba(40,140,50,0.6)'); gr.addColorStop(1, 'rgba(20,40,10,0)');
    g.fillStyle = gr; g.fillRect(-190, -520, 380, 520);
    g.lineCap = 'round';
    for (let k = 0; k < 14; k++) {
      const a0 = t * (1.2 + k * 0.05) + k * 0.9;
      const r = (40 + k * 18) * open;
      g.strokeStyle = k % 4 === 0 ? `rgba(255,90,50,${0.7 * open})` : `rgba(180,255,150,${0.55 * open})`;
      g.lineWidth = 5 - k * 0.2;
      g.beginPath(); g.ellipse(0, cy, r, r * 1.25, 0, a0, a0 + 1.6); g.stroke();
    }
  }
  g.restore();
  // pilares y dintel
  const piedra = g.createLinearGradient(-300, 0, 300, 0);
  piedra.addColorStop(0, '#2a1a16'); piedra.addColorStop(0.5, '#4a3026'); piedra.addColorStop(1, '#2a1a16');
  g.fillStyle = piedra; g.strokeStyle = 'rgba(255,120,60,0.55)'; g.lineWidth = 3;
  for (const d of [-1, 1]) {
    g.beginPath();
    g.moveTo(d * 190, 0); g.lineTo(d * 320, 0); g.lineTo(d * 290, -560); g.lineTo(d * 200, -540); g.closePath();
    g.fill(); g.stroke();
    // runas verdes
    for (let k = 0; k < 5; k++) {
      g.fillStyle = `rgba(120,255,100,${0.35 + 0.35 * Math.sin(t * 2 + k + d)})`;
      g.fillRect(d * 255 - 6, -80 - k * 95, 12, 40);
      g.fillStyle = piedra;
    }
    // cuerno superior
    g.beginPath(); g.moveTo(d * 240, -560); g.quadraticCurveTo(d * 380, -680, d * 330, -780); g.quadraticCurveTo(d * 320, -660, d * 200, -600); g.closePath();
    g.fill(); g.stroke();
  }
  g.beginPath(); g.moveTo(-330, -520); g.lineTo(330, -520); g.lineTo(290, -600); g.lineTo(-290, -600); g.closePath(); g.fill(); g.stroke();
  // escalones
  g.fillStyle = '#20120e';
  g.fillRect(-380, 0, 760, 30); g.fillRect(-440, 30, 880, 30);
  g.restore();
}

// ---------------------------------------------------------------- iconos de papel
function iconoRol(rol, x, y, s, alpha = 1) {
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  const col = { tanque: '#7fb2ff', sanador: '#6dff8e', dps: '#ff7a6a' }[rol];
  g.fillStyle = 'rgba(0,0,0,0.6)'; g.beginPath(); g.arc(0, 0, 22, 0, 7); g.fill();
  g.lineWidth = 3; g.strokeStyle = col; g.stroke();
  g.fillStyle = col;
  if (rol === 'tanque') {
    g.beginPath(); g.moveTo(-11, -12); g.lineTo(11, -12); g.lineTo(11, 0); g.quadraticCurveTo(10, 10, 0, 15); g.quadraticCurveTo(-10, 10, -11, 0); g.closePath(); g.fill();
  } else if (rol === 'sanador') {
    g.fillRect(-4, -13, 8, 26); g.fillRect(-13, -4, 26, 8);
  } else {
    g.save(); g.rotate(-Math.PI / 4); g.fillRect(-2.5, -15, 5, 22); g.fillRect(-8, 6, 16, 4); g.fillRect(-2, 10, 4, 6); g.restore();
  }
  g.restore();
}
const ROL_NOMBRE = { tanque: 'Tanque', sanador: 'Sanador', dps: 'DPS' };

// ---------------------------------------------------------------- página web
const TABS = ['Mis personajes', 'Cores', 'Progresión', 'Profesiones'];
// Ventana de navegador con la web de la hermandad. `contenido(x, y, w, h)` dibuja dentro.
function web(x, y, w, h, t, o = {}) {
  const { url = 'softres.xdataplusx.com', tab = -1, usuario = null, alpha = 1, contenido = null, discordHi = 0, discordPress = 0, sinTabs = false } = o;
  if (alpha <= 0) return;
  g.save(); g.globalAlpha *= alpha;
  g.shadowColor = 'rgba(0,0,0,0.8)'; g.shadowBlur = 40; g.shadowOffsetY = 12;
  rr(x, y, w, h, 14); g.fillStyle = '#121017'; g.fill();
  g.shadowBlur = 0; g.shadowOffsetY = 0;
  g.lineWidth = 2; g.strokeStyle = '#34303f'; g.stroke();
  // barra del navegador
  g.fillStyle = '#1d1a24'; rr(x, y, w, 60, [14, 14, 0, 0]); g.fill();
  ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(x + 30 + i * 26, y + 30, 8, 0, 7); g.fill(); });
  rr(x + 120, y + 13, w - 160, 34, 17); g.fillStyle = '#0d0b11'; g.fill();
  g.strokeStyle = '#9ad5a9'; g.lineWidth = 2.5; g.beginPath(); g.arc(x + 146, y + 27, 6, Math.PI, 0); g.stroke();
  g.fillStyle = '#9ad5a9'; g.fillRect(x + 139, y + 27, 14, 11);
  txt(url, x + 168, y + 31, { size: 25, color: '#e9e4f5', align: 'left', shadow: false });
  // cabecera de la página
  const hy = y + 60;
  let gr = g.createLinearGradient(0, hy, 0, hy + 84);
  gr.addColorStop(0, '#221433'); gr.addColorStop(1, '#170e22');
  g.fillStyle = gr; g.fillRect(x, hy, w, 84);
  g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(x, hy + 83, w, 1.5);
  emblema(x + 50, hy + 42, 0.2, t);
  txt('Pacto Oscuro', x + 92, hy + 42, { size: 34, fam: 'Cinzel', w: 700, color: C.gold, align: 'left' });
  if (!sinTabs) {
    let tx = x + 400;
    TABS.forEach((n, i) => {
      g.font = font(27, 'Alegreya Sans', 700);
      const tw = g.measureText(n).width;
      const on = i === tab;
      txt(n, tx, hy + 42, { size: 27, w: 700, color: on ? C.goldL : '#a79fb6', align: 'left', shadow: false });
      if (on) { g.fillStyle = C.gold; rr(tx, hy + 66, tw, 5, 2.5); g.fill(); }
      tx += tw + 44;
    });
  }
  // usuario o botón de Discord
  if (usuario) {
    const [n, cls] = usuario;
    g.beginPath(); g.arc(x + w - 190, hy + 42, 20, 0, 7); g.fillStyle = CLS[cls]; g.fill();
    txt(n, x + w - 160, hy + 42, { size: 28, w: 700, color: CLS[cls], align: 'left', shadow: false });
  } else botonDiscord(x + w - 330, hy + 16, 300, 52, { hi: discordHi, press: discordPress });
  // contenido
  if (contenido) {
    g.save(); rr(x, hy + 85, w, h - 145, [0, 0, 14, 14]); g.clip();
    gr = g.createLinearGradient(0, hy + 85, 0, y + h);
    gr.addColorStop(0, '#15101c'); gr.addColorStop(1, '#0c0a10');
    g.fillStyle = gr; g.fillRect(x, hy + 85, w, h - 145);
    contenido(x, hy + 85, w, h - 145);
    g.restore();
  }
  g.restore();
}
function botonDiscord(x, y, w, h, o = {}) {
  const { hi = 0, press = 0, alpha = 1, size = 26 } = o;
  g.save(); g.globalAlpha *= alpha;
  const sc = 1 + 0.06 * hi - 0.05 * press;
  g.translate(x + w / 2, y + h / 2); g.scale(sc, sc); g.translate(-w / 2, -h / 2);
  if (hi) { g.shadowColor = `rgba(120,140,255,${hi})`; g.shadowBlur = 30 * hi; }
  rr(0, 0, w, h, 10); g.fillStyle = press ? '#4752c4' : '#5865F2'; g.fill(); g.shadowBlur = 0;
  // globo de chat genérico
  g.fillStyle = '#fff'; rr(18, h / 2 - 12, 30, 22, 7); g.fill();
  g.beginPath(); g.moveTo(24, h / 2 + 8); g.lineTo(22, h / 2 + 16); g.lineTo(32, h / 2 + 9); g.fill();
  txt('Entrar con Discord', 60, h / 2 + 1, { size, w: 700, color: '#fff', align: 'left', shadow: false });
  g.restore();
}
// campo de formulario
function campo(x, y, w, etiqueta, valor, o = {}) {
  const { foco = 0, color = '#f0eaf8', alpha = 1, vacio = false } = o;
  g.save(); g.globalAlpha *= alpha;
  txt(etiqueta, x, y, { size: 24, w: 700, color: C.dim, align: 'left', shadow: false });
  rr(x, y + 18, w, 54, 8); g.fillStyle = '#0c0a10'; g.fill();
  g.lineWidth = foco ? 3 : 1.5; g.strokeStyle = foco ? C.gold : (vacio ? '#ff5a4f' : '#3a3448'); g.stroke();
  txt(valor || (vacio ? '— sin elegir —' : ''), x + 18, y + 46, { size: 28, w: 700, color: valor ? color : '#6d6578', align: 'left', shadow: false });
  g.restore();
}

// ---------------------------------------------------------------- juego: recuadro y ventanas
// recuadro de información de un objeto (tooltip), con la sección de BisTooltip
function tooltipObjeto(x, y, t, o = {}) {
  const { alpha = 1, bis = 1, lineas = null } = o;
  if (alpha <= 0) return;
  const w = 560;
  const bisL = lineas || [['Pícaro', 'Combate', 1], ['Guerrero', 'Furia', 2], ['Cazador', 'Supervivencia', 4]];
  const h = 250 + (bis > 0 ? 60 + bisL.length * 42 : 0);
  g.save(); g.globalAlpha *= alpha;
  rr(x, y, w, h, 8); g.fillStyle = 'rgba(8,10,28,0.96)'; g.fill();
  g.lineWidth = 3; g.strokeStyle = '#8f8fa8'; g.stroke();
  txt('Hoja de Terrallende', x + 24, y + 38, { size: 34, w: 700, color: C.epic === '#a335ee' ? '#b561ff' : C.purple, align: 'left', shadow: false });
  txt('Ligado al recogerlo', x + 24, y + 80, { size: 26, color: '#fff', align: 'left', shadow: false });
  txt('Mano derecha', x + 24, y + 114, { size: 26, color: '#fff', align: 'left', shadow: false });
  txt('Espada', x + w - 24, y + 114, { size: 26, color: '#fff', align: 'right', shadow: false });
  txt('+20 Agilidad', x + 24, y + 150, { size: 26, color: '#fff', align: 'left', shadow: false });
  txt('+30 Aguante', x + 24, y + 184, { size: 26, color: '#fff', align: 'left', shadow: false });
  txt('Objeto de ejemplo', x + 24, y + 222, { size: 24, color: '#1eff00', align: 'left', shadow: false });
  if (bis > 0) {
    g.save(); g.globalAlpha *= bis;
    g.fillStyle = 'rgba(232,196,106,0.5)'; g.fillRect(x + 20, y + 250, w - 40, 1.5);
    txt('BisTooltip — de los mejores para:', x + 24, y + 282, { size: 26, w: 700, color: C.gold, align: 'left', shadow: false });
    bisL.forEach(([cl, sp, n], i) => {
      const cls = { 'Pícaro': 'picaro', 'Guerrero': 'guerrero', 'Cazador': 'cazador' }[cl] || 'picaro';
      const p = P(bis, 0.2 + i * 0.25, 0.25);
      txtRich([[cl + ' ', CLS[cls], 700], [sp, '#fff', 500]], x + 24, y + 326 + i * 42, { size: 27, alpha: p });
      txt('puesto ' + n, x + w - 24, y + 326 + i * 42, { size: 27, w: 700, color: C.goldL, align: 'right', alpha: p, shadow: false });
    });
    g.restore();
  }
  g.restore();
}
function minimapa(x, y, s, t, o = {}) {
  const { hi = 0, press = 0, alpha = 1 } = o;
  g.save(); g.globalAlpha *= alpha; g.translate(x, y); g.scale(s, s);
  g.beginPath(); g.arc(0, 0, 120, 0, 7);
  const gr = g.createRadialGradient(-20, -20, 10, 0, 0, 120); gr.addColorStop(0, '#6a4a2a'); gr.addColorStop(1, '#2a1a10');
  g.fillStyle = gr; g.fill();
  g.lineWidth = 12; g.strokeStyle = '#8a7a5a'; g.stroke();
  g.fillStyle = '#ffd24a'; g.beginPath(); g.moveTo(0, -10); g.lineTo(8, 10); g.lineTo(-8, 10); g.closePath(); g.fill();
  // botón de BisTooltip en el borde
  const bx = -Math.cos(0.7) * 120, by = Math.sin(0.7) * 120;
  g.save(); g.translate(bx, by); g.scale(1 + 0.15 * hi - 0.1 * press, 1 + 0.15 * hi - 0.1 * press);
  if (hi) { g.shadowColor = '#ffe08a'; g.shadowBlur = 30 * hi; }
  g.beginPath(); g.arc(0, 0, 32, 0, 7); g.fillStyle = '#1a1030'; g.fill(); g.shadowBlur = 0;
  g.lineWidth = 5; g.strokeStyle = C.gold; g.stroke();
  txt('BiS', 0, 2, { size: 24, fam: 'Cinzel', w: 700, color: C.goldL, shadow: false });
  g.restore();
  g.restore();
  return [x + bx * s, y + by * s];
}
const RANURAS = ['Cabeza', 'Cuello', 'Hombros', 'Espalda', 'Pecho', 'Mano derecha'];
const ICONOS_RANURA = { 'Cabeza': 'pechera', 'Cuello': 'anillo', 'Hombros': 'pechera', 'Espalda': 'capa', 'Pecho': 'pechera', 'Mano derecha': 'espada' };
function ventanaBis(x, y, t, o = {}) {
  const { alpha = 1, hover = null, filas = 1, fuente = null } = o;
  if (alpha <= 0) return;
  const w = 980, h = 720;
  frame(x, y, w, h, { title: 'BisTooltip', alpha });
  g.save(); g.globalAlpha *= alpha;
  [['Clase', 'Pícaro', 'picaro'], ['Spec', 'Combate', null], ['Fase', '1', null]].forEach(([k, v, cls], i) => {
    const dx = x + 50 + i * 300;
    txt(k, dx, y + 62, { size: 24, w: 700, color: C.dim, align: 'left' });
    rr(dx, y + 78, 270, 48, 8); g.fillStyle = '#0c0a10'; g.fill(); g.lineWidth = 2; g.strokeStyle = '#5a4a30'; g.stroke();
    txt(v, dx + 16, y + 103, { size: 28, w: 700, color: cls ? CLS[cls] : C.text, align: 'left' });
    txt('▾', dx + 248, y + 103, { size: 24, color: C.gold });
  });
  RANURAS.forEach((r, i) => {
    const ry = y + 180 + i * 88;
    const p = clamp(filas * 6 - i);
    if (p <= 0) return;
    g.save(); g.globalAlpha *= p;
    txt(r, x + 50, ry, { size: 30, w: 700, color: C.text, align: 'left' });
    for (let k = 0; k < 6; k++) {
      const ix = x + 330 + k * 100;
      const hov = hover && hover[0] === i && hover[1] === k;
      itemIcon(ix, ry, 72, ICONOS_RANURA[r], { border: k === 0 ? C.gold : C.epic, glow: hov ? 0.9 : 0 });
    }
    g.restore();
  });
  if (filas >= 1) {
    txt('mejor', x + 330, y + 710, { size: 24, w: 700, color: C.gold });
    txt('alternativa', x + 830, y + 710, { size: 24, w: 700, color: C.dim });
    arrow(x + 390, y + 710, x + 760, y + 710, 1, 'rgba(232,196,106,0.5)', 3);
  }
  g.restore();
}
