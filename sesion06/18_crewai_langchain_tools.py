"""
Ejercicio 18 — Integración CrewAI + LangChain Tools.

Demuestra cómo usar tools de LangChain dentro de agentes de CrewAI,
combinando lo mejor de ambos frameworks.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from crewai import Agent, Task, Crew, Process
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


# Tools de LangChain que pueden usar los agentes de CrewAI
@tool
def buscar_en_csv(ruta: str, columna: str, valor: str) -> str:
    """
    Busca filas en un CSV donde una columna tiene un valor específico.
    Úsalo para encontrar datos específicos en archivos CSV.
    
    Args:
        ruta: Ruta al archivo CSV.
        columna: Nombre de la columna para buscar.
        valor: Valor a buscar.
    """
    try:
        df = pd.read_csv(ruta)
        if columna not in df.columns:
            return f"Error: Columna '{columna}' no existe"
        filtrado = df[df[columna].astype(str) == str(valor)]
        if len(filtrado) == 0:
            return f"No se encontraron filas con {columna} = {valor}"
        return f"Se encontraron {len(filtrado)} filas:\n{filtrado.to_string()}"
    except Exception as e:
        return f"Error: {e}"


@tool
def calcular_metricas_csv(ruta: str, columna: str) -> str:
    """
    Calcula métricas estadísticas de una columna numérica en un CSV.
    
    Args:
        ruta: Ruta al archivo CSV.
        columna: Nombre de la columna a analizar.
    """
    try:
        df = pd.read_csv(ruta)
        if columna not in df.columns:
            return f"Error: Columna '{columna}' no existe"
        if not pd.api.types.is_numeric_dtype(df[columna]):
            return f"Error: La columna '{columna}' no es numérica"
        stats = df[columna].describe()
        return f"Métricas de '{columna}':\n{stats.to_string()}"
    except Exception as e:
        return f"Error: {e}"


@tool
def contar_filas_csv(ruta: str) -> str:
    """
    Cuenta el número de filas en un archivo CSV.
    
    Args:
        ruta: Ruta al archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        return f"El CSV tiene {len(df)} filas y {len(df.columns)} columnas: {list(df.columns)}"
    except Exception as e:
        return f"Error: {e}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 18: INTEGRACIÓN CREWAI + LANGCHAIN TOOLS\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # Asegurar que existe el CSV
    csv_path = Path("data/sales.csv")
    if not csv_path.exists():
        csv_path.parent.mkdir(exist_ok=True)
        datos = {
            "producto": ["Laptop", "Mouse", "Monitor", "Teclado"],
            "cantidad": [5, 50, 20, 30],
            "precio_unitario": [1200, 25, 300, 45],
        }
        pd.DataFrame(datos).to_csv(csv_path, index=False)
        print(f"✅ CSV de ejemplo creado: {csv_path}\n")
    
    # Agente analista de datos (usa tools de LangChain)
    analista = Agent(
        role="Analista de Datos",
        goal="Analizar datos CSV y extraer insights",
        backstory=(
            "Eres un analista de datos experto. Tienes acceso a tools "
            "para leer y analizar archivos CSV. Usa estas tools para "
            "responder preguntas sobre los datos."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[buscar_en_csv, calcular_metricas_csv, contar_filas_csv],  # Tools de LangChain
        llm=llm,
    )
    
    # Agente sintetizador (no necesita tools, solo procesa texto)
    sintetizador = Agent(
        role="Sintetizador de Informes",
        goal="Crear informes claros y estructurados",
        backstory=(
            "Eres un escritor técnico que transforma análisis de datos "
            "en informes comprensibles para no técnicos."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    
    # Tarea 1: Análisis de datos (usa tools)
    tarea_analisis = Task(
        description=(
            f"Analiza el archivo {csv_path}. Responde: "
            "1) ¿Cuántas filas y columnas tiene? "
            "2) ¿Cuáles son las métricas de la columna 'cantidad'? "
            "3) ¿Qué productos hay en el archivo? "
            "Usa las tools disponibles para obtener esta información."
        ),
        expected_output="Análisis completo del CSV con métricas y productos",
        agent=analista,
    )
    
    # Tarea 2: Crear informe (no usa tools, solo procesa texto)
    tarea_informe = Task(
        description=(
            "Toma el análisis del analista y crea un informe ejecutivo "
            "de 2 párrafos que explique los hallazgos de forma clara "
            "para no técnicos."
        ),
        expected_output="Informe ejecutivo de 2 párrafos",
        agent=sintetizador,
        context=[tarea_analisis],
    )
    
    # Crew con ambos agentes
    crew = Crew(
        agents=[analista, sintetizador],
        tasks=[tarea_analisis, tarea_informe],
        verbose=True,
        process=Process.sequential,
    )
    
    print("=" * 60)
    print("INTEGRACIÓN CREWAI + LANGCHAIN TOOLS")
    print("=" * 60)
    print("\n🔧 Tools de LangChain disponibles:")
    print("   - buscar_en_csv: Busca datos en CSV")
    print("   - calcular_metricas_csv: Calcula estadísticas")
    print("   - contar_filas_csv: Cuenta filas y columnas")
    
    print("\n👥 Agentes:")
    print("   - Analista: Usa tools de LangChain")
    print("   - Sintetizador: Solo procesa texto")
    
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
    print("   Esta integración muestra:")
    print("   - CrewAI para orquestar equipos de agentes")
    print("   - LangChain Tools para acciones específicas")
    print("   - Sinergia perfecta entre ambos frameworks")
    print("\n   Es común usar:")
    print("   - Agentes de CrewAI (roles, tareas, coordinación)")
    print("   - Tools de LangChain (acciones específicas)")
    print("   - Pipelines de Runnables (procesamiento determinista)")
    print("=" * 60)


if __name__ == "__main__":
    main()

