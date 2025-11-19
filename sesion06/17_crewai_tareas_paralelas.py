"""
Ejercicio 17 — Tareas en paralelo con CrewAI.

Demuestra cómo ejecutar tareas en paralelo cuando no hay
dependencias entre ellas, optimizando el tiempo de ejecución.
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
    print("🟦 EJERCICIO 17: TAREAS EN PARALELO CON CREWAI\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Agentes especializados
    investigador_tecnologia = Agent(
        role="Investigador de Tecnología",
        goal="Investigar tendencias tecnológicas",
        backstory="Especialista en identificar nuevas tecnologías y su impacto",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    investigador_mercado = Agent(
        role="Investigador de Mercado",
        goal="Analizar tendencias de mercado y competencia",
        backstory="Experto en análisis de mercado y comportamiento de consumidores",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    investigador_regulacion = Agent(
        role="Investigador de Regulación",
        goal="Investigar aspectos legales y regulatorios",
        backstory="Especialista en leyes, regulaciones y compliance",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    sintetizador = Agent(
        role="Sintetizador de Información",
        goal="Combinar información de múltiples fuentes en un informe coherente",
        backstory="Experto en sintetizar información compleja de múltiples áreas",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tareas que se pueden ejecutar en paralelo (sin dependencias)
    tarea_tecnologia = Task(
        description=(
            "Investiga 3 tendencias tecnológicas clave en IA para 2025. "
            "Para cada una, proporciona: nombre, descripción y ejemplos. "
            "(Usa tu conocimiento para crear tendencias plausibles)."
        ),
        expected_output="Lista de 3 tendencias tecnológicas con detalles",
        agent=investigador_tecnologia,
    )
    
    tarea_mercado = Task(
        description=(
            "Analiza el mercado de IA: tamaño, crecimiento, competidores principales "
            "y oportunidades. (Usa tu conocimiento del mercado actual)."
        ),
        expected_output="Análisis de mercado con tamaño, crecimiento y competidores",
        agent=investigador_mercado,
    )
    
    tarea_regulacion = Task(
        description=(
            "Investiga aspectos regulatorios relevantes para IA: leyes actuales, "
            "tendencias regulatorias y consideraciones de compliance. "
            "(Usa tu conocimiento sobre regulación de IA)."
        ),
        expected_output="Resumen de aspectos regulatorios y de compliance",
        agent=investigador_regulacion,
    )
    
    # Tarea que depende de las anteriores (sintetiza todo)
    tarea_sintesis = Task(
        description=(
            "Combina la información de las 3 investigaciones (tecnología, mercado, regulación) "
            "en un informe ejecutivo de 4 párrafos. El informe debe cubrir: "
            "1) Resumen de tendencias tecnológicas, 2) Análisis de mercado, "
            "3) Consideraciones regulatorias, 4) Conclusiones y recomendaciones."
        ),
        expected_output="Informe ejecutivo completo combinando las 3 áreas",
        agent=sintetizador,
        context=[tarea_tecnologia, tarea_mercado, tarea_regulacion],
    )
    
    # Crew con proceso jerárquico (permite paralelismo)
    # Process.hierarchical requiere un manager_llm para coordinar las tareas
    crew = Crew(
        agents=[
            investigador_tecnologia,
            investigador_mercado,
            investigador_regulacion,
            sintetizador,
        ],
        tasks=[tarea_tecnologia, tarea_mercado, tarea_regulacion, tarea_sintesis],
        verbose=True,
        process=Process.hierarchical,  # Permite ejecución en paralelo cuando es posible
        manager_llm=llm,  # LLM que coordina las tareas en proceso jerárquico
    )
    
    print("=" * 60)
    print("TAREAS EN PARALELO")
    print("=" * 60)
    print("\n📊 Estructura:")
    print("   ┌─────────────────┐")
    print("   │  Investigación  │")
    print("   │   Tecnología    │")
    print("   └────────┬────────┘")
    print("            │")
    print("   ┌────────┴────────┐")
    print("   │  Investigación  │  ← Ejecutan en paralelo")
    print("   │     Mercado     │")
    print("   └────────┬────────┘")
    print("            │")
    print("   ┌────────┴────────┐")
    print("   │  Investigación  │")
    print("   │   Regulación    │")
    print("   └────────┬────────┘")
    print("            │")
    print("   ┌────────┴────────┐")
    print("   │   Sintetizador  │  ← Espera a las 3 anteriores")
    print("   └────────────────┘")
    
    print("\n🚀 Iniciando ejecución...\n")
    print("💡 Las 3 investigaciones se ejecutarán en paralelo si es posible.\n")
    
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
    print("   Process.hierarchical permite:")
    print("   - Ejecutar tareas en paralelo cuando no hay dependencias")
    print("   - Optimizar el tiempo total de ejecución")
    print("   - Mantener el orden cuando hay dependencias (context)")
    print("\n   Úsalo cuando:")
    print("   - Tienes múltiples tareas independientes")
    print("   - Quieres optimizar tiempo de ejecución")
    print("   - Algunas tareas dependen de otras (se ejecutan después)")
    print("=" * 60)


if __name__ == "__main__":
    main()

