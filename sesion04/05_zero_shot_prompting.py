"""
Ejercicio 05 — Zero-shot prompting para corrección de estilo.

Objetivo: demostrar cómo un prompt sin contexto produce resultados erráticos frente a otro con rol, tarea e instrucciones.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Corrige este texto:

[texto]"""

PROMPT_BUENO = """Actúa como corrector de estilo.

Tarea:
Reescribe el siguiente texto en español.

Instrucciones:
- Respeta el contenido factual.
- Mejora la claridad y la puntuación.
- Mantén el tono informal.
- No cambies el idioma.

Texto:
[texto]"""

DEMO_DATA = {
    "texto": (
        "ayer fuimos al evento de energia solar y, la verdad, moló bastante aunque habia partes "
        "que no entendi porque iban muy deprisa."
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

    pretty_print("Prompt bueno (actívalo cuando quieras comparar)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

