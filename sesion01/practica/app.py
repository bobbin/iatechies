import os, time, csv, base64, json, threading
from datetime import datetime
from typing import List, Optional

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from jsonschema import validate as jsonschema_validate, ValidationError

# ------------------------------
# Config (Local por defecto)
# ------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_TEXT = os.getenv("OLLAMA_MODEL_TEXT", "gemma:2b")
MODEL_VISION = os.getenv("OLLAMA_MODEL_VISION", "llava")

METRICS_FILE = os.getenv("METRICS_FILE", "metrics.csv")
KEEP_ALIVE_SECS = int(os.getenv("KEEP_ALIVE_SECS", "300"))

# ------------------------------
# Cloud (opcional)
# Activa con OLLAMA_MODE=cloud y define OLLAMA_CLOUD_URL + OLLAMA_CLOUD_API_KEY
# ------------------------------
OLLAMA_MODE = os.getenv("OLLAMA_MODE", "local").lower()  # 'local' | 'cloud'

# Suele ser https://api.ollama.ai (ajústalo si tu cuenta indica otro)
OLLAMA_CLOUD_URL = os.getenv("OLLAMA_CLOUD_URL", "https://api.ollama.ai")
OLLAMA_CLOUD_API_KEY = os.getenv("OLLAMA_CLOUD_API_KEY", "")

# Headers para Cloud (Authorization Bearer). En local no se usan.
CLOUD_HEADERS = {}
if OLLAMA_MODE == "cloud":
    if not OLLAMA_CLOUD_API_KEY:
        # Para no romper la app si alguien lo activa sin clave
        print("[WARN] OLLAMA_MODE=cloud pero falta OLLAMA_CLOUD_API_KEY")
    CLOUD_HEADERS = {
        "Authorization": f"Bearer {OLLAMA_CLOUD_API_KEY}",
        "Content-Type": "application/json"
    }
    # En modo cloud, el "base URL" cambia
    OLLAMA_URL = OLLAMA_CLOUD_URL

# ------------------------------
# Pydantic I/O
# ------------------------------
class SummarizeIn(BaseModel):
    text: str = Field(..., description="Texto a resumir.")
    temperature: Optional[float] = Field(0.2, ge=0, le=2)
    seed: Optional[int] = Field(42, description="Semilla para reproducibilidad (opcional).")

class ExtractIn(BaseModel):
    text: str = Field(..., description="Texto a analizar.")
    temperature: Optional[float] = Field(0.2, ge=0, le=2)
    seed: Optional[int] = Field(42)

class VisionIn(BaseModel):
    image_base64: str = Field(..., description="Imagen codificada en Base64 (jpg/png).")
    temperature: Optional[float] = Field(0.2, ge=0, le=2)

class HealthOut(BaseModel):
    status: str
    text_model: str
    vision_model: str
    warmed: bool

# ------------------------------
# JSON Schema para /extract
# ------------------------------
EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "titulo_sugerido": {"type": "string"},
        "temas": {"type": "array", "items": {"type": "string"}},
        "entidades": {"type": "array", "items": {"type": "string"}},
        "sentimiento": {"type": "string", "enum": ["negativo", "neutro", "positivo"]}
    },
    "required": ["titulo_sugerido", "temas", "entidades", "sentimiento"]
}

# ------------------------------
# Utilidades HTTP (local y cloud)
# ------------------------------
def _post_json(url: str, payload: dict) -> requests.Response:
    """
    En local: POST sin Authorization.
    En cloud: añade Authorization Bearer (si hay API key).
    """
    if OLLAMA_MODE == "cloud":
        return requests.post(url, headers=CLOUD_HEADERS, json=payload, timeout=300)
    else:
        return requests.post(url, json=payload, timeout=300)

def _metrics_write(row: List):
    write_header = not os.path.exists(METRICS_FILE)
    with open(METRICS_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(["timestamp","endpoint","model","latency_ms","prompt_tokens","output_tokens"])
        w.writerow(row)

def _ollama_generate(model: str, payload: dict) -> dict:
    """
    Llama a /api/generate (local o cloud).
    Cloud replica el API: mismo body (stream:false, prompt, options, images, format).
    """
    url = f"{OLLAMA_URL}/api/generate"
    # Aseguramos stream:false por defecto
    payload = {"model": model, **payload, "stream": False}
    r = _post_json(url, payload)
    if r.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Ollama error {r.status_code}: {r.text[:400]}")
    return r.json()

def _warm_model(model: str):
    try:
        # En Cloud, keep_alive puede ignorarse o no ser necesario.
        # Lo dejamos porque en local ayuda al cold start.
        _post_json(f"{OLLAMA_URL}/api/generate", {"model": model, "keep_alive": KEEP_ALIVE_SECS})
    except Exception:
        pass

def _safe_b64(image_base64: str) -> bytes:
    try:
        return base64.b64decode(image_base64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="image_base64 no es Base64 válido.")

# ------------------------------
# FastAPI
# ------------------------------
app = FastAPI(title="Newsroom Sidekick — Ollama Edition", version="1.1.0")

@app.on_event("startup")
def startup_event():
    # Precalentar en segundo plano (local: útil; cloud: probablemente innecesario)
    threading.Thread(target=_warm_model, args=(MODEL_TEXT,), daemon=True).start()
    threading.Thread(target=_warm_model, args=(MODEL_VISION,), daemon=True).start()

@app.get("/health", response_model=HealthOut)
def health():
    try:
        _warm_model(MODEL_TEXT)
        _warm_model(MODEL_VISION)
        return HealthOut(status="ok", text_model=MODEL_TEXT, vision_model=MODEL_VISION, warmed=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------
# Endpoints
# ------------------------------
@app.post("/summarize")
def summarize(inp: SummarizeIn):
    """
    Devuelve: ≤80 palabras + 3 viñetas. Respuesta en texto plano con el formato solicitado.
    """
    prompt = (
        "Resume el siguiente texto en como máximo 80 palabras y añade después EXACTAMENTE "
        "tres viñetas con los puntos clave. Responde en español.\n\n---\n"
        f"{inp.text}\n---"
    )
    options = {"temperature": inp.temperature}
    if inp.seed is not None:
        options["seed"] = int(inp.seed)

    t0 = time.time()
    data = _ollama_generate(MODEL_TEXT, {"prompt": prompt, "options": options})
    dt_ms = int((time.time() - t0) * 1000)

    _metrics_write([datetime.utcnow().isoformat(), "summarize", MODEL_TEXT,
                    dt_ms, data.get("prompt_eval_count"), data.get("eval_count")])

    return {
        "model": MODEL_TEXT,
        "mode": OLLAMA_MODE,
        "latency_ms": dt_ms,
        "response": data.get("response","").strip()
    }

@app.post("/extract")
def extract(inp: ExtractIn):
    """
    Devuelve JSON ESTRICTO según EXTRACT_SCHEMA.
    """
    prompt = (
        "Lee el texto y devuelve SOLO un JSON válido con esta estructura exacta: "
        "{'titulo_sugerido': str, 'temas': [str], 'entidades': [str], 'sentimiento': 'negativo|neutro|positivo'}. "
        "Sin comentarios, sin texto extra, solo el JSON.\n\n---\n"
        f"{inp.text}\n---"
    )
    options = {"temperature": inp.temperature}
    if inp.seed is not None:
        options["seed"] = int(inp.seed)

    # En Ollama (local o cloud) podemos usar 'format' con schema para forzar JSON
    payload = {"prompt": prompt, "options": options, "format": EXTRACT_SCHEMA}

    t0 = time.time()
    data = _ollama_generate(MODEL_TEXT, payload)
    dt_ms = int((time.time() - t0) * 1000)

    raw = data.get("response","").strip()

    # Validación de JSON
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        raw2 = raw.replace("'", '"')
        try:
            obj = json.loads(raw2)
        except Exception:
            raise HTTPException(status_code=502, detail=f"Salida no es JSON válido: {raw[:300]}")
    try:
        jsonschema_validate(instance=obj, schema=EXTRACT_SCHEMA)
    except ValidationError as ve:
        raise HTTPException(status_code=502, detail=f"JSON no cumple schema: {ve.message[:200]}")

    _metrics_write([datetime.utcnow().isoformat(), "extract", MODEL_TEXT,
                    dt_ms, data.get("prompt_eval_count"), data.get("eval_count")])

    return {
        "model": MODEL_TEXT,
        "mode": OLLAMA_MODE,
        "latency_ms": dt_ms,
        "json": obj
    }

@app.post("/vision")
def vision(inp: VisionIn):
    """
    Devuelve JSON con {descripcion, objetos[], alt_text}.
    Requiere VLM disponible en local o en Cloud bajo el mismo API.
    """
    _ = _safe_b64(inp.image_base64)  # solo validamos; Ollama espera Base64 como string

    prompt = (
        "Analiza la imagen y devuelve SOLO un JSON con esta estructura exacta: "
        "{'descripcion': str, 'objetos': [str], 'alt_text': str}. "
        "El 'alt_text' debe ser ≤150 caracteres y útil para accesibilidad. "
        "Solo JSON, sin texto adicional."
    )
    options = {"temperature": inp.temperature}

    t0 = time.time()
    data = _ollama_generate(MODEL_VISION, {
        "prompt": prompt,
        "images": [inp.image_base64],
        "format": "json",
        "options": options
    })
    dt_ms = int((time.time() - t0) * 1000)

    raw = data.get("response","").strip()
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        raw2 = raw.replace("'", '"')
        try:
            obj = json.loads(raw2)
        except Exception:
            raise HTTPException(status_code=502, detail=f"Salida visión no es JSON válido: {raw[:300]}")

    # Post-condición: alt_text ≤ 150 chars
    alt_text = obj.get("alt_text","")
    if not isinstance(alt_text, str) or len(alt_text) > 150:
        obj["alt_text"] = (str(alt_text)[:147] + "...") if alt_text else ""

    _metrics_write([datetime.utcnow().isoformat(), "vision", MODEL_VISION,
                    dt_ms, data.get("prompt_eval_count"), data.get("eval_count")])

    return {
        "model": MODEL_VISION,
        "mode": OLLAMA_MODE,
        "latency_ms": dt_ms,
        "json": obj
    }