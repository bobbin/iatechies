"""
Ejercicio 03 — Gemini Vision: alt-text + pie de foto (JSON).

Uso:
  python sesion10/03_gemini_vision_alt_caption.py ruta/a/imagen.jpg
"""

from __future__ import annotations

import argparse
import json
import os

import google.generativeai as genai

from _common import default_image_path, load_env, require_env, to_gemini_part
from _json_utils import dump_pretty, extract_first_json_object


def build_prompt() -> str:
    return (
        "Eres un editor digital.\n"
        "Devuelve SOLO un JSON con:\n"
        "- alt_text: string (máx 120 caracteres, accesible)\n"
        "- pie_foto: string (máx 180 caracteres, informativo)\n"
        "Sin explicaciones, SOLO JSON.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image_path",
        nargs="?",
        default=default_image_path("ejemplo.jpg"),
        help="Ruta a la imagen. Si no se indica, usa una imagen de ejemplo.",
    )
    args = parser.parse_args()

    load_env()
    api_key = require_env("GOOGLE_API_KEY")
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    image_part = to_gemini_part(args.image_path)
    resp = model.generate_content(
        [
            build_prompt(),
            image_part,
        ],
        request_options={"timeout": 60},
    )

    raw = (resp.text or "").strip()
    # Gemini a veces devuelve JSON válido o texto con JSON dentro.
    try:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise ValueError("El JSON devuelto no es un objeto.")
    except Exception:
        obj = extract_first_json_object(raw)

    print(dump_pretty(obj))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


