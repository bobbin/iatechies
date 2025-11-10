# Ejercicio 06 — Embeddings de titulares y similitud básica

## Objetivo

Obtener embeddings de varios titulares usando OpenAI, calcular similitud coseno y mostrar parejas más y menos parecidas.

## Conceptos clave

- **Embeddings:** representación vectorial para comparar semántica.
- **Similitud coseno:** métrica sencilla para medir cercanía.
- **Normalización:** convertir la lista de vectores en `numpy` para cálculos rápidos.

## Pasos

1. Comprueba que `DEFAULT_MODEL_EMBEDDINGS_OPENAI` está definido en `.env`.
2. Revisa cómo el script llama a `client.embeddings.create`.
3. Ejecuta el script y analiza las puntuaciones impresas.
4. Añade nuevos titulares y observa qué pares se parecen más.

## Ideas de extensión

- Construir una matriz de similitud completa y ordenarla.
- Guardar los embeddings en disco para reutilizarlos en otras sesiones (RAG).
- Comparar resultados con Hugging Face u Ollama replicando el mismo código.

