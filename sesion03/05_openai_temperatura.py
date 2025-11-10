"""
Ejercicio 05 — Comparar temperatura en OpenAI.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Iterable, List, Tuple

from dotenv import load_dotenv
from openai import OpenAI


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def get_client() -> OpenAI:
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Configura OPENAI_API_KEY antes de ejecutar este script.")
    return OpenAI(api_key=api_key)


def probar_temperaturas(
    prompt: str,
    temperaturas: Iterable[float] = (0.0, 0.3, 0.7),
    *,
    model: str | None = None,
) -> List[Tuple[float, str, float]]:
    """
    Devuelve una lista de tuplas (temperature, contenido, latencia_ms).
    """
    client = get_client()
    model_name = model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    resultados: List[Tuple[float, str, float]] = []

    for temp in temperaturas:
        inicio = time.perf_counter()
        respuesta = client.chat.completions.create(
            model=model_name,
            temperature=temp,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un editor de titulares conciso y claro.",
                },
                {
                    "role": "user",
                    "content": f"Reescribe este titular: {prompt}",
                },
            ],
        )
        duracion_ms = (time.perf_counter() - inicio) * 1000
        texto = respuesta.choices[0].message.content.strip()
        resultados.append((temp, texto, duracion_ms))

    return resultados


if __name__ == "__main__":
    titular = "La inflación cae dos décimas en octubre según el INE"
    resultados = probar_temperaturas(titular)

    print(f"Prompt: {titular}\n")
    for temp, texto, duracion in resultados:
        print(f"temperature={temp:.1f} · {duracion:.0f} ms")
        print(f" → {texto}\n")

