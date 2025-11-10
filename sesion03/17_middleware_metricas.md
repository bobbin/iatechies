# Ejercicio 17 — Middleware de métricas

## Objetivo

Añadir un middleware a FastAPI que mida latencia, anote un `request_id` y escriba métricas en un CSV (`logs/metrics.csv`) con campos clave.

## Conceptos clave

- **Middleware personalizado:** intercepta entrada y salida de cada petición.
- **Observabilidad:** registrar `endpoint`, `backend`, `model`, `latency_ms`, `tokens`.
- **Persistencia ligera:** CSV fácil de inspeccionar o importar en Excel.

## Pasos

1. Ejecuta `python sesion03/17_middleware_metricas.py` (levanta un servicio de ejemplo).
2. Realiza algunas peticiones a `/chat` y comprueba que se crea/actualiza `logs/metrics.csv`. Por ejemplo:

   ```powershell
   curl -X POST http://localhost:8003/chat -H "Content-Type: application/json" -d '{"backend":"openai","prompt":"Genera un resumen corto","temperature":0.2}'
   ```

3. Observa cómo se genera un `request_id` único por petición.
4. Conecta el middleware al microservicio del ejercicio 15 para tener métricas reales.

## Ideas de extensión

- Exportar métricas a Prometheus o a una herramienta interna.
- Añadir campos como `status_code`, `error_type` o coste estimado.
- Crear un script que agregue las métricas (P50, P95) a partir del CSV.

