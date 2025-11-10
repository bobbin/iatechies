# Ejercicio 08 — Generación de texto con Hugging Face Inference API

## Objetivo

Llamar a la Inference API de Hugging Face con un modelo open-source (p.ej. Mistral) para resumir una noticia en tres frases.

## Conceptos clave

- **Authorization Bearer:** usar `HF_API_KEY` en la cabecera.
- **Payload estándar:** `inputs`, `parameters`, `options`.
- **Comparativa:** observar estilo y tono respecto a OpenAI.

## Pasos

1. Configura `HF_API_KEY` y `DEFAULT_MODEL_HF` en `.env`.
2. Revisa la función `resumir_noticia_hf` que usa el cliente `OpenAI` apuntando a `https://router.huggingface.co/v1`.
3. Ejecuta el script y modifica la noticia para ver variaciones.
4. Cambia el modelo (por ejemplo `moonshotai/Kimi-K2-Instruct-0905:hf-inference` u otro disponible) para comprobar diferencias de calidad.

## Ideas de extensión

- Serializar respuestas en JSON y guardarlas con marca de tiempo.
- Ajustar parámetros como `max_new_tokens` o `temperature`.
- Manejar errores 503 (modelo cargando) con el cliente de reintentos del ejercicio 02.

