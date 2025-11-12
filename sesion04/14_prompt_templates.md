# Slide 14 — Prompt templates (concepto)

## Versión V1 (más floja)
```
PROMPT_RESUMEN_NOTICIA_V1

Eres un redactor.

Tarea:
Resume la siguiente noticia.

Texto:
[noticia]
```

## Versión V2 (mejorada)
```
PROMPT_RESUMEN_NOTICIA_V2

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

Responde SOLO con las 3 viñetas.
```

