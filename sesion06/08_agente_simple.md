# Ejercicio 8: Agente simple sin framework

## Objetivo
Crear un agente mínimo desde cero para entender los componentes básicos: objetivo, razonamiento, tools y memoria opcional.

## Conceptos Clave (Slides A3, A9)
- **Anatomía de un agente**:
  - **Objetivo**: Define qué debe lograr el agente
  - **Razonamiento**: El LLM que piensa y decide
  - **Tools**: Acciones que puede ejecutar
  - **Memoria**: Opcional, recuerda contexto previo
- **Agente vs LLM**: Un LLM solo responde, un agente cumple objetivos usando tools.

## Qué vamos a hacer
1. Crear una clase `AgenteSimple` con los componentes básicos.
2. Definir tools simples (diccionario, contar caracteres, convertir texto).
3. Mostrar cómo el agente usa su objetivo y memoria para responder.
4. Demostrar la diferencia entre un LLM simple y un agente.

## Instrucciones
Ejecuta el script:
```bash
python 08_agente_simple.py
```

**Nota**: Requiere `OPENAI_API_KEY` configurada. Este ejercicio muestra la estructura básica que luego los frameworks como LangChain organizan mejor.

