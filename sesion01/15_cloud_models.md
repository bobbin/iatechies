# Teoría y explicación: Trabajar con modelos Cloud en Ollama

Este ejercicio muestra cómo identificar y usar modelos remotos (cloud) en Ollama.

## Objetivo didáctico
* Identificar qué modelos son remotos (cloud) mediante los campos `remote_model` o `remote_host`.
* Listar solo los modelos cloud disponibles.
* Generar texto usando modelos cloud con el mismo API.

## Cómo funciona
1. Llama a `/api/tags` para obtener todos los modelos disponibles.
2. Detecta si un modelo es remoto revisando los campos `remote_model` o `remote_host`.
3. Filtra solo los modelos cloud.
4. Prueba generación con el modelo cloud disponible.

## Ejemplo de salida
```
Listando modelos CLOUD disponibles en Ollama...
============================================================

Total de modelos CLOUD: 1

Modelos CLOUD disponibles:
  - gpt-oss:20b-cloud

============================================================

Generando con: gpt-oss:20b-cloud
Respuesta: 1. Reproducibilidad: Al tener los prompts documentados...
```

## Mensajes clave
* "Los modelos remotos se conectan dinámicamente cuando los usas".
* "No necesitas descargar el modelo completo, se ejecuta en la nube".
* "Usa el mismo API de Ollama tanto para modelos locales como cloud".
