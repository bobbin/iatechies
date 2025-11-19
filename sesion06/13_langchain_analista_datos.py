"""
Ejercicio 13 — Agente analista de datos completo.

Crea un agente completo que analiza datos CSV, calcula métricas
y genera informes, siguiendo el ejemplo de las slides B9.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


@tool
def load_csv(ruta: str) -> str:
    """
    Carga un archivo CSV y devuelve información sobre su estructura.
    Úsalo primero para entender qué datos tienes disponibles.
    
    Args:
        ruta: Ruta al archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        info = {
            "filas": len(df),
            "columnas": list(df.columns),
            "tipos": {col: str(df[col].dtype) for col in df.columns},
            "muestra": df.head(5).to_dict("records"),
        }
        return (
            f"CSV cargado: {info['filas']} filas, {len(info['columnas'])} columnas\n"
            f"Columnas: {info['columnas']}\n"
            f"Tipos: {info['tipos']}\n"
            f"Primeras filas:\n{info['muestra']}"
        )
    except Exception as e:
        return f"Error cargando CSV: {e}"


@tool
def describe_data(ruta: str) -> str:
    """
    Genera un resumen estadístico descriptivo del CSV.
    Úsalo para entender la distribución de los datos.
    
    Args:
        ruta: Ruta al archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        descripcion = df.describe(include="all").to_string()
        return f"Descripción estadística:\n{descripcion}"
    except Exception as e:
        return f"Error describiendo datos: {e}"


@tool
def compute_metrics(ruta: str, columna: str) -> str:
    """
    Calcula métricas específicas de una columna numérica:
    suma, promedio, máximo, mínimo, mediana.
    
    Args:
        ruta: Ruta al archivo CSV.
        columna: Nombre de la columna a analizar.
    """
    try:
        df = pd.read_csv(ruta)
        if columna not in df.columns:
            return f"Error: Columna '{columna}' no existe. Disponibles: {list(df.columns)}"
        
        if not pd.api.types.is_numeric_dtype(df[columna]):
            return f"Error: La columna '{columna}' no es numérica"
        
        serie = df[columna]
        metricas = {
            "suma": serie.sum(),
            "promedio": serie.mean(),
            "maximo": serie.max(),
            "minimo": serie.min(),
            "mediana": serie.median(),
            "desviacion_estandar": serie.std(),
        }
        
        resultado = "\n".join([f"{k}: {v:.2f}" for k, v in metricas.items()])
        return f"Métricas de '{columna}':\n{resultado}"
    except Exception as e:
        return f"Error calculando métricas: {e}"


@tool
def generar_informe(metricas: str, conclusiones: str) -> str:
    """
    Genera un informe estructurado con métricas y conclusiones.
    
    Args:
        metricas: Las métricas calculadas (texto).
        conclusiones: Conclusiones del análisis (texto).
    """
    informe = f"""
# INFORME DE ANÁLISIS DE DATOS

## Métricas Calculadas
{metricas}

## Conclusiones
{conclusiones}

---
Generado por Agente Analista de Datos
"""
    return informe


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 13: AGENTE ANALISTA DE DATOS COMPLETO\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [load_csv, describe_data, compute_metrics, generar_informe]
    
    # Asegurar que existe el CSV
    csv_path = Path("data/sales.csv")
    if not csv_path.exists():
        csv_path.parent.mkdir(exist_ok=True)
        datos = {
            "producto": ["Laptop", "Mouse", "Monitor", "Teclado", "Cable HDMI", "Servidor"],
            "cantidad": [5, 50, 20, 30, 100, 2],
            "precio_unitario": [1200, 25, 300, 45, 10, 5000],
        }
        pd.DataFrame(datos).to_csv(csv_path, index=False)
        print(f"✅ CSV de ejemplo creado: {csv_path}\n")
    
    # Crear el agente usando la nueva API de LangChain 1.0+
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Eres un analista de datos experto. Tienes acceso a tools para analizar archivos CSV. "
            "Tu trabajo es analizar datos, calcular métricas y generar informes completos. "
            "Usa las tools disponibles de forma inteligente para responder las preguntas del usuario."
        ),
    )
    
    print("=" * 60)
    print("TAREA: Analizar CSV y generar informe")
    print("=" * 60)
    
    pregunta = f"""
    Analiza el archivo {csv_path} y genera un informe completo que incluya:
    1. Estructura del archivo
    2. Descripción estadística
    3. Métricas de la columna 'cantidad'
    4. Métricas de la columna 'precio_unitario'
    5. Conclusiones sobre los datos
    """
    
    print(f"\n🗣️ Tarea:\n{pregunta}\n")
    
    try:
        respuesta = agent.invoke({
            "messages": [{"role": "user", "content": pregunta}]
        })
        
        print("\n" + "=" * 60)
        print("RESULTADO FINAL")
        print("=" * 60)
        
        # Extraer la respuesta del formato de mensajes
        if "messages" in respuesta:
            ultimo_mensaje = respuesta["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(ultimo_mensaje.content)
            else:
                print(respuesta)
        else:
            print(respuesta)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Este agente:")
    print("   - Decide el orden de las tools automáticamente")
    print("   - Combina múltiples herramientas para resolver la tarea")
    print("   - Genera un informe completo sin intervención manual")
    print("   - Sigue el patrón ReAct: piensa → actúa → observa → repite")
    print("=" * 60)


if __name__ == "__main__":
    main()
