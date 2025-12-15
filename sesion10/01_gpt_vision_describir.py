"""
Ejercicio 01 — GPT Vision: describir imagen + tags + alt-text (JSON).

Uso:
  python sesion10/01_gpt_vision_describir.py ruta/a/imagen.jpg
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from openai import OpenAI

from _common import load_env, require_env, to_data_url
from _json_utils import dump_pretty, extract_first_json_object


def default_image_path() -> str:
    """
    Devuelve una ruta por defecto para demos:
    - `sesion10/inputs/ejemplo.jpg` si existe
    - si no, `sesion01/ejemplo.jpg`
    """
    here = Path(__file__).resolve().parent
    candidate = here / "inputs" / "ejemplo.jpg"
    if candidate.exists():
        return str(candidate)
    candidate = here.parent / "sesion01" / "ejemplo.jpg"
    return str(candidate)


def build_prompt() -> str:
    return (
        "Analiza la imagen y devuelve SOLO un JSON con estas claves:\n"
        "- descripcion: string (2-4 frases)\n"
        "- tags: array de 5 a 12 strings (sin #, sin duplicados)\n"
        "- alt_text: string (máx 120 caracteres, accesible, sin relleno)\n\n"
        "Reglas:\n"
        "- No inventes texto si no se ve; si no puedes leer algo, ponlo como null.\n"
        "- No incluyas explicaciones, SOLO JSON.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image_path",
        nargs="?",
        default=default_image_path(),
        help="Ruta a la imagen (jpg/png/webp...). Si no se indica, usa una imagen de ejemplo.",
    )
    args = parser.parse_args()

    load_env()
    api_key = require_env("OPENAI_API_KEY")
    model = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")

    client = OpenAI(api_key=api_key)
    data_url = to_data_url(args.image_path)

    resp = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": build_prompt()},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
    )

    raw = resp.output_text or ""
    obj = extract_first_json_object(raw)
    print(dump_pretty(obj))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


