"""
Ejercicio 07 — Chain-of-Thought ligero.

Objetivo: obligar al modelo a razonar en pasos antes de entregar la conclusión.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Explica el impacto de esta medida económica:
[texto]"""

PROMPT_BUENO = """Eres un analista económico que explica medidas a lectores no expertos.

Tarea:
Analiza la siguiente medida en 3 pasos:

1) Qué hace la medida (3 viñetas).
2) Efectos posibles a corto plazo (3 viñetas).
3) Efectos posibles a medio plazo (3 viñetas).

Medida descrita en la noticia:
[texto]

Responde siguiendo exactamente esta estructura:

1) Qué hace la medida:
- ...
- ...
- ...

2) Efectos posibles a corto plazo:
- ...
- ...
- ...

3) Efectos posibles a medio plazo:
- ...
- ...
- ..."""

DEMO_DATA = {
    "texto": (
        "El Gobierno anuncia una rebaja temporal del IVA de la electricidad al 5% durante seis meses "
        "para contener la factura de los hogares."
    )
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt sin estructura")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt con Chain-of-Thought (descomentar para usar)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

