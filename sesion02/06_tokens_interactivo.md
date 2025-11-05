# Teoría: Tokenizador Interactivo

Este ejercicio proporciona una herramienta interactiva para experimentar con la tokenización en tiempo real.

## Objetivo

Permitir al usuario escribir texto y ver inmediatamente cómo se tokeniza, con visualización por colores y estadísticas detalladas.

## Características

### Análisis Completo
- Conteo de caracteres, palabras y tokens
- Ratios (tokens/caracteres, tokens/palabras)
- Visualización con colores
- Desglose detallado de cada token
- Estimación de costos

### Visualización
- Cada token se muestra con un color diferente
- Fácil de ver cómo se divide el texto
- Muestra el ID y el texto de cada token

### Interactivo
- Escribe cualquier texto y presiona Enter
- Comandos: `salir`, `exit`, `quit` para terminar
- `clear` para limpiar la pantalla

## Uso

```bash
python 06_tokens_interactivo.py
```

Luego simplemente escribe texto y verás el análisis completo.

## Ejemplos de Uso

1. **Texto simple**: "Hola mundo"
2. **Con emojis**: "¡Hola! 😊🎉"
3. **Código**: "def f(x): return x**2"
4. **Multilingüe**: "Hello 你好"

## Conceptos Clave

- Experimenta con diferentes tipos de texto
- Observa cómo varían los ratios
- Ve cómo se dividen los tokens visualmente
- Aprende a estimar costos

## Explicación para el alumno

* "Esta herramienta te permite experimentar libremente con la tokenización."
* "Escribe cualquier texto y observa cómo se divide en tokens."
* "La visualización con colores hace fácil ver qué parte del texto es cada token."
* "Úsala para optimizar tus prompts antes de usarlos en producción."
