# Integración con Langfuse - Observabilidad de Agentes

## Concepto

**Langfuse** es una plataforma de observabilidad para aplicaciones LLM que permite:
- 📊 **Trazas detalladas** de conversaciones y agentes
- 💰 **Monitoreo de costes** y uso de tokens
- 📈 **Métricas de rendimiento** (latencia, éxito/fallo)
- 🔍 **Debugging avanzado** de prompts y respuestas
- 📉 **Análisis comparativo** entre modelos

Este ejercicio integra CrewAI con Langfuse para obtener visibilidad completa de la ejecución de agentes.

## ¿Por Qué Usar Langfuse?

### Sin Observabilidad ❌
```
Ejecutas un crew → Ves solo el resultado final
- No sabes cuántos tokens consumió
- No sabes qué modelo usó cada agente
- No puedes comparar ejecuciones
- Difícil debuggear problemas
- No tienes métricas de coste
```

### Con Langfuse ✅
```
Ejecutas un crew → Ves TODO en detalle
- Traza completa de cada agente
- Tokens de entrada/salida por llamada
- Latencia de cada operación
- Coste estimado en tiempo real
- Comparación entre ejecuciones
- Metadata personalizada
```

## Arquitectura de la Integración

```
┌─────────────────┐
│   CrewAI        │
│   (Agentes)     │
└────────┬────────┘
         │ @observe decorator
         ↓
┌─────────────────┐
│   Langfuse      │
│   SDK           │
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│ Langfuse Cloud  │
│ (Dashboard)     │
└─────────────────┘
```

## Configuración Inicial

### Paso 1: Crear Cuenta en Langfuse Cloud

1. Ve a https://cloud.langfuse.com
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto

### Paso 2: Obtener API Keys

1. En tu proyecto, ve a **Settings** → **API Keys**
2. Haz clic en **Create new API keys**
3. Copia:
   - **Public Key** (comienza con `pk-lf-`)
   - **Secret Key** (comienza con `sk-lf-`)

### Paso 3: Configurar Variables de Entorno

Agrega a tu archivo `.env`:

```env
# Langfuse Cloud
LANGFUSE_PUBLIC_KEY=pk-lf-tu-public-key-aqui
LANGFUSE_SECRET_KEY=sk-lf-tu-secret-key-aqui
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenAI (necesario para los agentes)
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### Paso 4: Instalar Langfuse SDK

```bash
pip install langfuse
```

## Uso del Decorador @observe

El decorador `@observe` de Langfuse captura automáticamente las ejecuciones:

```python
from langfuse.decorators import observe, langfuse_context

@observe(name="Crear Agente")
def crear_agente(role: str, model: str):
    # Agregar metadata personalizada
    langfuse_context.update_current_observation(
        metadata={
            "role": role,
            "model": model
        }
    )
    
    agent = Agent(
        role=role,
        goal="...",
        backstory="...",
        llm=LLM(model=model)
    )
    
    return agent

@observe(name="Ejecutar Crew")
def ejecutar_crew(crew: Crew):
    resultado = crew.kickoff()
    
    # Registrar el output
    langfuse_context.update_current_observation(
        output=str(resultado)
    )
    
    return resultado
```

## Experimentos Incluidos

### Experimento 1: Comparación de Modelos

Compara GPT-4.1 vs GPT-4.1-mini en la misma tarea:

```python
# GPT-4.1 (más potente, mejor razonamiento)
agente_gpt4 = crear_agente("Investigador", "gpt-4.1")

# GPT-4.1-mini (más rápido y económico)
agente_gpt_mini = crear_agente("Investigador", "gpt-4.1-mini")
```

**Qué observar en Langfuse:**
- Diferencia de tokens consumidos
- Diferencia de latencia (~2-3x más rápido el mini)
- Diferencia de coste (~94% más barato el mini: $0.15 vs $2.50 por 1M tokens)
- Calidad de las respuestas

### Experimento 2: Crew Multi-Agente

Crea un workflow de 3 agentes:
1. **Investigador** (GPT-4.1) → Recopila información
2. **Analista** (GPT-4.1) → Extrae insights
3. **Escritor** (GPT-4.1-mini) → Redacta artículo

**Qué observar en Langfuse:**
- Traza completa del flujo secuencial
- Cómo se pasa información entre tareas
- Tokens consumidos por cada agente
- Tiempo total vs tiempo por agente

### Experimento 3: Efecto de Temperatura

Compara el mismo modelo con temperaturas diferentes:
- **Temperatura 0.1** → Más determinista, consistente
- **Temperatura 0.9** → Más creativo, variable

**Qué observar en Langfuse:**
- Variabilidad en las respuestas
- Tokens generados (pueden variar)
- Creatividad vs precisión

## Ejecución

```bash
python sesion07/16_integracion_langfuse.py
```

**Salida esperada:**
```
🔍 INTEGRACIÓN CREWAI + LANGFUSE
===============================================================
✅ Langfuse inicializado correctamente
   Host: https://cloud.langfuse.com

📊 Ejecutando 3 experimentos con trazas en Langfuse...

🔬 EXPERIMENTO 1: COMPARACIÓN DE MODELOS
📊 Test 1: GPT-4.1
✅ GPT-4.1 completado: 847 caracteres

📊 Test 2: GPT-4.1-mini
✅ GPT-4.1-mini completado: 623 caracteres

🔬 EXPERIMENTO 2: CREW MULTI-AGENTE
🚀 Ejecutando crew...
✅ Crew completado

🔬 EXPERIMENTO 3: EFECTO DE LA TEMPERATURA
🌡️  Test 1: Temperatura 0.1 (Determinista)
🌡️  Test 2: Temperatura 0.9 (Creativo)

✅ TODOS LOS EXPERIMENTOS COMPLETADOS
```

## Visualizar en Langfuse Dashboard

### 1. Acceder al Dashboard

1. Ve a https://cloud.langfuse.com
2. Selecciona tu proyecto
3. Navega a **Traces** en el menú lateral

### 2. Vista de Trazas

Verás una lista de todas las ejecuciones:

```
┌─────────────────────────────────────────────┐
│ Traces                                      │
├─────────────────────────────────────────────┤
│ ○ Experimento: Comparación de Modelos      │
│   2 spans • 4,523 tokens • $0.032          │
│   GPT-4.1 vs GPT-4.1-mini • hace 2 min     │
├─────────────────────────────────────────────┤
│ ○ Experimento: Crew Multi-Agente           │
│   7 spans • 8,234 tokens • $0.089          │
│   3 agentes • hace 5 min                   │
├─────────────────────────────────────────────┤
│ ○ Experimento: Temperaturas Diferentes     │
│   2 spans • 1,876 tokens • $0.021          │
│   Temp 0.1 vs 0.9 • hace 8 min            │
└─────────────────────────────────────────────┘
```

### 3. Vista Detallada de una Traza

Al hacer clic en una traza, verás:

**Timeline de Ejecución:**
```
┌─ Experimento: Crew Multi-Agente ────────────┐
│                                              │
│  ├─ Crear Agente (Investigador)            │
│  │  └─ metadata: model=gpt-4.1              │
│  │                                          │
│  ├─ Crear Agente (Analista)                │
│  │  └─ metadata: model=gpt-4.1              │
│  │                                          │
│  ├─ Crear Agente (Escritor)                │
│  │  └─ metadata: model=gpt-4.1-mini         │
│  │                                          │
│  └─ Ejecutar Crew                           │
│     ├─ input: "Investiga sobre IA..."      │
│     ├─ tokens: 8,234 (6,123 in / 2,111 out)│
│     ├─ latencia: 23.4s                      │
│     ├─ coste: $0.089                        │
│     └─ output: "Artículo final..."          │
└──────────────────────────────────────────────┘
```

### 4. Métricas Agregadas

En la sección **Analytics**, verás:

- **Tokens por día/hora**
- **Coste acumulado**
- **Latencia promedio**
- **Tasa de error**
- **Modelos más usados**

### 5. Comparar Ejecuciones

Selecciona múltiples trazas y compara:

| Métrica | GPT-4.1 | GPT-4.1-mini | Diferencia |
|---------|---------|--------------|------------|
| **Tokens entrada** | 1,234 | 1,234 | 0% |
| **Tokens salida** | 856 | 623 | -27% |
| **Latencia** | 3.8s | 1.5s | -61% |
| **Coste** | $0.012 | $0.001 | -92% |

**💡 Conclusión**: GPT-4.1-mini es ~92% más barato y ~2.5x más rápido que GPT-4.1, ideal para tareas simples.

## Funcionalidades Avanzadas

### 1. Sessions

Agrupa trazas relacionadas:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Crear sesión
with langfuse.start_session(
    user_id="usuario-123",
    session_id="experimento-prod-001"
):
    # Todas las trazas aquí se agrupan
    resultado = crew.kickoff()
```

### 2. Tags y Filtros

Agrega tags para filtrar:

```python
langfuse_context.update_current_observation(
    tags=["producción", "experimento-a/b", "v1.2.0"]
)
```

### 3. Scores y Evaluación

Evalúa manualmente la calidad:

```python
langfuse_context.score_current_observation(
    name="calidad",
    value=0.85,  # 0.0 - 1.0
    comment="Respuesta precisa y bien estructurada"
)
```

### 4. Prompts Versionados

Guarda y versiona prompts:

```python
from langfuse import Langfuse

langfuse = Langfuse()

# Guardar prompt
langfuse.create_prompt(
    name="investigador-prompt",
    prompt="Investiga sobre {{topic}} y proporciona {{num_items}} ejemplos",
    labels=["investigación", "v1"]
)

# Usar prompt guardado
prompt = langfuse.get_prompt("investigador-prompt")
```

## Casos de Uso en Producción

### 1. Monitoreo de Costes

- Identifica qué agentes son más costosos
- Optimiza uso de modelos (GPT-4 solo cuando necesario)
- Establece alertas de coste

### 2. Debugging

- Encuentra qué agente falla en un workflow
- Ve los prompts exactos enviados
- Identifica patrones en errores

### 3. A/B Testing

- Compara diferentes configuraciones de agentes
- Evalúa impacto de cambios en prompts
- Mide mejoras en latencia

### 4. Compliance y Auditoría

- Registra todas las interacciones
- Exporta logs para auditoría
- Cumple requisitos de trazabilidad

## Mejores Prácticas

### ✅ DO

- Usar `@observe` en funciones clave
- Agregar metadata descriptiva
- Nombrar trazas de forma clara
- Usar tags para categorizar
- Flush al finalizar (`langfuse.flush()`)

### ❌ DON'T

- No loggear información sensible
- No usar en loops muy frecuentes (coste de red)
- No abusar de metadata (aumenta payload)
- No olvidar manejar errores

## Troubleshooting

### Error: "Invalid API key"

**Solución**: Verifica que las keys en `.env` son correctas y están activas.

### Error: "Connection timeout"

**Solución**: Verifica conexión a internet. Langfuse cloud requiere HTTPS saliente.

### Trazas no aparecen

**Solución**: 
```python
# Asegurar flush al final
langfuse.flush()

# O esperar un poco (se envían en batch)
import time
time.sleep(2)
```

## Recursos Adicionales

- **Documentación oficial**: https://langfuse.com/docs
- **Python SDK**: https://langfuse.com/docs/sdk/python
- **Ejemplos**: https://github.com/langfuse/langfuse-python
- **Discord**: Comunidad de Langfuse

## Próximos Pasos

Después de este ejercicio:

1. Experimenta con tus propios agentes
2. Configura alertas en Langfuse
3. Crea dashboards personalizados
4. Integra con tus pipelines de CI/CD
5. Exporta datos para análisis adicional

¡La observabilidad es clave para sistemas de producción! 🔍

