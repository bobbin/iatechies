"""
Ejercicio 17 — Prompts para RAG: por qué importa afinar las instrucciones.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Aquí tienes texto de contexto y la pregunta. Responde:

Contexto:
[fragmentos]

Pregunta:
[pregunta]"""

PROMPT_MEJOR = """Eres un asistente que responde preguntas usando SOLO el contexto proporcionado.

Instrucciones:
- Si el contexto no contiene la respuesta, responde: "NO LO SÉ".
- No uses conocimiento externo.

Contexto:
[fragmentos]

Pregunta:
[pregunta]

Responde en 2–3 frases, citando las partes relevantes del contexto."""

DEMO_DATA = {
    "fragmentos": (
        "Fragmento 1: El Plan Solar 2030 prevé instalar 5 GW adicionales de potencia en tejados industriales.\n"
        "Fragmento 2: Las ayudas cubren hasta el 35% de la inversión inicial para pymes manufactureras."
    ),
    "pregunta": "¿Qué apoyo económico reciben las pymes manufactureras en el Plan Solar 2030?"
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt RAG sin salvaguardas")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt RAG mejorado (activar para comparar)")
    # prompt_mejor = fill_placeholders(PROMPT_MEJOR, DEMO_DATA)
    # respuesta_mejor = run_prompt(prompt_mejor)
    # print(respuesta_mejor)


if __name__ == "__main__":
    main()

