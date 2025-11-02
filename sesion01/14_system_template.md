# Teoría y explicación: System prompt y plantillas personalizadas

Este guion muestra cómo inyectar un `system prompt` y sustituir la plantilla por defecto con el campo `template`.

## Objetivo didáctico
* Diferenciar entre el mensaje del usuario (`prompt`) y las instrucciones globales (`system`).
* Enseñar la sintaxis básica de plantillas Mustache que utiliza Ollama (`{{ .System }}`, `{{ .Prompt }}`).
* Demostrar que puedes recrear formatos estilo chat sin necesidad de `raw=True`.

## Ideas clave
* "Usa `system` para fijar tono, idioma o políticas antes de cualquier turno".
* "El campo `template` permite alinear Ollama con prompts heredados de otros proveedores".
* "Combínalo con `context` para mantener memoria entre llamadas manteniendo tu plantilla".
