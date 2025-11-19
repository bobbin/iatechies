# Ejercicio 6: Tool conectada a base de datos

## Objetivo
Aprender a crear tools que consultan datos de dominio (base de datos, APIs, microservicios). Esto se parece mucho a un caso de negocio real.

## Conceptos Clave
- **Capa de dominio**: La tool accede a tu lógica de negocio y datos.
- **Separación de responsabilidades**: El LLM entiende la pregunta, la tool obtiene los datos, el LLM genera la respuesta.
- **Casos reales**: En producción, esto se conecta a bases de datos reales, APIs o microservicios.

## Qué vamos a hacer
1. Simular una base de datos de usuarios.
2. Crear una tool que consulta esta "base de datos".
3. Mostrar cómo el modelo usa la tool para responder preguntas sobre usuarios.
4. Explicar cómo esto se extiende a casos reales.

## Instrucciones
Ejecuta el script:
```bash
python 06_tool_base_datos.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Este ejercicio muestra cómo conectar tools con tu capa de dominio real.

