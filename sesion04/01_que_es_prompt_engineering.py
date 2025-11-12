"""
Ejercicio 01 — Qué es de verdad el Prompt Engineering.

Objetivo: mostrar cómo cambia la respuesta cuando aportamos contexto, rol e instrucciones claras.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = "Explícame qué es la inflación."

PROMPT_BUENO = """Eres un editor de economía que explica conceptos complejos a lectores no expertos.

Tarea:
Explica qué es la inflación de forma clara en español.

Instrucciones:
- Usa un tono neutro e informativo.
- Imagina que escribes para un lector de un diario generalista.
- Usa como máximo 3 frases.

Explica qué es la inflación."""

DEMO_DATA = {
    "texto": (
        "La inflación es el aumento generalizado de los precios de bienes y servicios "
        "durante un periodo de tiempo. Cuando la inflación sube, el poder adquisitivo de la moneda baja."
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
    # Descomenta las líneas siguientes para lanzar la versión buena y comparar.
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

