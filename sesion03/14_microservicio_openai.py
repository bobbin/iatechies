"""
Ejercicio 14 — Microservicio FastAPI minimal que llama a OpenAI.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI(title="LLM Chat Service", version="0.1.0")


def get_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")
    return OpenAI(api_key=api_key)


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)
    temperature: float = Field(0.2, ge=0.0, le=1.0)
    model: Optional[str] = Field(
        default=None,
        description="Sobrescribe DEFAULT_MODEL_OPENAI si se indica.",
    )


class ChatResponse(BaseModel):
    message: str
    latency_ms: float
    model: str
    usage_prompt_tokens: Optional[int] = None
    usage_completion_tokens: Optional[int] = None


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    client = get_client()
    model_name = payload.model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    print(f"Payload: {payload}")
    inicio = time.perf_counter()
    try:
        respuesta = client.chat.completions.create(
            model=model_name,
            temperature=payload.temperature,
            messages=[
                {"role": "system", "content": "Eres un asistente útil y directo."},
                {"role": "user", "content": payload.prompt},
            ],
        )
    except Exception as exc:  # pragma: no cover - ejemplo simple
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    duracion_ms = (time.perf_counter() - inicio) * 1000

    choice = respuesta.choices[0].message.content.strip()
    usage = respuesta.usage

    return ChatResponse(
        message=choice,
        latency_ms=duracion_ms,
        model=model_name,
        usage_prompt_tokens=getattr(usage, "prompt_tokens", None),
        usage_completion_tokens=getattr(usage, "completion_tokens", None),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("14_microservicio_openai:app", host="0.0.0.0", port=8000, reload=True)

