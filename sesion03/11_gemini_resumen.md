# Ejercicio 11 — Resumen de noticia con Gemini

## Objetivo

Conectar con la API de Gemini (Google AI Studio) para pedir un resumen de tres bullet points y medir la latencia de la respuesta.

## Conceptos clave

- **Cliente oficial (`google-generativeai`):** inicialización con `GOOGLE_API_KEY`.
- **Modelos disponibles:** `gemini-1.5-pro`, `gemini-1.5-flash`, etc.
- **Métrica de latencia:** capturar tiempo de ida y vuelta para comparar luego.

## Pasos

1. Configura `GOOGLE_API_KEY` y `DEFAULT_MODEL_GOOGLE`.
2. Ejecuta el script con una noticia de ejemplo.
3. Observa el resumen en formato bullet y la latencia impresa.
4. Cambia de modelo (`pro` vs `flash`) para comparar velocidad y estilo.

## Ideas de extensión

- Añadir `safety_settings` personalizados según las políticas de tu medio.
- Registrar costes estimados combinando tokens y precios de Google.
- Integrar el resumen en Google Docs mediante la API oficial.

