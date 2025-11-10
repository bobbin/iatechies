"""
Ejercicio 04 — Reescritura de titulares con OpenAI.

Requiere configurar OPENAI_API_KEY y DEFAULT_MODEL_OPENAI en `.env`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv
from openai import OpenAI


def load_env() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path, override=False)


def get_openai_client() -> OpenAI:
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Configura OPENAI_API_KEY en tu archivo .env")
    return OpenAI(api_key=api_key)


def reescribir_titular(titular: str, *, model: str | None = None) -> str:
    client = get_openai_client()
    model_name = model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")

    respuesta = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "Eres un editor de titulares conciso y claro.",
            },
            {
                "role": "user",
                "content": f"Reescribe este titular: {titular}",
            },
        ],
    )

    return respuesta.choices[0].message.content.strip()


def demo(titulares: Iterable[str]) -> None:
    for idx, titular in enumerate(titulares, start=1):
        nuevo = reescribir_titular(titular)
        print(f"{idx:02d}. Original: {titular}")
        print(f"    Nuevo   : {nuevo}\n")


if __name__ == "__main__":
    ejemplos = [
        "El gobierno anuncia nuevas ayudas para autónomos",
        "Descubren una vulnerabilidad crítica en sistemas bancarios",
        "Barcelona presenta un plan para reducir el tráfico en el centro",
    ]
    demo(ejemplos)

