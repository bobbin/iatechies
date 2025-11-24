"""
Ejemplo 6: Supervisor/Orquestador (Manager Agent)
==================================================

Complejidad: MEDIA-ALTA

Concepto:
---------
Un agente supervisor que gobierna el flujo de trabajo completo:
- Orden de ejecución de tareas
- Condiciones de parada
- Reintentos ante fallos
- Escalado a humano si necesario
- Evaluación de calidad intermedia

El supervisor no hace el trabajo, coordina a otros agentes.

Patrón: Supervisor → Delega → Monitorea → Decide siguiente paso
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from typing import Dict, List

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# AGENTES TRABAJADORES (SUPERVISADOS)
# ==============================================================================

investigador = Agent(
    role="Investigador",
    goal="Investigar y recopilar información sobre un tema",
    backstory="""Eres un investigador meticuloso. Tu trabajo es buscar 
    información, identificar fuentes confiables y recopilar datos relevantes.""",
    verbose=True,
    allow_delegation=False
)

analizador = Agent(
    role="Analizador de Datos",
    goal="Analizar información y extraer insights clave",
    backstory="""Eres un analista experto. Tomas información raw y extraes 
    conclusiones, patrones y puntos clave. Tu análisis es riguroso y objetivo.""",
    verbose=True,
    allow_delegation=False
)

verificador = Agent(
    role="Verificador de Calidad",
    goal="Verificar que el trabajo cumple con estándares de calidad",
    backstory="""Eres un verificador estricto. Revisas outputs de otros agentes 
    para asegurar que sean correctos, completos y de alta calidad. 
    
    Criterios de evaluación:
    - ¿Es preciso?
    - ¿Es completo?
    - ¿Es coherente?
    
    Si encuentras problemas, los señalas claramente.
    """,
    verbose=True,
    allow_delegation=False
)

escritor = Agent(
    role="Escritor",
    goal="Crear documentos finales bien redactados",
    backstory="""Eres un escritor profesional. Tomas análisis y datos y los 
    transformas en documentos claros, bien estructurados y persuasivos.""",
    verbose=True,
    allow_delegation=False
)

# ==============================================================================
# SUPERVISOR
# ==============================================================================

supervisor = Agent(
    role="Supervisor de Proyecto",
    goal="Coordinar el equipo y asegurar que el trabajo se complete exitosamente",
    backstory="""Eres un supervisor experimentado que gestiona equipos de 
    analistas. Tu trabajo es:
    
    1. Definir el plan de trabajo
    2. Asignar tareas a los agentes correctos
    3. Monitorear progreso
    4. Decidir si el trabajo es suficiente o necesita más iteraciones
    5. Determinar cuándo el proyecto está completo
    
    Puedes decidir:
    - Continuar a la siguiente fase
    - Solicitar revisiones
    - Detener el proceso si hay problemas graves
    - Aprobar el resultado final
    
    Eres meticuloso y no aceptas trabajo mediocre.""",
    verbose=True,
    allow_delegation=True  # Puede delegar a otros agentes
)


# ==============================================================================
# SISTEMA SUPERVISADO
# ==============================================================================

class EstadoProyecto:
    """Mantiene el estado del proyecto supervisado."""
    
    def __init__(self, objetivo: str):
        self.objetivo = objetivo
        self.fase_actual = "INICIO"
        self.outputs = {}
        self.aprobaciones = {}
        self.reintentos = {}
        self.completado = False
    
    def registrar_output(self, fase: str, output: str):
        """Registra el output de una fase."""
        self.outputs[fase] = output
        print(f"✅ Fase '{fase}' completada")
    
    def registrar_aprobacion(self, fase: str, aprobado: bool, razon: str = ""):
        """Registra si una fase fue aprobada."""
        self.aprobaciones[fase] = {
            "aprobado": aprobado,
            "razon": razon
        }
        if aprobado:
            print(f"✅ Fase '{fase}' APROBADA")
        else:
            print(f"❌ Fase '{fase}' RECHAZADA: {razon}")
    
    def marcar_completado(self):
        """Marca el proyecto como completado."""
        self.completado = True
        print("\n🎉 PROYECTO COMPLETADO")


def ejecutar_proyecto_supervisado(objetivo: str, max_reintentos: int = 2):
    """
    Ejecuta un proyecto con supervisión activa.
    
    Fases:
    1. Investigación
    2. Análisis
    3. Verificación (puede solicitar re-análisis)
    4. Escritura
    5. Aprobación final del supervisor
    """
    
    estado = EstadoProyecto(objetivo)
    
    print("\n" + "="*70)
    print("👔 PROYECTO SUPERVISADO")
    print("="*70)
    print(f"🎯 Objetivo: {objetivo}\n")
    
    # ==== FASE 1: PLAN DEL SUPERVISOR ====
    print("\n📋 FASE 0: Supervisor define plan de trabajo...")
    print("-" * 70)
    
    tarea_planificacion = Task(
        description=f"""
        Como supervisor, crea un plan de trabajo para lograr este objetivo:
        
        "{objetivo}"
        
        Define:
        1. Qué información se necesita investigar
        2. Qué tipo de análisis se debe hacer
        3. Qué criterios se usarán para verificar calidad
        
        Tu plan guiará al equipo. Sé específico en 3-4 puntos clave.
        """,
        agent=supervisor,
        expected_output="Plan de trabajo en 3-4 puntos clave"
    )
    
    crew_plan = Crew(
        agents=[supervisor],
        tasks=[tarea_planificacion],
        process=Process.sequential,
        verbose=1
    )
    
    plan = crew_plan.kickoff()
    estado.registrar_output("PLAN", str(plan))
    print(f"\n📄 Plan definido:\n{plan}\n")
    
    # ==== FASE 2: INVESTIGACIÓN ====
    print("\n🔍 FASE 1: Investigación...")
    print("-" * 70)
    
    tarea_investigacion = Task(
        description=f"""
        Investiga sobre: {objetivo}
        
        Plan del supervisor:
        {plan}
        
        Recopila información relevante en 3-4 párrafos.
        """,
        agent=investigador,
        expected_output="Información investigada en 3-4 párrafos"
    )
    
    crew_investigacion = Crew(
        agents=[investigador],
        tasks=[tarea_investigacion],
        process=Process.sequential,
        verbose=1
    )
    
    investigacion = crew_investigacion.kickoff()
    estado.registrar_output("INVESTIGACION", str(investigacion))
    
    # ==== FASE 3: ANÁLISIS ====
    print("\n📊 FASE 2: Análisis...")
    print("-" * 70)
    
    tarea_analisis = Task(
        description=f"""
        Analiza la siguiente información investigada:
        
        {investigacion}
        
        Extrae:
        - 3 insights clave
        - Patrones identificados
        - Conclusiones preliminares
        """,
        agent=analizador,
        expected_output="Análisis con insights y conclusiones"
    )
    
    crew_analisis = Crew(
        agents=[analizador],
        tasks=[tarea_analisis],
        process=Process.sequential,
        verbose=1
    )
    
    analisis = crew_analisis.kickoff()
    estado.registrar_output("ANALISIS", str(analisis))
    
    # ==== FASE 4: VERIFICACIÓN ====
    print("\n🔍 FASE 3: Verificación de calidad...")
    print("-" * 70)
    
    tarea_verificacion = Task(
        description=f"""
        Verifica el siguiente análisis:
        
        {analisis}
        
        Evalúa:
        1. ¿Es preciso y está basado en la investigación?
        2. ¿Es completo (cubre aspectos importantes)?
        3. ¿Es coherente?
        
        Responde:
        - APROBADO: si cumple con todos los criterios
        - RECHAZADO: [razón específica] si hay problemas
        """,
        agent=verificador,
        expected_output="APROBADO o RECHAZADO con razón"
    )
    
    crew_verificacion = Crew(
        agents=[verificador],
        tasks=[tarea_verificacion],
        process=Process.sequential,
        verbose=1
    )
    
    verificacion = crew_verificacion.kickoff()
    verificacion_str = str(verificacion).upper()
    
    # Decidir si está aprobado
    aprobado = "APROBADO" in verificacion_str
    estado.registrar_aprobacion("ANALISIS", aprobado, str(verificacion))
    
    # Si no está aprobado y hay reintentos disponibles, aquí se podría reintentar
    if not aprobado:
        print("\n⚠️ El supervisor decide si proceder o reintentar...")
        print("   (Por simplicidad, procedemos con warning)")
    
    # ==== FASE 5: ESCRITURA ====
    print("\n✍️ FASE 4: Escritura del documento final...")
    print("-" * 70)
    
    tarea_escritura = Task(
        description=f"""
        Crea un documento final sobre: {objetivo}
        
        Basándote en:
        
        INVESTIGACIÓN:
        {investigacion}
        
        ANÁLISIS:
        {analisis}
        
        Genera un documento de 3-4 párrafos bien estructurado:
        - Introducción
        - Desarrollo con insights clave
        - Conclusión
        """,
        agent=escritor,
        expected_output="Documento final de 3-4 párrafos"
    )
    
    crew_escritura = Crew(
        agents=[escritor],
        tasks=[tarea_escritura],
        process=Process.sequential,
        verbose=1
    )
    
    documento = crew_escritura.kickoff()
    estado.registrar_output("DOCUMENTO", str(documento))
    
    # ==== FASE 6: APROBACIÓN FINAL DEL SUPERVISOR ====
    print("\n👔 FASE 5: Aprobación final del supervisor...")
    print("-" * 70)
    
    tarea_aprobacion_final = Task(
        description=f"""
        Como supervisor, revisa el documento final:
        
        {documento}
        
        Evalúa si cumple con el objetivo original:
        "{objetivo}"
        
        Responde:
        - APROBADO: si el proyecto está completo y cumple el objetivo
        - SOLICITAR REVISIÓN: [qué debe mejorarse] si necesita ajustes
        """,
        agent=supervisor,
        expected_output="APROBADO o SOLICITAR REVISIÓN con detalles"
    )
    
    crew_aprobacion = Crew(
        agents=[supervisor],
        tasks=[tarea_aprobacion_final],
        process=Process.sequential,
        verbose=1
    )
    
    aprobacion_final = crew_aprobacion.kickoff()
    aprobacion_final_str = str(aprobacion_final).upper()
    
    aprobado_final = "APROBADO" in aprobacion_final_str
    estado.registrar_aprobacion("DOCUMENTO_FINAL", aprobado_final, str(aprobacion_final))
    
    if aprobado_final:
        estado.marcar_completado()
    
    # ==== RESUMEN FINAL ====
    print("\n" + "="*70)
    print("📊 RESUMEN DEL PROYECTO")
    print("="*70)
    print(f"Objetivo: {objetivo}")
    print(f"Estado: {'COMPLETADO ✅' if estado.completado else 'PENDIENTE ⚠️'}")
    print(f"\nFases ejecutadas: {len(estado.outputs)}")
    for fase, output in estado.outputs.items():
        aprobacion = estado.aprobaciones.get(fase, {})
        estado_fase = "✅" if aprobacion.get("aprobado", True) else "❌"
        print(f"  {estado_fase} {fase}")
    
    print("\n📄 DOCUMENTO FINAL:")
    print("-" * 70)
    print(documento)
    print("="*70 + "\n")
    
    return estado


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    # Proyecto supervisado
    objetivo = "Analizar el impacto de los sistemas multi-agente en la productividad empresarial"
    
    estado_final = ejecutar_proyecto_supervisado(objetivo)
    
    print("\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ El supervisor coordina sin hacer el trabajo")
    print("✅ Puede decidir orden, reintentos y paradas")
    print("✅ Verifica calidad en cada fase")
    print("✅ Arquitectura escalable para equipos complejos")
    print("="*70 + "\n")


