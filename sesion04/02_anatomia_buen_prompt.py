"""
Ejercicio 02 — Anatomía de un buen prompt.

Objetivo: pasar de una instrucción ambigua a una estructura completa que guíe tono, formato y tarea.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Haz algo útil con este texto, por favor:
[texto]"""

PROMPT_BUENO = """Eres un redactor de un medio digital en España.

Tu tarea:
A partir del siguiente texto, genera una entradilla clara para acompañar el titular.

Instrucciones:
- Escribe en español.
- Máximo 2 frases.
- Tono neutro e informativo.
- No añadas opiniones ni adjetivos innecesarios.

Devuelve la respuesta en este formato:
[ENTRADILLA]: <tu texto aquí>

Texto:
[texto]"""

DEMO_DATA = {
    "texto": (
        "La startup SolarWind ha anunciado una inversión de 50 millones de euros para ampliar "
        "sus plantas solares en Andalucía, con el objetivo de duplicar la producción en dos años."
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

    pretty_print("Prompt bueno (descoméntalo para probar la mejora)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

