# Teoría: ¿Qué es un Token?

Este ejercicio introduce el concepto fundamental de **token** y cómo los modelos de lenguaje procesan el texto.

## Objetivo

Comprender que los tokens son las unidades básicas en que se divide un texto para ser procesado por un modelo de lenguaje, y que **no siempre coinciden con palabras completas**.

## Conceptos Clave

### ¿Qué es un Token?

Un token es una unidad de procesamiento. Según el algoritmo de tokenización:

- **BPE (Byte Pair Encoding)**: Combina pares frecuentes de bytes
- **SentencePiece**: Opera a nivel de caracteres Unicode  
- **Unigram**: Probabilístico basado en frecuencias

### Características Importantes

1. **No son palabras completas**: Un token puede ser:
   - Una palabra completa: `"hola"` → `[1234]`
   - Parte de una palabra: `"tokenización"` → `[567, 890]`
   - Un carácter: `"!"` → `[42]`
   - Un símbolo especial

2. **Dependen del modelo**: Diferentes modelos pueden tokenizar el mismo texto de forma distinta.

3. **Impacto en costes**: El número de tokens determina:
   - El tiempo de procesamiento
   - El costo de las APIs
   - El consumo de memoria

## Lo que verás en el ejercicio

- Cómo se tokeniza un texto simple
- Cómo afecta la puntuación al conteo de tokens
- Comparación de ratios caracteres/tokens
- Visualización de los IDs numéricos de tokens

## Explicación para el alumno

* "Imagina que el modelo necesita convertir el texto en números. Cada token es como una 'pieza de Lego' que tiene su propio número."
* "Cuando escribes 'Hola mundo', el modelo no ve dos palabras, ve una secuencia de tokens con IDs numéricos."
* "Entender esto te ayudará a optimizar tus prompts y controlar tus costes."
