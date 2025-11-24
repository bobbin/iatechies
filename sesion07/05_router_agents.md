# Router Agents (Detección de Intención y Selección de Agente)

## 🎯 Objetivo

Implementar un sistema tipo "dispatcher" que analiza solicitudes y las dirige automáticamente al especialista más adecuado.

## 🧠 Concepto

**Un router inteligente decide qué agente debe manejar cada tarea.**

```
Solicitud → Router (analiza intención) → Especialista → Respuesta
```

**¿Por qué es importante?**
- Un agente genérico es mediocre en todo
- Especialistas son expertos en su dominio
- El routing automático escala mejor que reglas manuales

## 📊 Arquitectura

```
                    ┌─────────────┐
                    │  Solicitud  │
                    └──────┬──────┘
                           │
                           v
                    ┌─────────────┐
                    │   Router    │
                    │ (Detecta    │
                    │  intención) │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┬─────────────┐
          │                │                │             │
          v                v                v             v
    ┌─────────┐      ┌──────────┐    ┌─────────┐  ┌──────────┐
    │Búsqueda │      │Matemático│    │Escritor │  │  Lógico  │
    └─────────┘      └──────────┘    └─────────┘  └──────────┘
          │                │                │             │
          └────────────────┴────────────────┴─────────────┘
                           │
                           v
                    ┌─────────────┐
                    │  Respuesta  │
                    └─────────────┘
```

## 🔑 Componentes del Sistema

### Router de Intenciones

**Rol**: Analizar solicitud y detectar intención

**Intenciones soportadas:**
| Intención | Trigger | Especialista |
|-----------|---------|--------------|
| BUSQUEDA | "buscar", "encontrar", "información sobre" | Búsqueda Documental |
| MATEMATICO | "calcular", "estadística", "promedio" | Análisis Matemático |
| ESCRITOR | "escribir", "redactar", "crear artículo" | Redacción |
| LOGICO | "si...entonces", "puzzle", "deducir" | Razonamiento Lógico |
| TECNICO | "código", "implementar", "debugging" | Técnico/Programación |

### Especialistas

**1. Búsqueda Documental**
- Recupera información de bases de conocimiento
- Sintetiza datos de múltiples fuentes
- Genera resúmenes precisos

**2. Análisis Matemático**
- Cálculos y operaciones numéricas
- Estadísticas y análisis de datos
- Modelos cuantitativos

**3. Redacción**
- Contenido original
- Artículos y ensayos
- Textos persuasivos

**4. Razonamiento Lógico**
- Puzzles y acertijos
- Análisis crítico
- Detección de falacias

**5. Técnico**
- Programación y código
- Debugging y optimización
- Arquitectura de sistemas

## 💡 Conceptos Clave

### Por Qué NO Usar un Agente Genérico

❌ **Agente Genérico**:
```python
"Eres un asistente que puede hacer de todo"
```
- Mediocre en todo
- No optimizado para ninguna tarea
- Respuestas menos precisas

✅ **Sistema Router**:
```python
Router → Detecta "cálculo" → Especialista Matemático
```
- Experto en su dominio
- Respuestas de alta calidad
- Fácil agregar nuevos especialistas

### Cómo Funciona la Detección

El router analiza:
1. **Palabras clave**: "calcular", "escribir", "buscar"
2. **Estructura**: Preguntas vs imperativos vs condicionales
3. **Contexto**: Tipo de información solicitada

## 🚀 Cómo Ejecutar

```bash
python 05_router_agents.py
```

## 📈 Output Esperado

### Ejemplo de Routing Exitoso

```
📝 Solicitud: "Calcula la media de 10, 20, 30"

🔍 Analizando intención...
🎯 Intención detectada: MATEMATICO

✅ Redirigiendo a: Especialista en Análisis Matemático
🔧 Procesando...

✅ RESPUESTA:
La media de 10, 20 y 30 es 20.
```

### Flujo Completo

```
Input: "Escribe un artículo sobre IA"
  ↓
Router: Detecta "escribir artículo" → ESCRITOR
  ↓
Especialista Escritor: Genera contenido
  ↓
Output: Artículo de 3 párrafos sobre IA
```

## 🎯 Ventajas del Patrón Router

| Aspecto | Sin Router | Con Router |
|---------|------------|------------|
| Precisión | ⭐⭐ | ⭐⭐⭐ |
| Especialización | ⭐ | ⭐⭐⭐ |
| Escalabilidad | ⭐ | ⭐⭐⭐ |
| Mantenibilidad | ⭐⭐ | ⭐⭐⭐ |

## 🔬 Experimentos Sugeridos

1. **Más especialistas**: Agrega "Traductor", "Analista Legal", etc.
2. **Router multi-nivel**: Router principal → Sub-routers especializados
3. **Fallback**: Si intención no clara, preguntar al usuario
4. **Métricas**: Trackear qué especialistas se usan más
5. **Routing híbrido**: Reglas + LLM para detección

## 🎓 Aplicaciones Reales

### Ejemplos del Mundo Real

**OpenAI/Anthropic**: Usan routing interno para dirigir queries

**Sistemas empresariales**:
- Chatbots: Detectar intención (soporte, ventas, información)
- Helpdesks: Dirigir tickets al departamento correcto
- APIs: Enrutar requests a servicios especializados

**E-commerce**:
- "Devolver producto" → Devoluciones
- "¿Cuándo llega mi pedido?" → Tracking
- "Recomendaciones" → Motor de recomendación

## 🏗️ Arquitectura Avanzada

### Router Jerárquico

```
Router Principal
    ├─→ Dominio Técnico
    │       ├─→ Python
    │       ├─→ JavaScript
    │       └─→ DevOps
    │
    ├─→ Dominio Creativo
    │       ├─→ Marketing
    │       ├─→ Storytelling
    │       └─→ Diseño
    │
    └─→ Dominio Analítico
            ├─→ Datos
            ├─→ Finanzas
            └─→ Ciencia
```

### Router con Confianza

```python
Router:
  "Calcular promedio" → MATEMATICO (confianza: 95%)
  "Analizar datos" → ¿MATEMATICO o BUSQUEDA? (confianza: 60%)
  
Si confianza < 80% → Preguntar al usuario
```

## ✅ Lo Que Aprenderás

- ✨ Especialistas superan a generalistas
- ✨ Routing automático escala mejor
- ✨ Arquitectura tipo dispatcher real
- ✨ Fácil agregar nuevos especialistas
- ✨ Patrón usado por grandes empresas

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐⭐⭐ Media-Alta  
**Tiempo de desarrollo**: 40-50 minutos  
**Aplicaciones reales**: Chatbots, helpdesks, APIs, sistemas empresariales

## 🆚 Comparación con Ejemplos Anteriores

| Ejemplo | Patrón | Decisión |
|---------|--------|----------|
| 01-03 | Secuenciales | Pre-definida |
| 04 - Competitivo | Paralelo | Post-ejecución (juez) |
| **05 - Router** | **Dispatcher** | **Pre-ejecución (intención)** |

## 🔗 Siguiente Paso

👉 **Ejemplo 06**: Supervisor/Orquestador (gobierno de equipos multi-agente)


