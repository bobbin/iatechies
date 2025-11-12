"""
Ejercicio 10 — Anti-hallucination.

Objetivo: enseñar a los modelos a reconocer cuándo deben responder "NO LO SÉ".
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Responde a esta pregunta sobre el texto. Si no lo sabes, invéntatelo un poco:

TEXTO:
[texto]

PREGUNTA:
[pregunta]"""

PROMPT_BUENO = """Eres un asistente para periodistas.

Instrucciones IMPORTANTES:
- Solo puedes usar el TEXTO como fuente.
- Si la respuesta no está claramente en el texto, responde EXACTAMENTE: "NO LO SÉ".

TEXTO:
[texto]

PREGUNTA:
[pregunta]

Responde:
- Una frase con la respuesta, si está en el texto.
- O exactamente "NO LO SÉ" si el texto no contiene la respuesta."""

DEMO_DATA = {
    "texto": (
        "La empresa OceanClean desplegará 15 barcos recolectores de plástico en el Mediterráneo durante 2026, "
        "priorizando las zonas costeras de España e Italia."
    ),
    "pregunta": "¿Cuántos barcos planea desplegar OceanClean en el Atlántico?"
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt sin salvaguardas")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt con política anti-alucinaciones (actívalo cuando toque)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

