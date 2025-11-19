# Ejercicio 19: Estudio de mercado completo con CrewAI

## Objetivo
Crear un equipo completo que realiza un estudio de mercado, siguiendo el ejemplo de las slides C4.

## Conceptos Clave (Slides C4-C5)
- **Equipo completo**: Múltiples agentes trabajando en un objetivo común.
- **Flujo estructurado**: Investigación → Análisis → Escritura → Revisión.
- **Caso de uso real**: Estudios de mercado son ideales para multiagentes.

## Qué vamos a hacer
1. Crear 4 agentes especializados:
   - Investigador: Recopila información
   - Analista: Sintetiza y analiza
   - Escritor: Crea el informe
   - Revisor: Asegura calidad
2. Definir tareas con dependencias claras.
3. Ejecutar un estudio de mercado completo.
4. Mostrar el resultado final estructurado.

## Instrucciones
Ejecuta el script:
```bash
python 19_crewai_estudio_mercado.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Puedes cambiar el sector a analizar modificando la variable `sector` en el código.

