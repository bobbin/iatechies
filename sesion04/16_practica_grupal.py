"""
Ejercicio 16 — Caso de práctica grupal.

Objetivo: partir de un prompt deficiente y, en equipo, transformarlo siguiendo la checklist.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_BASE = """Haz algo útil con esta noticia. Saca info y cosas interesantes:

[noticia]"""

# Deja este diccionario preparado para que cada grupo lo adapte a su caso de uso.
DEMO_DATA = {
    "noticia": (
        "La universidad pública ha creado una oficina de inteligencia artificial para apoyar proyectos docentes "
        "y de investigación, con un presupuesto inicial de 5 millones de euros."
    )
}


def main() -> None:
    prompt_cutre = fill_placeholders(PROMPT_BASE, DEMO_DATA)
    pretty_print("Prompt base (cutre)")
    print(prompt_cutre)
    try:
        respuesta_cutre = run_prompt(prompt_cutre)
    except Exception as exc:  # noqa: BLE001
        respuesta_cutre = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_cutre)

    pretty_print("Espacio para vuestro prompt PRO")
    print("👉 Cread vuestra versión aplicando rol, tarea, checklist y formato deseado.")
    # Cuando el grupo tenga su prompt mejorado, sustituid `prompt_pro` por esa cadena.
    # prompt_pro = "... vuestra versión ..."
    # respuesta_pro = run_prompt(prompt_pro)
    # print(respuesta_pro)


if __name__ == "__main__":
    main()

