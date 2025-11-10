# Ejercicio 01 — Sanity check de credenciales cloud

## Objetivo

Validar rápidamente que las claves de OpenAI, Hugging Face y Google Gemini están configuradas y que cada servicio responde antes de avanzar con el resto de ejercicios.

## Conceptos clave

- **Smoke test multi-proveedor:** comprobar claves y modelos por defecto en un único paso.
- **Errores descriptivos:** mensajes claros cuando falta una variable o la clave es inválida.
- **Prevención de sorpresas:** detectar problemas de red/autenticación antes de las demos.

## Pasos

1. Copia `env.example` a `.env` y rellena todas las claves.
2. Ejecuta `python sesion03/01_cliente_generico.py`.
3. Observa la tabla resultante: cada fila indica si la conexión ha sido correcta y qué modelo se ha usado para la prueba.
4. La verificación de Hugging Face usa el nuevo `InferenceClient` oficial (`provider="hf-inference"`) para lanzar una mini generación de texto (por defecto `mistralai/Mistral-7B-Instruct-v0.2`, cámbialo en `.env` si prefieres otro).
5. Corrige cualquier error (clave inexistente, licencia sin aceptar, modelo no disponible) antes de continuar con la sesión.

## Ideas de extensión

- Guardar el resultado en un archivo JSON para integrarlo en pipelines CI/CD.
- Añadir más proveedores (Ollama, Azure OpenAI, Anthropic…) replicando el patrón.
- Programar este chequeo como tarea automática diaria para monitorizar caducidad de claves. 

