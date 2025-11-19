# Ejercicio 17: Tareas en paralelo con CrewAI

## Objetivo
Aprender a ejecutar tareas en paralelo cuando no hay dependencias entre ellas, optimizando el tiempo de ejecución.

## Conceptos Clave (Slides C3-C5)
- **Tareas paralelas**: Cuando no hay dependencias, las tareas pueden ejecutarse simultáneamente.
- **Process.hierarchical**: Permite paralelismo cuando es posible.
- **Optimización**: Reduce el tiempo total de ejecución del crew.

## Qué vamos a hacer
1. Crear 3 agentes investigadores que trabajan en áreas diferentes.
2. Definir tareas independientes que se pueden ejecutar en paralelo.
3. Crear una tarea de síntesis que depende de las anteriores.
4. Usar `Process.hierarchical` para permitir paralelismo.

## Instrucciones
Ejecuta el script:
```bash
python 17_crewai_tareas_paralelas.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Observa cómo las tareas independientes se ejecutan en paralelo.

