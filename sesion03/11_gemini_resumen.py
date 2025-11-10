"""
Ejercicio 11 — Resumen de noticia con Gemini.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


def init_gemini() -> genai.GenerativeModel:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Configura GOOGLE_API_KEY en tu .env")

    genai.configure(api_key=api_key)
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")
    return genai.GenerativeModel(model_name)


def resumir_noticia(texto: str) -> tuple[str, float]:
    model = init_gemini()
    prompt = (
        "Resume la siguiente noticia en 3 bullet points claros y directos. "
        "Evita adjetivos superfluos y mantén los hechos clave.\n\n"
        f"{texto}"
    )
    inicio = time.perf_counter()
    respuesta = model.generate_content(prompt, request_options={"timeout": 60})
    duracion_ms = (time.perf_counter() - inicio) * 1000
    return respuesta.text.strip(), duracion_ms


if __name__ == "__main__":
    noticia = (
        "Google ha anunciado nuevas funciones basadas en Gemini para optimizar flujos de trabajo en Google Workspace, "
        "incluyendo resúmenes automáticos de documentos y sugerencias de respuestas para correos largos."
    )
    resumen, latencia = resumir_noticia(noticia)
    print(f"Latencia: {latencia:.0f} ms\n")
    print(resumen)

