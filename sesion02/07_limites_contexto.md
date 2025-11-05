# Teoría: Límites de Contexto

Este ejercicio demuestra los límites de contexto y qué sucede cuando se exceden.

## Objetivo

Entender que cada modelo tiene un límite máximo de tokens que puede procesar simultáneamente, y las consecuencias de excederlo.

## Conceptos Clave

### Límites Fundamentales

- **Límite máximo**: Cada modelo tiene un máximo de tokens que puede procesar
- **Exceder el límite**: Puede causar errores, truncado automático o degradación de calidad
- **No siempre más es mejor**: Ventanas más grandes requieren hardware más potente

### Qué Pasa al Exceder

1. **Truncado automático**: El contenido más antiguo se descarta
2. **Errores**: La petición puede fallar completamente
3. **Degradación**: La calidad de las respuestas puede disminuir

## Lo que verás en el ejercicio

- Pruebas con diferentes tamaños de contexto
- Medición de éxito/fallo según el tamaño
- Análisis de tiempo de procesamiento
- Identificación del límite máximo

## Explicación para el alumno

* "Cada modelo tiene un 'presupuesto' de tokens que no puede excederse."
* "Es como intentar meter más agua en un vaso: llega un punto donde no cabe más."
* "Conocer estos límites es crucial para evitar errores en producción."
