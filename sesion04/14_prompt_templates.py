"""
Ejercicio 14 — Prompt templates V1 vs V2.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_V1 = """PROMPT_RESUMEN_NOTICIA_V1

Eres un redactor.

Tarea:
Resume la siguiente noticia.

Texto:
[noticia]"""

PROMPT_V2 = """PROMPT_RESUMEN_NOTICIA_V2

Eres un redactor de un diario generalista en España.

Tarea:
Resume la siguiente noticia para un lector no experto.

Instrucciones:
- Escribe en español.
- Tono neutro e informativo.
- Usa exactamente 3 viñetas.
- No añadas información que no aparezca en el texto.

Texto:
[noticia]

Responde SOLO con las 3 viñetas."""

DEMO_DATA = {
    "noticia": (
        "La compañía AeroGreen lanzará una flota de taxis aéreos eléctricos en 2027, tras recibir autorización "
        "de la Agencia Estatal de Seguridad Aérea. El proyecto comenzará en Madrid y Barcelona."
    )
}


def main() -> None:
    prompt_v1 = fill_placeholders(PROMPT_V1, DEMO_DATA)
    pretty_print("Template V1")
    print(prompt_v1)
    try:
        respuesta_v1 = run_prompt(prompt_v1)
    except Exception as exc:  # noqa: BLE001
        respuesta_v1 = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_v1)

    pretty_print("Template V2 (activar para comparar)")
    # prompt_v2 = fill_placeholders(PROMPT_V2, DEMO_DATA)
    # respuesta_v2 = run_prompt(prompt_v2)
    # print(respuesta_v2)


if __name__ == "__main__":
    main()

