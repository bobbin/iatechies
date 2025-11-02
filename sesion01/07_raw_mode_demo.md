# Teoría y explicación: Raw mode en Ollama

Este ejercicio introduce el modo `raw`, que permite enviar prompts sin que Ollama añada instrucciones extra.

## Puntos clave para el alumno
* En condiciones normales Ollama envuelve nuestro prompt con mensajes del sistema. Con `raw` tomamos el control total.
* Es útil cuando trabajamos con formatos especiales como `[INST] ... [/INST]` que usan algunos modelos.
* Necesitamos saber exactamente qué espera el modelo, porque ya no hay "ruedas de apoyo".

## ¿Qué hace el script?
1. Define un prompt usando el formato de instrucciones típico de modelos estilo Alpaca.
2. Llama a `api/generate` con `raw=True` para evitar modificaciones.
3. Imprime la respuesta directa del modelo `mistral`.

## Cómo explicarlo de forma sencilla
* "Raw mode es como hablar directamente con el motor del modelo, sin intérpretes".
* "Si no activamos raw, Ollama podría añadir mensajes que rompan el formato especial".
* "Hay que usarlo con cuidado y solo cuando sabemos lo que estamos haciendo".
