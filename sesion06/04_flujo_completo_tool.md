# Ejercicio 4: Flujo completo de tool (dos turnos)

## Objetivo
Aprender cómo se cierra el ciclo completo: el modelo pide una tool, tú la ejecutas, luego le mandas el resultado como mensaje de tool para que genere la respuesta final al usuario.

## Conceptos Clave
- **Turno 1**: El modelo decide usar una tool y proporciona los argumentos.
- **Ejecución**: Tu código ejecuta la función real.
- **Turno 2**: Envías el resultado como mensaje de tipo "tool" y el modelo genera la respuesta final.
- **Bucle completo**: Este es el patrón fundamental de herramientas en OpenAI.

## Qué vamos a hacer
1. Crear una tool para obtener el clima.
2. Primer turno: el modelo decide usar la tool.
3. Ejecutar la tool y obtener el resultado.
4. Segundo turno: enviar el resultado al modelo para que genere la respuesta final.
5. Mostrar el flujo completo del bucle.

## Instrucciones
Ejecuta el script:
```bash
python 04_flujo_completo_tool.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Este ejercicio muestra el bucle completo de herramientas, clave para entender cómo funcionan los agentes.

