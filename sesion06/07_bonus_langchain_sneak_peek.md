# Ejercicio 7: Bonus - LangChain sneak peek

## Objetivo
Mostrar cómo LangChain simplifica el trabajo con tools, usando el decorador `@tool` y agentes. Esto conecta con la parte de LangChain que viene después.

## Conceptos Clave
- **Decorador @tool**: Convierte una función Python en una tool de LangChain automáticamente.
- **Docstring como descripción**: LangChain usa la docstring de la función como descripción de la tool.
- **Ciclo ReAct automático**: LangChain maneja el bucle modelo → tool → modelo por ti.
- **Agentes**: Simplifican la orquestación del flujo completo.

## Qué vamos a hacer
1. Crear una tool usando el decorador `@tool` de LangChain.
2. Configurar un agente ReAct simple.
3. Mostrar cómo LangChain maneja todo el ciclo automáticamente.
4. Comparar con el enfoque manual de los ejercicios anteriores.

## Instrucciones
Ejecuta el script:
```bash
python 07_bonus_langchain_sneak_peek.py
```

**Nota**: Requiere `OPENAI_API_KEY` y las dependencias de LangChain. Este ejercicio es un "sneak peek" de lo que viene en los ejercicios siguientes sobre LangChain.

