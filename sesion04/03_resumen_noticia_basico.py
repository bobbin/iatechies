"""
Ejercicio 03 — Resumen de noticia con prompt débil vs estructurado.

Objetivo: ver cómo cambia el resultado cuando forzamos tono, formato y nivel de detalle.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Resume este texto.
[noticia]"""

PROMPT_BUENO = """Eres un redactor de un diario generalista en España.

Tarea:
Resume la siguiente noticia para un lector no experto.

Instrucciones:
- Escribe en español.
- Usa un tono neutro e informativo.
- Resume en exactamente 3 viñetas.
- No añadas información que no aparezca en el texto.

TEXTO:
[noticia]

Responde SOLO con las 3 viñetas."""

DEMO_DATA = {
    "noticia": (
        "El Ayuntamiento de Madrid ha aprobado un plan para ampliar un 30% las zonas verdes de la ciudad en los "
        "próximos cinco años. El proyecto incluye la plantación de 200.000 nuevos árboles y la creación de 15 parques "
        "de barrio, con una inversión de 120 millones de euros."
    )
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt malo")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt bueno (avisad cuando queráis lanzarlo)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

