# Sesión 03 — APIs multi-backend

Esta sesión introduce un patrón común para trabajar con múltiples proveedores de LLM (OpenAI, Hugging Face y Google Gemini) y construye los componentes necesarios para acabar con un microservicio observable y listo para producción.

## Qué encontrarás

- **Bloque B:** Abstracciones básicas, timeouts, reintentos y configuración desde `.env`.
- **Bloque C:** Casos prácticos con la API de OpenAI (chat, temperatura, embeddings y clasificación).
- **Bloque D:** Ejemplos equivalentes usando la Hugging Face Inference API.
- **Bloque E:** Integraciones con Google Gemini, incluido un vistazo a capacidades multimodales.
- **Bloque F:** Construcción incremental de un microservicio `/chat` y `/embed` multi-backend.
- **Bloque G:** Métricas, benchmarking y cálculo de costes para tomar decisiones informadas.

Cada ejercicio cuenta con un archivo `.md` (contexto teórico y guía) y un `.py` (código de referencia). Ajusta los nombres de modelos y claves en `.env` antes de ejecutar.

## Dependencias

Revisa `requirements.txt` para instalar librerías de cliente (`openai`, `google-generativeai`, etc.) y utilidades comunes (`httpx`, `python-dotenv`, `fastapi`). Ejecuta:

```
pip install -r requirements.txt
```

## Recomendaciones

- Copia `.env.example` a `.env` y completa tus claves y modelos antes de lanzar los scripts.
- Activa entornos virtuales separados para cada bloque si quieres evitar dependencias innecesarias.
- Usa los scripts como base para pruebas automatizadas o demos en directo.

¡Disfruta la sesión y adapta los ejercicios a los flujos de tu redacción! 

