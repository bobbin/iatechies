"""
Ejercicio 17 — Middleware de métricas y logging en CSV.
"""

from __future__ import annotations

import csv
import os
import time
import uuid
from pathlib import Path
from threading import Lock
from typing import Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI(title="LLM Service con métricas", version="0.1.0")

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_PATH = LOG_DIR / "metrics.csv"
CSV_HEADER = [
    "timestamp",
    "request_id",
    "endpoint",
    "backend",
    "model",
    "latency_ms",
    "status_code",
    "tokens_prompt",
    "tokens_completion",
]
_lock = Lock()


def ensure_log_file() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    if not LOG_PATH.exists():
        with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)


def log_metrics(row: Dict[str, str | int | float | None]) -> None:
    ensure_log_file()
    with _lock, LOG_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([row.get(col, "") for col in CSV_HEADER])


def get_openai_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")
    return OpenAI(api_key=api_key)


class ChatRequest(BaseModel):
    backend: str = Field("openai", description="openai | hf | google | ollama")
    prompt: str = Field(..., min_length=3, max_length=2000)
    temperature: float = Field(0.2, ge=0.0, le=1.0)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    inicio = time.perf_counter()
    metrics: Dict[str, Optional[str | float | int]] = {
        "backend": None,
        "model": None,
        "tokens_prompt": None,
        "tokens_completion": None,
    }
    request.state.metrics = metrics
    request.state.request_id = request_id

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as exc:
        status_code = 500
        raise exc
    finally:
        duracion_ms = (time.perf_counter() - inicio) * 1000
        metrics["latency_ms"] = f"{duracion_ms:.2f}"
        log_metrics(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "request_id": request_id,
                "endpoint": request.url.path,
                "backend": metrics.get("backend"),
                "model": metrics.get("model"),
                "latency_ms": f"{duracion_ms:.2f}",
                "status_code": status_code,
                "tokens_prompt": metrics.get("tokens_prompt"),
                "tokens_completion": metrics.get("tokens_completion"),
            }
        )

    response.headers["X-Request-ID"] = request_id
    return response


@app.post("/chat")
async def chat(request: Request, payload: ChatRequest):
    request.state.metrics["backend"] = payload.backend
    if payload.backend != "openai":
        # Ejemplo simplificado: devolvemos una respuesta dummy para otros backends.
        message = f"[{payload.backend}] backend pendiente de implementación real."
        request.state.metrics["model"] = "demo"
        return JSONResponse(
            {
                "backend": payload.backend,
                "model": "demo",
                "message": message,
            }
        )

    client = get_openai_client()
    model_name = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    try:
        respuesta = client.chat.completions.create(
            model=model_name,
            temperature=payload.temperature,
            messages=[
                {"role": "system", "content": "Eres un asistente útil y directo."},
                {"role": "user", "content": payload.prompt},
            ],
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    usage = respuesta.usage
    request.state.metrics["model"] = model_name
    request.state.metrics["tokens_prompt"] = getattr(usage, "prompt_tokens", None)
    request.state.metrics["tokens_completion"] = getattr(usage, "completion_tokens", None)

    return {
        "backend": payload.backend,
        "model": model_name,
        "message": respuesta.choices[0].message.content.strip(),
        "usage": usage,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("17_middleware_metricas:app", host="0.0.0.0", port=8003, reload=True)

