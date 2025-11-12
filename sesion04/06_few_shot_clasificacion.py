"""
Ejercicio 06 — Few-shot prompting para clasificación de noticias.

Objetivo: comparar una instrucción zero-shot con una versión enriquecida con ejemplos.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_ZERO_SHOT = """Clasifica la siguiente noticia en una de estas secciones:
["politica", "economia", "deportes", "sociedad", "tecnologia", "cultura"].

Devuelve SOLO el nombre de la sección.

Noticia:
[texto]"""

PROMPT_FEW_SHOT = """Eres un sistema que clasifica noticias en:
["politica", "economia", "deportes", "sociedad", "tecnologia", "cultura"].

Ejemplos:
Noticia: "El Gobierno aprueba una nueva ley educativa."
Sección: "politica"

Noticia: "La inflación sube al 3,2% en la zona euro."
Sección: "economia"

Noticia: "El Barça vence 2-0 en el clásico."
Sección: "deportes"

Ahora clasifica esta noticia:
[texto]

Responde SOLO con una de las secciones de la lista."""

DEMO_DATA = {
    "texto": (
        "La cadena de supermercados EcoMarket ha anunciado la implantación de sistemas de pago sin cajeros en 30 "
        "tiendas de España durante 2026."
    )
}


def main() -> None:
    prompt_zero = fill_placeholders(PROMPT_ZERO_SHOT, DEMO_DATA)
    pretty_print("Prompt zero-shot")
    print(prompt_zero)
    try:
        respuesta_zero = run_prompt(prompt_zero)
    except Exception as exc:  # noqa: BLE001
        respuesta_zero = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_zero)

    pretty_print("Prompt few-shot (actívalo cuando toque)")
    # prompt_few = fill_placeholders(PROMPT_FEW_SHOT, DEMO_DATA)
    # respuesta_few = run_prompt(prompt_few)
    # print(respuesta_few)


if __name__ == "__main__":
    main()

