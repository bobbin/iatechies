# Agentes con Reglas Híbridas (Simbólico + LLM)

## 🎯 Objetivo

Combinar decisiones deterministas (reglas duras) con razonamiento probabilístico (LLM) para crear sistemas más robustos y predecibles.

## 🧠 Concepto

**No todo debe depender del LLM.**

```
Reglas Duras (deterministas)
     +
Razonamiento LLM (probabilístico)
     =
Sistema Híbrido Robusto
```

**¿Por qué es importante?**
- Las reglas aportan **estabilidad**
- El LLM aporta **flexibilidad**
- Juntos cubren casos críticos y creativos

## 📊 Arquitectura

```
         Solicitud
             │
             v
    ┌────────────────┐
    │ FASE 1: REGLAS │ → Validación inicial
    │  (Determinista)│    (fecha, fuente, longitud)
    └───────┬────────┘
            │ ✅ Pasa
            v
    ┌────────────────┐
    │ FASE 2: LLM    │ → Análisis y resumen
    │  (Probabilístico)│   con citas
    └───────┬────────┘
            │
            v
    ┌────────────────┐
    │ FASE 3: REGLAS │ → Validar citas
    │  (Determinista)│    existen en docs
    └───────┬────────┘
            │ ✅ Pasa
            v
    ┌────────────────┐
    │ FASE 4: LLM    │ → Revisión calidad
    │  (Probabilístico)│
    └───────┬────────┘
            │
            v
    ┌────────────────┐
    │ FASE 5: REGLAS │ → Formato final
    │  (Determinista)│    + disclaimer
    └────────────────┘
```

## 🔑 Componentes del Sistema

### Motor de Reglas (Simbólico)

**Reglas implementadas:**

| Regla | Validación | Consecuencia |
|-------|------------|--------------|
| REGLA_001 | Fecha obligatoria | Rechazo inmediato |
| REGLA_002 | Fuente en whitelist | Rechazo inmediato |
| REGLA_003 | Longitud mínima 50 chars | Rechazo inmediato |
| REGLA_004 | Sin palabras prohibidas | Rechazo inmediato |
| REGLA_005 | Citas válidas | Warning/rechazo |

### Agentes LLM

**1. Analizador**
- Genera resumen con citas
- Razonamiento flexible
- Output: Texto con [referencias]

**2. Revisor**
- Valida coherencia
- Verifica calidad
- Output: APROBADO o mejoras

## 💡 Conceptos Clave

### ¿Cuándo usar Reglas vs LLM?

**Usa REGLAS para:**
- ✅ Validaciones críticas de seguridad
- ✅ Límites estrictos (fechas, formatos)
- ✅ Decisiones binarias (sí/no)
- ✅ Consistencia absoluta

**Usa LLM para:**
- ✅ Razonamiento complejo
- ✅ Análisis de contenido
- ✅ Generación creativa
- ✅ Comprensión contextual

### Ejemplo de Híbrido

**Escenario**: Validar una respuesta con citas

```python
# ❌ Solo LLM (no confiable)
"Por favor asegúrate de que las citas existan"
→ Puede alucinar o ignorar

# ✅ Híbrido
1. LLM genera respuesta con citas
2. REGLA valida que [1], [2] existen en documentos
3. Si falla → rechazo automático
```

## 🚀 Cómo Ejecutar

```bash
python 03_agentes_con_reglas.py
```

## 📈 Output Esperado

### Caso 1: Solicitud Válida
```
📋 FASE 1: Validación... ✅
🤖 FASE 2: Análisis LLM...
🔍 FASE 3: Validar citas... ✅
👁️ FASE 4: Revisión... APROBADO
🔒 FASE 5: Formato final
✅ RESULTADO: [respuesta formateada]
```

### Caso 2: Solicitud Inválida
```
📋 FASE 1: Validación...
❌ REGLA_001: Falta fecha en la solicitud
❌ SOLICITUD RECHAZADA
```

## 🎯 Ventajas del Enfoque Híbrido

| Aspecto | Solo LLM | Solo Reglas | Híbrido |
|---------|----------|-------------|---------|
| Flexibilidad | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| Predicibilidad | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Seguridad | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Creatividad | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ |

## 🔬 Experimentos Sugeridos

1. **Agrega más reglas**: Límite de tiempo, validación de formato
2. **Prueba casos límite**: Textos en el borde de la longitud mínima
3. **Implementa retry**: Si citas fallan, pide corrección al LLM
4. **Logs de auditoría**: Registra qué reglas pasaron/fallaron

## 🎓 Aplicaciones Reales

- **Sistemas financieros**: Reglas de compliance + análisis LLM
- **Healthcare**: Validaciones médicas + diagnóstico asistido
- **Legal**: Verificación de precedentes + análisis de casos
- **Seguridad**: Firewalls deterministas + detección de anomalías

## ✅ Lo Que Aprenderás

- ✨ No todo debe depender del LLM
- ✨ Reglas aportan estabilidad crítica
- ✨ Combinar ambos es más robusto
- ✨ Validaciones críticas deben ser deterministas

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐⭐ Media  
**Tiempo de desarrollo**: 30-40 minutos  
**Aplicaciones reales**: Finanzas, salud, legal, seguridad

## 🆚 Comparación con Ejemplos Anteriores

| Ejemplo | Patrón | Fortaleza |
|---------|--------|-----------|
| 01 - Reflexivos | Auto-mejora | Calidad iterativa |
| 02 - Self-Prompt | Auto-optimización | Mejores queries |
| **03 - Híbrido** | **Reglas + LLM** | **Robustez + flexibilidad** |

## 🔗 Siguiente Paso

👉 **Ejemplo 04**: Agentes Competitivos (múltiples soluciones + juez)


