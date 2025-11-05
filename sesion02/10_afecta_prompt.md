# Teoría: Cómo Afecta el Prompt al Contexto

Este ejercicio muestra cómo diferentes estructuras de prompt afectan el uso del contexto.

## Objetivo

Entender que la forma en que escribes el prompt determina cuántos tokens se consumen y cómo se procesa.

## Conceptos Clave

### Estructura del Prompt

- **Prompt corto**: Directo al grano, menos tokens
- **Prompt con instrucciones**: Más tokens pero más claro
- **Prompt con contexto largo**: Muchos tokens, puede ser innecesario
- **Prompt con ejemplos**: Útil pero consume muchos tokens

### Impacto en el Contexto

- **Más palabras = más tokens**: Cada palabra cuenta
- **Instrucciones innecesarias**: Consumen tokens sin valor
- **Ejemplos repetitivos**: Pueden ser redundantes
- **Optimización**: Reducir tokens sin perder claridad

## Lo que verás en el ejercicio

- Comparación de diferentes estructuras de prompt
- Medición de tokens y tiempo por estructura
- Análisis de eficiencia
- Ejemplos de optimización

## Estrategias de Optimización

1. **Elimina palabras innecesarias**: "Por favor, si es posible" → "Por favor"
2. **Sé directo**: "Podrías resumir" → "Resume"
3. **Usa ejemplos solo si son necesarios**: No repitas información
4. **Optimiza el contexto**: Solo incluye lo esencial

## Explicación para el alumno

* "Cada palabra en tu prompt consume tokens."
* "Ser más claro no siempre significa usar más palabras."
* "Optimizar el prompt puede reducir costos significativamente."
* "Prueba diferentes estructuras y mide el impacto."
