"""
Ejercicio 10 — Embeddings con Hugging Face y búsqueda semántica básica.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def obtener_embeddings(textos: List[str], model_id: str) -> np.ndarray:
    load_env()
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_API_KEY no disponible.")

    client = InferenceClient(provider="hf-inference", api_key=api_key)
    vectores = client.feature_extraction(
        textos,
        model=model_id,
    )
    return np.array(vectores, dtype=np.float32)


def buscar_similares(
    corpus: List[str],
    embeddings: np.ndarray,
    consulta: str,
    *,
    model_id: str,
    top_k: int = 3,
) -> List[Tuple[str, float]]:
    consulta_emb = obtener_embeddings([consulta], model_id=model_id).squeeze(0)
    norm_corpus = embeddings / np.maximum(np.linalg.norm(embeddings, axis=1, keepdims=True), 1e-12)
    norm_query = consulta_emb / max(np.linalg.norm(consulta_emb), 1e-12)
    similitudes = norm_corpus @ norm_query

    indices = np.argsort(similitudes)[::-1][:top_k]
    return [(corpus[i], float(similitudes[i])) for i in indices]


if __name__ == "__main__":
    titulares = [
        "El Congreso aprueba la nueva ley de vivienda tras un intenso debate",
        "La selección femenina conquista su segundo mundial consecutivo",
        "Se lanza una misión privada a la Luna con participación europea",
        "Empresas tecnológicas españolas lideran la adopción de IA generativa",
        "Nuevos datos confirman la desaceleración económica en la eurozona",
        "El Barça se refuerza con una estrella del baloncesto argentino",
        "La OMS alerta de un repunte de casos de gripe aviar en Asia",
        "Google presenta mejoras de Gemini enfocadas a productividad",
    ]

    modelo_embeddings = os.getenv(
        "DEFAULT_MODEL_EMBEDDINGS_HF",
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    matriz = obtener_embeddings(titulares, modelo_embeddings)
    consulta = "El gobierno presenta medidas económicas de emergencia"
    resultados = buscar_similares(
        titulares,
        matriz,
        consulta,
        model_id=modelo_embeddings,
    )

    print(f"Consulta: {consulta}\n")
    for texto, score in resultados:
        print(f"- {score:.2f}: {texto}")

