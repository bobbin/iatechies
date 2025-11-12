"""
Ejercicio 09 — Forzar una salida estructurada en JSON.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """Saca los datos clave de esta noticia:
[texto]"""

PROMPT_BUENO = """Eres un asistente que extrae información de noticias.

Tarea:
Devuelve un JSON con estas claves:
- "titulo": string
- "tema_principal": string
- "personas_clave": lista de strings
- "lugar_principal": string o null

Instrucciones:
- Usa solo información presente en el texto.
- Si no conoces un campo, usa null.
- NO añadas texto fuera del JSON.

Noticia:
[texto]

Responde SOLO con el JSON."""

DEMO_DATA = {
    "texto": (
        "La empresa BioHealth inauguró un nuevo laboratorio en Barcelona dedicado a vacunas de ARN. "
        "La directora general, Laura Méndez, explicó que el centro generará 200 empleos especializados."
    )
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt sin formato")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt con formato JSON (actívalo cuando quieras)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

