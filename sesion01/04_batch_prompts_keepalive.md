# Teoría y explicación: Lotes de prompts y keep_alive

Este ejercicio muestra cómo enviar muchos prompts seguidos y mantener el modelo cargado para ahorrar tiempo.

## ¿Qué se busca enseñar?
* Que cargar un modelo puede tardar, pero una vez en memoria las respuestas son más rápidas.
* Que `keep_alive` mantiene el modelo "calentito" durante unos minutos aunque no le hablemos.
* Que podemos medir el tiempo total de un lote de peticiones **comparando** con y sin `keep_alive`.

## Recorrido del script
1. Preparamos una lista de 5 frases que el modelo debe generar.
2. **Ejecutamos DOS lotes en orden inverso** para la comparación justa:
   - **Primero CON keep_alive=300**: pre-cargamos el modelo explícitamente
   - **Segundo SIN keep_alive**: después de 5 segundos de espera, el modelo se descarga
3. Cada prompt se envía y generamos respuesta sin streaming.
4. Al final comparamos los tiempos y mostramos conclusiones.

## ¿Por qué este orden?
**IMPORTANTE**: El orden de ejecución importa mucho. Si ejecutas primero SIN keep_alive, el modelo se carga en la primera llamada. Si luego ejecutas CON keep_alive, el modelo ya está en memoria de la ejecución anterior y la comparación no es justa.

Por eso el script invierte el orden y espera 5 segundos para que Ollama descargue el modelo.

## Ejemplo de salida
```
============================================================
Experimento: Comparando keep_alive
NOTA: El orden importa. El primer lote carga el modelo desde cero,
      el segundo lote puede aprovechar el modelo ya cargado.

============================================================
LOTE 1: CON keep_alive (modelo pre-cargado)
============================================================
OK: Modelo pre-cargado y mantenido 300s
  1/5
  2/5
  3/5
  4/5
  5/5

Esperando 5 segundos para que Ollama descargue el modelo...

============================================================
LOTE 2: SIN keep_alive (modelo se carga en primer prompt)
============================================================
  1/5
  2/5
  3/5
  4/5
  5/5

============================================================
COMPARACION:
Con keep_alive:    96.32s
Sin keep_alive:    60.63s
Diferencia:        35.69s (37.0% mas lento con keep_alive)

CONCLUSION: En este caso, el modelo ya estaba en memoria de ejecuciones anteriores.
============================================================
```

## Mensaje para el alumno
* "Calentar el modelo es como precalentar el horno: tardas una vez y luego todo va más fluido".
* "`keep_alive` es un temporizador que evita que Ollama cierre el modelo por inactividad".
* "El **orden de ejecución** importa mucho en las comparaciones de rendimiento".
* "Si haces muchas peticiones seguidas, `keep_alive` puede ayudar. Si solo haces unas pocas, puede no merecer la pena".
