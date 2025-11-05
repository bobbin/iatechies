# Sesión 02: Tokens y Tokenización

Colección de ejercicios prácticos para entender, contar y visualizar tokens en modelos de lenguaje.

## Objetivos de Aprendizaje

Al finalizar esta sesión, serás capaz de:

- ✅ Entender qué es un token y cómo funciona la tokenización
- ✅ Contar tokens de forma precisa y estimar costos
- ✅ Visualizar tokens para comprender el proceso
- ✅ Identificar trampas comunes que disparan el conteo de tokens
- ✅ Comparar diferentes textos y optimizar prompts

## Requisitos

- Python 3.10+
- Ollama corriendo en local (http://localhost:11434) - **requerido para ejercicios 07-10**
- Instala dependencias:
  ```bash
  pip install -r requirements.txt
  ```
  
  O simplemente:
  ```bash
  pip install tiktoken requests
  ```

## Ejercicios

### 01_que_es_token.py
**Introducción al concepto de token**

Muestra cómo se tokeniza un texto usando `tiktoken` y qué son los tokens.

- Ejemplos simples de tokenización
- Visualización de tokens individuales
- Comparación de ratios

**Conceptos clave:**
- Los tokens son IDs numéricos que representan partes del texto
- No siempre coinciden con palabras completas
- Cada token puede ser decodificado de vuelta a texto

---

### 02_contar_tokens.py
**Métodos para contar tokens**

Compara métodos de conteo real vs estimaciones.

- Conteo real con `tiktoken`
- Estimaciones simples (caracteres/4, palabras*1.3)
- Comparación de errores

**Conceptos clave:**
- El conteo exacto requiere tokenización real
- Las estimaciones pueden tener errores significativos
- Para facturación precisa, siempre usa `tiktoken`

---

### 03_visualizar_tokens.py
**Visualización de tokens**

Muestra tokens con colores para entender cómo se divide el texto.

- Visualización con colores ANSI
- Desglose detallado de cada token
- Comparación visual entre textos

**Conceptos clave:**
- Cada token se muestra con un color diferente
- Los tokens pueden decodificarse de vuelta a texto
- La visualización ayuda a entender la tokenización

---

### 04_trampas_tokenizacion.py
**Casos extremos y sorpresas**

Muestra casos donde el conteo de tokens puede ser inesperado.

- Emojis (consumen más tokens)
- Código (ratios diferentes)
- Idiomas (chino, japonés, etc.)
- Comparación de ratios

**Conceptos clave:**
- Emojis pueden consumir 2-3 tokens cada uno
- El código se tokeniza de forma diferente
- Idiomas no latinos requieren más tokens
- Siempre mide antes de desplegar

---

### 05_comparar_textos.py
**Comparación y análisis**

Compara cómo diferentes textos se tokenizan.

- Comparación por longitud
- Comparación por idioma
- Ejemplo de optimización (encontrar mejor variante)

**Conceptos clave:**
- Diferentes textos tienen ratios diferentes
- La longitud no es proporcional a tokens
- Comparar variantes ayuda a optimizar prompts

---

### 06_tokens_interactivo.py
**Tokenizador Interactivo**

Herramienta interactiva para experimentar con tokenización.

- Escribe texto y ve el análisis completo
- Visualización con colores en tiempo real
- Estadísticas detalladas (ratios, costos)
- Desglose de cada token individual

**Conceptos clave:**
- Experimenta libremente con diferentes textos
- Visualización inmediata de cómo se tokeniza
- Útil para optimizar prompts antes de producción

---

### 07_limites_contexto.py
**Límites de Contexto**

Demuestra los límites de contexto y qué pasa cuando se exceden.

- Pruebas con diferentes tamaños
- Identificación de límites máximos
- Qué pasa al exceder el límite
- Medición de impacto

**Conceptos clave:**
- Cada modelo tiene un límite máximo
- Exceder causa errores o truncado
- Más grande no siempre es mejor

---

### 08_latencia_contexto.py
**Latencia y Contexto**

Muestra cómo el tamaño del contexto afecta la latencia.

- Medición de latencia según tamaño
- Análisis de crecimiento no lineal
- Impacto en eficiencia
- Cuellos de botella

**Conceptos clave:**
- Más contexto = más latencia
- Crecimiento puede ser exponencial
- Hardware exponencialmente más potente
- Optimizar contexto es clave

---

### 09_tecnicas_contexto.py
**Técnicas para Manejar Contexto**

Demuestra técnicas para procesar textos largos.

- Truncado simple
- Ventanas deslizantes
- Chunking por oraciones
- Comparación de técnicas

**Conceptos clave:**
- Truncado: simple pero pierde información
- Ventanas: procesa todo con solapamiento
- Chunking: mantiene coherencia semántica
- Cada técnica tiene su caso de uso

---

### 10_afecta_prompt.py
**Cómo Afecta el Prompt al Contexto**

Muestra cómo diferentes estructuras afectan el contexto.

- Comparación de estructuras de prompt
- Impacto en tokens y tiempo
- Ejemplos de optimización
- Recomendaciones

**Conceptos clave:**
- Estructura del prompt determina tokens
- Más palabras = más tokens
- Optimización reduce costos
- Medir siempre antes de optimizar

---

### 11_sliding_windows.py
**Sliding Windows (Ventanas Deslizantes)**

Procesa textos largos en ventanas solapadas y agrega resultados.

- Creación de ventanas por tokens
- Medición por ventana (tokens/tiempo) y total
- Resumen agregado

**Conceptos clave:**
- Solapamiento preserva contexto local
- Ajuste de tamaño/solapamiento afecta coste/calidad
- Útil para documentos que exceden el contexto

## Uso

### Ejecutar un ejercicio individual

```bash
# Ejercicios de tokens (solo requieren tiktoken)
python 01_que_es_token.py
python 02_contar_tokens.py
python 03_visualizar_tokens.py
python 04_trampas_tokenizacion.py
python 05_comparar_textos.py
python 06_tokens_interactivo.py

# Ejercicios de contexto (requieren Ollama corriendo)
python 07_limites_contexto.py
python 08_latencia_contexto.py
python 09_tecnicas_contexto.py
python 10_afecta_prompt.py
python 11_sliding_windows.py

# Ejercicios de embeddings
cd embeddings
python 01_inspector_basico.py
python 02_busqueda_titulares.py
python 03_multilingue.py
python 04_deduplicador.py
python 05_tags_inteligentes.py
```

### Flujo de aprendizaje recomendado

**Parte 1: Tokens**
1. **Ejercicio 01**: Entender el concepto básico
2. **Ejercicio 02**: Aprender a contar tokens
3. **Ejercicio 03**: Ver cómo se tokeniza
4. **Ejercicio 04**: Conocer casos extremos
5. **Ejercicio 05**: Analizar y optimizar
6. **Ejercicio 06**: Herramienta interactiva

**Parte 2: Contexto**
7. **Ejercicio 07**: Entender límites de contexto
8. **Ejercicio 08**: Ver impacto en latencia
9. **Ejercicio 09**: Aprender técnicas de manejo
10. **Ejercicio 10**: Optimizar prompts

## Conceptos Importantes

### ¿Qué es un Token?

Un token es la unidad mínima de procesamiento en un texto. Según el algoritmo:
- Puede ser un carácter, sílaba o subcadena
- No siempre coincide con palabras completas
- Cada token tiene un ID numérico único

### Algoritmos de Tokenización

- **BPE (Byte Pair Encoding)**: Combina pares frecuentes de bytes
- **SentencePiece**: Opera a nivel de caracteres Unicode
- **Unigram**: Probabilístico basado en frecuencias

### Impacto en Costos

El recuento de tokens impacta directamente en:
- ⏱️ Tiempo de procesamiento
- 💰 Costo de las APIs
- 🧠 Consumo de memoria
- 📊 Rendimiento del modelo

### Límites de Contexto

- **Ventana de contexto**: Máximo de tokens que un modelo puede procesar simultáneamente
- **Exceder límites**: Puede causar errores, truncado o degradación de calidad
- **Latencia**: Más contexto = más tiempo de procesamiento (a veces exponencial)
- **Técnicas**: Truncado, ventanas deslizantes, chunking para manejar textos largos
- **Optimización**: Estructura del prompt afecta significativamente el uso del contexto

## Trampas Comunes

### ⚠️ Casos Extremos
- Emojis: 2-3 tokens cada uno
- Símbolos especiales: Múltiples tokens
- Código: Tokenización subóptima

### 🌍 Impacto Multilingüe
- Chino, Japonés: Más tokens por carácter
- Árabe, Ruso: Ratios diferentes
- Español/Inglés: Generalmente más eficientes

### 🔧 Herramientas de Debug
- Visualizadores de tokens
- Testing antes de producción
- Monitoreo en tiempo real

## Tips de Optimización

1. **Minimiza emojis** en prompts de producción
2. **Evita símbolos innecesarios**
3. **Optimiza código** antes de incluirlo
4. **Considera el idioma** al planificar costos
5. **Mide siempre** antes de escalar

## Archivos Generados

Algunos ejercicios generan archivos:
- `tokens_visualizacion.txt`: Visualización exportada
- `comparacion_tokens.csv`: Comparaciones en formato CSV

## Notas Importantes

- Usamos `tiktoken` con el encoding `cl100k_base` (el mismo que GPT-4)
- Los resultados son precisos y consistentes
- Puedes cambiar el encoding según necesites (p50k_base, r50k_base, etc.)
- La visualización muestra los tokens reales del modelo

## Próximos Pasos

Después de completar estos ejercicios, podrás:
- Optimizar tus prompts para reducir tokens
- Predecir costos con mayor precisión
- Identificar problemas de tokenización antes de producción
- Tomar decisiones informadas sobre formato de datos

## Recursos Adicionales

- [Documentación de Ollama](https://ollama.com)
- Herramientas de visualización de tokens online
- Tokenizer playgrounds de Hugging Face
- Extensión de navegador para visualizar tokens

---

¡Disfruta explorando el mundo de los tokens! 🚀
