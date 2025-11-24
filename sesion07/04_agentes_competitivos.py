"""
Ejemplo 4: Agentes Competitivos (Competitive Multi-Agent)
==========================================================

Complejidad: MEDIA

Concepto:
---------
Varios agentes generan soluciones diferentes para el mismo problema.
Un agente "juez" evalúa todas las respuestas y selecciona la mejor.

Beneficios:
- Diversidad de perspectivas
- Minimización de alucinaciones por consenso
- Mejor calidad del resultado final

Patrón: Competidor 1 ┐
        Competidor 2 ├→ Juez → Mejor solución
        Competidor 3 ┘
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# DEFINICIÓN DE AGENTES COMPETIDORES
# ==============================================================================

# COMPETIDOR 1: Enfoque técnico-analítico
analista_tecnico = Agent(
    role="Analista Técnico",
    goal="Proporcionar respuestas precisas basadas en datos y hechos técnicos",
    backstory="""Eres un ingeniero con mente analítica. Te enfocas en 
    precisión técnica, datos concretos y aspectos de implementación. 
    Tu estilo es directo y basado en evidencia.""",
    verbose=True,
    allow_delegation=False
)

# COMPETIDOR 2: Enfoque creativo-conceptual
pensador_creativo = Agent(
    role="Pensador Creativo",
    goal="Ofrecer perspectivas innovadoras y analogías comprensibles",
    backstory="""Eres un visionario que piensa fuera de la caja. Te especializas 
    en encontrar patrones, crear analogías y explicar conceptos complejos de 
    forma intuitiva. Tu estilo es narrativo y metafórico.""",
    verbose=True,
    allow_delegation=False
)

# COMPETIDOR 3: Enfoque práctico-aplicado
experto_practico = Agent(
    role="Experto Práctico",
    goal="Dar respuestas orientadas a la aplicación real y casos de uso",
    backstory="""Eres un profesional con experiencia en campo. Te enfocas en 
    la aplicabilidad práctica, casos de uso reales y consejos accionables. 
    Tu estilo es pragmático y orientado a resultados.""",
    verbose=True,
    allow_delegation=False
)

# ==============================================================================
# AGENTE JUEZ
# ==============================================================================

juez = Agent(
    role="Juez Evaluador",
    goal="Evaluar respuestas y seleccionar la mejor basándose en criterios objetivos",
    backstory="""Eres un evaluador experimentado que analiza múltiples 
    respuestas según criterios claros:
    
    1. CLARIDAD: ¿Es fácil de entender?
    2. PRECISIÓN: ¿Es técnicamente correcta?
    3. UTILIDAD: ¿Es práctica y aplicable?
    4. COMPLETITUD: ¿Cubre aspectos importantes?
    
    Evalúas cada respuesta con una puntuación del 1-10 en cada criterio 
    y explicas por qué una respuesta es superior.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA DE COMPETICIÓN
# ==============================================================================

def ejecutar_competicion(pregunta: str):
    """
    Ejecuta una competición entre múltiples agentes.
    
    Proceso:
    1. Todos los agentes responden la misma pregunta
    2. El juez evalúa todas las respuestas
    3. Se selecciona la mejor
    """
    print("\n" + "="*70)
    print("🏆 COMPETICIÓN MULTI-AGENTE")
    print("="*70)
    print(f"❓ Pregunta: {pregunta}\n")
    
    # ===== FASE 1: RESPUESTAS DE LOS COMPETIDORES =====
    print("📝 FASE 1: Generando respuestas de los competidores...\n")
    
    # Tarea para el analista técnico
    tarea_tecnico = Task(
        description=f"""
        Responde la siguiente pregunta desde un enfoque técnico-analítico:
        
        {pregunta}
        
        Proporciona una respuesta clara de 3-4 oraciones enfocándote en:
        - Aspectos técnicos
        - Datos concretos
        - Precisión factual
        """,
        agent=analista_tecnico,
        expected_output="Respuesta técnica concisa (3-4 oraciones)"
    )
    
    # Tarea para el pensador creativo
    tarea_creativo = Task(
        description=f"""
        Responde la siguiente pregunta desde un enfoque creativo-conceptual:
        
        {pregunta}
        
        Proporciona una respuesta clara de 3-4 oraciones enfocándote en:
        - Analogías comprensibles
        - Perspectivas innovadoras
        - Conexiones conceptuales
        """,
        agent=pensador_creativo,
        expected_output="Respuesta creativa concisa (3-4 oraciones)"
    )
    
    # Tarea para el experto práctico
    tarea_practico = Task(
        description=f"""
        Responde la siguiente pregunta desde un enfoque práctico-aplicado:
        
        {pregunta}
        
        Proporciona una respuesta clara de 3-4 oraciones enfocándote en:
        - Casos de uso reales
        - Aplicaciones prácticas
        - Consejos accionables
        """,
        agent=experto_practico,
        expected_output="Respuesta práctica concisa (3-4 oraciones)"
    )
    
    # Ejecutar respuestas en paralelo (CrewAI las procesará secuencialmente)
    crew_competidores = Crew(
        agents=[analista_tecnico, pensador_creativo, experto_practico],
        tasks=[tarea_tecnico, tarea_creativo, tarea_practico],
        process=Process.sequential,
        verbose=1
    )
    
    crew_competidores.kickoff()
    
    # Capturar respuestas
    respuesta_tecnico = tarea_tecnico.output.raw_output
    respuesta_creativo = tarea_creativo.output.raw_output
    respuesta_practico = tarea_practico.output.raw_output
    
    print("\n" + "-"*70)
    print("📊 RESPUESTAS DE LOS COMPETIDORES:")
    print("-"*70)
    print(f"\n🔧 ANALISTA TÉCNICO:\n{respuesta_tecnico}\n")
    print(f"\n💡 PENSADOR CREATIVO:\n{respuesta_creativo}\n")
    print(f"\n⚙️ EXPERTO PRÁCTICO:\n{respuesta_practico}\n")
    
    # ===== FASE 2: EVALUACIÓN DEL JUEZ =====
    print("\n" + "="*70)
    print("⚖️ FASE 2: Evaluación del juez...")
    print("="*70 + "\n")
    
    tarea_evaluacion = Task(
        description=f"""
        Evalúa las siguientes tres respuestas a la pregunta: "{pregunta}"
        
        RESPUESTA A (Analista Técnico):
        {respuesta_tecnico}
        
        RESPUESTA B (Pensador Creativo):
        {respuesta_creativo}
        
        RESPUESTA C (Experto Práctico):
        {respuesta_practico}
        
        Evalúa cada respuesta según:
        1. CLARIDAD (1-10): ¿Es fácil de entender?
        2. PRECISIÓN (1-10): ¿Es técnicamente correcta?
        3. UTILIDAD (1-10): ¿Es práctica y aplicable?
        4. COMPLETITUD (1-10): ¿Cubre aspectos importantes?
        
        Formato de respuesta:
        - Puntuaciones para cada respuesta
        - Justificación de la puntuación
        - Declaración del GANADOR (A, B o C)
        - Explicación de por qué esa respuesta es superior
        """,
        agent=juez,
        expected_output="Evaluación detallada con ganador declarado"
    )
    
    crew_juez = Crew(
        agents=[juez],
        tasks=[tarea_evaluacion],
        process=Process.sequential,
        verbose=1
    )
    
    evaluacion = crew_juez.kickoff()
    
    print("\n" + "="*70)
    print("🏅 RESULTADO DE LA EVALUACIÓN")
    print("="*70)
    print(evaluacion)
    print("="*70 + "\n")
    
    return {
        "respuesta_tecnico": respuesta_tecnico,
        "respuesta_creativo": respuesta_creativo,
        "respuesta_practico": respuesta_practico,
        "evaluacion": evaluacion
    }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    # Ejemplo 1: Pregunta sobre concepto técnico
    print("\n🧪 CASO 1: Pregunta sobre concepto técnico")
    print("="*70)
    
    pregunta1 = "¿Qué es un sistema multi-agente y por qué es útil?"
    resultado1 = ejecutar_competicion(pregunta1)
    
    # Ejemplo 2: Pregunta sobre aplicación práctica
    # print("\n\n🧪 CASO 2: Pregunta sobre aplicación práctica")
    # print("="*70)
    
    # pregunta2 = "¿Cómo puede una empresa pequeña empezar a usar IA?"
    # resultado2 = ejecutar_competicion(pregunta2)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ Diversidad de perspectivas mejora la respuesta final")
    print("✅ El juez proporciona evaluación objetiva")
    print("✅ Minimiza alucinaciones al comparar múltiples outputs")
    print("✅ Patrón útil para decisiones críticas")
    print("="*70 + "\n")


