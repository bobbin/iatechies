# Ejercicio 10: Structured Chat Agent en LangChain

## Objetivo
Aprender a usar Structured Chat Agent, que es más robusto que ReAct para trabajar con tools bien definidas y tareas estructuradas.

## Conceptos Clave (Slides B5-B6)
- **Structured Chat Agent**: Variante de agente más robusta para tools bien definidas.
- **Ventajas sobre ReAct**: Mejor manejo de errores, más predecible con schemas claros.
- **Cuándo usarlo**: Cuando las tools tienen schemas bien definidos y el flujo es más estructurado.

## Qué vamos a hacer
1. Crear tools para análisis de datos CSV.
2. Configurar un Structured Chat Agent.
3. Ejecutar tareas de análisis que requieren múltiples pasos.
4. Comparar con el enfoque ReAct del ejercicio anterior.

## Instrucciones
Ejecuta el script:
```bash
python 10_langchain_structured_agent.py
```

**Nota**: Requiere `OPENAI_API_KEY` y pandas. Este ejercicio muestra cuándo usar Structured Chat Agent vs ReAct Agent.

