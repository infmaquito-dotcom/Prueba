"""Genera la narración con TU voz usando XTTS-v2, en tu PC (con tarjeta NVIDIA).

Uso (desde la carpeta video_tbc, con el entorno activado):
    python herramientas/voz_xtts.py --voz mi_voz.wav --prueba     # solo 3 frases, para escuchar
    python herramientas/voz_xtts.py --voz mi_voz.wav              # todas las frases
    python herramientas/voz_xtts.py --voz mi_voz.wav --solo r3,b5 # rehacer frases concretas

Deja un archivo por frase en voz_xtts/<id>.wav (por ejemplo voz_xtts/g1.wav).
Las frases que ya existen no se vuelven a generar (salvo con --solo o --rehacer).
"""
import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voz", nargs="+", required=True, help="una o varias grabaciones tuyas (wav o mp3)")
    ap.add_argument("--salida", default=os.path.join(RAIZ, "voz_xtts"))
    ap.add_argument("--prueba", action="store_true", help="genera solo las 3 primeras frases")
    ap.add_argument("--solo", default="", help="ids separados por coma, por ejemplo: g1,r3")
    ap.add_argument("--rehacer", action="store_true", help="vuelve a generar todo")
    ap.add_argument("--velocidad", type=float, default=1.0, help="1.0 normal; 0.9 más pausado")
    ap.add_argument("--temperatura", type=float, default=0.65, help="más baja = más estable")
    args = ap.parse_args()

    for v in args.voz:
        if not os.path.exists(v):
            sys.exit(f"No encuentro la grabación: {v}")

    with open(os.path.join(RAIZ, "narracion.json"), encoding="utf-8") as f:
        guion = json.load(f)
    frases = [c for e in guion["escenas"] for c in e["cues"]]
    if args.solo:
        ids = {x.strip() for x in args.solo.split(",") if x.strip()}
        faltan = ids - {c["id"] for c in frases}
        if faltan:
            sys.exit("Estas frases no existen: " + ", ".join(sorted(faltan)))
        frases = [c for c in frases if c["id"] in ids]
    elif args.prueba:
        frases = frases[:3]

    os.environ.setdefault("COQUI_TOS_AGREED", "1")  # licencia CPML de XTTS-v2: uso no comercial
    import torch
    from TTS.api import TTS

    if not torch.cuda.is_available():
        print("AVISO: no se detecta la tarjeta NVIDIA; funcionará, pero muy lento.")
    disp = "cuda" if torch.cuda.is_available() else "cpu"
    print("Cargando XTTS-v2 (la primera vez descarga unos 2 GB)...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(disp)

    os.makedirs(args.salida, exist_ok=True)
    for i, c in enumerate(frases, 1):
        ruta = os.path.join(args.salida, c["id"] + ".wav")
        if os.path.exists(ruta) and not (args.rehacer or args.solo):
            print(f"[{i}/{len(frases)}] {c['id']}: ya existe, la salto")
            continue
        # "decir" es el texto escrito como se pronuncia (números en letras, siglas deletreadas)
        texto = c["decir"].replace("...", ",")
        print(f"[{i}/{len(frases)}] {c['id']}: {c['texto']}")
        tts.tts_to_file(text=texto, speaker_wav=args.voz, language="es", file_path=ruta,
                        speed=args.velocidad, temperature=args.temperatura)
    print(f"\nListo. Audios en: {args.salida}")
    print("Escúchalos; si alguno sale raro, rehazlo con --solo <id> (cada vez sale un poco distinto).")


if __name__ == "__main__":
    main()
