# Teoría y explicación: Lotes de prompts y keep_alive

Este ejercicio muestra cómo enviar muchos prompts seguidos y mantener el modelo cargado para ahorrar tiempo.

## ¿Qué se busca enseñar?
* Que cargar un modelo puede tardar, pero una vez en memoria las respuestas son más rápidas.
* Que `keep_alive` mantiene el modelo "calentito" durante unos minutos aunque no le hablemos.
* Que podemos medir el tiempo total de un lote de peticiones.

## Recorrido del script
1. Preparamos una lista de 10 frases que el modelo debe generar.
2. Hacemos una llamada inicial vacía con `keep_alive=300` (5 minutos) para que Ollama no descargue el modelo enseguida.
3. Recorremos cada prompt y pedimos la generación sin streaming.
4. Al final mostramos cuánto tardó todo el lote.

## Mensaje para el alumno
* "Calentar el modelo es como precalentar el horno: tardas una vez y luego todo va más fluido".
* "`keep_alive` es un temporizador que evita que Ollama cierre el modelo por inactividad".
* "Medir el tiempo nos permite comprobar si la estrategia realmente mejora el rendimiento".
