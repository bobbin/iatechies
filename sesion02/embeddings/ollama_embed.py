"""
Utilidades para embeddings con Ollama.

Uso básico:
    from ollama_embed import embed, cosine_sim
    v = embed("texto")  # np.ndarray shape (D,)
"""

from __future__ import annotations

import os
import requests
import numpy as np

OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")


def _embed_api(texts: list[str]) -> list[list[float]]:
    r = requests.post(
        f"{OLLAMA}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return data.get("embeddings", [])


def embed(text: str) -> np.ndarray:
    """Devuelve embedding 1D (np.ndarray) de un texto."""
    vecs = _embed_api([text])
    if not vecs:
        return np.zeros(0, dtype=np.float32)
    v = np.array(vecs[0], dtype=np.float32)
    return v


def cosine_sim(v1: np.ndarray, v2: np.ndarray) -> float:
    if v1.size == 0 or v2.size == 0:
        return 0.0
    a = np.linalg.norm(v1)
    b = np.linalg.norm(v2)
    if a == 0 or b == 0:
        return 0.0
    return float(np.dot(v1, v2) / (a * b))


