# Self-Prompt Editing (Optimización Automática de Consultas)

## 🎯 Objetivo

Crear agentes que aprenden a hacer mejores preguntas cuando detectan errores o resultados insuficientes.

## 🧠 Concepto

El sistema adapta sus propias consultas basándose en el feedback de resultados.

```
Consulta → Buscar → ¿Éxito?
                       ↓ No
                   Optimizar → Nueva Consulta → Buscar
```

**¿Por qué es importante?**
- Los LLMs no siempre hacen la pregunta correcta al primer intento
- Los errores pueden detectarse y corregirse automáticamente
- El sistema se vuelve más robusto sin intervención humana

## 📊 Arquitectura

```
┌─────────────────┐
│ Pregunta Usuario│
└────────┬────────┘
         │
         v
┌─────────────────┐
│   Buscador      │ → Búsqueda inicial
└────────┬────────┘
         │
         v
   ¿Resultados OK?
    /          \
  Sí            No
   │             │
   │             v
   │      ┌─────────────┐
   │      │ Optimizador │ → Mejora query
   │      └──────┬──────┘
   │             │
   │             v
   │      Nueva búsqueda
   │             │
   └─────────────┘
         │
         v
┌─────────────────┐
│  Respondedor    │ → Respuesta final
└─────────────────┘
```

## 🔑 Agentes del Sistema

### 1. Buscador
- **Rol**: Ejecutar búsquedas
- **Input**: Query del usuario
- **Output**: Resultados + metadatos de calidad

### 2. Optimizador de Consultas
- **Rol**: Mejorar queries fallidas
- **Técnicas**:
  - Agregar sinónimos
  - Reformular más amplio/específico
  - Incluir contexto adicional
- **Output**: Nueva query optimizada

### 3. Respondedor
- **Rol**: Sintetizar información encontrada
- **Output**: Respuesta final al usuario

## 💡 Conceptos Clave

### Detección Automática de Errores

El sistema identifica tres tipos de problemas:

1. **SIN_RESULTADOS**: No se encontró nada
2. **POCOS_RESULTADOS**: Insuficiente información
3. **EXITO**: Resultados satisfactorios

### Técnicas de Optimización

**Ejemplo de transformación**:

❌ **Query original** (ambigua):
```
"¿Qué es programación?"
```

✅ **Query optimizada**:
```
"¿Qué es Python y cuáles son sus características?"
```

### Bucle de Retroalimentación

```python
while resultados_insuficientes:
    query = optimizar_query(query_anterior, error_detectado)
    resultados = buscar(query)
```

## 🚀 Cómo Ejecutar

```bash
python 02_self_prompt_editing.py
```

## 📈 Output Esperado

### Caso 1: Query Ambigua (se optimiza)
```
🔍 Pregunta: "¿Qué es programación?"
⚠️  Estado: SIN_RESULTADOS
✨ Optimizando...
🔄 Nueva query: "¿Qué es Python y sus características?"
✅ Estado: EXITO (3 resultados)
```

### Caso 2: Query Específica (funciona directo)
```
🔍 Pregunta: "¿Qué es CrewAI?"
✅ Estado: EXITO (3 resultados)
📝 Respuesta generada
```

## 🔬 Experimentos Sugeridos

1. **Prueba queries vagas**: "inteligencia", "código", "datos"
2. **Agrega más técnicas**: Expansión con sinónimos, desambiguación
3. **Limita intentos**: Máximo 3 re-intentos
4. **Logs de aprendizaje**: Guarda query original → query optimizada

## 🎯 Aplicaciones Reales

- **RAG Systems**: Cuando retrieval falla, reformular query
- **Search Engines**: Sugerencias automáticas de búsqueda
- **APIs**: Retry con parámetros ajustados
- **Chatbots**: Clarificar preguntas del usuario

## ✅ Lo Que Aprenderás

- ✨ Agentes no son estáticos, pueden mejorar
- ✨ Detección de errores en tiempo real
- ✨ Auto-corrección sin intervención humana
- ✨ Patrón aplicable a múltiples dominios

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐⭐ Baja-Media  
**Tiempo de desarrollo**: 20-30 minutos  
**Aplicaciones reales**: RAG, búsquedas, APIs, chatbots

## 🆚 Comparación con Ejemplo 01

| Aspecto | Reflexivos | Self-Prompt |
|---------|-----------|-------------|
| Foco | Mejorar contenido | Mejorar preguntas |
| Trigger | Siempre critica | Solo si falla |
| Objetivo | Calidad del output | Efectividad del input |

## 🔗 Siguiente Paso

👉 **Ejemplo 03**: Agentes con Reglas Híbridas (determinismo + LLM)


