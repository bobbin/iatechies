# Ejercicio 09 — Cambiar de modelo con la misma llamada (Hugging Face)

## Objetivo

Reutilizar el mismo cliente de la Inference API cambiando únicamente el `model_id` para comparar estilo, longitud y tono de varias familias open-source.

## Conceptos clave

- **Modelo como parámetro:** no tocar la lógica, sólo el identificador.
- **Batería de pruebas:** ejecutar la misma instrucción en varios modelos.
- **Análisis cualitativo:** observar diferencias y tomar notas de cada salida.

## Pasos

1. Define una lista de modelos a probar disponibles en `hf-inference` (añade el sufijo `:hf-inference` si el proveedor lo requiere).
2. Ejecuta el script y observa las variaciones impresas.
3. Ajusta parámetros (`temperature`, `max_tokens`) si lo necesitas.
4. Completa una pequeña tabla comparativa (longitud, tono, precisión aparente).

## Ideas de extensión

- Guardar resultados en SQLite o CSV junto a metadatos del modelo.
- Añadir métricas automáticas: nº de frases, nº de palabras por salida.
- Integrar con el benchmark del bloque G para comparar latencias entre modelos.

