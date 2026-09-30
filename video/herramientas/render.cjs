// Dibuja el video cuadro por cuadro en Chromium y lo codifica con ffmpeg.
//
//   node render.cjs vista  <trabajo> 3.5 10 42 ...      -> PNG de esos segundos (revisión)
//   node render.cjs tramo  <trabajo> <desde> <hasta> <salida.mp4>   -> un tramo de video
//
// Requiere: playwright-core (npm) y ffmpeg (FFMPEG=/ruta/a/ffmpeg).
const { chromium } = require('playwright-core');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const RAIZ = path.resolve(__dirname, '..');
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FFMPEG = process.env.FFMPEG || 'ffmpeg';

async function abrir(trabajo) {
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--allow-file-access-from-files', '--disable-gpu-vsync'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => { console.error('ERROR en página:', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.join(RAIZ, 'escenas', 'index.html'));
  const tl = JSON.parse(fs.readFileSync(path.join(trabajo, 'timeline.json'), 'utf8'));
  await page.evaluate(tl => window.initTL(tl), tl);
  await page.evaluate(() => window.listo());
  return { browser, page, tl };
}

async function vista(trabajo, tiempos) {
  const { browser, page } = await abrir(trabajo);
  const dir = path.join(trabajo, 'vista');
  fs.mkdirSync(dir, { recursive: true });
  for (const t of tiempos) {
    const b64 = await page.evaluate(t => { window.draw(t); return document.getElementById('c').toDataURL('image/jpeg', 0.85).split(',')[1]; }, Number(t));
    const f = path.join(dir, `t${String(t).padStart(6, '0')}.jpg`);
    fs.writeFileSync(f, Buffer.from(b64, 'base64'));
    console.log(f);
  }
  await browser.close();
}

async function tramo(trabajo, desde, hasta, salida) {
  const { browser, page } = await abrir(trabajo);
  const f0 = Math.round(desde * FPS), f1 = Math.round(hasta * FPS);
  const ff = spawn(FFMPEG, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-tune', 'animation', salida], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = f0; f < f1; f++) {
    const b64 = await page.evaluate(t => { window.draw(t); return document.getElementById('c').toDataURL('image/jpeg', 0.93).split(',')[1]; }, f / FPS);
    const buf = Buffer.from(b64, 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 300 === 0) console.log(`${path.basename(salida)}: ${f - f0}/${f1 - f0} cuadros (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
}

(async () => {
  const [modo, trabajo, ...resto] = process.argv.slice(2);
  if (modo === 'vista') await vista(trabajo, resto);
  else if (modo === 'tramo') await tramo(trabajo, Number(resto[0]), Number(resto[1]), resto[2]);
  else { console.error('uso: render.cjs vista|tramo ...'); process.exit(2); }
})();
