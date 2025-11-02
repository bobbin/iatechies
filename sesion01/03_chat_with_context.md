# Teoría y explicación: Conversación con memoria

Este ejercicio enseña cómo mantener el contexto entre varias preguntas a un modelo local.

## Objetivo principal
* Que el alumno entienda que las conversaciones son una secuencia de turnos y que debemos enviar el contexto anterior para que el modelo recuerde la historia.

## ¿Qué hace el código?
1. Define una función `turn` que recibe el mensaje del usuario y el contexto anterior.
2. Llama a `api/generate` de Ollama y, si tenemos contexto previo, lo adjunta en el cuerpo de la petición.
3. Guarda la nueva respuesta y el contexto que devuelve el modelo para usarlo en la siguiente llamada.
4. Realiza tres turnos, demostrando que la IA recuerda que se llama "Ada" y sigue las instrucciones iniciales.

## Conceptos a remarcar al alumno
* "El contexto es como la memoria corta del asistente. Sin él olvidaría lo que hemos dicho hace un momento".
* "Cada respuesta trae un paquete de contexto que debemos volver a enviar si queremos continuar la charla".
* "Así podemos construir chatbots más naturales".
