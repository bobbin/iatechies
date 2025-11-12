# Slide extra — Versionado de prompts

## Versión 1 — Detector de frases confusas (V1)
```
PROMPT_FRASES_CONFUSAS_V1

Señala frases confusas en este texto:

[artículo]
```

## Versión 2 — Detector de frases confusas (V2, mejor)
```
PROMPT_FRASES_CONFUSAS_V2

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
[artículo]
```

## Notas de versión
```
PROMPT_FRASES_CONFUSAS
- V1: sin rol ni formato.
- V2: añade rol, criterios y formato de salida con lista numerada.
```

