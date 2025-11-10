# Ejercicio 10 — Embeddings con modelo OSS (Hugging Face) y búsqueda semántica

## Objetivo

Generar embeddings con un modelo open-source alojado en Hugging Face y realizar una búsqueda de titulares similares.

## Conceptos clave

- **Embeddings en HF:** mismos conceptos que en OpenAI, distinto proveedor.
- **Normalización:** convertir la lista de vectores en `numpy` para cálculos.
- **Top-K semántico:** usar similitud coseno para recuperar titulares relacionados.

## Pasos

1. Selecciona un modelo de embeddings disponible en `hf-inference` en `.env` (`DEFAULT_MODEL_EMBEDDINGS_HF`, por ejemplo `sentence-transformers/all-MiniLM-L6-v2`).
2. Ejecuta el script para indexar un pequeño set de titulares.
3. Introduce un titular de consulta y observa los resultados ordenados por similitud (usamos `InferenceClient.feature_extraction` desde `huggingface_hub`).
4. Compara las puntuaciones con las del ejercicio 06 (OpenAI).

## Ideas de extensión

- Calcular cobertura cruzada: ¿qué titulares aparecen en ambos top 3?
- Guardar los embeddings en un archivo `.npz` para reutilizarlos.
- Integrarlo con un motor de búsqueda simple (FastAPI + endpoints GET).

