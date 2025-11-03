# Chat interactivo simple — Ejercicio extra

Chat de línea de comandos (CLI) con memoria de contexto.

## Objetivo

Construir un chat interactivo básico que mantiene la conversación con Ollama.

## Características

- ✅ Mantiene el contexto entre mensajes
- ✅ Acepta múltiples comandos de salida (`salir`, `exit`, `quit`)
- ✅ Maneja Ctrl+C (interrupción de teclado)
- ✅ Detecta mensajes vacíos
- ✅ Muestra errores de forma amigable

## Cómo ejecutarlo

```bash
python 03b_chat_interactive.py
```

## Ejemplo de uso

```
🤖 Chat iniciado. Escribe 'salir', 'exit' o 'quit' para terminar.

Tú: Hola, ¿cómo estás?
🤖: Bien, gracias. ¿Y tú?

Tú: Me llamo Carlos
🤖: Hola Carlos, encantado de conocerte.

Tú: ¿Recuerdas mi nombre?
🤖: Sí, te llamas Carlos.

Tú: salir
¡Hasta luego! 👋
```

## Diferencias con el ejercicio 03

- **03**: Demuestra el concepto con 3 turnos predefinidos
- **03b**: Chat interactivo completo que puedes usar en práctica real

## Notas

El contexto se mantiene automáticamente: cada respuesta trae un `context` que se envía con el siguiente mensaje. Esto permite conversaciones naturales donde el modelo "recuerda" lo anterior.

