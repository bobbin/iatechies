"""
Ejercicio 16 — Roles complejos en CrewAI.

Demuestra cómo crear agentes con roles más complejos,
personalidades definidas y habilidades específicas.
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
    print("🟦 EJERCICIO 16: ROLES COMPLEJOS EN CREWAI\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Agente 1: Investigador con personalidad detallada
    investigador = Agent(
        role="Investigador de Tendencias Tecnológicas",
        goal="Descubrir y analizar las últimas tendencias en inteligencia artificial y automatización",
        backstory=(
            "Eres un investigador con 15 años de experiencia en tecnología. "
            "Tienes un PhD en Ciencias de la Computación y has trabajado en "
            "Google y Microsoft. Eres meticuloso, detallista y siempre buscas "
            "fuentes confiables. Te especializas en identificar tendencias antes "
            "de que se vuelvan mainstream."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Agente 2: Analista estratégico
    analista = Agent(
        role="Analista Estratégico de Negocios",
        goal="Evaluar el impacto comercial y estratégico de las tendencias tecnológicas",
        backstory=(
            "Eres un consultor estratégico con MBA de Harvard. Has ayudado a "
            "más de 50 empresas Fortune 500 a tomar decisiones tecnológicas. "
            "Eres pragmático, orientado a resultados y siempre piensas en ROI. "
            "Tu trabajo es separar el 'hype' del valor real de negocio."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Agente 3: Redactor especializado
    redactor = Agent(
        role="Redactor Técnico Senior",
        goal="Crear contenido técnico claro y atractivo para audiencias técnicas y no técnicas",
        backstory=(
            "Eres un escritor técnico con 10 años de experiencia. Has escrito "
            "para TechCrunch, Wired y Harvard Business Review. Dominas el arte "
            "de explicar conceptos complejos de forma simple. Tu estilo es "
            "claro, conciso y siempre incluye ejemplos prácticos."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Agente 4: Revisor de calidad
    revisor = Agent(
        role="Revisor de Calidad y Fact-Checker",
        goal="Verificar la precisión, coherencia y calidad del contenido generado",
        backstory=(
            "Eres un editor senior con ojo crítico para detalles. Has trabajado "
            "en publicaciones científicas y revistas de tecnología. Tu trabajo "
            "es asegurar que todo sea preciso, bien estructurado y libre de errores. "
            "Eres exigente pero constructivo."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tareas con contexto y dependencias
    tarea_investigacion = Task(
        description=(
            "Investiga 3 tendencias clave en IA y automatización para 2025. "
            "Para cada tendencia, proporciona: nombre, descripción breve, "
            "ejemplos de uso y potencial impacto. (Como no tienes acceso a internet, "
            "usa tu conocimiento para crear tendencias plausibles y bien fundamentadas)."
        ),
        expected_output="Una lista estructurada de 3 tendencias con sus detalles",
        agent=investigador,
    )
    
    tarea_analisis = Task(
        description=(
            "Toma las 3 tendencias del investigador y evalúa cada una desde "
            "una perspectiva de negocio. Para cada tendencia, determina: "
            "1) Potencial de mercado, 2) Viabilidad técnica, 3) ROI estimado, "
            "4) Riesgos principales. Luego, rankea las tendencias del 1 al 3 "
            "según su potencial comercial."
        ),
        expected_output="Un análisis estratégico con ranking de las 3 tendencias",
        agent=analista,
        context=[tarea_investigacion],
    )
    
    tarea_redaccion = Task(
        description=(
            "Escribe un artículo de blog de 3 párrafos sobre la tendencia #1 "
            "del análisis. El artículo debe ser: accesible para no técnicos, "
            "incluir ejemplos concretos, y explicar por qué es importante. "
            "Usa un tono profesional pero cercano."
        ),
        expected_output="Un artículo de blog completo de 3 párrafos",
        agent=redactor,
        context=[tarea_analisis],
    )
    
    tarea_revision = Task(
        description=(
            "Revisa el artículo del redactor. Verifica: coherencia, precisión, "
            "estructura y claridad. Si encuentras problemas, sugiere mejoras "
            "específicas. Si está bien, aprueba el contenido."
        ),
        expected_output="Feedback de revisión o aprobación del artículo",
        agent=revisor,
        context=[tarea_redaccion],
    )
    
    # Crear el crew
    crew = Crew(
        agents=[investigador, analista, redactor, revisor],
        tasks=[tarea_investigacion, tarea_analisis, tarea_redaccion, tarea_revision],
        verbose=True,
        process=Process.sequential,  # Ejecución secuencial
    )
    
    print("=" * 60)
    print("EQUIPO DE AGENTES CON ROLES COMPLEJOS")
    print("=" * 60)
    print("\n👥 Agentes:")
    print("   1. Investigador de Tendencias Tecnológicas")
    print("   2. Analista Estratégico de Negocios")
    print("   3. Redactor Técnico Senior")
    print("   4. Revisor de Calidad y Fact-Checker")
    
    print("\n📋 Flujo de trabajo:")
    print("   Investigador → Analista → Redactor → Revisor")
    
    print("\n🚀 Iniciando ejecución...\n")
    
    try:
        resultado = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("RESULTADO FINAL")
        print("=" * 60)
        print(resultado)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Este ejemplo muestra:")
    print("   - Roles con personalidades detalladas (backstory)")
    print("   - Habilidades específicas por rol")
    print("   - Tareas con dependencias (context)")
    print("   - Flujo secuencial bien definido")
    print("   - Cada agente tiene su propio 'prompting' implícito")
    print("=" * 60)


if __name__ == "__main__":
    main()

