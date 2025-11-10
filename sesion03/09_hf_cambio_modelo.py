"""
Ejercicio 09 — Cambiar de modelo con la misma llamada (Hugging Face).
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path
from typing import Iterable, List, Tuple

from dotenv import load_dotenv
from openai import OpenAI

HF_BASE_URL = "https://router.huggingface.co/v1"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def generar_para_modelo(model_id: str, prompt: str) -> Tuple[str, float]:
    load_env()
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("Configura HF_API_KEY en tu .env")

    client = OpenAI(base_url=HF_BASE_URL, api_key=api_key)
    respuesta = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "Eres un analista que responde en español claro."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=220,
    )

    texto = respuesta.choices[0].message.content.strip()
    longitud = len(texto.split())
    return texto, longitud


def comparar_modelos(modelos: Iterable[str], prompt: str) -> List[Tuple[str, str, int]]:
    resultados = []
    for modelo in modelos:
        print(f"\nProbando modelo: {modelo}")
        texto, palabras = generar_para_modelo(modelo, prompt)
        resultados.append((modelo, texto, palabras))
    return resultados


if __name__ == "__main__":
    prompt = textwrap.dedent(
        """
        Resume la siguiente noticia en 3 frases y destaca el dato más relevante:

        La compañía AeroTech ha presentado su nuevo avión híbrido, capaz de ahorrar un 20%
        de combustible en rutas de medio alcance gracias a un sistema eléctrico auxiliar.
        """
    ).strip()

    modelos_demo = [
        os.getenv("DEFAULT_MODEL_HF", "moonshotai/Kimi-K2-Instruct-0905"),
        "openai/gpt-oss-120b",
        "deepseek-ai/DeepSeek-V3.2-Exp",
    ]

    resultados = comparar_modelos(modelos_demo, prompt)
    print("\n=== Comparativa de salidas ===")
    for modelo, texto, palabras in resultados:
        print(f"\n[{modelo}] ({palabras} palabras)")
        print(texto)

