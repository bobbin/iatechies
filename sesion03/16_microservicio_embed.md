# Ejercicio 16 — Endpoint `/embed` unificado

## Objetivo

Añadir un endpoint `POST /embed` al microservicio multi-backend que genere embeddings usando el proveedor indicado y devuelva metadatos comunes.

## Conceptos clave

- **Embeddings multi-backend:** misma interfaz, distintos proveedores.
- **Respuesta compacta:** opcionalmente devolver hash o longitud para no saturar la respuesta.
- **Preparación para RAG:** endpoint listo para indexar texto en bases vectoriales.

## Pasos

1. Ejecuta `python sesion03/16_microservicio_embed.py`.
2. Envía un JSON con `{"backend": "openai", "texts": [...]}` y observa la respuesta. Desde PowerShell o Git Bash puedes probarlo con:

   ```powershell
   curl -X POST http://localhost:8002/embed -H "Content-Type: application/json" -d "{\"backend\":\"openai\",\"texts\":[\"Titular de ejemplo uno\",\"Titular de ejemplo dos\"]}"
   ```

3. Cambia a `hf` u `ollama` (si tienes modelo local de embeddings) para comparar dimensiones.
4. Ajusta la respuesta para incluir vector completo, hash o sólo estadísticas.

## Ideas de extensión

- Incorporar normalización de vectores y guardado automático en una base vectorial.
- Implementar control de versiones de embeddings (modelo + fecha).
- Añadir autenticación o rate limiting por backend para evitar abuso.

