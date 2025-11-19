# Ejercicio 6: Tools con validación y manejo de errores

## Objetivo
Aprender a crear tools robustas que validan entradas y manejan errores de forma predecible. Esto es crítico para agentes en producción.

## Conceptos Clave (Slides A6, A8)
- **Validación de entradas**: Las tools deben verificar que los datos de entrada sean válidos.
- **Mensajes de error claros**: Los errores deben ser descriptivos para que el agente pueda corregirlos.
- **Predecibilidad**: Las tools deben comportarse de forma consistente.

## Qué vamos a hacer
1. Crear 4 tools con validación:
   - `calcular_edad`: Valida formato de fecha y fechas futuras
   - `dividir_numeros`: Previene división por cero
   - `buscar_en_lista`: Maneja listas vacías y elementos no encontrados
   - `validar_email`: Verifica formato de email
2. Probar casos válidos e inválidos para cada tool.
3. Mostrar cómo los mensajes de error ayudan al agente.

## Instrucciones
Ejecuta el script:
```bash
python 06_tools_validacion.py
```

Observa cómo cada tool valida sus entradas y devuelve mensajes de error útiles.

