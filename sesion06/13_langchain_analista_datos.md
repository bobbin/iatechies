# Ejercicio 13: Agente analista de datos completo

## Objetivo
Crear un agente completo que analiza datos CSV, calcula métricas y genera informes, siguiendo el ejemplo conceptual de las slides B9.

## Conceptos Clave (Slides B9, B11)
- **Agente completo**: Combina múltiples tools para resolver tareas complejas.
- **Decisión automática**: El agente decide el orden de las tools.
- **Patrón ReAct**: El agente piensa, actúa, observa y repite hasta completar la tarea.

## Qué vamos a hacer
1. Crear 4 tools para análisis de datos:
   - `load_csv`: Carga y muestra estructura del CSV
   - `describe_data`: Resumen estadístico
   - `compute_metrics`: Métricas específicas
   - `generar_informe`: Crea informe final
2. Configurar un agente ReAct que use estas tools.
3. Ejecutar una tarea compleja que requiere múltiples pasos.
4. Observar cómo el agente decide el orden de ejecución.

## Instrucciones
Ejecuta el script:
```bash
python 13_langchain_analista_datos.py
```

**Nota**: Requiere `OPENAI_API_KEY` y pandas. Este ejercicio muestra un agente completo en acción, similar a los ejemplos de las slides.

