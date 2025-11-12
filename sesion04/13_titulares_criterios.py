"""
Ejercicio 13 — Generación de titulares con criterios claros.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Haz un titular mejor para esta noticia:

[texto]"""

PROMPT_BUENO = """Eres editor de titulares de un diario generalista en España.

Tarea:
Proponer 3 titulares alternativos para la siguiente noticia.

Instrucciones:
- Escribe en español.
- Máximo 80 caracteres por titular.
- Tono informativo y sobrio, sin clickbait.
- No repitas el titular original.

TEXTO:
[texto]

Devuelve SOLO una lista numerada del 1 al 3 con los 3 titulares."""

DEMO_DATA = {
    "texto": (
        "El Ministerio de Sanidad ha presentado un plan nacional para reducir las listas de espera quirúrgicas, "
        "destinando 600 millones de euros adicionales y contratando a 4.000 profesionales sanitarios."
    )
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt sin criterios")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt con checklist de criterios (activar cuando toque)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

