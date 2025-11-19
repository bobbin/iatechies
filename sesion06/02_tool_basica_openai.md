# Ejercicio 2: Tool básica con OpenAI

## Objetivo
Aprender a usar tools oficiales de OpenAI. El modelo devuelve una estructura JSON con el nombre de la función y los argumentos; tú solo la ejecutas.

## Conceptos Clave
- **tools**: La definición de la función (JSON Schema).
- **tool_calls**: El pedido del modelo para ejecutar una tool.
- **arguments**: Los parámetros vienen en JSON, los parseas y ejecutas tu función real.
- **tool_choice**: Controla si el modelo debe usar tools ("auto", "required", "none").

## Qué vamos a hacer
1. Definir una tool simple (sumar dos números) usando JSON Schema.
2. Llamar al modelo con la tool disponible.
3. Parsear la respuesta del modelo y ejecutar la función.
4. Mostrar la diferencia con el enfoque manual del ejercicio anterior.

## Instrucciones
Ejecuta el script:
```bash
python 02_tool_basica_openai.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Este ejercicio muestra la versión "bien hecha" con tools oficiales.

