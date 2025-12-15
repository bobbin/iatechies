"""
Ejercicio 07 — PDF: extraer datos de una factura (Gemini).

Requisitos:
  - pypdf
  - GOOGLE_API_KEY (y opcional DEFAULT_MODEL_GOOGLE) en sesion10/.env o variables de entorno

Uso:
  python sesion10/07_gemini_pdf_factura_extract.py ruta/a/factura.pdf
  python sesion10/07_gemini_pdf_factura_extract.py   # modo demo: sesion10/inputs/factura.pdf
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import google.generativeai as genai
from pypdf import PdfReader

from _common import load_env, require_env
from _json_utils import dump_pretty, extract_first_json_object


def default_pdf_path() -> str:
    here = Path(__file__).resolve().parent
    return str(here / "inputs" / "factura.pdf")


def extract_text_from_pdf(pdf_path: str | Path, *, max_chars: int = 60_000) -> str:
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        if txt.strip():
            parts.append(f"\n--- PAGE {i} ---\n{txt}")
    text = "\n".join(parts).strip()
    if not text:
        return ""
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[TRUNCATED]"
    return text


def build_prompt(pdf_text: str) -> str:
    return (
        "Eres un extractor de datos de FACTURAS a partir del texto extraído de un PDF.\n"
        "Devuelve SOLO un JSON con este esquema:\n"
        "{\n"
        '  "proveedor": string|null,\n'
        '  "nif_proveedor": string|null,\n'
        '  "cliente": string|null,\n'
        '  "nif_cliente": string|null,\n'
        '  "numero_factura": string|null,\n'
        '  "fecha_emision": string|null,   // ISO 8601 si es posible\n'
        '  "fecha_vencimiento": string|null,\n'
        '  "moneda": string|null,          // p.ej. EUR\n'
        '  "base_imponible": number|null,\n'
        '  "iva": number|null,\n'
        '  "total": number|null,\n'
        '  "items": [\n'
        '    {"descripcion": string, "cantidad": number|null, "precio_unitario": number|null, "importe": number|null}\n'
        "  ]\n"
        "}\n\n"
        "Reglas:\n"
        "- Si un dato no aparece claro, usa null.\n"
        "- No inventes importes ni NIF.\n"
        "- Si hay varios IVAs, pon iva como el total de impuestos si puedes; si no, null.\n"
        "- Sin explicaciones, SOLO JSON.\n\n"
        "Texto del PDF:\n"
        f"{pdf_text}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=default_pdf_path(),
        help="Ruta al PDF de la factura. Si no se indica, usa sesion10/inputs/factura.pdf",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=60_000,
        help="Máximo de caracteres del texto del PDF a enviar al modelo.",
    )
    args = parser.parse_args()

    load_env()
    api_key = require_env("GOOGLE_API_KEY")
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"No existe el PDF: {pdf_path}\n"
            "Coloca uno en sesion10/inputs/factura.pdf o pasa la ruta como argumento."
        )

    pdf_text = extract_text_from_pdf(pdf_path, max_chars=args.max_chars)
    if not pdf_text:
        raise RuntimeError(
            "No se pudo extraer texto del PDF (¿es un PDF escaneado?). "
            "Para escaneados, hay que hacer OCR."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content([build_prompt(pdf_text)], request_options={"timeout": 90})

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


