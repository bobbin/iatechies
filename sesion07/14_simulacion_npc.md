# Ejemplo 14: Simulación NPC (TownAI Lite)

Este ejemplo implementa una simulación simplificada inspirada en el paper "Generative Agents" (Simulacra of Human Behavior), donde múltiples agentes (NPCs) conviven en un entorno, tienen memoria y persiguen objetivos.

## 🎯 Concepto Clave: Memoria Compartida

A diferencia de un chat normal, aquí los agentes no solo responden a un prompt, sino que consultan un "Estado del Mundo" persistente antes de actuar.

### Arquitectura

1.  **WorldMemory (El Tablero)**:
    - Un archivo JSON (`world_memory.json`) que actúa como base de datos del mundo.
    - Guarda: Hora actual, descripción de lugares y log de eventos pasados.

2.  **Ciclo de Juego**:
    - La simulación se divide en "Turnos" (Mañana, Mediodía, Tarde).
    - En cada turno, se instancia un `Crew` que coordina a los agentes para que realicen UNA acción cada uno.

3.  **Los NPCs**:
    - **Beto (Panadero)**: Quiere vender y chismear.
    - **Sargento Clave (Guardia)**: Busca un objeto robado.
    - **Sombra (Pícaro)**: Quiere robar y molestar al guardia.

## 🧠 Flujo de Pensamiento del Agente

Cada vez que es el turno de un agente:

1.  **Observa**: Llama a `Observar Entorno`. Recibe el JSON con los últimos eventos.
    *   *Ej: "Veo que Sombra acaba de robar una manzana en la plaza".*
2.  **Decide**: Basado en su `role` y `goal`, decide qué hacer.
    *   *Ej (Guardia): "¡Debo perseguir a Sombra!".*
3.  **Actúa**: Llama a `Realizar Acción` para escribir en el log del mundo.
    *   *Ej: "Corro hacia la plaza gritando alto al ladrón".*

## 🚀 Ejecución

```bash
python 14_simulacion_npc.py
```

Al finalizar, verás una **Crónica del Día** con todas las interacciones generadas. También puedes inspeccionar el archivo `world_memory.json` para ver el estado crudo.

## 🧪 Experimentos Sugeridos

1.  **Cambia el orden**: En `ejecutar_turno`, cambia el orden de la lista `agents`. Si el Pícaro actúa antes que el Guardia, la historia cambia.
2.  **Añade un lugar**: Edita `WorldMemory` para añadir "La Iglesia" o "El Castillo".
3.  **Añade un evento externo**: Inyecta un evento en el JSON manualmente a mitad de ejecución (avanzado).

