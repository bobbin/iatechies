# Agentes Reflexivos (Self-Reflection Loop)

## 🎯 Objetivo

Aprender el patrón más básico de multi-agente: la auto-reflexión en bucle.

## 🧠 Concepto

Un agente reflexivo sigue este proceso:

```
Generar → Criticar → Mejorar
```

**¿Por qué funciona?**
- El LLM puede evaluar su propio output
- La crítica intermedia detecta problemas
- El refinamiento produce mejor calidad

## 📊 Arquitectura

```
┌─────────────┐
│  Escritor   │ → Genera artículo inicial
└──────┬──────┘
       │
       v
┌─────────────┐
│   Crítico   │ → Identifica problemas
└──────┬──────┘
       │
       v
┌─────────────┐
│   Editor    │ → Versión mejorada
└─────────────┘
```

## 🔑 Agentes del Sistema

### 1. Escritor de Contenido
- **Rol**: Generar primera versión
- **Output**: Artículo de 3 párrafos
- **Fortaleza**: Creatividad inicial

### 2. Crítico de Contenido
- **Rol**: Detectar debilidades
- **Output**: Lista de 3-5 mejoras
- **Fortaleza**: Análisis objetivo

### 3. Editor Refinador
- **Rol**: Incorporar feedback
- **Output**: Versión final mejorada
- **Fortaleza**: Síntesis y mejora

## 💡 Conceptos Clave

### Por Qué No Es "Un Prompt Largo"

❌ **Single Prompt**:
```python
"Escribe un artículo y asegúrate de que sea perfecto"
```

✅ **Patrón Reflexivo**:
```python
1. Escribir (foco en crear)
2. Criticar (foco en detectar)
3. Refinar (foco en mejorar)
```

**Ventaja**: Cada agente se enfoca en una tarea específica.

### Separación de Responsabilidades

- **Escritor**: No se preocupa por la crítica
- **Crítico**: No tiene que generar contenido
- **Editor**: Solo mejora, no crea desde cero

## 🚀 Cómo Ejecutar

```bash
python 01_agentes_reflexivos.py
```

## 📈 Output Esperado

Verás tres fases:

1. **Fase 1 - Escritura**: Artículo inicial (puede tener debilidades)
2. **Fase 2 - Crítica**: Lista de problemas encontrados
3. **Fase 3 - Refinamiento**: Artículo mejorado

## 🔬 Experimentos Sugeridos

1. **Cambia el tema**: Prueba con temas técnicos vs creativos
2. **Agrega más ciclos**: Crítico → Editor → Crítico → Editor
3. **Modifica el crítico**: Hazlo más o menos estricto
4. **Elimina un agente**: Compara calidad sin el crítico

## ✅ Lo Que Aprenderás

- ✨ Los agentes pueden auto-evaluarse
- ✨ La reflexión mejora la calidad
- ✨ El proceso secuencial tiene valor
- ✨ Cada agente tiene un rol claro

## 🎓 Nivel de Complejidad

**Complejidad**: ⭐ Baja  
**Tiempo de desarrollo**: 15-20 minutos  
**Aplicaciones reales**: Escritura, análisis, generación de código

## 🔗 Siguiente Paso

👉 **Ejemplo 02**: Self-Prompt Editing (optimizar preguntas)


