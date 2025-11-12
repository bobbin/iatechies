"""
Ejercicio 18 — Mensaje final.

Objetivo: reutilizar uno de los prompts “buenos” para cerrar la sesión y recordar buenas prácticas.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_FINAL = """Eres un editor de economía que explica conceptos complejos a lectores no expertos.

Tarea:
Explica qué es la inflación de forma clara en español.

Instrucciones:
- Usa un tono neutro e informativo.
- Imagina que escribes para un lector de un diario generalista.
- Usa como máximo 3 frases.

Explica qué es la inflación."""


def main() -> None:
    prompt = fill_placeholders(PROMPT_FINAL, {})
    pretty_print("Prompt ideal para cerrar la sesión")
    print(prompt)
    try:
        respuesta = run_prompt(prompt)
    except Exception as exc:  # noqa: BLE001
        respuesta = f"[Error al llamar al modelo: {exc}]"
    print(respuesta)


if __name__ == "__main__":
    main()

