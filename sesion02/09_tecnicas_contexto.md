# Teoría: Técnicas para Manejar Contexto

Este ejercicio demuestra técnicas para manejar textos que exceden los límites de contexto.

## Objetivo

Aprender técnicas prácticas para procesar documentos largos sin perder información importante.

## Técnicas Principales

### 1. Truncado Simple

**Cómo funciona**: Corta el texto al límite de tokens, descartando el final.

**Ventajas**:
- Simple de implementar
- Rápido

**Desventajas**:
- Pierde información del final
- Puede perder contexto importante

**Cuándo usar**: Cuando el inicio del texto es más importante que el final.

### 2. Ventanas Deslizantes

**Cómo funciona**: Divide el texto en segmentos solapados que se procesan secuencialmente.

**Ventajas**:
- Procesa todo el texto
- Mantiene contexto local con solapamiento
- No pierde información

**Desventajas**:
- Más complejo de implementar
- Requiere múltiples llamadas

**Cuándo usar**: Para análisis de documentos largos donde necesitas procesar todo.

### 3. Chunking por Oraciones

**Cómo funciona**: Divide el texto en chunks respetando límites de oraciones.

**Ventajas**:
- Mantiene coherencia semántica
- No corta oraciones a la mitad
- Más natural que el truncado

**Desventajas**:
- Puede crear chunks de tamaños variables
- Requiere procesamiento adicional

**Cuándo usar**: Cuando necesitas mantener la coherencia del texto.

## Lo que verás en el ejercicio

- Implementación de cada técnica
- Comparación de resultados
- Análisis de ventajas y desventajas
- Recomendaciones de uso

## Explicación para el alumno

* "No siempre puedes meter todo el texto de una vez."
* "Las técnicas de segmentación te permiten procesar documentos largos."
* "Cada técnica tiene su caso de uso ideal."
* "El solapamiento ayuda a mantener el contexto entre segmentos."
