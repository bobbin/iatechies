"""
Ejercicio 08 — Comparar razonamiento estructurado frente a una petición vaga.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_SIN_ESTRUCTURA = """¿Esta medida es buena o mala para la economía? Explícalo:
[texto]"""

PROMPT_CON_ESTRUCTURA = """Eres un analista económico neutral.

Tarea:
Evaluar una medida sin tomar posición política.

Instrucciones:
1) Explica en 2 viñetas los posibles efectos positivos.
2) Explica en 2 viñetas los posibles efectos negativos.
3) Termina con una frase final explicando qué información adicional haría falta para evaluarla mejor.

Medida descrita en la noticia:
[texto]

Responde exactamente con esa estructura."""

DEMO_DATA = {
    "texto": (
        "El Ministerio de Industria propone subvencionar el 40% de la inversión inicial de las pymes que adopten "
        "energías renovables en sus instalaciones."
    )
}


def main() -> None:
    prompt_simple = fill_placeholders(PROMPT_SIN_ESTRUCTURA, DEMO_DATA)
    pretty_print("Prompt sin estructura")
    print(prompt_simple)
    try:
        respuesta_simple = run_prompt(prompt_simple)
    except Exception as exc:  # noqa: BLE001
        respuesta_simple = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_simple)

    pretty_print("Prompt con estructura (actívalo cuando toque)")
    # prompt_cot = fill_placeholders(PROMPT_CON_ESTRUCTURA, DEMO_DATA)
    # respuesta_cot = run_prompt(prompt_cot)
    # print(respuesta_cot)


if __name__ == "__main__":
    main()

