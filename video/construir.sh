#!/usr/bin/env bash
# Construye el video completo: narración -> música -> imágenes -> video final.
#
# Requisitos (una sola vez):
#   pip install kokoro-onnx soundfile numpy scipy imageio-ffmpeg
#   npm i playwright-core            (y un Chromium; ver CHROME en herramientas/render.cjs)
#   Modelo de voz Kokoro v1.0 en $KOKORO_DIR:
#     https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
#     https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
set -euo pipefail
cd "$(dirname "$0")"
TRABAJO=${TRABAJO:-build}
PARTES=${PARTES:-4}
SALIDA=${SALIDA:-SoftReserve335_PactoOscuro.mp4}
FFMPEG=${FFMPEG:-$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")}
export FFMPEG
mkdir -p "$TRABAJO"

echo "== 1/4 narración"
python3 herramientas/tts.py "$TRABAJO"
echo "== 2/4 música y efectos"
python3 herramientas/musica.py "$TRABAJO"

echo "== 3/4 imágenes ($PARTES partes en paralelo)"
DUR=$(python3 -c "import json; print(json.load(open('$TRABAJO/timeline.json'))['duracion'])")
rm -f "$TRABAJO"/parte_*.mp4 "$TRABAJO/partes.txt"
for i in $(seq 0 $((PARTES - 1))); do
  A=$(python3 -c "print(round($DUR * $i / $PARTES * 30) / 30)")
  B=$(python3 -c "print(round($DUR * ($i + 1) / $PARTES * 30) / 30)")
  node herramientas/render.cjs tramo "$TRABAJO" "$A" "$B" "$TRABAJO/parte_$i.mp4" &
  echo "file 'parte_$i.mp4'" >> "$TRABAJO/partes.txt"
done
wait

echo "== 4/4 unir video y audio"
"$FFMPEG" -y -loglevel error -f concat -safe 0 -i "$TRABAJO/partes.txt" -i "$TRABAJO/mezcla.wav" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 \
  -shortest -movflags +faststart "$SALIDA"
cp "$TRABAJO/subtitulos.srt" "${SALIDA%.mp4}.srt"
echo "listo: $SALIDA"
