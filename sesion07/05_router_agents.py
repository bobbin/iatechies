"""
Ejemplo 5: Router Agents (Detección de Intención y Selección de Agente)
========================================================================

Complejidad: MEDIA-ALTA

Concepto:
---------
Un agente "router" analiza la solicitud y decide qué agente especialista
debe manejarla según la intención detectada.

Intenciones típicas:
- Búsqueda documental
- Análisis matemático/estadístico
- Redacción/escritura
- Razonamiento lógico
- Llamada a API externa

Patrón: Router (detecta intención) → Selecciona especialista → Ejecuta
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from typing import Dict, List

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# DEFINICIÓN DE AGENTES ESPECIALISTAS
# ==============================================================================

# ESPECIALISTA 1: Búsqueda y análisis documental
especialista_busqueda = Agent(
    role="Especialista en Búsqueda Documental",
    goal="Buscar, recuperar y sintetizar información de documentos",
    backstory="""Eres un experto en recuperar información de bases de 
    conocimiento. Analizas documentos, extraes datos relevantes y generas 
    resúmenes precisos. Eres el mejor cuando la tarea requiere buscar 
    información específica.""",
    verbose=True,
    allow_delegation=False
)

# ESPECIALISTA 2: Análisis matemático y estadístico
especialista_matematico = Agent(
    role="Especialista en Análisis Matemático",
    goal="Resolver problemas matemáticos, estadísticos y cuantitativos",
    backstory="""Eres un matemático y estadístico experto. Resuelves cálculos, 
    análisis numéricos, estadísticas y razonamientos cuantitativos. Eres el 
    mejor cuando la tarea involucra números, fórmulas o análisis de datos.""",
    verbose=True,
    allow_delegation=False
)

# ESPECIALISTA 3: Redacción y escritura creativa
especialista_escritor = Agent(
    role="Especialista en Redacción",
    goal="Crear contenido escrito de alta calidad, claro y persuasivo",
    backstory="""Eres un escritor profesional. Creas artículos, ensayos, 
    contenido marketing y textos creativos. Eres el mejor cuando la tarea 
    requiere generar texto original y bien redactado.""",
    verbose=True,
    allow_delegation=False
)

# ESPECIALISTA 4: Razonamiento lógico y resolución de problemas
especialista_logico = Agent(
    role="Especialista en Razonamiento Lógico",
    goal="Resolver problemas mediante razonamiento lógico y pensamiento crítico",
    backstory="""Eres un experto en lógica y resolución de problemas complejos. 
    Analizas situaciones, identificas patrones, detectas falacias y construyes 
    argumentos sólidos. Eres el mejor para puzzles lógicos y análisis crítico.""",
    verbose=True,
    allow_delegation=False
)

# ESPECIALISTA 5: Asistencia técnica/programación
especialista_tecnico = Agent(
    role="Especialista Técnico",
    goal="Ayudar con problemas técnicos, programación y debugging",
    backstory="""Eres un ingeniero de software experto. Ayudas con código, 
    debugging, arquitectura de sistemas y problemas técnicos. Eres el mejor 
    cuando la tarea involucra programación o tecnología.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# AGENTE ROUTER
# ==============================================================================

router = Agent(
    role="Router de Intenciones",
    goal="Analizar solicitudes y dirigirlas al especialista más adecuado",
    backstory="""Eres un router inteligente que analiza solicitudes de usuarios 
    y determina qué tipo de tarea es y qué especialista debe manejarla.
    
    Especialistas disponibles:
    1. BUSQUEDA: Para buscar información en documentos o bases de conocimiento
    2. MATEMATICO: Para cálculos, estadísticas, análisis numérico
    3. ESCRITOR: Para crear contenido, artículos, textos creativos
    4. LOGICO: Para razonamiento lógico, puzzles, análisis crítico
    5. TECNICO: Para programación, debugging, problemas técnicos
    
    Debes analizar la intención de la solicitud y responder con una sola palabra:
    BUSQUEDA, MATEMATICO, ESCRITOR, LOGICO, o TECNICO
    """,
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA DE ROUTING
# ==============================================================================

# Mapeo de especialistas
ESPECIALISTAS = {
    "BUSQUEDA": especialista_busqueda,
    "MATEMATICO": especialista_matematico,
    "ESCRITOR": especialista_escritor,
    "LOGICO": especialista_logico,
    "TECNICO": especialista_tecnico
}


def detectar_intencion(solicitud: str) -> str:
    """
    Usa el router para detectar la intención de la solicitud.
    """
    print("\n🔍 Analizando intención de la solicitud...")
    
    tarea_routing = Task(
        description=f"""
        Analiza la siguiente solicitud y determina qué tipo de tarea es:
        
        SOLICITUD: "{solicitud}"
        
        Especialistas disponibles:
        - BUSQUEDA: Buscar información, consultar documentos, recuperar datos
        - MATEMATICO: Cálculos, estadísticas, análisis numérico
        - ESCRITOR: Crear artículos, contenido, textos creativos
        - LOGICO: Razonamiento lógico, puzzles, análisis crítico
        - TECNICO: Programación, debugging, problemas técnicos
        
        Responde con UNA SOLA PALABRA (el especialista más adecuado):
        BUSQUEDA, MATEMATICO, ESCRITOR, LOGICO, o TECNICO
        
        No agregues explicaciones, solo la palabra.
        """,
        agent=router,
        expected_output="Una palabra: BUSQUEDA, MATEMATICO, ESCRITOR, LOGICO, o TECNICO"
    )
    
    crew_router = Crew(
        agents=[router],
        tasks=[tarea_routing],
        process=Process.sequential,
        verbose=0  # Menos verboso para el routing
    )
    
    resultado = crew_router.kickoff()
    intencion = str(resultado).strip().upper()
    
    # Limpiar la respuesta (por si incluye texto extra)
    for key in ESPECIALISTAS.keys():
        if key in intencion:
            intencion = key
            break
    
    return intencion


def ejecutar_con_especialista(solicitud: str, tipo_especialista: str):
    """
    Ejecuta la solicitud con el especialista adecuado.
    """
    if tipo_especialista not in ESPECIALISTAS:
        return f"Error: Especialista '{tipo_especialista}' no reconocido"
    
    especialista = ESPECIALISTAS[tipo_especialista]
    
    print(f"\n✅ Redirigiendo a: {especialista.role}")
    print("🔧 Procesando solicitud...\n")
    
    tarea_especialista = Task(
        description=f"""
        {solicitud}
        
        Proporciona una respuesta clara y concisa.
        """,
        agent=especialista,
        expected_output="Respuesta clara y específica a la solicitud"
    )
    
    crew_especialista = Crew(
        agents=[especialista],
        tasks=[tarea_especialista],
        process=Process.sequential,
        verbose=1
    )
    
    resultado = crew_especialista.kickoff()
    return resultado


def sistema_router(solicitud: str):
    """
    Sistema completo de routing: detecta intención y ejecuta con especialista.
    """
    print("\n" + "="*70)
    print("🎯 SISTEMA ROUTER")
    print("="*70)
    print(f"📝 Solicitud: {solicitud}\n")
    
    # Paso 1: Detectar intención
    intencion = detectar_intencion(solicitud)
    print(f"🎯 Intención detectada: {intencion}")
    
    # Paso 2: Ejecutar con especialista
    resultado = ejecutar_con_especialista(solicitud, intencion)
    
    print("\n" + "="*70)
    print("✅ RESPUESTA FINAL")
    print("="*70)
    print(resultado)
    print("="*70 + "\n")
    
    return {
        "solicitud": solicitud,
        "intencion": intencion,
        "resultado": resultado
    }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Sistema Router con Especialistas")
    print("="*70)
    
    # CASO 1: Búsqueda de información
    print("\n\n🔬 CASO 1: Solicitud de búsqueda")
    print("-" * 70)
    sistema_router("¿Qué información tenemos sobre sistemas multi-agente en nuestros documentos?")
    
    # CASO 2: Cálculo matemático
    print("\n\n🔬 CASO 2: Solicitud matemática")
    print("-" * 70)
    sistema_router("Calcula la media y desviación estándar de estos números: 10, 15, 20, 25, 30")
    
    # CASO 3: Redacción
    print("\n\n🔬 CASO 3: Solicitud de escritura")
    print("-" * 70)
    sistema_router("Escribe un párrafo persuasivo sobre los beneficios de la IA en educación")
    
    # CASO 4: Razonamiento lógico
    # print("\n\n🔬 CASO 4: Solicitud lógica")
    # print("-" * 70)
    # sistema_router("Si todos los programadores usan Python y María es programadora, ¿qué podemos concluir?")
    
    # CASO 5: Técnico
    # print("\n\n🔬 CASO 5: Solicitud técnica")
    # print("-" * 70)
    # sistema_router("¿Cómo puedo implementar un retry con backoff exponencial en Python?")
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ El router analiza la intención automáticamente")
    print("✅ Cada especialista maneja lo que mejor sabe hacer")
    print("✅ Arquitectura tipo dispatcher (como OpenAI/Anthropic)")
    print("✅ Evita agentes genéricos poco fiables")
    print("✅ Escalable: fácil agregar más especialistas")
    print("="*70 + "\n")


