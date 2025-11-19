# Ejercicio 7: Patrón ReAct manual

## Objetivo
Implementar manualmente el patrón ReAct (Reasoning + Acting) para entender cómo funciona internamente antes de usar frameworks como LangChain.

## Conceptos Clave (Slides A3-A4)
- **Patrón ReAct**: El ciclo fundamental de los agentes:
  - **Pensar** (Thought): El modelo razona sobre qué hacer
  - **Decidir** (Action): Elige qué tool usar
  - **Actuar** (Acting): Ejecuta la tool
  - **Observar** (Observation): Ve el resultado
  - **Repetir**: Hasta tener la respuesta final
- **Ciclo iterativo**: Los agentes pueden necesitar múltiples pasos para resolver un problema.

## Qué vamos a hacer
1. Crear una clase `AgenteReActManual` que implementa el ciclo ReAct.
2. Definir tools simples (sumar, multiplicar, factorial).
3. Ejecutar ejemplos donde el agente debe usar múltiples tools.
4. Mostrar cómo el historial de acciones se usa para el siguiente paso.

## Instrucciones
Ejecuta el script:
```bash
python 07_patron_react_manual.py
```

**Nota**: Requiere `OPENAI_API_KEY` configurada. Este ejercicio muestra cómo funcionan internamente los agentes de LangChain.

