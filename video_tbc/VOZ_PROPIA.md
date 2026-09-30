# Narración con tu voz (XTTS-v2 en tu PC)

Para Windows con tarjeta NVIDIA RTX serie 50 (por ejemplo RTX 5070).
Tiempo aproximado: 20–30 minutos la primera vez (casi todo es descarga).

## 1. Instalar Python

1. Descarga **Python 3.11** desde <https://www.python.org/downloads/windows/>.
2. Al instalar, marca la casilla **«Add python.exe to PATH»**.

## 2. Descargar el proyecto

Entra a <https://github.com/infmaquito-dotcom/Prueba/tree/claude/video-request-fo0kh4>,
pulsa **Code → Download ZIP** y descomprímelo (por ejemplo en `C:\PactoVideo`).

## 3. Preparar el entorno (una sola vez)

Abre la carpeta `video_tbc`, haz clic en la barra de dirección del explorador, escribe
`powershell` y pulsa Enter. En la ventana que se abre, copia estas líneas una por una:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
pip install coqui-tts
```

> La serie RTX 50 necesita PyTorch con **CUDA 12.8** (`cu128`); por eso se instala así y
> no con el paquete antiguo `TTS`.

Comprueba que ve tu tarjeta:

```powershell
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Debe decir `True NVIDIA GeForce RTX 5070`.

## 4. Grabar tu voz (1–2 minutos)

- Cuarto silencioso, sin música ni ventilador cerca, a 15–20 cm del micrófono.
- Habla como en el video: tranquilo, cercano, como explicando las reglas a un compañero.
- Graba con **Audacity** (gratis) y exporta como **WAV**, con el nombre `mi_voz.wav`,
  dentro de la carpeta `video_tbc`.
- Corta los silencios largos del principio y del final. Nada de audios de WhatsApp.

Texto para leer (puedes leerlo dos veces con calma):

> Hola, compañeros de Pacto Oscuro. Hoy les explico cómo vamos a repartir el botín en la
> nueva etapa. Primero, entren a la web de la hermandad con su cuenta de Discord y
> registren a su personaje principal. Después, completen la sección de sus personajes con
> la clase y la especialización. Es importante: sin registro no hay core, y sin core no
> hay rotación. Antes de cada banda, un oficial compartirá el enlace para reservar. Elijan
> bien: miren primero qué objeto les conviene y de qué jefe sale. Cuando caiga un objeto,
> aparecerá un aviso con tres botones, y el dado se tira solo. Quien lleve menos premios
> tiene prioridad. Así de simple, así de justo. Nos vemos en Karazhan, en Gruul y en
> Magtheridon. ¡Vamos, Pacto Oscuro!

## 5. Generar la narración

Con la ventana de PowerShell abierta en `video_tbc` (si la cerraste, vuelve a escribir
`.venv\Scripts\activate`):

```powershell
python herramientas\voz_xtts.py --voz mi_voz.wav --prueba
```

La primera vez descarga el modelo (unos 2 GB). Luego escucha los 3 audios de la carpeta
`voz_xtts`. Si te gustan, genera todo (unos pocos minutos con la RTX 5070):

```powershell
python herramientas\voz_xtts.py --voz mi_voz.wav
```

Escucha cada frase. Si alguna sale rara (palabra mal dicha, tono extraño), rehazla; cada
intento sale un poco distinto:

```powershell
python herramientas\voz_xtts.py --voz mi_voz.wav --solo r3,b5
```

Otras opciones: `--velocidad 0.92` (más pausado), `--temperatura 0.5` (más estable,
menos expresivo). Si tienes varias grabaciones buenas, pásalas todas:
`--voz toma1.wav toma2.wav`.

> Los nombres de las frases (`g1`, `r3`, `b5`…) están en `narracion.json` y en el
> `README.md`, junto al texto de cada una.

## 6. Enviarme los audios

Sube la carpeta `voz_xtts` completa a la misma rama en GitHub
(**Add file → Upload files**, dentro de `video_tbc/voz_xtts/`), o súbela como prefieras y
avísame. Yo rehago el video: las animaciones se ajustan solas al ritmo de tu voz.

> Ojo: si el repositorio es público, tu voz también lo será. Si prefieres, mándamela por
> otro medio.

## Si algo falla

- **`no kernel image is available`** → PyTorch no es la versión `cu128`: repite el paso 3.
- **Error de `weights_only`, `transformers` o de licencia** → `pip install -U coqui-tts`.
- **Cualquier otro error** → cópiame el mensaje completo y lo resolvemos.

La licencia de XTTS-v2 (Coqui Public Model License) permite solo uso **no comercial**;
un video interno de la hermandad está bien.
