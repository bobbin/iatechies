# Ejercicio 14 — Microservicio `/chat` con OpenAI

## Objetivo

Construir un microservicio minimalista (FastAPI) con un único endpoint `POST /chat` que llame a OpenAI y devuelva respuesta + latencia.

## Conceptos clave

- **FastAPI:** framework rápido para prototipos de APIs.
- **Dependencias:** reutilizar `get_openai_client` dentro de la ruta.
- **Observabilidad mínima:** incluir latencia en la respuesta.

## Pasos

1. Configura tus variables en `.env` y ejecuta `python sesion03/14_microservicio_openai.py` (o lanza `uvicorn` apuntando al objeto `app`).
2. Envía una petición POST con JSON `{"prompt": "...", "temperature": 0.2}` usando `curl` o `httpie`.
3. Comprueba la respuesta que incluye `message` y `latency_ms`.
4. Prueba el endpoint desde PowerShell con cualquiera de estas opciones (ambas generan el mismo JSON y evitan problemas de salto de línea):

   **a. Usando `curl.exe` en una sola línea**

   ```powershell
   curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"prompt":"que puedes hacer por la redaccion de un periodico", "temperature":0.2}'
   ```

   **b. Usando `Invoke-RestMethod`**

   ```powershell
   Invoke-RestMethod -Method Post `
       -Uri http://localhost:8000/chat `
       -ContentType "application/json" `
       -Body ( @{ prompt = "Hola, ¿qué puedes hacer por la redacción?"; temperature = 0.2 } | ConvertTo-Json )
   ```

5. Añade validaciones adicionales (p.ej. longitud máxima de prompt).

## Ideas de extensión

- Registrar cada petición con un middleware de logging sencillo.
- Añadir autenticación básica (token de servicio) para entornos cerrados.
- Implementar streaming de tokens usando `StreamingResponse`.

