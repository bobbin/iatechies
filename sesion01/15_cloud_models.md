# Teoría y explicación: Trabajar con modelos en Ollama Cloud

Guion dedicado a consumir Ollama Cloud usando el endpoint `https://api.ollama.com/v1` y un token personal.

## Objetivo didáctico
* Explicar cómo autenticar peticiones con `Authorization: Bearer <token>`.
* Listar los modelos disponibles para un equipo y lanzar la misma petición contra varios modelos cloud.
* Reforzar que el API de generación es el mismo que el local, solo cambia la URL base.

## Mensajes clave
* "Guarda tu token en `OLLAMA_API_KEY` y evita hardcodearlo en repositorios".
* "Los endpoints difieren: `/api/tags` en local versus `/v1/models` en cloud".
* "Puedes mezclar modelos cloud y locales en un router propio usando las mismas funciones auxiliares".
