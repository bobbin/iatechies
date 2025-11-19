# Ejercicio 21: Diseña un Escape Room IA Multiagente

## Objetivo
Crear un equipo multiagente que diseña, valida y prueba un Escape Room interactivo que el usuario puede jugar por chat.

## Contexto

Un Escape Room debe tener:
- Una historia coherente
- Uno o varios puzzles
- Pistas coherentes y progresivas
- Una solución válida
- Lógica interna consistente

Este ejercicio demuestra cómo diferentes especialistas (agentes) colaboran para crear algo complejo.

## Equipo Multiagente

### 1. 🧩 Puzzle Architect
**Responsabilidad**: Diseña los acertijos
- Define mecánicas, reglas y dificultad
- Asegura que el puzzle sea resoluble en texto
- Limita el uso de conocimientos externos

### 2. 🔎 Clue Designer
**Responsabilidad**: Genera pistas coherentes
- Pistas progresivas y no obvias
- Proporciona feedback cuando el usuario se bloquea
- Las pistas tienen sentido con la narrativa

### 3. 📜 Story Weaver (Narrative Agent)
**Responsabilidad**: Crea el ambiente narrativo
- Historia, personajes, tono
- Introduce cada puzzle dentro de la trama
- Asegura continuidad narrativa

### 4. ✔️ Logic Guardian (Consistency & Logic)
**Responsabilidad**: Revisa coherencia
- Detecta contradicciones
- Comprueba que las pistas llevan a la solución
- Puede pedir correcciones

### 5. 🧪 Puzzle Tester (QA Agent)
**Responsabilidad**: Prueba el Escape Room
- "Juega" una versión abreviada
- Comprueba dificultad
- Simula errores de usuario

## Flujo de Trabajo

```
Story Weaver → Puzzle Architect → Clue Designer → Logic Guardian → Puzzle Tester
```

**Justificación del flujo secuencial:**
- Cada tarea depende de la anterior
- Permite que cada agente vea el trabajo previo
- Asegura coherencia en cada paso
- El Logic Guardian valida antes del test final

## Tools Disponibles

- **`get_random_word`**: Genera palabras aleatorias para inspirar elementos
- **`generate_cipher`**: Crea textos cifrados para puzzles de descifrado

## Tareas Definidas

1. **Tarea Narrativa** (Story Weaver): Crear escenario, historia y reglas
2. **Tarea Puzzle** (Puzzle Architect): Diseñar el acertijo principal
3. **Tarea Pistas** (Clue Designer): Generar pistas progresivas
4. **Tarea Validación** (Logic Guardian): Revisar coherencia total
5. **Tarea Test** (Puzzle Tester): Probar y evaluar el Escape Room

## Instrucciones

Ejecuta el script:
```bash
python 21_crewai_escape_room.py
```

**Nota**: Requiere `OPENAI_API_KEY`. El ejercicio demuestra cómo un equipo de especialistas colabora para crear un producto complejo y coherente.

## Conceptos Clave

- **Especialización**: Cada agente tiene un rol específico
- **Colaboración**: Los agentes trabajan juntos hacia un objetivo común
- **Validación**: El Logic Guardian asegura calidad
- **Testing**: El Puzzle Tester verifica que todo funcione
- **Tools**: Las herramientas enriquecen las capacidades de los agentes

## Extensión

Puedes extender este ejercicio:
- Agregar más puzzles
- Crear un chat interactivo que use el diseño
- Iterar sobre el diseño basándote en feedback
- Agregar más tools (búsqueda web, generación de imágenes, etc.)

