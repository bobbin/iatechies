# Sesión 10 — Procesado de imágenes (multimodal) con Gemini y GPT

En esta sesión tienes **ejercicios prácticos** para analizar imágenes con modelos multimodales de:

- **Google Gemini** (SDK: `google-generativeai`)
- **OpenAI GPT** (SDK: `openai`, endpoint `responses`)

Los scripts **no incluyen claves**. Reutilizan el mismo patrón de sesiones anteriores: cargan un archivo `.env` local (opcional) y, si no existe, usan las variables de entorno ya definidas.

## Setup rápido

1) Crea `sesion10/.env` copiando el de sesiones anteriores (si ya lo tienes en tu máquina):

- Copia `sesion03/env.example` → `sesion10/.env` y rellena valores, o
- Copia tu `sesion03/.env` local → `sesion10/.env`.

2) Instala dependencias:

```bash
pip install -r sesion10/requirements.txt
```

3) Coloca imágenes en `sesion10/inputs/` (hay un `.gitkeep` para que exista la carpeta).

## Variables esperadas

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `DEFAULT_MODEL_OPENAI` (por defecto: `gpt-4o-mini`)
- `DEFAULT_MODEL_GOOGLE` (por defecto: `gemini-1.5-pro`)

## Ejercicios

- **01 — GPT**: descripción + etiquetas + alt-text en JSON.
- **02 — GPT**: “OCR” (lectura de texto) + extracción estructurada (factura/recibo) en JSON.
- **03 — Gemini**: alt-text accesible + pie de foto en JSON.
- **04 — Gemini**: detección de objetos con *bounding boxes aproximadas* (normalizadas 0..1) en JSON.
- **05 — Comparar 2 imágenes**: diferencias y cambios (elige proveedor con `--provider`).
- **06 — PDF (factura)**: extraer texto de un PDF y generar un JSON de factura (GPT).
- **07 — PDF (factura)**: extraer texto de un PDF y generar un JSON de factura (Gemini).

## Ejecución

Ejemplos (PowerShell/Windows):

```powershell
python sesion10\01_gpt_vision_describir.py sesion10\inputs\ejemplo.jpg
python sesion10\02_gpt_vision_ocr_extract.py sesion10\inputs\ticket.jpg
python sesion10\03_gemini_vision_alt_caption.py sesion10\inputs\ejemplo.jpg
python sesion10\04_gemini_vision_objetos_bbox.py sesion10\inputs\escena.jpg
python sesion10\05_comparar_dos_imagenes.py --provider openai sesion10\inputs\a.jpg sesion10\inputs\b.jpg
python sesion10\05_comparar_dos_imagenes.py --provider gemini sesion10\inputs\a.jpg sesion10\inputs\b.jpg
python sesion10\06_gpt_pdf_factura_extract.py sesion10\inputs\factura.pdf
python sesion10\07_gemini_pdf_factura_extract.py sesion10\inputs\factura.pdf
```

> Consejo: si quieres reutilizar una imagen de ejemplo ya existente en el repo, prueba con `sesion01/ejemplo.jpg`.


