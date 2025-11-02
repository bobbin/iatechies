# Teoría y explicación: Streaming de tokens

Este ejercicio enseña a consumir el endpoint `/api/generate` en modo `stream` para procesar tokens a medida que Ollama los produce.

## Objetivo didáctico
* Mostrar cómo decodificar los fragmentos JSON progresivos que envía Ollama.
* Enseñar a detectar el chunk final (`done=True`) para recoger métricas como `total_tokens`.
* Ilustrar un CLI minimalista que imprime la respuesta sin esperar al final.

## Ideas clave para el alumno
* "Activar `stream=True` reduce la latencia percibida del usuario".
* "Cada línea JSON puede traer campos distintos: texto parcial, conteo de tokens o motivos de parada".
* "En entornos cloud debes añadir el header `Authorization: Bearer ...` para autenticarte".
