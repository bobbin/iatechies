# Ejercicio 11: Agente con memoria en LangChain

## Objetivo
Aprender a usar diferentes tipos de memoria en LangChain para que el agente recuerde contexto entre interacciones.

## Conceptos Clave (Slides B8)
- **Memoria en LangChain**: Permite que el agente recuerde información previa.
- **Tipos de memoria**:
  - `ConversationBufferMemory`: Guarda todo el historial
  - `ConversationSummaryMemory`: Resumen del historial
  - `VectorStoreRetrieverMemory`: Búsqueda semántica en historial
- **Integración**: La memoria se integra automáticamente en agents y chains.

## Qué vamos a hacer
1. Crear un agente con `ConversationBufferMemory`.
2. Realizar múltiples interacciones que dependen del contexto previo.
3. Mostrar cómo la memoria mantiene el historial.
4. Explicar los diferentes tipos de memoria disponibles.

## Instrucciones
Ejecuta el script:
```bash
python 11_langchain_memoria.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Observa cómo el agente recuerda información de interacciones anteriores.

