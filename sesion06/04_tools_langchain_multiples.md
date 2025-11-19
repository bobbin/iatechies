# Ejercicio 4: Múltiples Tools trabajando juntas

## Objetivo
Entender cómo definir múltiples tools y cómo un agente puede decidir cuál usar según el contexto. Esto es fundamental para construir agentes útiles.

## Conceptos Clave (Slides A5-A7)
- **Múltiples Tools**: Un agente puede tener acceso a varias tools y decidir cuál usar.
- **Composición**: Las tools pueden trabajar juntas para resolver tareas complejas.
- **Decisión del modelo**: El LLM decide qué tool usar basándose en la descripción y el contexto.

## Qué vamos a hacer
1. Definir 4 tools diferentes:
   - `leer_archivo`: Lee contenido de archivos
   - `contar_palabras`: Analiza la longitud de un texto
   - `buscar_palabra`: Busca términos específicos
   - `extraer_lineas`: Extrae secciones de un documento
2. Simular un flujo de trabajo donde se usan varias tools secuencialmente.
3. Mostrar los schemas que el LLM ve para cada tool.

## Instrucciones
Ejecuta el script:
```bash
python 04_tools_multiples.py
```

Observa cómo cada tool tiene su propio schema y cómo pueden combinarse para resolver tareas más complejas.

