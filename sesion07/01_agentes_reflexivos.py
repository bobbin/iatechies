"""
Ejemplo 1: Agentes Reflexivos (Self-Reflection Loop)
=====================================================

Complejidad: BAJA

Concepto:
---------
Un patrón mínimo donde el agente:
1. Genera una respuesta inicial
2. Se critica a sí mismo
3. Produce una versión mejorada

Esto demuestra que un agente es más que un "prompt largo" y puede 
revisar su propio output antes de entregarlo.

Patrón: Genera → Critica → Mejora
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# DEFINICIÓN DE AGENTES
# ==============================================================================

# AGENTE 1: Escritor inicial (genera primera versión)
escritor = Agent(
    role="Escritor de Contenido",
    goal="Crear un artículo claro y bien estructurado sobre el tema solicitado",
    backstory="""Eres un escritor experimentado que puede crear contenido 
    sobre cualquier tema. Tu primera versión siempre es buena, pero sabes 
    que puede mejorarse con revisión.""",
    verbose=True,
    allow_delegation=False  # No delega, trabaja solo
)

# AGENTE 2: Crítico interno (revisa y critica)
critico = Agent(
    role="Crítico de Contenido",
    goal="Identificar debilidades, inconsistencias y áreas de mejora en el contenido",
    backstory="""Eres un crítico literario con ojo clínico. Analizas textos 
    buscando problemas de claridad, estructura, evidencia y coherencia. 
    Tu trabajo es encontrar qué puede mejorarse.""",
    verbose=True,
    allow_delegation=False
)

# AGENTE 3: Editor final (incorpora feedback y mejora)
editor = Agent(
    role="Editor Refinador",
    goal="Crear la versión final del contenido incorporando las críticas recibidas",
    backstory="""Eres un editor senior que toma textos iniciales y críticas 
    constructivas para producir versiones mejoradas. Mantienes lo bueno y 
    corriges lo señalado.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# DEFINICIÓN DE TAREAS (FLUJO REFLEXIVO)
# ==============================================================================

def crear_flujo_reflexivo(tema: str):
    """
    Crea el flujo de tareas para el patrón reflexivo.
    
    Flujo:
    1. Escritor crea versión inicial
    2. Crítico analiza y señala problemas
    3. Editor produce versión mejorada
    """
    
    # TAREA 1: Generar contenido inicial
    tarea_escritura = Task(
        description=f"""
        Escribe un artículo corto (3 párrafos) sobre: {tema}
        
        Requisitos:
        - Introducción clara
        - Desarrollo con ejemplos
        - Conclusión
        
        Sé conciso pero informativo.
        """,
        agent=escritor,
        expected_output="Un artículo de 3 párrafos bien estructurado"
    )
    
    # TAREA 2: Crítica reflexiva
    tarea_critica = Task(
        description="""
        Analiza el artículo generado y proporciona crítica constructiva.
        
        Evalúa:
        - Claridad de las ideas
        - Calidad de los ejemplos
        - Coherencia entre párrafos
        - Solidez de la conclusión
        
        Lista 3-5 puntos específicos de mejora.
        No reescribas el texto, solo señala qué mejorar.
        """,
        agent=critico,
        expected_output="Lista de 3-5 puntos de mejora específicos",
        context=[tarea_escritura]  # Depende de la tarea anterior
    )
    
    # TAREA 3: Refinamiento final
    tarea_refinamiento = Task(
        description="""
        Toma el artículo original y las críticas recibidas para crear 
        una versión mejorada.
        
        Instrucciones:
        - Mantén la estructura original
        - Incorpora las mejoras sugeridas
        - Corrige los problemas señalados
        - Preserva lo que funcionaba bien
        
        Genera la versión final del artículo.
        """,
        agent=editor,
        expected_output="Versión mejorada del artículo incorporando el feedback",
        context=[tarea_escritura, tarea_critica]  # Depende de ambas anteriores
    )
    
    return [tarea_escritura, tarea_critica, tarea_refinamiento]


# ==============================================================================
# EJECUCIÓN DEL CREW REFLEXIVO
# ==============================================================================

def ejecutar_reflexion(tema: str):
    """
    Ejecuta el patrón de reflexión completo.
    """
    print("\n" + "="*70)
    print(f"🔄 INICIANDO PATRÓN REFLEXIVO")
    print(f"📝 Tema: {tema}")
    print("="*70 + "\n")
    
    # Crear tareas del flujo reflexivo
    tareas = crear_flujo_reflexivo(tema)
    
    # Crear el Crew (equipo)
    crew = Crew(
        agents=[escritor, critico, editor],
        tasks=tareas,
        process=Process.sequential,  # Ejecutar en secuencia: escribir → criticar → refinar
        verbose=2  # Máximo detalle en los logs
    )
    
    # Ejecutar el flujo completo
    resultado = crew.kickoff()
    
    print("\n" + "="*70)
    print("✅ RESULTADO FINAL (después de reflexión)")
    print("="*70)
    print(resultado)
    print("="*70 + "\n")
    
    return resultado


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":
    # Ejemplo 1: Tema técnico
    tema1 = "los beneficios de la arquitectura multi-agente en IA"
    resultado1 = ejecutar_reflexion(tema1)
    
    # Ejemplo 2: Tema general
    # tema2 = "cómo la inteligencia artificial está transformando la medicina"
    # resultado2 = ejecutar_reflexion(tema2)
    
    print("\n✨ Observa cómo el artículo final es mejor que la versión inicial")
    print("📊 Este patrón funciona porque:")
    print("   1. El crítico identifica problemas específicos")
    print("   2. El editor incorpora mejoras sistemáticamente")
    print("   3. El resultado es más robusto que un single-shot")


