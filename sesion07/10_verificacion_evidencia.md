# Verificación de Evidencia (Evidence Checking Agents)

## 🎯 Objetivo

Implementar verificación rigurosa de que cada afirmación esté respaldada por evidencia real, eliminando alucinaciones elegantes.

## 🧠 Concepto

**Antídoto contra la "alucinación elegante"**

```
Afirmación → Extraer citas → ¿Existen? → ¿Soportan? → Aprobar/Rechazar
```

**¿Qué es alucinación elegante?**
- Respuestas que suenan convincentes y bien escritas
- Pero carecen de soporte factual real
- El gran problema de los LLMs

**Solución**: Verificación estricta automática

## 📊 Arquitectura

```
┌─────────────────┐
│    Pregunta     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Generador     │ → Respuesta con citas [doc_X]
└────────┬────────┘
         │
         v
┌─────────────────┐
│Extraer Citas    │ → [doc_1], [doc_2], ...
└────────┬────────┘
         │
         v
┌─────────────────┐
│¿Citas existen?  │
└────────┬────────┘
         │
    ┌────┴────┐
    NO        SÍ
    │         │
    v         v
RECHAZAR  ┌──────────────┐
          │¿Citas        │
          │soportan      │
          │afirmaciones? │
          └──────┬───────┘
                 │
            ┌────┴────┐
            NO        SÍ
            │         │
            v         v
        RECHAZAR  APROBAR
```

## 🔑 Componentes del Sistema

### Motor de Verificación

**Funciones principales:**

1. **extraer_citas(texto)**
   - Busca patrones `[doc_X]`
   - Retorna lista de citas

2. **verificar_existencia_citas(citas)**
   - Valida que cada doc_X exista
   - Retorna errores si no existen

3. **verificar_soporte_afirmacion(afirmacion, cita)**
   - Verifica que el documento soporta la afirmación
   - Usa similitud semántica o palabras clave
   - Retorna bool + razón

4. **generar_reporte_verificacion()**
   - Reporte completo de verificación
   - Estado de cada cita y afirmación

### Niveles de Verificación

| Nivel | Verificación | Strictness |
|-------|--------------|-----------|
| 1 | ¿Citas existen? | Básico |
| 2 | ¿Citas mencionan tema? | Medio |
| 3 | ¿Citas soportan afirmación específica? | Alto |
| 4 | ¿Evidencia suficiente? | Muy Alto |

## 💡 Conceptos Clave

### Sin vs Con Verificación

**Sin verificación**:
```
Pregunta: "¿Mejora la productividad?"
Respuesta: "Sí, estudios muestran mejora del 40% [doc_1]"

Problema: doc_1 no existe o no dice eso
→ Alucinación elegante
```

**Con verificación**:
```
Pregunta: "¿Mejora la productividad?"
Respuesta: "Sí, estudios muestran mejora del 40% [doc_1]"

Verificación:
1. ¿doc_1 existe? ✅
2. ¿doc_1 menciona "40%"? ✅
3. ¿doc_1 habla de productividad? ✅
→ APROBADO
```

### Tipos de Fallos

**1. Cita Inexistente**
```
"Según [doc_99]..." 
→ doc_99 no existe
❌ RECHAZO inmediato
```

**2. Cita Irrelevante**
```
Afirmación: "Python es rápido"
Cita: [doc_5] sobre JavaScript
→ doc_5 no soporta la afirmación
❌ RECHAZO
```

**3. Interpretación Errónea**
```
Doc: "El rendimiento puede mejorar"
Afirmación: "El rendimiento siempre mejora [doc_1]"
→ Sobregeneralización
❌ RECHAZO
```

### Métodos de Verificación

**Nivel 1 - Simple (ejemplo)**:
```python
# Palabras clave
if palabra_afirmacion in documento:
    return True
```

**Nivel 2 - Embeddings**:
```python
# Similitud semántica
sim = cosine_similarity(
    embed(afirmacion),
    embed(documento)
)
return sim > threshold
```

**Nivel 3 - Entailment**:
```python
# Modelo de implicación lógica
entails = entailment_model(
    premise=documento,
    hypothesis=afirmacion
)
return entails == "ENTAILMENT"
```

**Nivel 4 - LLM Verificador**:
```python
# LLM especializado
prompt = f"""
Documento: {documento}
Afirmación: {afirmacion}
¿El documento soporta la afirmación?
"""
return llm(prompt) == "SÍ"
```

## 🚀 Cómo Ejecutar

```bash
python 10_verificacion_evidencia.py
```

## 📈 Output Esperado

```
🔍 SISTEMA DE VERIFICACIÓN DE EVIDENCIA

📚 Documentos disponibles:
[doc_1]: Los sistemas multi-agente permiten...
[doc_2]: CrewAI es un framework...

📝 FASE 1: Generando respuesta con citas...
📄 Respuesta: "Los sistemas multi-agente mejoran 
eficiencia en 40% [doc_1]..."

🔎 FASE 2: Extrayendo afirmaciones...
Afirmaciones: 3

⚖️ FASE 3: Verificación automática...
Citas encontradas: [doc_1]
✅ Citas válidas: True

Verificaciones:
- Afirmación 1: "mejoran eficiencia 40%"
  Cita: doc_1
  ✅ doc_1 soporta (80% match)

✅ RESPUESTA APROBADA
Todas las afirmaciones respaldadas por evidencia.
```

## 🎯 Importancia Crítica

### Por Qué es Fundamental

| Sin Verificación | Con Verificación |
|------------------|------------------|
| Alucinaciones frecuentes | Eliminadas |
| Confianza baja | Confianza alta |
| No apto para producción | Listo para producción |
| Riesgo legal/reputacional | Mitigado |

### Casos Críticos

**Medicina**: 
```
"Este tratamiento es efectivo [doc_X]"
→ DEBE ser verificable
```

**Legal**:
```
"El precedente establece [caso_Y]"
→ DEBE existir y decir eso
```

**Financiero**:
```
"ROI proyectado 20% [reporte_Z]"
→ DEBE estar en el reporte
```

## 🔬 Experimentos Sugeridos

1. **Embeddings reales**: Usa OpenAI embeddings para similitud
2. **Entailment model**: Integra RoBERTa o BART para implicación
3. **LLM verificador**: Usa GPT-4 solo para verificar
4. **Threshold tuning**: Ajusta umbrales de similitud
5. **Feedback loop**: Re-generar si falla verificación

## 🎓 Aplicaciones Reales

### RAG de Producción

```
Usuario: Pregunta
  ↓
RAG retrieve → chunks
  ↓
LLM genera → respuesta con citas
  ↓
Verificador → valida cada cita
  ↓
¿Aprobado?
  - SÍ → Enviar respuesta
  - NO → Re-generar con feedback
```

### Chatbots Empresariales

```
Cliente: "¿Cuál es la política de devolución?"
Bot: "30 días sin preguntas [policy_doc]"
Verificador: ✅ policy_doc dice exactamente eso
→ Respuesta confiable
```

### Análisis Legal

```
Abogado: "¿Qué dice el precedente X?"
Sistema: "El caso establece Y [caso_X]"
Verificador: ✅ Texto literal del caso
→ Citable en corte
```

## 🏗️ Arquitectura Avanzada

### Pipeline Completo

```python
def respuesta_verificada(pregunta):
    # 1. Retrieve
    docs = retrieve(pregunta)
    
    # 2. Generate con citas
    respuesta = generate(pregunta, docs, require_citations=True)
    
    # 3. Verificar
    reporte = verificar(respuesta, docs)
    
    # 4. Decidir
    if reporte.aprobado:
        return respuesta
    else:
        # Re-intentar con feedback
        return generate(
            pregunta, 
            docs, 
            feedback=reporte.errores
        )
```

### Verificación Multi-Nivel

```python
# Nivel 1: Existencia (rápido, determinista)
if not citas_existen(respuesta):
    return RECHAZO_INMEDIATO

# Nivel 2: Similitud (rápido, aproximado)
if similitud < 0.7:
    FLAG_REVISAR

# Nivel 3: LLM verificador (lento, preciso)
if not llm_verifica(afirmacion, doc):
    return RECHAZO
```

## ✅ Lo Que Aprenderás

- ✨ Verificación automática de evidencia
- ✨ Detección de alucinaciones
- ✨ Validación cita por cita
- ✨ Crítico para sistemas de producción
- ✨ Fundamento de Agentic RAG robusto

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐⭐⭐⭐ Alta  
**Tiempo de desarrollo**: 80-90 minutos  
**Aplicaciones reales**: RAG, chatbots, medicina, legal, finanzas

## 🆚 Evolución de Calidad

```
V1 - RAG básico:
  Retrieve → Generate
  → Alucinaciones frecuentes

V2 - RAG con prompt:
  Retrieve → Generate ("usa solo docs")
  → Menos alucinaciones, no eliminadas

V3 - RAG con verificación (AQUÍ):
  Retrieve → Generate → Verificar → Aprobar/Rechazar
  → Alucinaciones eliminadas
```

## 📊 Métricas de Calidad

```python
# Sin verificación
precision = 0.65  # 65% correcto
alucinaciones = 0.35  # 35% inventado

# Con verificación
precision = 0.95  # 95% correcto
alucinaciones = 0.05  # 5% inventado (y detectado)
```

## 🔗 Siguiente Paso

👉 **Ejemplo 11**: Agentic RAG (sistema completo: Planner → Retriever → Verifier → Writer)


