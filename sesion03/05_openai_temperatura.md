# Ejercicio 05 — Comparar temperatura con un caso real

## Objetivo

Observar cómo la temperatura afecta la creatividad de un titular usando el mismo prompt y distintos valores (`0.0`, `0.3`, `0.7`), incluyendo latencia de cada llamada.

## Conceptos clave

- **Temperature:** controla aleatoriedad vs determinismo.
- **Serie de experimentos:** repetir el mismo prompt para comparar salidas.
- **Métricas básicas:** capturar tiempo de respuesta para cada ejecución.

## Pasos

1. Configura `OPENAI_API_KEY` y ejecuta el script.
2. Comprueba cómo cambia el estilo del titular para cada temperatura.
3. Observa las diferencias de latencia (pueden ser pequeñas pero útiles para comparar).
4. Añade más temperaturas o prompts para construir tu propia batería de pruebas.

## Ideas de extensión

- Guardar los resultados en CSV junto al parámetro usado.
- Añadir `top_p` como segundo parámetro de exploración.
- Integrar esta comparativa en un dashboard para el equipo editorial.

