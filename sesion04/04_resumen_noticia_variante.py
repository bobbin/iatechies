"""
Ejercicio 04 — Comparar una variante todavía más débil contra el prompt robusto.

Objetivo: mostrar el contraste entre una petición vaga y el mismo prompt estructurado del ejercicio anterior.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MUY_MALO = """Resume esto rápido y hazlo bien:
[noticia]"""

PROMPT_ROBUSTO = """Eres un redactor de un diario generalista en España.

Tarea:
Resume la siguiente noticia para un lector no experto.

Instrucciones:
- Escribe en español.
- Usa un tono neutro e informativo.
- Resume en exactamente 3 viñetas.
- No añadas información que no aparezca en el texto.

TEXTO:
[noticia]

Responde SOLO con las 3 viñetas."""

DEMO_DATA = {
    "noticia": (
        "La Unión Europea ha acordado un fondo de 10.000 millones de euros para impulsar la fabricación de baterías "
        "eléctricas. El objetivo es reducir la dependencia de proveedores asiáticos y acelerar la transición hacia el "
        "vehículo eléctrico."
    )
}


def main() -> None:
    prompt_muy_malo = fill_placeholders(PROMPT_MUY_MALO, DEMO_DATA)
    pretty_print("Prompt muy malo")
    print(prompt_muy_malo)
    try:
        respuesta_muy_mala = run_prompt(prompt_muy_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_muy_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_muy_mala)

    pretty_print("Prompt robusto (lanza cuando quieras comparar)")
    # prompt_robusto = fill_placeholders(PROMPT_ROBUSTO, DEMO_DATA)
    # respuesta_robusta = run_prompt(prompt_robusto)
    # print(respuesta_robusta)


if __name__ == "__main__":
    main()

