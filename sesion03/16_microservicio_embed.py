"""
Ejercicio 16 — Endpoint `/embed` unificado.
"""

from __future__ import annotations

import os
from hashlib import sha1
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import numpy as np
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from huggingface_hub import InferenceClient
from openai import OpenAI
from pydantic import BaseModel, Field

Backend = Literal["openai", "hf", "ollama"]

app = FastAPI(title="Embedding Router", version="0.1.0")


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def embeddings_openai(texts: List[str], model: Optional[str]) -> np.ndarray:
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")
    client = OpenAI(api_key=api_key)
    model_name = model or os.getenv("DEFAULT_MODEL_EMBEDDINGS_OPENAI", "text-embedding-3-small")
    respuesta = client.embeddings.create(model=model_name, input=texts)
    vectores = [np.array(item.embedding, dtype=np.float32) for item in respuesta.data]
    return np.vstack(vectores)


def embeddings_hf(texts: List[str], model: Optional[str]) -> np.ndarray:
    load_env()
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_API_KEY no configurado.")
    client = InferenceClient(provider="hf-inference", api_key=api_key)
    model_id = model or os.getenv("DEFAULT_MODEL_EMBEDDINGS_HF", "sentence-transformers/all-MiniLM-L6-v2")
    vectores = client.feature_extraction(texts, model=model_id)
    return np.array(vectores, dtype=np.float32)


def embeddings_ollama(texts: List[str], model: Optional[str]) -> np.ndarray:
    model_name = model or "nomic-embed-text"
    vectores: List[np.ndarray] = []
    for texto in texts:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": model_name, "prompt": texto},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        vectores.append(np.array(data["embedding"], dtype=np.float32))
    return np.vstack(vectores)


class EmbedRequest(BaseModel):
    backend: Backend = Field(..., description="openai | hf | ollama")
    texts: List[str] = Field(..., min_items=1, description="Lista de textos a convertir en embeddings.")
    model: Optional[str] = None
    return_vectors: bool = Field(False, description="Si es True, devuelve los vectores completos.")


class EmbedResponse(BaseModel):
    backend: Backend
    model: str
    dimension: int
    vectors: List[List[float]] | None
    hashes: List[str]


def hashear_vector(vector: np.ndarray) -> str:
    return sha1(vector.tobytes()).hexdigest()[:12]


@app.post("/embed", response_model=EmbedResponse)
def embed_router(payload: EmbedRequest) -> EmbedResponse:
    try:
        if payload.backend == "openai":
            vectores = embeddings_openai(payload.texts, payload.model)
            model_usado = payload.model or os.getenv("DEFAULT_MODEL_EMBEDDINGS_OPENAI", "text-embedding-3-small")
        elif payload.backend == "hf":
            vectores = embeddings_hf(payload.texts, payload.model)
            model_usado = payload.model or os.getenv("DEFAULT_MODEL_EMBEDDINGS_HF", "sentence-transformers/all-MiniLM-L6-v2")
        elif payload.backend == "ollama":
            vectores = embeddings_ollama(payload.texts, payload.model)
            model_usado = payload.model or "nomic-embed-text"
        else:  # pragma: no cover - validado por Pydantic
            raise ValueError(f"Backend no soportado: {payload.backend}")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    dimension = int(vectores.shape[1])
    hashes = [hashear_vector(vec) for vec in vectores]
    vectors_json = vectores.round(6).tolist() if payload.return_vectors else None

    return EmbedResponse(
        backend=payload.backend,
        model=model_usado,
        dimension=dimension,
        vectors=vectors_json,
        hashes=hashes,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("16_microservicio_embed:app", host="0.0.0.0", port=8002, reload=True)

