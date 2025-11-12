"""
Ejercicio 12 — Prompt crítico: la IA revisa a la IA.
"""

from __future__ import annotations

from common import fill_placeholders, pretty_print, run_prompt

PROMPT_MALO = """¿Está bien este resumen?

Texto:
[texto]

Resumen:
[resumen]"""

PROMPT_BUENO = """Actúas como revisor crítico de resúmenes de noticias.

TAREA:
1. Lee el TEXTO ORIGINAL.
2. Lee el RESUMEN.
3. Indica:
   - 2 aciertos del resumen.
   - 2 posibles problemas (errores, invenciones o información importante que falta).

Responde en este formato:

Aciertos:
- ...
- ...

Posibles problemas:
- ...
- ...

TEXTO ORIGINAL:
[texto]

RESUMEN:
[resumen]"""

DEMO_DATA = {
    "texto": (
        "El Banco Central Europeo decidió mantener los tipos de interés en el 4,5% a pesar de la desaceleración "
        "económica en varios países miembros. El organismo argumenta que la inflación sigue por encima del objetivo."
    ),
    "resumen": "El BCE bajó los tipos por la caída de la inflación y dijo que estudia nuevos estímulos.",
}


def main() -> None:
    prompt_malo = fill_placeholders(PROMPT_MALO, DEMO_DATA)
    pretty_print("Prompt sin guía crítica")
    print(prompt_malo)
    try:
        respuesta_mala = run_prompt(prompt_malo)
    except Exception as exc:  # noqa: BLE001
        respuesta_mala = f"[Error al llamar al modelo: {exc}]"
    print(respuesta_mala)

    pretty_print("Prompt crítico (activar al comparar)")
    # prompt_bueno = fill_placeholders(PROMPT_BUENO, DEMO_DATA)
    # respuesta_buena = run_prompt(prompt_bueno)
    # print(respuesta_buena)


if __name__ == "__main__":
    main()

