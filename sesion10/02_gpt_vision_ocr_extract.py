"""
Ejercicio 02 — GPT Vision: OCR aproximado + extracción estructurada (ticket/factura).

Uso:
  python sesion10/02_gpt_vision_ocr_extract.py ruta/a/ticket.jpg
"""

from __future__ import annotations

import argparse
import os

from openai import OpenAI

from _common import default_image_path, load_env, require_env, to_data_url
from _json_utils import dump_pretty, extract_first_json_object


def build_prompt() -> str:
    return (
        "Eres un extractor de datos de tickets/facturas a partir de imagen.\n"
        "Devuelve SOLO un JSON con este esquema:\n"
        "{\n"
        '  "comercio": string|null,\n'
        '  "fecha": string|null,  // ISO 8601 si es posible\n'
        '  "moneda": string|null, // p.ej. EUR\n'
        '  "total": number|null,\n'
        '  "items": [\n'
        '    {"descripcion": string, "importe": number|null}\n'
        "  ],\n"
        '  "texto_ocr": string  // transcripción aproximada del texto visible\n'
        "}\n\n"
        "Reglas:\n"
        "- Si un dato no se ve con claridad, usa null.\n"
        "- No inventes productos ni importes.\n"
        "- Mantén items vacíos si no se distinguen.\n"
        "- Sin explicaciones, SOLO JSON.\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image_path",
        nargs="?",
        default=default_image_path("ticket.jpg"),
        help="Ruta a la imagen del ticket/factura. Si no se indica, usa una imagen de ejemplo.",
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


