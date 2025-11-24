# Configuración de Costes en Langfuse

## Problema: No se muestran los costes

Si ves las trazas en Langfuse pero **no se calculan los costes**, es porque Langfuse necesita dos cosas:

### 1. **Nombre Exacto del Modelo**

Langfuse tiene una base de datos de precios de modelos. El nombre del modelo debe coincidir **exactamente** con el que Langfuse reconoce.

#### Modelos Actuales de OpenAI (2025):

- `gpt-4.1` ✅ (Modelo principal, más potente)
- `gpt-4.1-mini` ✅ (Versión económica y rápida)

**IMPORTANTE**: Los modelos anteriores (gpt-4o, gpt-4-turbo, gpt-3.5-turbo) están obsoletos o son muy caros. Solo usa GPT-4.1 y GPT-4.1-mini.

### 2. **Tipo de Observación Correcto**

Para que Langfuse calcule costes, debes usar:
- `langfuse.start_generation()` en lugar de `langfuse.start_span()`

La diferencia:
- **`start_span()`**: Observación genérica, no calcula costes
- **`start_generation()`**: Observación de LLM, calcula costes automáticamente

### 3. **Información de Uso (opcional pero recomendado)**

Aunque Langfuse puede estimar costes por el modelo, es mejor proporcionar el uso exacto:

```python
generation.update(
    output=resultado,
    usage={
        "input": 1234,      # tokens de entrada
        "output": 567,      # tokens de salida
        "total": 1801       # total
    }
)
```

## Solución Rápida

### Paso 1: Verificar el Modelo en tu Código

Abre `16_integracion_langfuse.py` y asegúrate de usar solo los modelos actuales:

```python
# ✅ CORRECTO - Modelos actuales (2025)
agente = crear_agente("Investigador", "gpt-4.1", 0.3)
agente = crear_agente("Escritor", "gpt-4.1-mini", 0.7)

# ❌ OBSOLETOS - No usar
agente = crear_agente("Investigador", "gpt-4o", 0.3)      # Obsoleto
agente = crear_agente("Investigador", "gpt-4-turbo", 0.3)  # Muy caro
agente = crear_agente("Investigador", "gpt-3.5-turbo", 0.3) # Obsoleto
```

### Paso 2: Verificar que usas `start_generation()`

```python
# ❌ NO calcula costes
span = langfuse.start_span(name="Test", metadata={"modelo": "gpt-4.1"})

# ✅ SÍ calcula costes
generation = langfuse.start_generation(
    name="Test GPT-4.1",
    model="gpt-4.1",  # Nombre exacto del modelo
    model_parameters={"temperature": 0.3},
    input="Tu prompt aquí"
)
```

### Paso 3: Configurar Modelos en Langfuse (CRÍTICO)

Como `gpt-4.1` y `gpt-4.1-mini` son modelos muy recientes (2025), **Langfuse Cloud puede no tenerlos en su base de datos aún**. Debes agregarlos manualmente:

#### Agregar GPT-4.1:

1. Ve a **Langfuse Dashboard** → **Settings** → **Model Definitions**
2. Haz clic en **+ Add Model**
3. Configura GPT-4.1:
   - **Model Name**: `gpt-4.1`
   - **Match Pattern**: `gpt-4.1` (exacto)
   - **Input Price**: $2.50 per 1M tokens
   - **Output Price**: $10.00 per 1M tokens
   - **Unit**: `TOKENS`
4. Haz clic en **Save**

#### Agregar GPT-4.1-mini:

1. Haz clic en **+ Add Model** de nuevo
2. Configura GPT-4.1-mini:
   - **Model Name**: `gpt-4.1-mini`
   - **Match Pattern**: `gpt-4.1-mini` (exacto)
   - **Input Price**: $0.15 per 1M tokens
   - **Output Price**: $0.60 per 1M tokens
   - **Unit**: `TOKENS`
3. Haz clic en **Save**

**⚠️ IMPORTANTE**: Sin estos modelos configurados, Langfuse mostrará las trazas pero **no calculará costes**.

## Verificación

Después de hacer los cambios:

1. Ejecuta de nuevo el script
2. Ve a Langfuse Dashboard
3. Busca la traza más reciente
4. Deberías ver:
   - ✅ Model: `gpt-4o`
   - ✅ Tokens: input/output/total
   - ✅ Cost: $0.00XX

## Precios de Referencia (2025)

| Modelo | Input (por 1M tokens) | Output (por 1M tokens) | Uso Recomendado |
|--------|----------------------|------------------------|-----------------|
| `gpt-4.1` | $2.50 | $10.00 | Tareas complejas, razonamiento avanzado |
| `gpt-4.1-mini` | $0.15 | $0.60 | Tareas simples, alta velocidad, bajo coste |

**Fuente**: [OpenAI Pricing](https://platform.openai.com/pricing)

### 💡 Comparación de Rendimiento

- **GPT-4.1**: ~2x más rápido que GPT-4 Turbo, mejor calidad
- **GPT-4.1-mini**: ~3x más rápido que GPT-3.5, mejor calidad, más barato

### 🎯 Cuándo Usar Cada Uno

- **Usa GPT-4.1** para:
  - Análisis complejos
  - Razonamiento multicapa
  - Tareas críticas que requieren máxima precisión

- **Usa GPT-4.1-mini** para:
  - Redacción y resúmenes
  - Clasificación y categorización
  - Tareas repetitivas
  - Prototipos y desarrollo
  - Optimización de costes

## Recursos

- [Langfuse Model Pricing](https://langfuse.com/docs/model-usage-and-cost)
- [OpenAI Pricing](https://openai.com/pricing)
- [Langfuse Generations](https://langfuse.com/docs/tracing/generations)

