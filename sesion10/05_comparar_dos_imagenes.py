"""
Ejercicio 05 — Comparar dos imágenes con OpenAI o Gemini (JSON).

Uso:
  python sesion10/05_comparar_dos_imagenes.py --provider openai a.jpg b.jpg
  python sesion10/05_comparar_dos_imagenes.py --provider gemini a.jpg b.jpg
"""

from __future__ import annotations

import argparse
import json
import os

import google.generativeai as genai
from openai import OpenAI

from _common import default_image_path, load_env, require_env, to_data_url, to_gemini_part
from _json_utils import dump_pretty, extract_first_json_object


def build_prompt() -> str:
    return (
        "Compara las dos imágenes (A y B). Devuelve SOLO un JSON con:\n"
        "{\n"
        '  "resumen": string,\n'
        '  "cambios": [\n'
        "    {\n"
        '      "tipo": "nuevo"|"eliminado"|"modificado"|"desconocido",\n'
        '      "detalle": string,\n'
        '      "zona": {"x": number, "y": number, "w": number, "h": number} | null\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Reglas:\n"
        "- bbox normalizada 0..1 respecto a la imagen donde el cambio es más visible.\n"
        "- Si no puedes ubicar el cambio, usa zona=null.\n"
        "- No inventes texto no visible.\n"
        "- Sin explicaciones, SOLO JSON.\n"
    )


def run_openai(image_a: str, image_b: str) -> dict:
    api_key = require_env("OPENAI_API_KEY")
    model = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    resp = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Imagen A:"},
                    {"type": "input_image", "image_url": to_data_url(image_a)},
                    {"type": "input_text", "text": "Imagen B:"},
                    {"type": "input_image", "image_url": to_data_url(image_b)},
                    {"type": "input_text", "text": build_prompt()},
                ],
            }
        ],
    )
    return extract_first_json_object(resp.output_text or "")


def run_gemini(image_a: str, image_b: str) -> dict:
    api_key = require_env("GOOGLE_API_KEY")
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    resp = model.generate_content(
        [
            "Imagen A:",
            to_gemini_part(image_a),
            "Imagen B:",
            to_gemini_part(image_b),
            build_prompt(),
        ],
        request_options={"timeout": 90},
    )

    raw = (resp.text or "").strip()
    try:
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise ValueError("El JSON devuelto no es un objeto.")
        return obj
    except Exception:
        return extract_first_json_object(raw)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["openai", "gemini"], default="openai")
    parser.add_argument(
        "image_a",
        nargs="?",
        default=default_image_path("a.jpg"),
        help="Ruta imagen A. Si no se indica, usa una imagen de ejemplo.",
    )
    parser.add_argument(
        "image_b",
        nargs="?",
        default=default_image_path("b.jpg"),
        help="Ruta imagen B. Si no se indica, usa una imagen de ejemplo.",
    )
    args = parser.parse_args()

    load_env()

    if args.provider == "openai":
        obj = run_openai(args.image_a, args.image_b)
    else:
        obj = run_gemini(args.image_a, args.image_b)

    print(dump_pretty(obj))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


