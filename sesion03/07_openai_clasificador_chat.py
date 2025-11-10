"""
Ejercicio 07 — Clasificador de secciones con OpenAI mediante prompt.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from openai import OpenAI

SECCIONES = ["política", "economía", "deportes", "cultura", "tecnología"]


def get_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")
    return OpenAI(api_key=api_key)


def clasificar_noticia(client: OpenAI, texto: str, model: str | None = None) -> str:
    model_name = model or os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    respuesta = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "Devuelve solo una palabra (política, economía, deportes, cultura "
                    "o tecnología). Si dudas, escoge la más probable."
                ),
            },
            {"role": "user", "content": f"Clasifica esta noticia: {texto}"},
        ],
    )
    contenido = respuesta.choices[0].message.content.strip().lower()
    return contenido.split()[0]


def evaluar_dataset(dataset: List[Tuple[str, str]]) -> Dict[str, float]:
    client = get_client()
    aciertos = 0
    for texto, seccion_real in dataset:
        pred = clasificar_noticia(client, texto)
        ok = pred == seccion_real
        aciertos += int(ok)
        estado = "✅" if ok else "❌"
        print(f"{estado} [{seccion_real}] → {pred} :: {texto}")
    return {"precision": aciertos / len(dataset)}


if __name__ == "__main__":
    dataset_demo = [
        (
            "El presidente anuncia una reforma constitucional para ampliar derechos sociales.",
            "política",
        ),
        (
            "La bolsa española cierra con subidas gracias al empuje del sector bancario.",
            "economía",
        ),
        ("El Barça remonta en el último minuto y se clasifica para la final.", "deportes"),
        ("La Filarmónica presenta una temporada dedicada a compositores latinoamericanos.", "cultura"),
        (
            "Una startup española lanza un chip cuántico diseñado para mejorar la IA generativa.",
            "tecnología",
        ),
    ]
    metricas = evaluar_dataset(dataset_demo)
    print(f"\nPrecisión media: {metricas['precision']:.2%}")

