"""
Ejercicio 19 — Estudio de mercado completo con CrewAI.

Crea un equipo completo que realiza un estudio de mercado,
siguiendo el ejemplo de las slides C4.
"""

from __future__ import annotations

import os
from pathlib import Path

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 19: ESTUDIO DE MERCADO COMPLETO CON CREWAI\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Equipo completo para estudio de mercado
    investigador = Agent(
        role="Investigador de Mercado",
        goal="Recopilar información relevante sobre el mercado objetivo",
        backstory=(
            "Eres un investigador con 10 años de experiencia en estudios de mercado. "
            "Te especializas en encontrar datos, estadísticas y tendencias. "
            "Eres meticuloso y siempre buscas múltiples fuentes de información."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    analista = Agent(
        role="Analista de Datos",
        goal="Analizar y sintetizar la información recopilada",
        backstory=(
            "Eres un analista con experiencia en interpretar datos complejos. "
            "Tu trabajo es identificar patrones, oportunidades y amenazas. "
            "Eres objetivo y basas tus conclusiones en evidencia."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    escritor = Agent(
        role="Escritor de Informes",
        goal="Crear informes claros y profesionales",
        backstory=(
            "Eres un escritor técnico con experiencia en crear informes ejecutivos. "
            "Sabes cómo estructurar información compleja de forma clara y accesible. "
            "Tu estilo es profesional pero comprensible."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    revisor = Agent(
        role="Revisor de Calidad",
        goal="Asegurar la calidad y precisión del informe final",
        backstory=(
            "Eres un editor senior con ojo crítico. Revisas informes para "
            "asegurar que sean precisos, bien estructurados y libres de errores. "
            "Eres exigente pero constructivo."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tareas del estudio de mercado
    # El usuario puede elegir el sector
    sector = "inteligencia artificial educativa"  # Puedes cambiar esto
    
    tarea_investigacion = Task(
        description=(
            f"Investiga el mercado de '{sector}'. Recopila información sobre: "
            "1) Tamaño del mercado y crecimiento, 2) Principales competidores, "
            "3) Tendencias actuales, 4) Oportunidades identificadas. "
            "(Como no tienes acceso a internet real, usa tu conocimiento para "
            "crear información plausible y bien fundamentada)."
        ),
        expected_output="Información estructurada sobre el mercado con los 4 puntos solicitados",
        agent=investigador,
    )
    
    tarea_analisis = Task(
        description=(
            "Toma la información del investigador y realiza un análisis profundo. "
            "Identifica: 1) Fortalezas del mercado, 2) Debilidades/riesgos, "
            "3) Oportunidades de crecimiento, 4) Amenazas competitivas. "
            "Proporciona recomendaciones estratégicas basadas en el análisis."
        ),
        expected_output="Análisis estratégico con fortalezas, debilidades, oportunidades y amenazas",
        agent=analista,
        context=[tarea_investigacion],
    )
    
    tarea_escritura = Task(
        description=(
            "Escribe un informe ejecutivo completo basado en la investigación y análisis. "
            "El informe debe tener: 1) Resumen ejecutivo, 2) Análisis de mercado, "
            "3) Análisis competitivo, 4) Oportunidades y recomendaciones, 5) Conclusiones. "
            "Usa un tono profesional y estructurado."
        ),
        expected_output="Informe ejecutivo completo con todas las secciones solicitadas",
        agent=escritor,
        context=[tarea_analisis],
    )
    
    tarea_revision = Task(
        description=(
            "Revisa el informe del escritor. Verifica: coherencia, precisión, "
            "estructura y claridad. Si encuentras problemas, sugiere mejoras específicas. "
            "Si está bien, aprueba el informe final."
        ),
        expected_output="Feedback de revisión o aprobación del informe",
        agent=revisor,
        context=[tarea_escritura],
    )
    
    # Crear el crew
    crew = Crew(
        agents=[investigador, analista, escritor, revisor],
        tasks=[tarea_investigacion, tarea_analisis, tarea_escritura, tarea_revision],
        verbose=True,
        process=Process.sequential,
    )
    
    print("=" * 60)
    print("ESTUDIO DE MERCADO COMPLETO")
    print("=" * 60)
    print(f"\n🎯 Sector a analizar: {sector}")
    print("\n👥 Equipo:")
    print("   1. Investigador de Mercado")
    print("   2. Analista de Datos")
    print("   3. Escritor de Informes")
    print("   4. Revisor de Calidad")
    
    print("\n📋 Flujo:")
    print("   Investigación → Análisis → Escritura → Revisión")
    
    print("\n🚀 Iniciando estudio de mercado...\n")
    
    try:
        resultado = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("INFORME FINAL DEL ESTUDIO DE MERCADO")
        print("=" * 60)
        print(resultado)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Este ejemplo muestra:")
    print("   - Un equipo completo trabajando en un objetivo común")
    print("   - Cada agente aporta desde su especialidad")
    print("   - Flujo secuencial bien definido")
    print("   - Resultado final de alta calidad")
    print("\n   Sigue el patrón de las slides C4:")
    print("   - Researcher → busca info")
    print("   - Analyst → sintetiza")
    print("   - Writer → redacta")
    print("   - Reviewer → corrige")
    print("=" * 60)


if __name__ == "__main__":
    main()

