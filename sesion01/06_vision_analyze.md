# Teoría y explicación: Analizar imágenes con un modelo multimodal

Este ejercicio enseña a enviar una imagen al modelo `llava` para que devuelva una descripción estructurada.

## ¿Qué queremos enseñar?
* Que existen modelos que procesan texto e imágenes a la vez (modelos multimodales).
* Que debemos convertir la imagen a Base64 para enviarla por la API.
* Que podemos pedir un formato JSON con objetos y descripción.

## Pasos del script
1. Leemos la ruta de la imagen desde la línea de comandos, o usamos `ejemplo.jpg` por defecto.
2. Codificamos la imagen en Base64 y la incluimos en el campo `images`.
3. Mandamos un prompt que pide objetos y una descripción breve en JSON.
4. Procesamos la respuesta y la mostramos como un diccionario Python.

## Cómo contarlo en clase
* "Los modelos multimodales son como asistentes que pueden mirar una foto y contarnos lo que ven".
* "Base64 es un truco para convertir la imagen en texto y poder enviarla por internet".
* "Obligamos a que la respuesta sea JSON para integrar el resultado en nuestras aplicaciones".
