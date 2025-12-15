from __future__ import annotations

import json


def extract_first_json_object(text: str) -> dict:
    """
    Extrae el primer objeto JSON { ... } que aparezca en un texto.

    Útil cuando el modelo devuelve JSON pero lo envuelve con explicaciones.
    """
    if not text:
        raise ValueError("Texto vacío; no hay JSON que extraer.")

    start = text.find("{")
    if start == -1:
        raise ValueError("No se encontró '{' en la salida; no parece JSON.")

    # Buscamos el primer "}" que cierre un JSON válido, incrementando progresivamente.
    for end in range(len(text), start, -1):
        if text[end - 1] != "}":
            continue
        chunk = text[start:end]
        try:
            obj = json.loads(chunk)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue

    raise ValueError("No se pudo extraer un objeto JSON válido de la salida.")


def dump_pretty(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


