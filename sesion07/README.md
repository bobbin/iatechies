# Sesión 07: Arquitecturas Multi-Agente con CrewAI

## 🎯 Objetivo de la Sesión

Dominar los patrones de arquitectura multi-agente, desde agentes reflexivos simples hasta equipos complejos que simulan departamentos de análisis documental.

## 📚 Contenidos

### Nivel 1: Fundamentos (Complejidad Baja)

1. **Agentes Reflexivos (Self-Reflection Loop)**
   - Patrón: Generar → Criticar → Mejorar
   - Archivo: `01_agentes_reflexivos.py`
   - Concepto clave: Un agente puede revisar su propio output

2. **Self-Prompt Editing**
   - Patrón: Detectar errores → Optimizar prompt → Reintentar
   - Archivo: `02_self_prompt_editing.py`
   - Concepto clave: Agentes que mejoran su forma de preguntar

3. **Agentes con Reglas Híbridas**
   - Patrón: Reglas deterministas + Razonamiento LLM
   - Archivo: `03_agentes_con_reglas.py`
   - Concepto clave: No todo debe depender del LLM

### Nivel 2: Colaboración (Complejidad Media)

4. **Agentes Competitivos**
   - Patrón: Múltiples soluciones → Juez → Mejor respuesta
   - Archivo: `04_agentes_competitivos.py`
   - Concepto clave: Diversidad reduce alucinaciones

5. **Router Agents**
   - Patrón: Detectar intención → Seleccionar especialista
   - Archivo: `05_router_agents.py`
   - Concepto clave: Arquitectura dispatcher

6. **Supervisor/Orquestador**
   - Patrón: Controla flujo, reintentos, calidad
   - Archivo: `06_supervisor_orquestador.py`
   - Concepto clave: Gobierno de equipos multi-agente

### Nivel 3: Sistemas Avanzados (Complejidad Alta)

7. **Memoria Evolutiva**
   - Patrón: Almacenar experiencias → Mejorar decisiones futuras
   - Archivo: `07_memoria_evolutiva.py`
   - Concepto clave: Aprendizaje de casos pasados

8. **Agentes con MCPs**
   - Patrón: Agentes con "sentidos" (archivos, APIs, DBs)
   - Archivo: `08_agentes_mcp.py`
   - Concepto clave: Integración con infraestructura real

9. **Multi-Agente Multimodal**
   - Patrón: Texto + Imágenes + PDFs con razonamiento híbrido
   - Archivo: `09_multimodal_ligero.py`
   - Concepto clave: Pipelines multi-sensoriales

### Nivel 4: Sistemas de Producción (Complejidad Muy Alta)

10. **Verificación de Evidencia**
    - Patrón: Validar citas y evidencia contra fuentes
    - Archivo: `10_verificacion_evidencia.py`
    - Concepto clave: Antídoto contra alucinaciones

11. **Agentic RAG**
    - Patrón: Planner → Retriever → Verifier → Writer
    - Archivo: `11_agentic_rag.py`
    - Concepto clave: RAG como grafo de decisiones

12. **Equipo Forense Completo** ⭐
    - Patrón: Sistema completo de análisis documental
    - Archivo: `12_equipo_forense.py`
    - Concepto clave: Integración de todos los patrones

## 🚀 Instalación

```bash
cd sesion07
pip install -r requirements.txt
```

## 🔑 Configuración

Crea un archivo `.env` con tus claves de API:

```env
OPENAI_API_KEY=tu_clave_aqui
# Para ejemplos multimodales (opcional)
ANTHROPIC_API_KEY=tu_clave_aqui
```

## 📖 Cómo Usar Esta Sesión

1. **Progresión Secuencial**: Los ejemplos están ordenados por complejidad
2. **Código Comentado**: Cada ejemplo tiene explicaciones detalladas
3. **Ejecutable**: Todos los ejemplos se pueden ejecutar directamente
4. **Incremental**: Cada ejemplo construye sobre los anteriores

## 🎓 Conceptos Clave

### Diferencia entre Agente y Multi-Agente

- **Agente Simple**: Un solo LLM con herramientas
- **Multi-Agente**: Varios agentes con roles especializados que colaboran

### Por Qué CrewAI

- **Sintaxis clara**: Roles, objetivos, herramientas bien definidos
- **Colaboración natural**: Los agentes se coordinan automáticamente
- **Producción**: Usado en sistemas reales empresariales

### Patrones Arquitectónicos

1. **Reflexión**: Auto-crítica y mejora
2. **Competición**: Múltiples soluciones, mejor resultado
3. **Jerarquía**: Supervisor → Especialistas
4. **Pipeline**: Flujo secuencial con validación
5. **Router**: Decisión de quién ejecuta qué
6. **Memoria**: Aprendizaje de experiencias pasadas

## 📊 Progresión de Aprendizaje

```
Sesión 06 → Agentes individuales con tools
Sesión 07 → Equipos de agentes coordinados ← ESTÁS AQUÍ
Sesión 08 → RAG avanzado
Sesión 09 → Multimodal profundo
```

## 🛠️ Tecnologías

- **CrewAI**: Framework multi-agente
- **LangChain**: Tools y componentes
- **OpenAI/Anthropic**: Modelos de lenguaje
- **ChromaDB**: Base vectorial (ejemplos avanzados)
- **FastMCP**: Integración con MCPs

## 💡 Consejos

1. **Ejecuta los ejemplos en orden**: La complejidad es progresiva
2. **Lee los comentarios**: Explican las decisiones de diseño
3. **Experimenta**: Modifica roles, objetivos y herramientas
4. **Observa los logs**: CrewAI muestra la coordinación entre agentes

## 🎯 Objetivo Final

Al terminar esta sesión, serás capaz de:

✅ Diseñar arquitecturas multi-agente escalables  
✅ Implementar patrones de reflexión y verificación  
✅ Construir equipos especializados con roles claros  
✅ Integrar agentes con herramientas reales (MCPs, APIs, DBs)  
✅ Crear sistemas de producción robustos anti-alucinación  

---

**¿Listo para construir equipos de agentes que trabajan como departamentos reales?** 🚀


