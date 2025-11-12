# Slide 17 — Por qué importa para el resto del curso

## Prompt malo en RAG
```
Aquí tienes texto de contexto y la pregunta. Responde:

Contexto:
[fragmentos]

Pregunta:
[pregunta]
```

## Prompt un poco mejor en RAG
```
Eres un asistente que responde preguntas usando SOLO el contexto proporcionado.

Instrucciones:
- Si el contexto no contiene la respuesta, responde: "NO LO SÉ".
- No uses conocimiento externo.

Contexto:
[fragmentos]

Pregunta:
[pregunta]

Responde en 2–3 frases, citando las partes relevantes del contexto.
```

