# Teoría: Latencia y Contexto

Este ejercicio muestra cómo el tamaño del contexto afecta la latencia de procesamiento.

## Objetivo

Comprender que más contexto no solo consume más tokens, sino que también aumenta significativamente el tiempo de procesamiento.

## Conceptos Clave

### Relación Contexto-Latencia

- **Crecimiento no lineal**: El tiempo puede crecer más rápido que los tokens
- **Hardware exponencial**: Ventanas grandes requieren hardware mucho más potente
- **Cuellos de botella**: En producción, esto puede crear problemas de rendimiento

### Impacto en Producción

- **Latencia percibida**: Los usuarios esperan respuestas rápidas
- **Costos de infraestructura**: Más hardware = más costo
- **Escalabilidad**: Difícil escalar con contextos muy grandes

## Lo que verás en el ejercicio

- Medición de latencia con diferentes tamaños
- Comparación de crecimiento tokens vs tiempo
- Análisis de eficiencia (tokens por segundo)
- Identificación de cuellos de botella

## Explicación para el alumno

* "Más contexto significa más tiempo de procesamiento."
* "El crecimiento puede ser exponencial, no solo lineal."
* "En producción, esto se traduce en usuarios esperando más tiempo."
* "Optimizar el contexto es clave para mantener buena experiencia."
