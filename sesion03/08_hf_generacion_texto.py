"""
Ejercicio 08 — Generación de texto con la Hugging Face Inference API.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI

HF_BASE_URL = "https://router.huggingface.co/v1"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def resumir_noticia_hf(texto: str, *, model: str | None = None) -> str:
    load_env()
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_API_KEY no encontrado en el entorno.")

    client = OpenAI(base_url=HF_BASE_URL, api_key=api_key)
    model_id = model or os.getenv("DEFAULT_MODEL_HF", "moonshotai/Kimi-K2-Instruct-0905")

    prompt = (
        "Resume la siguiente noticia en 3 frases claras y directas, sin opinión.\n\n"
        f"Noticia: {texto}"
    )

    respuesta = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "Eres un asistente de redacción conciso."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.7,
    )

    return respuesta.choices[0].message.content.strip()


if __name__ == "__main__":
    noticia = (
        "El Parlamento Europeo ha aprobado hoy una nueva normativa de protección de datos "
        "para medios digitales, que incluye obligaciones específicas para plataformas con IA."
    )
    resumen = resumir_noticia_hf(noticia)
    print("Resumen generado por Hugging Face:")
    print(resumen)

