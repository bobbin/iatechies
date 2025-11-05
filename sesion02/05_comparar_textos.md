# Teoría: Comparar Textos y Tokenización

Este ejercicio permite comparar diferentes textos y analizar cómo varía su tokenización según múltiples factores.

## Objetivo

Aprender a comparar textos y entender qué factores influyen en su tokenización, permitiendo optimizar prompts y predecir costos.

## Factores que Afectan la Tokenización

### 1. Longitud del Texto
- **No es lineal**: Duplicar caracteres no siempre duplica tokens
- **Overhead**: Los textos muy cortos pueden tener ratios peores
- **Eficiencia**: Textos más largos pueden ser más eficientes por token

### 2. Idioma
- **Idiomas latinos**: Generalmente más eficientes
- **Idiomas no latinos**: Pueden requerir más tokens por carácter
- **Mezcla de idiomas**: Puede afectar la tokenización

### 3. Tipo de Contenido
- **Texto natural**: Generalmente más eficiente
- **Código**: Puede tener ratios variables
- **Símbolos especiales**: Menos eficientes
- **URLs, números**: Pueden ser tokenizados de forma inesperada

## Métricas de Comparación

### Ratios Clave
- **Tokens/Caracteres**: Indica cuántos tokens por carácter
- **Tokens/Palabras**: Indica cuántos tokens por palabra
- **Eficiencia relativa**: Comparación entre textos

### Análisis
- **Más eficiente**: Menor ratio tokens/caracteres
- **Menos eficiente**: Mayor ratio tokens/caracteres
- **Diferencia**: Factor de diferencia entre textos

## Casos de Uso

### 1. Optimización de Prompts
Comparar diferentes versiones de un prompt para encontrar la más eficiente.

### 2. Planificación de Costos
Entender cómo diferentes tipos de contenido afectan el costo.

### 3. Selección de Contenido
Decidir qué formato de datos usar para minimizar tokens.

### 4. Análisis de Eficiencia
Identificar patrones en la tokenización de diferentes textos.

## Lo que verás en el ejercicio

- Comparación de textos por longitud
- Comparación por idioma
- Comparación por tipo de contenido
- Herramienta para encontrar la variante óptima
- Exportación de resultados a CSV

## Explicación para el alumno

* "Comparar textos es como comparar precios: ayuda a encontrar la mejor opción."
* "No todos los textos son iguales: algunos consumen más tokens que otros para el mismo contenido."
* "Aprender a comparar te ayuda a escribir prompts más eficientes y reducir costos."
* "La exportación te permite hacer análisis más profundos con herramientas externas."
