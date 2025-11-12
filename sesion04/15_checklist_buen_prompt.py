"""
Ejercicio 15 — Checklist de buen prompt.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_SIN_CHECKLIST = """Explica esto:

[texto]"""

PROMPT_CON_CHECKLIST = """Eres un divulgador científico.

Tarea:
Explicar el contenido del siguiente texto a un público general.

Instrucciones:
- Escribe en español.
- Máximo 4 frases.
- Tono claro y cercano, sin jerga técnica.
- No inventes información que no esté en el texto.

Formato de salida:
Un único párrafo de 3–4 frases.

Texto:
[texto]"""

DEMO_DATA = {
    "texto": (
        "El telescopio espacial Kepler identificó más de 2.600 planetas fuera del Sistema Solar, "
        "lo que demuestra que las estrellas con sistemas planetarios son comunes en la Vía Láctea."
    )
}


def main() -> None:
    prompt_simple = fill_placeholders(PROMPT_SIN_CHECKLIST, DEMO_DATA)
    pretty_print("Prompt sin checklist")
    print(prompt_simple)
    try:
        respuesta_simple = run_prompt(prompt_simple)
    except Exception as exc:  # noqa: BLE001
        respuesta_simple = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_simple)

    pretty_print("Prompt usando checklist (activar cuando toque)")
    # prompt_checklist = fill_placeholders(PROMPT_CON_CHECKLIST, DEMO_DATA)
    # respuesta_checklist = run_prompt(prompt_checklist)
    # print(respuesta_checklist)


if __name__ == "__main__":
    main()

