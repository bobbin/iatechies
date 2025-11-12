"""
Utilidades compartidas para los ejercicios de la sesión 04 sobre prompt engineering.

Estas funciones ofrecen:
- `run_prompt`: enviar un prompt a un servidor Ollama (por defecto `http://localhost:11434`).
- `pretty_print`: mostrar títulos bonitos en consola.
- `fill_placeholders`: sustituir marcadores como `[texto]` o `[noticia]` por el material que queramos usar en clase.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")

DEFAULT_REPLACEMENTS: Dict[str, str] = {
    "texto": "Pega aquí el texto que quieras usar en la demostración.",
    "noticia": "Pega aquí la noticia que vais a resumir.",
    "pregunta": "Escribe aquí la pregunta concreta que quieras lanzar.",
    "fragmentos": "Añade aquí los fragmentos/localidades del contexto.",
    "resumen": "Incluye aquí el resumen generado por la IA.",
    "artículo": "Copia aquí el artículo completo.",
    "medida": "Describe aquí la medida económica.",
}


def run_prompt(prompt: str, *, model: str | None = None, options: Dict[str, Any] | None = None) -> str:
    """
    Envía `prompt` a Ollama y devuelve el texto de respuesta.

    Los alumnos pueden cambiar `DEFAULT_MODEL` o pasar un `model` explícito al llamar.
    Si queréis usar otro backend, sustituid esta función por la llamada correspondiente.
    """
    payload: Dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    if options:
        payload["options"] = options

    response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()


def pretty_print(title: str) -> None:
    """Imprime un separador con título para que las demos sean más legibles."""
    separator = "═" * len(title)
    print(f"\n{title}\n{separator}")


def fill_placeholders(template: str, extra_replacements: Dict[str, str] | None = None) -> str:
    """
    Sustituye marcadores como `[texto]`, `[noticia]`, etc., por los valores indicados.

    Deja los marcadores sin tocar si no encontramos sustituto, para recordar al alumno
    que hace falta personalizarlos durante la práctica.
    """
    replacements = DEFAULT_REPLACEMENTS.copy()
    if extra_replacements:
        replacements.update(extra_replacements)

    prompt = template
    for key, value in replacements.items():
        prompt = prompt.replace(f"[{key}]", value)
        prompt = prompt.replace(f"<{key}>", value)

    return prompt


__all__ = ["run_prompt", "pretty_print", "fill_placeholders", "DEFAULT_REPLACEMENTS"]

