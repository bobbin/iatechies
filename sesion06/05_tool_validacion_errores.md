# Ejercicio 5: Tool con validación y manejo de errores

## Objetivo
Aprender a crear tools que validan parámetros y devuelven errores controlados, que el modelo puede explicar al usuario de forma amigable.

## Conceptos Clave
- **Validación en la tool**: La lógica de negocio vive en tu función, no en el modelo.
- **Errores estructurados**: Los errores se devuelven en formato JSON que el modelo puede interpretar.
- **Explicación automática**: El modelo traduce los errores técnicos a mensajes amigables para el usuario.

## Qué vamos a hacer
1. Crear una tool que valida reglas de negocio (límites, restricciones).
2. Mostrar cómo la tool devuelve errores estructurados.
3. Demostrar cómo el modelo explica los errores al usuario.
4. Comparar casos válidos e inválidos.

## Instrucciones
Ejecuta el script:
```bash
python 05_tool_validacion_errores.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Este ejercicio muestra cómo manejar errores de forma profesional en tools.

