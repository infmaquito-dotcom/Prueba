"""Genera la narración frase por frase y la línea de tiempo del video.

Salidas (en la carpeta indicada):
  voz/<cue>.wav     una pista por frase
  narracion.wav     narración completa, ya ubicada en el tiempo
  timeline.json     inicio/fin de cada escena y de cada frase (lo usa la animación)
  subtitulos.srt    subtítulos en español
"""
import json, sys, os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL_DIR = os.environ.get("KOKORO_DIR", "/tmp/claude-0/tts")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "build")

SR = 24000
PAUSA_FRASE = 0.7      # silencio entre frases de una misma escena
ENTRADA = {"gancho": 3.2}   # tiempo de imagen antes de la primera frase
ENTRADA_DEF = 1.0
SALIDA_ESC = {"cierre": 5.5, "gancho": 1.6}
SALIDA_DEF = 1.4


def recortar(s, umbral=0.01):
    idx = np.where(np.abs(s) > umbral)[0]
    if len(idx) == 0:
        return s
    a = max(0, idx[0] - int(0.03 * SR))
    b = min(len(s), idx[-1] + int(0.08 * SR))
    return s[a:b]


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    with open(os.path.join(RAIZ, "narracion.json"), encoding="utf-8") as f:
        guion = json.load(f)
    os.makedirs(os.path.join(SALIDA, "voz"), exist_ok=True)
    k = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))

    t = 0.0
    escenas, pistas, srt = [], [], []
    for esc in guion["escenas"]:
        ini = t
        t += ENTRADA.get(esc["id"], ENTRADA_DEF)
        cues = []
        for i, c in enumerate(esc["cues"]):
            ruta = os.path.join(SALIDA, "voz", c["id"] + ".wav")
            if os.path.exists(ruta) and os.environ.get("REHACER") != "1":
                s, _ = sf.read(ruta, dtype="float32")
            else:
                s, sr = k.create(c["decir"], voice=guion["voz"], speed=guion["velocidad"], lang="es-419")
                assert sr == SR
                s = recortar(s)
                sf.write(ruta, s, SR)
            dur = len(s) / SR
            cues.append({"id": c["id"], "ini": round(t, 3), "fin": round(t + dur, 3), "texto": c["texto"]})
            pistas.append((t, s))
            srt.append((t, t + dur, c["texto"]))
            t += dur + (PAUSA_FRASE if i < len(esc["cues"]) - 1 else 0)
        t += SALIDA_ESC.get(esc["id"], SALIDA_DEF)
        escenas.append({"id": esc["id"], "titulo": esc["titulo"], "ini": round(ini, 3), "fin": round(t, 3), "cues": cues})
        print(f"{esc['id']:<11} {t - ini:6.1f} s")

    total = t
    mezcla = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for (ini, s) in pistas:
        a = int(ini * SR)
        mezcla[a:a + len(s)] += s
    sf.write(os.path.join(SALIDA, "narracion.wav"), mezcla, SR)

    with open(os.path.join(SALIDA, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump({"duracion": round(total, 3), "escenas": escenas}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(SALIDA, "subtitulos.srt"), "w", encoding="utf-8") as f:
        for n, (a, b, txt) in enumerate(srt, 1):
            f.write(f"{n}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n\n")
    print(f"TOTAL {total:.1f} s  ({int(total // 60)}:{int(total % 60):02})")


if __name__ == "__main__":
    main()
