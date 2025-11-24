"""
Ejemplo 2: Self-Prompt Editing (Optimización de Prompts)
=========================================================

Complejidad: BAJA-MEDIA

Concepto:
---------
El agente adapta su prompt según los errores detectados:
- Falta de evidencia
- Exceso de ruido
- Ambigüedad en la query

El sistema aprende a hacer mejores preguntas.

Patrón: Consulta → Error → Optimizar Prompt → Nueva Consulta
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# SIMULACIÓN DE BASE DE CONOCIMIENTO
# ==============================================================================

# Base de conocimiento simulada (en producción sería un RAG real)
BASE_CONOCIMIENTO = {
    "python": [
        "Python es un lenguaje de programación interpretado de alto nivel",
        "Python fue creado por Guido van Rossum en 1991",
        "Python destaca por su sintaxis clara y legible"
    ],
    "machine learning": [
        "Machine Learning es una rama de la IA que permite a las máquinas aprender",
        "Los algoritmos de ML incluyen supervisado, no supervisado y por refuerzo",
        "TensorFlow y PyTorch son frameworks populares para ML"
    ],
    "crewai": [
        "CrewAI es un framework para construir sistemas multi-agente",
        "CrewAI permite definir roles, objetivos y tareas para agentes",
        "Los agentes en CrewAI pueden colaborar y delegar tareas"
    ]
}


def buscar_informacion(query: str) -> dict:
    """
    Simula una búsqueda en base de conocimiento.
    Retorna resultados y metadatos de calidad.
    """
    query_lower = query.lower()
    resultados = []
    
    # Buscar coincidencias
    for tema, contenidos in BASE_CONOCIMIENTO.items():
        if tema in query_lower:
            resultados.extend(contenidos)
    
    # Evaluar calidad de resultados
    if len(resultados) == 0:
        estado = "SIN_RESULTADOS"
        mensaje = "No se encontró información relevante"
    elif len(resultados) <= 2:
        estado = "POCOS_RESULTADOS"
        mensaje = "Se encontraron pocos resultados, considera ampliar la búsqueda"
    else:
        estado = "EXITO"
        mensaje = "Búsqueda exitosa"
    
    return {
        "estado": estado,
        "resultados": resultados,
        "mensaje": mensaje,
        "num_resultados": len(resultados)
    }


# ==============================================================================
# DEFINICIÓN DE AGENTES
# ==============================================================================

# AGENTE 1: Buscador inicial
buscador = Agent(
    role="Agente Buscador",
    goal="Buscar información relevante en la base de conocimiento",
    backstory="""Eres un agente que busca información. Comienzas con una 
    consulta inicial y evalúas si los resultados son suficientes.""",
    verbose=True,
    allow_delegation=False
)

# AGENTE 2: Optimizador de prompts
optimizador = Agent(
    role="Optimizador de Consultas",
    goal="Mejorar consultas que no obtuvieron buenos resultados",
    backstory="""Eres un experto en reformular preguntas. Cuando una búsqueda 
    falla o da pocos resultados, analizas por qué y creas una versión mejorada 
    de la consulta. 
    
    Técnicas que usas:
    - Agregar sinónimos y términos relacionados
    - Reformular de forma más amplia o más específica
    - Cambiar el enfoque de la pregunta
    - Incluir contexto adicional
    """,
    verbose=True,
    allow_delegation=False
)

# AGENTE 3: Respondedor
respondedor = Agent(
    role="Agente Respondedor",
    goal="Generar respuestas basadas en la información encontrada",
    backstory="""Eres un agente que sintetiza información y genera respuestas 
    claras. Solo respondes con base en los datos obtenidos.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# FLUJO CON AUTO-OPTIMIZACIÓN
# ==============================================================================

def ejecutar_busqueda_adaptativa(pregunta_usuario: str):
    """
    Ejecuta búsqueda con auto-optimización del prompt.
    """
    print("\n" + "="*70)
    print(f"🔍 BÚSQUEDA ADAPTATIVA")
    print(f"❓ Pregunta original: {pregunta_usuario}")
    print("="*70 + "\n")
    
    # ==== PASO 1: Búsqueda inicial ====
    print("\n📊 PASO 1: Búsqueda inicial...")
    resultado_busqueda = buscar_informacion(pregunta_usuario)
    
    print(f"Estado: {resultado_busqueda['estado']}")
    print(f"Mensaje: {resultado_busqueda['mensaje']}")
    print(f"Resultados encontrados: {resultado_busqueda['num_resultados']}")
    
    # ==== PASO 2: Decidir si optimizar ====
    if resultado_busqueda['estado'] != "EXITO":
        print("\n⚠️ PASO 2: Resultados insuficientes, optimizando consulta...")
        
        # Crear tarea para optimizar
        tarea_optimizacion = Task(
            description=f"""
            La búsqueda original dio estos resultados:
            - Estado: {resultado_busqueda['estado']}
            - Mensaje: {resultado_busqueda['mensaje']}
            - Pregunta original: "{pregunta_usuario}"
            
            Tu tarea:
            1. Analiza por qué la búsqueda falló
            2. Genera una versión mejorada de la consulta que probablemente 
               obtenga mejores resultados
            
            Temas disponibles en la base: python, machine learning, crewai
            
            Responde SOLO con la nueva consulta, sin explicaciones adicionales.
            """,
            agent=optimizador,
            expected_output="Una consulta optimizada (una línea de texto)"
        )
        
        # Ejecutar optimización
        crew_optimizacion = Crew(
            agents=[optimizador],
            tasks=[tarea_optimizacion],
            process=Process.sequential,
            verbose=1
        )
        
        nueva_consulta = crew_optimizacion.kickoff()
        print(f"\n✨ Nueva consulta optimizada: {nueva_consulta}")
        
        # ==== PASO 3: Re-búsqueda con prompt optimizado ====
        print("\n🔄 PASO 3: Re-búsqueda con consulta optimizada...")
        resultado_busqueda = buscar_informacion(str(nueva_consulta))
        
        print(f"Estado: {resultado_busqueda['estado']}")
        print(f"Resultados encontrados: {resultado_busqueda['num_resultados']}")
    
    # ==== PASO 4: Generar respuesta final ====
    print("\n📝 PASO 4: Generando respuesta final...")
    
    if resultado_busqueda['num_resultados'] > 0:
        # Crear tarea para responder
        tarea_respuesta = Task(
            description=f"""
            Pregunta del usuario: {pregunta_usuario}
            
            Información encontrada:
            {chr(10).join(f"- {r}" for r in resultado_busqueda['resultados'])}
            
            Genera una respuesta clara y concisa basada SOLO en esta información.
            """,
            agent=respondedor,
            expected_output="Respuesta clara en 2-3 oraciones"
        )
        
        crew_respuesta = Crew(
            agents=[respondedor],
            tasks=[tarea_respuesta],
            process=Process.sequential,
            verbose=1
        )
        
        respuesta_final = crew_respuesta.kickoff()
    else:
        respuesta_final = "Lo siento, no pude encontrar información relevante incluso después de optimizar la búsqueda."
    
    print("\n" + "="*70)
    print("✅ RESPUESTA FINAL")
    print("="*70)
    print(respuesta_final)
    print("="*70 + "\n")
    
    return respuesta_final


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Self-Prompt Editing")
    print("="*70)
    
    # CASO 1: Pregunta que falla y se auto-optimiza
    print("\n\n🔬 CASO 1: Pregunta ambigua (debería optimizarse)")
    print("-" * 70)
    pregunta1 = "¿Qué es programación?"  # Muy genérico, no matchea temas específicos
    ejecutar_busqueda_adaptativa(pregunta1)
    
    # CASO 2: Pregunta que funciona directamente
    print("\n\n🔬 CASO 2: Pregunta específica (debería funcionar directamente)")
    print("-" * 70)
    pregunta2 = "¿Qué es CrewAI y para qué sirve?"  # Match directo
    ejecutar_busqueda_adaptativa(pregunta2)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ El sistema detecta cuando una consulta falla")
    print("✅ Auto-optimiza el prompt para obtener mejores resultados")
    print("✅ Aprende a hacer preguntas más efectivas")
    print("✅ Patrón aplicable a RAG, búsquedas y APIs")
    print("="*70 + "\n")


