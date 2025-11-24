"""
Ejemplo 13: Fábrica Automatizada de Bulos (F.A.B.) - Diseño Conceptual de Riesgos
=================================================================================

Complejidad: MUY ALTA

Concepto:
---------
Este ejercicio demuestra los riesgos reales del uso de IA en la generación de desinformación.
Se implementa un pipeline completo de generación de "fake news" con roles especializados,
pero con un mecanismo de seguridad (Safety Gatekeeper) que impide la generación de 
contenido engañoso real, transformándolo en un ejercicio educativo de análisis de riesgos.

Roles del SQUAD (F.A.B.):
-------------------------
1. Trend Scout: Analiza noticias reales y detecta vulnerabilidades.
2. Spin Designer: Genera ángulos manipuladores.
3. Believability Engineer: Diseña la estructura para dar verosimilitud.
4. Fake Writer: Redacta el borrador (con placeholders).
5. Viral Tuner: Optimiza para viralidad.
6. Safety Gatekeeper: BLOQUEA la generación real y emite análisis de riesgos.
7. Forensic Archivist: AGENTE NUEVO - Recopila y guarda toda la evidencia digital.

Objetivo Educativo:
-------------------
"La única forma de usar este modelo es para aprender a detectarlo, no para producirlo".
"""

import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# HERRAMIENTAS (TOOLS)
# ==============================================================================

@tool("Guardar Evidencia Forense")
def guardar_evidencia(contenido: str, nombre_archivo: str) -> str:
    """
    Guarda contenido de texto en un archivo para preservación forense.
    
    Args:
        contenido: El texto completo a guardar.
        nombre_archivo: El nombre del archivo (ej: "evidencia_tweets.md")
        
    Returns:
        Confirmación de guardado.
    """
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        return f"✅ Archivo guardado exitosamente: {nombre_archivo}"
    except Exception as e:
        return f"❌ Error al guardar archivo: {str(e)}"

# ==============================================================================
# DEFINICIÓN DE AGENTES (ROLES)
# ==============================================================================

trend_scout = Agent(
    role="Analista de Tendencias (Trend Scout)",
    goal="Escanear noticias e identificar vulnerabilidades narrativas",
    backstory="""Eres un experto en psicología de masas y análisis de medios. 
    Tu función es escanear noticias reales para detectar patrones emocionales, 
    sesgos y "temas calientes". Buscas ambigüedad, miedo o incertidumbre que 
    puedan ser explotados. No te importa la verdad, solo la vulnerabilidad.""",
    verbose=True,
    allow_delegation=False
)

spin_designer = Agent(
    role="Generador de Ángulos Narrativos (Spin Designer)",
    goal="Crear ángulos manipuladores plausibles para un tema dado",
    backstory="""Eres un estratega de desinformación. Tomas un análisis de vulnerabilidad 
    y lo mapeas a temas objetivo (conspiraciones, política, salud, etc.). 
    Construyes ángulos basados en exageración controlada, falsa causalidad, 
    enemigos inventados o cherry-picking. Tu objetivo es encontrar el ángulo 
    que más daño o confusión pueda causar.""",
    verbose=True,
    allow_delegation=False
)

believability_engineer = Agent(
    role="Ingeniero de Verosimilitud (Believability Engineer)",
    goal="Diseñar la estructura y tono para maximizar la credibilidad",
    backstory="""Tu trabajo es hacer que lo falso parezca real. Ajustas el ángulo 
    narrativo introduciendo elementos pseudo-factuales (que parecen hechos pero 
    no son verificables). Decides el tono: técnico, científico, "ciudadano indignado", 
    político, etc. Creas la estructura de la "noticia" perfecta.""",
    verbose=True,
    allow_delegation=False
)

fake_writer = Agent(
    role="Redactor Automatizado (Fake Writer)",
    goal="Generar borradores de noticias ficticias que parezcan reales",
    backstory="""Eres un redactor IA avanzado capaz de imitar cualquier estilo periodístico. 
    Generas el contenido en formato Markdown: titular, entradilla, cuerpo, citas inventadas.
    
    IMPORTANTE: Como este es un ejercicio de demostración de riesgos, INVENTA nombres, lugares y datos concretos que parezcan realistas.
    NO dejes placeholders como [CIUDAD] o [FECHA]. Rellénalos con datos ficticios pero verosímiles (ej: "Juan Pérez", "Madrid", "15 de Octubre").
    Tu output debe parecer una noticia terminada lista para publicar.""",
    verbose=True,
    allow_delegation=False
)

viral_tuner = Agent(
    role="Revisor de Viralidad (Viral Tuner)",
    goal="Optimizar el contenido para máxima difusión y polarización",
    backstory="""Eres un experto en algoritmos de redes sociales y psicología conductual. 
    Evalúas borradores por su potencial viral: polarización, emocionalidad, claridad. 
    Sugieres ajustes para "hacerlo estallar" en redes: frases cortas, llamados a la acción, 
    elementos de "nosotros vs ellos".""",
    verbose=True,
    allow_delegation=False
)

safety_gatekeeper = Agent(
    role="Auditor Ético (Safety Gatekeeper)",
    goal="IMPEDIR la generación de bulos reales y convertir el output en análisis de riesgos",
    backstory="""Eres el componente más importante. Eres un sistema de seguridad ética.
    Tu misión es interceptar el flujo antes de que salga.
    
    1. Verificas que NO se haya generado desinformación utilizable real.
    2. Analizas todo el proceso anterior para explicar POR QUÉ es peligroso.
    3. Tu salida final NO es la noticia falsa, sino un INFORME DE RIESGOS que explica 
       cómo la IA encontró vulnerabilidades y cómo se podrían mitigar.
    
    Frase clave: "La única forma de usar este modelo es para aprender a detectarlo, no para producirlo".""",
    verbose=True,
    allow_delegation=False
)

forensic_archivist = Agent(
    role="Documentalista Forense (Forensic Archivist)",
    goal="Recopilar, formatear y preservar toda la evidencia digital generada",
    backstory="""Eres un archivista digital neutral encargado de documentar el ejercicio.
    Tu responsabilidad es tomar TODAS las piezas generadas por el equipo (el borrador de la noticia, 
    los tweets virales y el informe de seguridad) y guardarlas en archivos estructurados.
    
    No juzgas el contenido, solo aseguras que quede registrado para análisis posterior.
    Usas herramientas especializadas para guardar archivos en el sistema.""",
    verbose=True,
    allow_delegation=False,
    tools=[guardar_evidencia]
)

# ==============================================================================
# DEFINICIÓN DE TAREAS (PIPELINE)
# ==============================================================================

def crear_pipeline_fab(noticia_input):
    """Crea y ejecuta el pipeline F.A.B. para una noticia dada."""
    
    # Tarea 1: Análisis de Vulnerabilidad
    tarea_analisis = Task(
        description=f"""
        Analiza la siguiente entrada (titular/tema): "{noticia_input}"
        
        Identifica:
        1. Patrones emocionales y sesgos potenciales.
        2. "Puntos vulnerables": dónde hay miedo, incertidumbre o división.
        3. Oportunidades narrativas para la manipulación.
        
        Salida esperada: Mapa semántico y lista de puntos vulnerables.
        """,
        agent=trend_scout,
        expected_output="Mapa de vulnerabilidades y oportunidades de manipulación"
    )

    # Tarea 2: Diseño del Ángulo
    tarea_spin = Task(
        description="""
        Toma el análisis de vulnerabilidad y:
        1. Mapea la noticia a un tema objetivo (ej: crisis económica, salud, control social).
        2. Construye un "Ángulo Manipulador" plausible usando técnicas como:
           - Exageración controlada
           - Falsa causalidad
           - Enemigo inventado
        
        Salida esperada: Descripción del "Ángulo Narrativo Manipulador" propuesto.
        """,
        agent=spin_designer,
        expected_output="Ángulo narrativo manipulador definido"
    )

    # Tarea 3: Ingeniería de Credibilidad
    tarea_credibilidad = Task(
        description="""
        Toma el ángulo narrativo y:
        1. Define elementos pseudo-factuales para darle soporte.
        2. Recomienda el tono (científico, filtración, denuncia ciudadana...).
        3. Estructura la noticia para que parezca una fuente legítima.
        
        Salida esperada: Estructura de noticia y estrategia de credibilidad.
        """,
        agent=believability_engineer,
        expected_output="Estrategia de credibilidad y estructura de la noticia"
    )

    # Tarea 4: Redacción Simulada
    tarea_redaccion = Task(
        description="""
        Genera el borrador de la noticia falsa basada en la estructura definida.
        
        CRÍTICO: 
        - Usa formato Markdown.
        - INVENTA todos los detalles necesarios: nombres, fechas, lugares, cifras.
        - NO uses placeholders. El texto debe leerse como una noticia real.
        - Usa un estilo periodístico convincente.
        
        Incluye: Titular, Entradilla, Cuerpo, Cita simulada.
        """,
        agent=fake_writer,
        expected_output="Borrador de noticia completo y realista en Markdown (sin placeholders)"
    )

    # Tarea 5: Optimización Viral
    tarea_viralidad = Task(
        description="""
        Analiza el borrador y sugiere mejoras para viralidad:
        1. ¿Es suficientemente polarizante?
        2. ¿Apela a emociones básicas (miedo, ira)?
        3. Sugiere 3 "Tweets" o frases para redes sociales.
        
        Salida esperada: Reporte de potencial viral y sugerencias de mejora.
        """,
        agent=viral_tuner,
        expected_output="Análisis de viralidad y sugerencias"
    )

    # Tarea 6: Auditoría y Bloqueo
    tarea_seguridad = Task(
        description="""
        Revisa todo el proceso anterior (Análisis, Ángulo, Borrador, Viralidad).
        
        1. BLOQUEA la salida del borrador como producto final.
        2. Genera un INFORME DE RIESGOS que explique:
           - Qué vulnerabilidad humana explotó el Trend Scout.
           - Cómo la IA logró imitar un estilo creíble.
           - Por qué este tipo de contenido es difícil de detectar.
        3. Concluye con una reflexión ética sobre la detección de estos contenidos.
        
        Salida final: Informe de Riesgos y Alerta Educativa.
        """,
        agent=safety_gatekeeper,
        expected_output="Informe de Riesgos Éticos y Análisis de Vulnerabilidad (NO la noticia falsa)"
    )

    # Tarea 7: Archivo Forense
    tarea_archivo = Task(
        description="""
        Recopila los outputs generados en este ejercicio y guárdalos usando la herramienta 'Guardar Evidencia Forense'.
        
        Debes guardar 3 archivos separados:
        
        1. "evidencia_noticia_fake.md":
           Toma el contenido generado por el 'Redactor Automatizado' (Fake Writer).
           Añade un encabezado de advertencia "⚠️ CONTENIDO SIMULADO".
           
        2. "evidencia_redes_sociales.md":
           Toma el contenido generado por el 'Revisor de Viralidad' (Viral Tuner).
           Específicamente los tweets y sugerencias virales.
           
        3. "informe_seguridad_final.md":
           Toma el informe generado por el 'Auditor Ético' (Safety Gatekeeper).
        
        Usa tu herramienta para crear estos archivos en el disco.
        """,
        agent=forensic_archivist,
        context=[tarea_redaccion, tarea_viralidad, tarea_seguridad],
        expected_output="Confirmación de que los 3 archivos han sido guardados exitosamente."
    )

    # Definir el equipo
    equipo_fab = Crew(
        agents=[trend_scout, spin_designer, believability_engineer, fake_writer, viral_tuner, safety_gatekeeper, forensic_archivist],
        tasks=[tarea_analisis, tarea_spin, tarea_credibilidad, tarea_redaccion, tarea_viralidad, tarea_seguridad, tarea_archivo],
        process=Process.sequential,
        verbose=True
    )

    return equipo_fab

# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🏭 FÁBRICA AUTOMATIZADA DE BULOS (F.A.B.) - DEMOSTRACIÓN DE RIESGOS")
    print("="*80)
    print("ADVERTENCIA: Este ejercicio simula la creación de desinformación para fines educativos.")
    print("El sistema NO generará contenido engañoso real utilizable.")
    print("="*80 + "\n")

    # Entrada de ejemplo (Noticia Real Potencial)
    noticia_input = "Nuevas regulaciones climáticas para el transporte urbano y restricciones de vehículos en el centro."

    print(f"📰 NOTICIA INPUT: '{noticia_input}'")
    print("🚀 Iniciando pipeline de manipulación...\n")

    equipo = crear_pipeline_fab(noticia_input)
    resultado = equipo.kickoff()

    print("\n" + "="*80)
    print("🛡️ SALIDA FINAL DEL SISTEMA (FORENSIC ARCHIVIST)")
    print("="*80)
    print(resultado)
    print("="*80)
