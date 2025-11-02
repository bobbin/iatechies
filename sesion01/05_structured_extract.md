# Teoría y explicación: Extracción estructurada

Aquí practicamos cómo pedir a un modelo que rellene un JSON siguiendo un esquema fijo.

## Objetivo docente
* Mostrar que podemos guiar al modelo para que entregue datos listos para usar en lugar de texto libre.
* Presentar la idea de un **esquema JSON**: definimos qué campos queremos, su tipo y cuáles son obligatorios.

## Cómo funciona el script
1. Construimos un `schema` con las claves `empresa`, `fecha` y `total`.
2. Creamos un prompt con un texto sencillo de factura y le pedimos solo el JSON.
3. Llamamos a la API indicando `format: schema` para que Ollama obligue al modelo a respetar la estructura.
4. Convertimos la respuesta a un objeto Python usando `json.loads` y la mostramos.

## Puntos que resaltamos al alumno
* "Si definimos un esquema, evitamos que la IA divague y podamos insertar el resultado en nuestra base de datos".
* "Es ideal para procesar documentos o formularios de manera automática".
* "Incluso con modelos generales, podemos conseguir salidas bastante limpias".
