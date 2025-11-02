# Teoría y explicación: Comparar modelos

Este ejercicio nos muestra cómo medir y comparar dos modelos de lenguaje locales usando la API de Ollama.

## ¿Qué idea principal trabajamos?
* Aprender que distintos modelos responden igual al mismo prompt pero tardan tiempos distintos.
* Guardar los resultados en un archivo CSV para analizarlos después (por ejemplo en Excel o Google Sheets).

## ¿Qué hace el script?
1. Define la URL del servidor Ollama, la lista de modelos y los mensajes que enviaremos.
2. Para cada combinación prompt + modelo hace una llamada HTTP `POST` a `api/generate`.
3. Mide cuánto tarda la respuesta y recoge cuántos tokens ha usado.
4. Guarda todo en `results_compare.csv` para que podamos revisar la latencia y el número de tokens.

## Conceptos clave
* **Latencia**: tiempo que tarda en llegar la respuesta. Lo calculamos restando el tiempo final menos el inicial.
* **Tokens**: trocitos en los que el modelo divide el texto. Saber cuántos entran y salen ayuda a estimar coste y rendimiento.
* **CSV**: formato de tabla simple que luego podemos abrir para comparar resultados.

## ¿Cómo lo explicamos al alumno?
* "Vamos a preguntar lo mismo a varios modelos y ver cuál responde más rápido".
* "Mediremos el tiempo con un cronómetro dentro del código y guardaremos los datos en una hoja de cálculo".
* "Así aprendemos a evaluar modelos de forma objetiva, sin depender solo de nuestra impresión".
