# Ejercicio 02 — Primeras llamadas HTTP a OpenAI y Hugging Face

## Objetivo

Enviar la primera petición real a OpenAI (`/v1/chat/completions`) y a la Inference API de Hugging Face usando `requests`, sin depender de los SDK oficiales, para comprender la estructura cruda de cada API.

## Conceptos clave

- **Autenticación con Bearer token:** cabeceras `Authorization` obligatorias.
- **Payloads mínimos:** qué campos son imprescindibles en cada caso (`model`, `messages`, `inputs`, `parameters`).
- **Latencia básica:** medir el tiempo de ida y vuelta de cada servicio.

## Pasos

1. Asegúrate de haber pasado el sanity check del ejercicio 01 (claves válidas).
2. Ejecuta `python sesion03/02_timeout_reintentos.py`.
3. Observa cómo el script imprime la respuesta de OpenAI y Hugging Face junto con la latencia (Hugging Face se llama contra el nuevo router `hf-inference` lanzando una generación rápida de texto).
4. Modifica el `prompt` o los parámetros (`temperature`, `max_new_tokens`) para experimentar.

## Ideas de extensión

- Añadir Gemini usando `requests` (requiere firmar la petición con la misma cabecera `x-goog-api-key`).
- Integrar el cliente de reintentos del ejercicio 02 original si prevés errores 429.
- Guardar las respuestas en un archivo JSON para inspeccionarlas con herramientas externas.

