# Newsroom Sidekick — Ollama Edition (API)

API mínima (FastAPI) para demo de aula:
- `POST /summarize` → resumen ≤ 80 palabras + 3 viñetas
- `POST /extract` → extracción **JSON** válida según esquema (validada con `jsonschema`)
- `POST /vision` → análisis de imagen (Base64) con **VLM** (p. ej., `llava`)
- `GET /health` → precalienta modelos y reporta estado
- Métricas en `metrics.csv` (latencia, tokens, endpoint, modelo, timestamp)

> 100% local con **Ollama** (`/api/generate`). Pensado para clase/capstone.

---

## Requisitos

- Python 3.10+
- **Ollama** corriendo en `http://localhost:11434`
- Modelos:
  - Texto: por defecto `gemma:2b` (cámbialo si prefieres otro).
  - Visión: `llava` (`ollama pull llava`).

Instalación:
```bash
python -m venv .venv && source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env


POST /summarize
{
  "text": "Aquí el contenido a resumir...",
  "temperature": 0.2,
  "seed": 42
}

curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Texto a resumir...","temperature":0.2,"seed":42}'



POST /extract
{
  "text": "Borrador de noticia o documento...",
  "temperature": 0.2,
  "seed": 42
}

Salida:
{
  "model": "gemma:2b",
  "latency_ms": 678,
  "json": {
    "titulo_sugerido": "Ejemplo",
    "temas": ["economía","IA"],
    "entidades": ["Prensa Ibérica"],
    "sentimiento": "neutro"
  }
}

curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"text":"Texto para extraer entidades/temas...","temperature":0.2,"seed":42}'


POST /vision
{
  "image_base64": "<IMAGEN_EN_BASE64>",
  "temperature": 0.2
}

salida:
{
  "model": "llava",
  "latency_ms": 1432,
  "json": {
    "descripcion": "Una sala de prensa con micrófonos...",
    "objetos": ["micrófono","mesa","personas"],
    "alt_text": "Presentación en sala de prensa con varios micrófonos."
  }
}

IMG_B64=$(base64 -w0 sample.jpg)
curl -X POST http://localhost:8000/vision \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\":\"$IMG_B64\", \"temperature\":0.2}"
