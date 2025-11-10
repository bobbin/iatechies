# Ejercicio 18 — Script de benchmark multi-backend

## Objetivo

Construir un script que cargue una lista de prompts, llame al endpoint `/chat` de nuestro microservicio multi-backend y registre latencia, P50/P95 y tokens medios por proveedor en `benchmark_results.csv`.

## Conceptos clave

- **Benchmark reproducible:** mismos prompts, mismos parámetros para todos.
- **Métricas agregadas:** `latencia_media`, `p50`, `p95`, `tokens_promedio`.
- **Persistencia:** guardar resultados para compararlos en distintas fechas.

## Pasos

1. Define un archivo `prompts.txt` (o usa la lista incluida en el script).
2. Ejecuta `python sesion03/18_benchmark_multibackend.py` mientras el microservicio esté activo.
3. Revisa el CSV generado en `logs/benchmark_results.csv`.
4. Analiza los datos y decide qué backend ofrece mejor relación coste/calidad.

## Ideas de extensión

- Añadir métricas de coste estimado si conoces el precio por token de cada backend.
- Enviar peticiones en paralelo (con `asyncio` o `concurrent.futures`) para simular carga real.
- Visualizar los resultados en un dashboard o gráfico rápido (p.ej. con `matplotlib`).

