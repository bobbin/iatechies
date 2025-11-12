"""
Slide extra — Versionado de prompts para detectar frases confusas.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_V1 = """PROMPT_FRASES_CONFUSAS_V1

Señala frases confusas en este texto:

[artículo]"""

PROMPT_V2 = """PROMPT_FRASES_CONFUSAS_V2

Eres un revisor de estilo para un diario generalista.

Tarea:
Detectar frases potencialmente confusas en el siguiente texto.

Instrucciones:
- Marca como confusas frases que sean muy largas, ambiguas o con demasiadas subordinadas.
- Escribe tus resultados en este formato:

Frases confusas:
1. "<frase literal>"
   Motivo: <explicación breve>
2. "<frase literal>"
   Motivo: <explicación breve>

Texto:
[artículo]"""

DEMO_DATA = {
    "artículo": (
        "La compañía anunció que el nuevo sistema, que estará disponible a partir de septiembre, permitirá a los "
        "usuarios gestionar trámites y pagos, aunque todavía no se ha detallado cómo se integrará con los servicios ya existentes."
    )
}


def main() -> None:
    prompt_v1 = fill_placeholders(PROMPT_V1, DEMO_DATA)
    pretty_print("Versión 1")
    print(prompt_v1)
    try:
        respuesta_v1 = run_prompt(prompt_v1)
    except Exception as exc:  # noqa: BLE001
        respuesta_v1 = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_v1)

    pretty_print("Versión 2 (activar para comparar)")
    # prompt_v2 = fill_placeholders(PROMPT_V2, DEMO_DATA)
    # respuesta_v2 = run_prompt(prompt_v2)
    # print(respuesta_v2)


if __name__ == "__main__":
    main()

