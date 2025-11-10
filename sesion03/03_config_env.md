# Ejercicio 03 — Configuración desde variables de entorno

## Objetivo

Centralizar claves y nombres de modelos en un archivo `.env`, cargarlos desde el código y exponer una función `get_config()` que devuelva un diccionario listo para usar.

## Conceptos clave

- **Separación de secretos:** nunca hardcodear claves en el repositorio.
- **`.env` + `.env.example`:** patrón para compartir configuración sin filtrar datos sensibles.
- **Normalización de defaults:** elegir un modelo por proveedor y exponerlo de forma consistente.

## Pasos

1. Copia `env.example` a `.env` y rellena tus claves y modelos.
2. Ejecuta el script: muestra la configuración cargada y valida que existan claves mínimas.
3. Extiende `Config` con nuevos campos según tus necesidades (p.ej. región, endpoints).
4. Integra `get_config()` en otros ejercicios como fuente de verdad.

## Ideas de extensión

- Validar con `pydantic` o `attrs` para tener errores más descriptivos.
- Cargar un perfil alternativo (`.env.staging`) y elegirlo con `ENVIRONMENT=staging`.
- Serializar la configuración en un `config.json` para otras herramientas.

