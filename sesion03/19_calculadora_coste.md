# Ejercicio 19 — Calculadora de coste por feature

## Objetivo

Leer el CSV de métricas/benchmark, estimar coste mensual según volumen de peticiones y precios por backend, e imprimir un resumen comparativo.

## Conceptos clave

- **Coste = peticiones × tokens medios × precio/token.**
- **Escenarios de uso:** estimar peticiones/día y extrapolar a un mes.
- **Decisiones informadas:** justificar elegir un backend según coste-calidad.

## Pasos

1. Asegúrate de tener métricas en `logs/metrics.csv` o benchmarks en `logs/benchmark_results.csv`.
2. Ajusta el diccionario `PRECIOS_POR_1K_TOKENS` con tus tarifas reales.
3. Ejecuta `python sesion03/19_calculadora_coste.py`.
4. Introduce el nº de peticiones diarias estimadas cuando se te solicite.

## Ideas de extensión

- Leer precios desde `.env` o un archivo YAML compartido con finanzas.
- Generar un informe PDF o enviar el resumen por Slack/Teams.
- Incorporar costes de infraestructura local (Ollama) para comparar “coste total”.

