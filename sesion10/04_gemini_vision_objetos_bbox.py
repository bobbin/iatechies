"""
Ejercicio 04 — Gemini Vision: objetos + bounding boxes aproximadas (JSON).

Uso:
  python sesion10/04_gemini_vision_objetos_bbox.py ruta/a/imagen.jpg
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
        "Analiza la imagen. Devuelve SOLO un JSON con esta forma:\n"
        "{\n"
        '  "objetos": [\n'
        "    {\n"
        '      "label": string,\n'
        '      "confidence": number,\n'
        '      "bbox": {"x": number, "y": number, "w": number, "h": number}\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Reglas:\n"
        "- bbox normalizada 0..1 respecto a ancho/alto.\n"
        "- x,y es la esquina superior izquierda.\n"
        "- Incluye 5 a 12 objetos máximos, prioriza los más relevantes.\n"
        "- Si dudas, baja confidence; no inventes objetos.\n"
        "- Sin explicaciones, SOLO JSON.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image_path",
        nargs="?",
        default=default_image_path("escena.jpg"),
        help="Ruta a la imagen. Si no se indica, usa una imagen de ejemplo.",
    )
    args = parser.parse_args()

    load_env()
    api_key = require_env("GOOGLE_API_KEY")
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    resp = model.generate_content(
        [build_prompt(), to_gemini_part(args.image_path)],
        request_options={"timeout": 90},
    )

    raw = (resp.text or "").strip()
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


