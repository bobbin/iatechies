# Ejercicio 1: Patrón "manual" sin tools oficiales

## Objetivo
Mostrar por qué las tools oficiales son mejores. Este ejemplo demuestra que sin tools, todo es texto frágil que requiere parseo manual.

## Conceptos Clave
- **Parseo manual**: El modelo responde con texto y tú debes parsearlo.
- **Fragilidad**: El formato puede variar y romperse fácilmente.
- **Contraste**: Este ejercicio sirve para luego mostrar la versión "bien hecha" con tools.

## Qué vamos a hacer
1. Crear un prompt que pide al modelo responder en un formato específico.
2. Parsear manualmente la respuesta del modelo.
3. Ejecutar la acción correspondiente (cálculo o búsqueda).
4. Mostrar los problemas de este enfoque.

## Instrucciones
Ejecuta el script:
```bash
python 01_patron_manual_sin_tools.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Este ejercicio muestra los problemas del enfoque manual antes de pasar a tools oficiales.

