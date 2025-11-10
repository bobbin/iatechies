"""
Ejercicio 12 — Generación de preguntas de entrevista con Gemini y comparación con OpenAI.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def generar_preguntas_gemini(noticia: str) -> List[str]:
    load_env()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Configura GOOGLE_API_KEY.")

    genai.configure(api_key=api_key)
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")
    modelo = genai.GenerativeModel(model_name)
    prompt = (
        "A partir de la siguiente noticia, genera 5 preguntas incisivas para una entrevista "
        "al protagonista. Deben ser directas, concretas y orientadas a obtener información nueva. "
        "Responde en formato lista numerada.\n\n"
        f"{noticia}"
    )
    respuesta = modelo.generate_content(prompt, request_options={"timeout": 60})
    texto = respuesta.text.strip()
    return [line.strip("-• ") for line in texto.splitlines() if line.strip()]


def generar_preguntas_openai(noticia: str) -> List[str]:
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Configura OPENAI_API_KEY para comparar con OpenAI.")
    client = OpenAI(api_key=api_key)
    model_name = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")

    respuesta = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un periodista experto en entrevistas incisivas. "
                    "Proporciona una lista numerada con preguntas directas y concretas."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Genera 5 preguntas incisivas para entrevistar al protagonista de esta noticia:\n"
                    f"{noticia}"
                ),
            },
        ],
    )
    texto = respuesta.choices[0].message.content.strip()
    return [line.strip("-• ") for line in texto.splitlines() if line.strip()]


if __name__ == "__main__":
    noticia_demo = (
        "Una investigación periodística revela que la compañía MetroCity ha utilizado algoritmos de IA "
        "para fijar precios discriminatorios en el transporte público, afectando especialmente a barrios periféricos."
    )

    print("Preguntas propuestas por Gemini:\n")
    for pregunta in generar_preguntas_gemini(noticia_demo):
        print(f"- {pregunta}")

    try:
        print("\nPreguntas propuestas por OpenAI:\n")
        for pregunta in generar_preguntas_openai(noticia_demo):
            print(f"- {pregunta}")
    except RuntimeError as exc:
        print(f"\nNo se generaron preguntas con OpenAI: {exc}")

