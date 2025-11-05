# Teoría: Trampas y Sorpresas en la Tokenización

Este ejercicio explora casos extremos donde el conteo de tokens puede ser inesperado y costoso.

## Objetivo

Identificar y comprender situaciones donde el conteo de tokens puede dispararse de forma no lineal, afectando significativamente los costos.

## Trampas Principales

### 1. Casos Extremos

#### Emojis
- **Problema**: Los emojis pueden consumir múltiples tokens cada uno
- **Ejemplo**: `😊` puede ser 2-3 tokens
- **Impacto**: Un mensaje con muchos emojis puede duplicar o triplicar el costo

#### Símbolos Especiales
- **Problema**: Símbolos matemáticos, técnicos, y especiales se tokenizan de forma ineficiente
- **Ejemplo**: `©®™€£¥` cada uno puede ser múltiples tokens
- **Impacto**: Textos con muchos símbolos pueden ser muy costosos

#### Fragmentos de Código
- **Problema**: El código a menudo se tokeniza de forma subóptima
- **Ejemplo**: `def f(x): return x**2` puede tener más tokens que palabras equivalentes
- **Impacto**: Incluir código en prompts puede disparar costos

### 2. Impacto Multilingüe

#### Idiomas No Latinos
- **Chino, Japonés, Coreano**: Requieren más tokens por carácter
- **Árabe, Hebreo**: Pueden tener diferentes ratios de tokenización
- **Ruso, Cirílico**: Generalmente más tokens que latinos

#### Comparación
- **Español/Inglés**: ~1 token por palabra (promedio)
- **Chino**: ~1.5-2 tokens por carácter
- **Japonés**: Variable, puede ser muy alto

### 3. Herramientas de Debug

Para evitar sorpresas:
- **Visualizadores de tokens**: Anticipa el consumo antes de producción
- **Testing**: Prueba casos extremos antes de desplegar
- **Monitoreo**: Rastrea el consumo real en producción

## Lo que verás en el ejercicio

- Comparación de tokenización entre diferentes tipos de contenido
- Análisis de ratios inesperados
- Impacto en costos de diferentes trampas
- Ejemplos de optimización

## Estrategias de Mitigación

1. **Minimizar emojis** en prompts de producción
2. **Evitar símbolos innecesarios**
3. **Optimizar código** antes de incluirlo en prompts
4. **Considerar idioma** al planificar costos
5. **Medir siempre** antes de escalar

## Explicación para el alumno

* "Las trampas de tokenización son como 'grietas' en el presupuesto: pequeños cambios que multiplican el costo."
* "Un emoji puede costar lo mismo que una palabra completa, o más."
* "Conocer estas trampas te ayuda a escribir prompts más eficientes y predecir costos reales."
