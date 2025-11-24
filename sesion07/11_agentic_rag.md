# Agentic RAG (Planner → Retriever → Verifier → Writer)

## 🎯 Objetivo

Construir un sistema RAG robusto donde la recuperación y generación son procesos agénticos con razonamiento, verificación y reintentos automáticos.

## 🧠 Concepto

**RAG ya NO es "retrieve + generate"**

```
Pregunta → Plan → Retrieve → Verify → (retry?) → Write → Memory
```

**Diferencias fundamentales:**

| RAG Tradicional | Agentic RAG |
|-----------------|-------------|
| 1 búsqueda | Búsquedas iterativas |
| Sin validación | Verificación estricta |
| No aprende | Memoria evolutiva |
| Fallos silenciosos | Reintentos inteligentes |

## 📊 Arquitectura

```
┌─────────────┐
│  Pregunta   │
└──────┬──────┘
       │
       v
┌─────────────┐
│  PLANNER    │ → Estrategia de búsqueda
└──────┬──────┘
       │
       v
┌─────────────┐     ┌──────────────┐
│  RETRIEVER  │────→│ Base Vectorial│
└──────┬──────┘     └──────────────┘
       │
       v
┌─────────────┐
│  VERIFIER   │ → ¿Suficiente?
└──────┬──────┘
       │
   ┌───┴───┐
   NO      SÍ
   │       │
   v       v
Replan   WRITER → Respuesta con citas
   │       │
   └───┐   v
       │  MEMORY → Aprender
       │
       └──→ (retry con nuevo plan)
```

## 🔑 Agentes del Sistema

### 1. Planner (Planificador)

**Responsabilidad**: Estrategia de búsqueda

```
Input: Pregunta compleja
Output:
- Términos de búsqueda
- Cantidad de chunks necesarios
- Estrategia (secuencial, paralelo, etc.)
```

**Ejemplo**:
```
Pregunta: "¿Cómo funcionan sistemas multi-agente?"

Plan:
- Términos: ["multi-agente", "coordinación", "especialización"]
- Chunks: 3-4
- Estrategia: Buscar conceptos generales primero
```

### 2. Retriever (Recuperador)

**Responsabilidad**: Búsqueda inteligente

```
Input: Plan de búsqueda
Acción:
- Ejecutar búsquedas en base vectorial
- Evaluar relevancia
- Puede hacer múltiples búsquedas
Output: Chunks recuperados con scores
```

**Mejoras sobre RAG simple**:
- ✅ Múltiples búsquedas si necesario
- ✅ Refinamiento de términos
- ✅ Scoring de relevancia

### 3. Verifier (Verificador)

**Responsabilidad**: Control de calidad

```
Input: Chunks recuperados + Pregunta
Evalúa:
- ¿Son relevantes?
- ¿Son suficientes?
- ¿Falta información?
Output:
- SUFICIENTE → continuar
- INSUFICIENTE → retry con feedback
- IRRELEVANTE → replanear
```

**Criterios de verificación**:
1. Relevancia al tema
2. Completitud de información
3. Calidad de los chunks
4. Cobertura de la pregunta

### 4. Writer (Escritor)

**Responsabilidad**: Generación con citas

```
Input: Chunks verificados
Genera:
- Respuesta clara y concisa
- Cita cada afirmación [chunk_X]
- SOLO usa información de chunks
Output: Respuesta con citas verificables
```

### 5. Memory (Memoria)

**Responsabilidad**: Aprendizaje continuo

```
Registra:
- Pregunta
- Plan usado
- Chunks efectivos
- Número de intentos
- Éxito/fallo

Mejora:
- Futuros planes
- Selección de términos
- Estrategias de búsqueda
```

## 💡 Conceptos Clave

### Pipeline con Reintentos

```python
intentos = 0
max_intentos = 3

while intentos < max_intentos:
    chunks = retrieve(plan)
    
    if verifier.es_suficiente(chunks):
        respuesta = writer.generar(chunks)
        memory.guardar(exitoso=True)
        return respuesta
    else:
        # Ajustar estrategia
        plan = planner.replanificar(feedback=verifier.gaps)
        intentos += 1

# Si agota intentos
return "Información insuficiente"
```

### Verificación de Suficiencia

**Insuficiente** (requiere retry):
```
Pregunta: "¿Ventajas de multi-agentes?"
Chunks: [chunk sobre definición]
❌ Falta: ejemplos, ventajas concretas
→ Retry con términos "beneficios", "ventajas"
```

**Suficiente** (continuar):
```
Pregunta: "¿Ventajas de multi-agentes?"
Chunks: [definición, beneficios, ejemplos]
✅ Completo → Generar respuesta
```

### Aprendizaje de Experiencias

```json
{
  "pregunta": "¿Cómo funcionan...?",
  "plan": {"términos": ["multi-agente", "coordinación"]},
  "chunks_efectivos": ["chunk_1", "chunk_2"],
  "intentos": 2,
  "exitoso": true
}
```

**Uso futuro**:
```
Pregunta similar → Consultar memoria
→ Usar términos que funcionaron antes
→ Respuesta más rápida y efectiva
```

## 🚀 Cómo Ejecutar

```bash
python 11_agentic_rag.py
```

## 📈 Output Esperado

```
🤖 AGENTIC RAG PIPELINE

📋 FASE 1: Planificación...
Plan creado:
  Términos: ["multi-agente", "verificación"]
  Chunks: 3

🔎 FASE 2: Recuperación (intento 1/3)...
🔍 Buscando chunks...
✅ Recuperados 3 chunks

⚖️ FASE 3: Verificación...
⚠️ Información insuficiente, reintentando...

🔎 FASE 2: Recuperación (intento 2/3)...
🔍 Buscando chunks con términos ampliados...
✅ Recuperados 4 chunks

⚖️ FASE 3: Verificación...
✅ Verificación EXITOSA

✍️ FASE 4: Generación de respuesta...
[Respuesta generada con citas]

💾 FASE 5: Registrando en memoria...
✅ Experiencia registrada

✅ RESPUESTA FINAL
[Respuesta con citas verificables]
📚 Fuentes: [chunk_1, chunk_2, chunk_3]
```

## 🎯 Ventajas sobre RAG Tradicional

| Aspecto | RAG Tradicional | Agentic RAG |
|---------|----------------|-------------|
| Búsqueda | Single-shot | Iterativa |
| Validación | ❌ | ✅ Verificación |
| Reintentos | ❌ | ✅ Automáticos |
| Aprendizaje | ❌ | ✅ Memoria |
| Calidad | Variable | Consistente |
| Producción | Riesgoso | Robusto |

## 🔬 Experimentos Sugeridos

1. **Estrategias adaptativas**: Plan cambia según tipo de pregunta
2. **Verificación semántica**: Usa embeddings para verificar relevancia
3. **Query expansion**: Expandir términos con sinónimos automáticamente
4. **Ensemble retrieval**: Múltiples métodos de búsqueda en paralelo
5. **Feedback humano**: Usuario valida respuestas → mejora memoria

## 🎓 Aplicaciones Reales

### Chatbot Empresarial

```
Usuario: "¿Cuál es nuestra política de vacaciones?"

Agentic RAG:
1. Plan: Buscar en docs de RRHH
2. Retrieve: Políticas, casos especiales
3. Verify: ¿Cubre todos los casos?
4. Write: Respuesta con citas a policy docs
5. Memory: Pregunta frecuente → optimizar
```

### Análisis Legal

```
Abogado: "Precedentes sobre caso X"

Agentic RAG:
1. Plan: Buscar jurisprudencia relevante
2. Retrieve: Casos similares
3. Verify: ¿Suficientes precedentes?
4. Write: Lista con citas exactas
5. Memory: Pattern de búsqueda exitoso
```

### Soporte Técnico

```
Cliente: "Error connecting to database"

Agentic RAG:
1. Plan: Buscar KB de errores
2. Retrieve: Casos similares, soluciones
3. Verify: ¿Solución clara?
4. Write: Pasos con referencias
5. Memory: Error común → priorizar en KB
```

## 🏗️ Arquitectura Avanzada

### Multi-Step Reasoning

```
Pregunta compleja:
"Compare sistemas multi-agente vs monolíticos"

Plan:
  Step 1: Buscar "multi-agente características"
  Step 2: Buscar "sistemas monolíticos características"
  Step 3: Buscar "comparación arquitecturas"
  
Execute sequentially:
  → Retrieve 1 → Verify → Continue
  → Retrieve 2 → Verify → Continue
  → Retrieve 3 → Verify → Continue
  
Synthesize:
  Writer integra los 3 conjuntos de chunks
```

### Self-Correcting RAG

```python
respuesta = writer.generar(chunks)

# Auto-verificación
citas_validas = verificar_citas(respuesta, chunks)

if not citas_validas:
    # Regenerar con feedback
    respuesta = writer.generar(
        chunks,
        feedback="Citas inválidas detectadas"
    )
```

### Confidence Scoring

```python
resultado = {
    "respuesta": "...",
    "confianza": 0.85,  # basado en scores de chunks
    "fuentes": ["chunk_1", "chunk_2"],
    "gaps": []  # información que falta
}

if confianza < 0.7:
    agregar_disclaimer("Información parcial")
```

## ✅ Lo Que Aprenderás

- ✨ RAG agéntico vs tradicional
- ✨ Pipeline con múltiples agentes coordinados
- ✨ Verificación y reintentos automáticos
- ✨ Memoria para aprendizaje continuo
- ✨ Sistema robusto de producción

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐⭐⭐⭐⭐ Muy Alta  
**Tiempo de desarrollo**: 90-120 minutos  
**Aplicaciones reales**: Chatbots, análisis legal, soporte, investigación

## 📊 Comparativa de Evolución

```
RAG V1 (2020):
  retrieve(query) → generate(chunks)
  ❌ Alucinaciones frecuentes

RAG V2 (2022):
  retrieve(query) + prompt("usa solo chunks")
  ⚠️ Mejor, pero no robusto

Agentic RAG (2024):
  plan → retrieve → verify → (retry) → write → memory
  ✅ Producción-ready
```

## 🔗 Siguiente Paso

👉 **Ejemplo 12**: Equipo Forense Completo (integración de TODOS los patrones)


