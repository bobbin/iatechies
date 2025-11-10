# Ejercicio 07 — Clasificador de secciones vía prompt

## Objetivo

Usar la API de chat de OpenAI para clasificar noticias en secciones (`política`, `economía`, `deportes`, `cultura`, `tecnología`) sin entrenar un modelo propio.

## Conceptos clave

- **Clasificación con prompt:** aprovechar un LLM generalista para etiquetar.
- **Salida controlada:** pedir explícitamente “devuelve solo una palabra”.
- **Batch pequeño:** enviar varias noticias en un bucle y observar consistencia.

## Pasos

1. Define una lista de noticias de prueba con su sección esperada.
2. Ejecuta el script y revisa qué sección se predice para cada texto.
3. Calcula la tasa de acierto simple impresa al final.
4. Ajusta el prompt si necesitas más control o un formato de salida distinto.

## Ideas de extensión

- Añadir más secciones o transformar la respuesta a un `enum`.
- Enviar un `few-shot` con dos ejemplos de clasificación correctos.
- Medir coste aproximado multiplicando tokens por precio del modelo.

