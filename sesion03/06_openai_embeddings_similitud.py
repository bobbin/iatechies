"""
Ejercicio 06 — Embeddings de titulares y similitud básica.
"""

from __future__ import annotations

import itertools
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI


def get_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en el entorno.")
    return OpenAI(api_key=api_key)


def obtener_embeddings(textos: list[str], model: str | None = None) -> np.ndarray:
    client = get_client()
    model_name = model or os.getenv(
        "DEFAULT_MODEL_EMBEDDINGS_OPENAI",
        "text-embedding-3-small",
    )

    respuesta = client.embeddings.create(model=model_name, input=textos)
    vectores = [np.array(item.embedding, dtype=np.float32) for item in respuesta.data]
    return np.vstack(vectores)


def similitud_coseno(matriz: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(matriz, axis=1, keepdims=True)
    normalizado = matriz / np.maximum(norm, 1e-12)
    return normalizado @ normalizado.T


def imprimir_similitudes(textos: list[str], sim_matrix: np.ndarray) -> None:
    print("Similitud coseno (0 = muy distintos, 1 = idénticos):\n")
    for i, j in itertools.combinations(range(len(textos)), 2):
        print(f"- {textos[i]}  ↔  {textos[j]} : {sim_matrix[i, j]:.2f}")


if __name__ == "__main__":
    titulares = [
        "El BCE mantiene los tipos de interés por primera vez en un año",
        "El Real Madrid vence 3-0 y se coloca líder de la Liga",
        "La inflación se modera en la eurozona durante octubre",
        "Nvidia lanza un chip optimizado para inteligencia artificial generativa",
    ]

    embeddings = obtener_embeddings(titulares)
    matriz_similitud = similitud_coseno(embeddings)
    imprimir_similitudes(titulares, matriz_similitud)

