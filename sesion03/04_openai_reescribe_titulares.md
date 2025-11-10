# Ejercicio 04 — Reescritura de titulares con OpenAI

## Objetivo

Construir un primer cliente `chat.completions` minimalista que reescriba titulares con un `system` específico.

## Conceptos clave

- **Roles en el prompt:** separar instrucciones (`system`) de la petición (`user`).
- **Modelo configurable:** usa `DEFAULT_MODEL_OPENAI` desde la configuración.
- **Salida simple:** devolver sólo el nuevo titular.

## Pasos

1. Asegúrate de tener `OPENAI_API_KEY` en `.env`.
2. Revisa la función `reescribir_titular` y cómo monta los mensajes.
3. Ejecuta el script y pasa titulares adicionales para probar.
4. Ajusta el `system` para tus líneas editoriales.

## Ideas de extensión

- Guardar los titulares originales y reescritos en CSV.
- Añadir un `temperature` fijo o configurable por CLI.
- Mostrar coste aproximado usando la información de uso que devuelve la API.

