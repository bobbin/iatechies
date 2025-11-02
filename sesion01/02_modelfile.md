# Teoría y explicación: Personalizar un modelo con Modelfile

Este ejercicio introduce los **Modelfile** de Ollama, que son recetas muy sencillas para crear variantes de un modelo base.

## ¿Qué aprendemos?
* Que podemos partir de un modelo existente (por ejemplo `mistral:7b`) y ajustarlo con instrucciones propias.
* Que las instrucciones del sistema sirven para que el modelo responda siempre de una forma concreta.
* Que podemos fijar parámetros como la `temperature` para controlar la creatividad.

## ¿Qué contiene el Modelfile?
1. `FROM mistral:7b`: indicamos el modelo base que queremos extender.
2. `SYSTEM ...`: añadimos un mensaje permanente que obliga al modelo a responder en JSON con claves `pros` y `contras`.
3. `PARAMETER temperature 0.2`: pedimos respuestas más estables y menos aleatorias.

## ¿Cómo lo transmitimos al alumno?
* "Un Modelfile es como una hoja de instrucciones que personaliza un modelo".
* "Le decimos cómo debe hablar y qué formato debe devolver, sin tener que recordárselo en cada prompt".
* "Así evitamos errores y ganamos consistencia en nuestras aplicaciones".
