# Teoría y explicación: Enrutador híbrido local/nube

Este ejercicio muestra una estrategia básica para decidir si respondemos con un modelo local pequeño o uno más grande en la nube.

## Meta educativa
* Comprender que podemos combinar varios modelos y escoger el más adecuado según reglas simples.
* Mostrar cómo medir latencia y decidir automáticamente qué modelo usar.
* Demostrar que Ollama puede usar tanto modelos locales como en la nube de forma transparente.

## Cómo funciona el router
1. Calcula una estimación rápida de tokens del prompt (`est_tokens` = largo / 4).
2. Si el prompt es corto (< 50 tokens), usa el modelo local pequeño (`gemma:2b`).
3. Si el prompt es largo (≥ 50 tokens), usa el modelo cloud más potente (`gpt-oss:20b-cloud`).
4. Devuelve qué ruta se eligió, la respuesta recortada y la latencia.
5. En el `main` probamos con dos prompts de distinta complejidad para ver la diferencia.

## Ejemplo de salida
```
--- [LOCAL] ---
Prompt:
Resume en 3 viñetas por qué usar modelos locales.

Respuesta:
1. Privacidad y control de datos
2. Latencia y rendimiento
3. Costo y autonomía
...
latencia_ms=5468 coste_est=0.0

--- [CLOUD] ---
Prompt:
Escribe un plan de pruebas detallado de 1500 palabras para un sistema RAG con métricas.

Respuesta:
I. Introducción
II. Componentes del sistema RAG...
...
latencia_ms=4528 coste_est=0.0
```

## Mensaje para el alumno
* "Podemos tener lo mejor de ambos mundos: velocidad con modelos pequeños para tareas sencillas y potencia con modelos grandes para retos complejos".
* "Las reglas pueden ser tan simples o complejas como queramos; incluso podríamos usar machine learning para decidir".
* "Tanto modelos locales como cloud están en Ollama, así que la decisión es transparente".
