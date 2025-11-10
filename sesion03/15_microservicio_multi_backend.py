"""
Ejercicio 15 — Microservicio `/chat` multi-backend.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Tuple

import google.generativeai as genai
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from huggingface_hub import InferenceClient
from openai import OpenAI
from pydantic import BaseModel, Field

Backend = Literal["openai", "hf", "google", "ollama"]

app = FastAPI(title="LLM Router", version="0.1.0")


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def call_openai(prompt: str, temperature: float, model: Optional[str]) -> Tuple[str, str, Dict[str, Any]]:
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")
    client = OpenAI(api_key=api_key)
    model_name = model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    respuesta = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "Eres un asistente útil y directo."},
            {"role": "user", "content": prompt},
        ],
    )
    choice = respuesta.choices[0].message.content.strip()
    usage = respuesta.usage
    meta = {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
    }
    return choice, model_name, meta


def call_huggingface(prompt: str, temperature: float, model: Optional[str]) -> Tuple[str, str, Dict[str, Any]]:
    load_env()
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_API_KEY no configurado.")
    client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=api_key)
    model_id = model or os.getenv("DEFAULT_MODEL_HF", "moonshotai/Kimi-K2-Instruct-0905")
    respuesta = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "Eres un analista que responde en español claro."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=256,
    )
    texto = respuesta.choices[0].message.content.strip()
    return texto, model_id, {}


def call_gemini(prompt: str, temperature: float, model: Optional[str]) -> Tuple[str, str, Dict[str, Any]]:
    load_env()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY no configurado.")
    genai.configure(api_key=api_key)
    model_name = model or os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")
    generative_model = genai.GenerativeModel(model_name)
    respuesta = generative_model.generate_content(
        prompt,
        generation_config={"temperature": temperature},
        request_options={"timeout": 60},
    )
    return respuesta.text.strip(), model_name, {}


def call_ollama(prompt: str, temperature: float, model: Optional[str]) -> Tuple[str, str, Dict[str, Any]]:
    model_name = model or "llama3"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "options": {"temperature": temperature, "num_predict": 256},
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip(), model_name, {"total_duration": data.get("total_duration")}


class ChatRequest(BaseModel):
    backend: Backend = Field(..., description="Proveedor: openai | hf | google | ollama")
    prompt: str = Field(..., min_length=3, max_length=2000)
    temperature: float = Field(0.2, ge=0.0, le=1.2)
    model: Optional[str] = None


class ChatResponse(BaseModel):
    backend: Backend
    model: str
    message: str
    latency_ms: float
    metadata: Dict[str, Any]


@app.post("/chat", response_model=ChatResponse)
def chat_router(payload: ChatRequest) -> ChatResponse:
    inicio = time.perf_counter()
    try:
        if payload.backend == "openai":
            mensaje, modelo, meta = call_openai(payload.prompt, payload.temperature, payload.model)
        elif payload.backend == "hf":
            mensaje, modelo, meta = call_huggingface(payload.prompt, payload.temperature, payload.model)
        elif payload.backend == "google":
            mensaje, modelo, meta = call_gemini(payload.prompt, payload.temperature, payload.model)
        elif payload.backend == "ollama":
            mensaje, modelo, meta = call_ollama(payload.prompt, payload.temperature, payload.model)
        else:  # pragma: no cover - validado por Pydantic
            raise ValueError(f"Backend no soportado: {payload.backend}")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    duracion_ms = (time.perf_counter() - inicio) * 1000

    return ChatResponse(
        backend=payload.backend,
        model=modelo,
        message=mensaje,
        latency_ms=duracion_ms,
        metadata=meta,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("15_microservicio_multi_backend:app", host="0.0.0.0", port=8001, reload=True)

