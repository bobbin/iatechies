# Teoría: Contar Tokens

Este ejercicio enseña diferentes métodos para contar tokens y por qué es importante hacerlo correctamente.

## Objetivo

Aprender a contar tokens de forma precisa y entender cómo esto afecta el costo y rendimiento de las aplicaciones con LLMs.

## Métodos de Conteo

### 1. Tokenización Real (Precisa)
Usa la API de tokenización del modelo para obtener el conteo exacto.

**Ventaja**: Precisión total  
**Desventaja**: Requiere llamada a API

### 2. Estimación Simple (Aproximada)
Reglas del pulgar comunes:
- **4 caracteres ≈ 1 token** (para inglés)
- **1.3 tokens por palabra** (promedio)

**Ventaja**: Rápido, sin API  
**Desventaja**: Puede tener errores del 20-50%

### 3. Conteo Real en Respuesta
Usa los campos `prompt_eval_count` y `eval_count` de la respuesta de Ollama.

**Ventaja**: Incluye overhead del sistema  
**Desventaja**: Solo disponible después de la llamada

## Impacto en Costos

El conteo de tokens impacta directamente en:
- **Facturación**: La mayoría de APIs cobran por token
- **Rendimiento**: Más tokens = más tiempo de procesamiento
- **Límites**: Los modelos tienen límites de contexto en tokens

## Lo que verás en el ejercicio

- Comparación entre métodos de conteo
- Análisis de ratios (tokens/caracteres, tokens/palabras)
- Estimación de costos basada en tokens
- Errores de los métodos aproximados

## Explicación para el alumno

* "Contar tokens es como medir ingredientes en una receta: si te equivocas, el resultado (y el costo) cambia."
* "Las estimaciones rápidas son útiles para planificar, pero para facturar necesitas el conteo exacto."
* "Un error del 20% en 1000 tokens puede significar pagar de más o quedarte sin presupuesto."
