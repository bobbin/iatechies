"""
Ejercicio 20 — Flujo con revisión y iteración en CrewAI.

Demuestra cómo crear un flujo donde un revisor puede solicitar
mejoras y el proceso se repite hasta alcanzar la calidad deseada.
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
    print("🟦 EJERCICIO 20: FLUJO CON REVISIÓN E ITERACIÓN\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    # Agentes
    escritor = Agent(
        role="Escritor de Contenido",
        goal="Crear contenido de alta calidad",
        backstory=(
            "Eres un escritor creativo con experiencia en múltiples formatos. "
            "Puedes escribir artículos, posts, informes y más. "
            "Eres flexible y puedes mejorar tu trabajo basándote en feedback."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    revisor = Agent(
        role="Revisor Estricto",
        goal="Asegurar que el contenido cumple estándares de calidad",
        backstory=(
            "Eres un revisor muy exigente. Revisas contenido buscando: "
            "claridad, precisión, estructura, tono y gramática. "
            "Si el contenido no cumple tus estándares, proporcionas feedback "
            "específico y constructivo para mejoras."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tarea 1: Escritura inicial
    tarea_escritura = Task(
        description=(
            "Escribe un artículo de 3 párrafos sobre 'El futuro de los agentes de IA'. "
            "El artículo debe ser: informativo, accesible para no técnicos, "
            "y debe incluir ejemplos concretos. Usa un tono profesional pero cercano."
        ),
        expected_output="Artículo de 3 párrafos sobre el futuro de los agentes de IA",
        agent=escritor,
    )
    
    # Tarea 2: Revisión (puede solicitar mejoras)
    tarea_revision = Task(
        description=(
            "Revisa el artículo del escritor. Evalúa: "
            "1) ¿Es claro y comprensible? "
            "2) ¿Tiene ejemplos concretos? "
            "3) ¿El tono es apropiado? "
            "4) ¿La estructura es lógica? "
            "\n"
            "Si el artículo cumple todos los criterios, aprueba el contenido. "
            "Si no, proporciona feedback específico y solicita una versión mejorada."
        ),
        expected_output="Aprobación del contenido o feedback detallado para mejoras",
        agent=revisor,
        context=[tarea_escritura],
    )
    
    # Tarea 3: Mejora (si es necesario)
    tarea_mejora = Task(
        description=(
            "Si el revisor proporcionó feedback, mejora el artículo original "
            "incorporando todas las sugerencias. Si el artículo fue aprobado, "
            "simplemente confirma que está listo."
        ),
        expected_output="Versión mejorada del artículo o confirmación de aprobación",
        agent=escritor,
        context=[tarea_revision],
    )
    
    # Crew con flujo de revisión
    crew = Crew(
        agents=[escritor, revisor],
        tasks=[tarea_escritura, tarea_revision, tarea_mejora],
        verbose=True,
        process=Process.sequential,
    )
    
    print("=" * 60)
    print("FLUJO CON REVISIÓN E ITERACIÓN")
    print("=" * 60)
    print("\n📋 Flujo:")
    print("   1. Escritor crea contenido inicial")
    print("   2. Revisor evalúa y proporciona feedback")
    print("   3. Escritor mejora basándose en feedback")
    print("   4. (Opcional: ciclo se repite si es necesario)")
    
    print("\n🚀 Iniciando proceso de escritura y revisión...\n")
    
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
    print("   Este flujo muestra:")
    print("   - Cómo un revisor puede solicitar mejoras")
    print("   - Cómo el escritor puede iterar sobre su trabajo")
    print("   - Proceso de calidad iterativo")
    print("\n   En producción, podrías:")
    print("   - Agregar más rondas de revisión")
    print("   - Definir criterios de aprobación claros")
    print("   - Automatizar la decisión de cuándo parar")
    print("=" * 60)


if __name__ == "__main__":
    main()

