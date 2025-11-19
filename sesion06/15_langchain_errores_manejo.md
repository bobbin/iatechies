# Ejercicio 15: Manejo de errores y límites en LangChain

## Objetivo
Aprender a manejar errores comunes y configurar límites para evitar que los agentes se queden atascados o consuman recursos excesivos.

## Conceptos Clave (Slides B14)
- **Manejo de errores**: Las tools deben devolver mensajes de error claros.
- **Límites**: Configurar `max_iterations` y `max_execution_time`.
- **Errores típicos**:
  - Dar demasiadas tools
  - Tools mal definidas
  - No limitar pasos del agente
  - No testear las responses
  - No controlar fallos de APIs

## Qué vamos a hacer
1. Crear tools que manejan errores correctamente.
2. Configurar límites en el AgentExecutor.
3. Probar casos que generan errores.
4. Mostrar cómo el agente puede corregir errores automáticamente.

## Instrucciones
Ejecuta el script:
```bash
python 15_langchain_errores_manejo.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Observa cómo los límites y el manejo de errores previenen problemas comunes.

