# Teoría y explicación: Semillas para respuestas reproducibles

Este ejercicio explica cómo conseguir que un modelo genere siempre la misma respuesta usando una semilla (`seed`).

## ¿Qué queremos que entienda el alumno?
* Los modelos suelen ser algo aleatorios; dos ejecuciones iguales pueden devolver textos distintos.
* Si fijamos un número de semilla, el modelo utiliza la misma "ruleta" interna y la respuesta se repite.
* Cambiar la semilla produce variaciones útiles para generar alternativas controladas.

## Funcionamiento del script
1. Define una función `gen` que llama a Ollama con la opción `seed` dentro de `options`.
2. Lanza dos veces la generación con `seed=42` y una vez con `seed=7`.
3. Imprime las tres respuestas y comprueba si las dos primeras coinciden.

## Cómo contarlo de forma sencilla
* "La semilla es el truco para congelar la suerte del modelo".
* "Si necesitamos reproducir un resultado en una demo o test, fijar la semilla es fundamental".
* "Cambiar de semilla nos permite explorar respuestas distintas sin dejarlo al azar completo".
