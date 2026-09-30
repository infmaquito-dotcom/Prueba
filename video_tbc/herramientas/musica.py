"""Música de fondo y efectos, generados por código (sin grabaciones con derechos).

Lee timeline.json y narracion.wav de la carpeta de trabajo y escribe:
  musica.wav   música + efectos, bajando de volumen cuando habla el narrador
  mezcla.wav   música + voz, lista para el video
"""
import json, os, sys
import numpy as np
import soundfile as sf
from scipy import signal

TRABAJO = sys.argv[1] if len(sys.argv) > 1 else "build"
SR = 48000
rng = np.random.default_rng(7)

tl = json.load(open(os.path.join(TRABAJO, "timeline.json"), encoding="utf-8"))
DUR = tl["duracion"] + 1.0
N = int(DUR * SR)
ESC = {e["id"]: e for e in tl["escenas"]}
CUE = {c["id"]: c for e in tl["escenas"] for c in e["cues"]}


def nota(n):  # número MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    na, nr = min(na, n // 2), min(nr, n // 2)
    e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    e[n - nr:] *= np.cos(np.linspace(0, np.pi / 2, nr)) ** 2
    return e


def pad_voice(f, n, brillo=10):
    """Voz de 'pad': armónicos de sierra suavizados, con leve desafinado."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    for det in (-0.0025, 0.0, 0.0031):
        ff = f * (1 + det)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, brillo + 1):
            if ff * h > 6000:
                break
            out += np.sin(2 * np.pi * ff * h * t + ph * h) / (h ** 1.3)
    return out / 3


def coro(f, n):
    """'Aah' de coro: senoides con vibrato lento y formantes suaves."""
    t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 4.8 * t + rng.uniform(0, 6))
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    out = np.zeros(n)
    for h, a in ((1, 1.0), (2, 0.5), (3, 0.35), (4, 0.18), (5, 0.12), (6, 0.08)):
        # realce de formante cerca de 700 Hz (vocal "a")
        g = a * (1 + 1.5 * np.exp(-((f * h - 750) / 300) ** 2))
        out += g * np.sin(h * ph)
    return out / 3


# ---------------------------------------------------------------- progresión
# Re menor: Dm - Bb - Gm - A   (épica oscura);  cada acorde dura CH segundos
CH = 4.0
ACORDES = [
    [50, 53, 57, 62],   # Dm
    [46, 50, 53, 58],   # Bb
    [43, 50, 55, 58],   # Gm
    [45, 49, 52, 57],   # A
]
# en escenas "luminosas" usamos Bb - F - C - Dm
LUZ = [
    [46, 50, 53, 58],   # Bb
    [41, 48, 53, 57],   # F
    [48, 52, 55, 60],   # C
    [50, 53, 57, 62],   # Dm
]
ESCENAS_LUZ = {"herramientas", "recibir", "resumen", "cierre"}


def intensidad(t):
    """Cuánta energía lleva la música en cada momento (0..1)."""
    for e in tl["escenas"]:
        if e["ini"] <= t < e["fin"]:
            return {"gancho": 0.95, "problema": 0.55, "herramientas": 0.75, "registro": 0.6,
                    "cores": 0.7, "bistooltip": 0.6, "reserva": 0.6, "objeto": 0.65, "gana": 0.7,
                    "recibir": 0.8, "rotacion": 0.65, "asistencia": 0.6, "resumen": 0.8, "cierre": 1.0}[e["id"]]
    return 0.8


def escena_en(t):
    for e in tl["escenas"]:
        if e["ini"] <= t < e["fin"]:
            return e["id"]
    return "cierre"


pad = np.zeros(N)
voces = np.zeros(N)
bajo = np.zeros(N)
campanas = np.zeros(N)

nch = int(DUR / CH) + 1
for i in range(nch):
    t0 = i * CH
    esc = escena_en(t0 + 0.1)
    prog = LUZ if esc in ESCENAS_LUZ else ACORDES
    acorde = prog[i % 4]
    a = int(t0 * SR)
    n = int((CH + 1.5) * SR)            # se solapa para ligar acordes
    n = min(n, N - a)
    if n <= 0:
        break
    en = env_adsr(n, 1.4, 1.6)
    br = 6 + int(6 * intensidad(t0))
    for m in acorde[1:]:
        pad[a:a + n] += pad_voice(nota(m), n, br) * en * 0.22
    for m in acorde[1:3]:
        voces[a:a + n] += coro(nota(m + 12), n) * en * 0.12
    raiz = acorde[0] - 12
    tt = np.arange(n) / SR
    bajo[a:a + n] += (np.sin(2 * np.pi * nota(raiz) * tt) + 0.3 * np.sin(4 * np.pi * nota(raiz) * tt)) * en * 0.30
    # arpegio de campanas, suave, en escenas explicativas
    if esc not in ("problema",):
        paso = CH / 8
        for j in range(8):
            m = acorde[[1, 2, 3, 2, 1, 2, 3, 2][j]] + 24
            b = a + int(j * paso * SR)
            nb = int(1.8 * SR)
            nb = min(nb, N - b)
            if nb <= 0:
                continue
            tb = np.arange(nb) / SR
            f = nota(m)
            campanas[b:b + nb] += (np.sin(2 * np.pi * f * tb) + 0.25 * np.sin(2 * np.pi * f * 2.76 * tb)) \
                * np.exp(-tb * 3.2) * 0.05 * (0.5 + intensidad(t0) * 0.5)

# filtro pasa-bajos al pad para que sea cálido y no tape la voz
b_lp, a_lp = signal.butter(2, 2200 / (SR / 2))
pad = signal.lfilter(b_lp, a_lp, pad)
voces = signal.lfilter(*signal.butter(2, [250 / (SR / 2), 3000 / (SR / 2)], "band"), voces)

# curva de energía por escena, suavizada
curva = np.array([intensidad(x / 100) for x in range(int(DUR * 100) + 1)])
curva = np.convolve(curva, np.ones(200) / 200, mode="same")
curva = np.interp(np.arange(N) / SR, np.arange(len(curva)) / 100, curva)

musica = (pad + bajo) * (0.55 + 0.45 * curva) + voces * curva + campanas

# ------------------------------------------------------------------- efectos
fx = np.zeros(N)


def poner(t, s, g=1.0):
    a = int(t * SR)
    if a >= N:
        return
    n = min(len(s), N - a)
    fx[a:a + n] += s[:n] * g


def golpe(dur=3.0, f0=60):
    """Golpe grave de timbal/impacto."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t * 18))
    ph = 2 * np.pi * np.cumsum(f) / SR
    tono = np.sin(ph) * np.exp(-t * 2.2)
    ruido = signal.lfilter(*signal.butter(2, 900 / (SR / 2)), rng.normal(0, 1, n)) * np.exp(-t * 9) * 0.6
    return (tono + ruido) * 0.9


def brillo_botin(dur=2.5):
    """Destello mágico: barrido ascendente de campanitas."""
    n = int(dur * SR)
    out = np.zeros(n)
    for k, m in enumerate([74, 77, 81, 86, 89, 93]):
        a = int(k * 0.07 * SR)
        nn = n - a
        t = np.arange(nn) / SR
        out[a:] += np.sin(2 * np.pi * nota(m) * t) * np.exp(-t * 2.5) * 0.18
    return out


def dados(dur=0.7):
    """Traqueteo de dados."""
    n = int(dur * SR)
    out = np.zeros(n)
    for k in range(9):
        a = int(rng.uniform(0, dur * 0.8) * SR)
        nn = int(0.025 * SR)
        if a + nn > n:
            continue
        clic = rng.normal(0, 1, nn) * np.exp(-np.arange(nn) / SR * 180)
        out[a:a + nn] += signal.lfilter(*signal.butter(2, [1500 / (SR / 2), 6000 / (SR / 2)], "band"), clic) * 0.5
    return out


def fanfarria():
    """Acorde corto de victoria (Re mayor)."""
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for m in (62, 66, 69, 74):
        out += pad_voice(nota(m), n, 8) * 0.12
    return signal.lfilter(b_lp, a_lp, out) * env_adsr(n, 0.04, 1.8)


def whoosh(dur=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    r = rng.normal(0, 1, n)
    b, a = signal.butter(2, [400 / (SR / 2), 2500 / (SR / 2)], "band")
    return signal.lfilter(b, a, r) * np.sin(np.pi * t / dur) ** 2 * 0.25


def tic():
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.25


def c(cue, frac=0.0):
    x = CUE[cue]
    return x["ini"] + frac * (x["fin"] - x["ini"])


# Estos momentos coinciden con los de escenas/index.html (mismos cues y fracciones)
poner(0.6, golpe(4.0, 40), 1.0)              # se abre el portal
poner(0.9, whoosh(2.5), 1.0)
poner(2.6, brillo_botin(3.0), 0.8)
poner(ESC["problema"]["ini"], whoosh(1.2))
for k in ("h2", "h3", "h4"):                  # aparece cada herramienta
    poner(c(k, 0.0), brillo_botin(), 0.6)
poner(c("h6", 0.05), golpe(2.5, 70), 0.5)
poner(c("r2", 0.25), tic(), 1.0)              # clic en "Entrar con Discord"
poner(c("r4", 0.3), tic(), 0.8)               # clic en "No voy a raidear en TBC"
poner(c("k1", 0.0), whoosh(1.0), 0.8)
poner(c("b3", 0.55), tic(), 1.0)              # clic en el botón del minimapa
poner(c("b5", 0.3), tic(), 0.9)               # clic derecho: opciones
poner(c("v2", 0.35), tic(), 1.0)              # clic en "Reservar"
poner(c("o1", 0.15), brillo_botin(), 0.6)     # cae un objeto
poner(c("o6", 0.33), tic(), 1.0)              # pulsa MS
poner(c("o6", 0.42), dados(), 1.0)            # el addon tira el dado
for k in range(6):                            # cuenta atrás
    poner(c("o6", 0.7) + k * 0.5, tic(), 0.6)
poner(c("w3", 0.05), dados(), 0.8)
poner(c("w3", 0.55), dados(), 0.8)
poner(c("w4", 0.0), fanfarria(), 0.9)         # gana Veltra
poner(c("w5", 0.4), tic(), 0.8)               # "Ver lista"
poner(c("e1", 0.0), fanfarria(), 0.9)         # aviso a la banda
poner(c("e3", 0.25), brillo_botin(), 0.8)     # llega a la bolsa
poner(c("m1", 0.2), brillo_botin(), 0.6)      # marca de conjunto
poner(c("m6", 0.25), whoosh(1.0), 1.0)        # termina la ronda
poner(ESC["cierre"]["ini"] + 0.2, whoosh(1.4), 0.8)
poner(c("c2", 0.0) - 0.3, golpe(4.0, 45), 1.0)
poner(c("c2", 0.0) - 0.2, brillo_botin(3.0), 0.9)

# ------------------------------------------------------------------ reverb
def reverb(x, seg=3.2, mezcla=0.35):
    n = int(seg * SR)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, n) * np.exp(-t * 3.0 / seg * 2.3)
    ir = signal.lfilter(*signal.butter(1, 5000 / (SR / 2)), ir)
    ir /= np.sqrt((ir ** 2).sum())
    wet = signal.fftconvolve(x, ir)[:len(x)]
    return x * (1 - mezcla) + wet * mezcla * 1.6


musica = reverb(musica, 3.5, 0.45)
fx = reverb(fx, 2.2, 0.25)

# estéreo: pequeña diferencia de tiempo para dar amplitud
izq = musica + fx
der = np.concatenate([np.zeros(int(0.011 * SR)), musica[:-int(0.011 * SR)]]) + fx

# ------------------------------------------------------ bajar música con voz
voz, vsr = sf.read(os.path.join(TRABAJO, "narracion.wav"), dtype="float64")
voz = signal.resample_poly(voz, SR, vsr)
voz = np.pad(voz, (0, max(0, N - len(voz))))[:N]
envv = np.sqrt(np.convolve(voz ** 2, np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same"))
envv = np.clip(envv / 0.05, 0, 1)
envv = np.convolve(envv, np.ones(int(0.5 * SR)) / int(0.5 * SR), mode="same")   # suavizar
duck = 1 - 0.78 * np.clip(envv, 0, 1)

m_st = np.stack([izq, der], 1)
m_st *= 0.20 / np.percentile(np.abs(m_st), 99.9)
m_st *= duck[:, None]
# desvanecer al final
fade = int(3.0 * SR)
m_st[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
m_st[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
sf.write(os.path.join(TRABAJO, "musica.wav"), m_st.astype(np.float32), SR)

voz_n = voz * (0.85 / np.abs(voz).max())
# ecualización ligera de la voz: un poco más de calidez
voz_n = voz_n + 0.25 * signal.lfilter(*signal.butter(2, 250 / (SR / 2)), voz_n)
mezcla = m_st + voz_n[:, None]
mezcla *= 0.95 / np.abs(mezcla).max()
sf.write(os.path.join(TRABAJO, "mezcla.wav"), mezcla.astype(np.float32), SR)
print("audio listo:", round(len(mezcla) / SR, 1), "s")
