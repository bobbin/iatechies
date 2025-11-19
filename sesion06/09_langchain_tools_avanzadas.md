# Ejercicio 9: Tools avanzadas en LangChain

## Objetivo
Aprender a crear tools más complejas con validación avanzada, tipos personalizados y mejor integración con LangChain.

## Conceptos Clave (Slides B4, B6)
- **Tools avanzadas**: Pueden aceptar parámetros estructurados (JSON, objetos).
- **Validación**: Usar Pydantic para validar entradas complejas.
- **Resultados estructurados**: Las tools pueden devolver JSON para facilitar el procesamiento.

## Qué vamos a hacer
1. Crear 3 tools avanzadas:
   - `buscar_productos`: Búsqueda con filtros complejos (JSON)
   - `analizar_sentimiento`: Análisis de texto con resultado estructurado
   - `procesar_archivo`: Múltiples operaciones en un solo tool
2. Mostrar cómo manejar parámetros complejos.
3. Demostrar la diferencia entre tools simples y avanzadas.

## Instrucciones
Ejecuta el script:
```bash
python 09_langchain_tools_avanzadas.py
```

Observa cómo las tools avanzadas manejan casos más complejos y devuelven resultados estructurados.

