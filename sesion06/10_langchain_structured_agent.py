"""
Ejercicio 10 — Structured Chat Agent en LangChain.

Demuestra el uso de agentes en LangChain 1.0+, que es más robusto
para trabajar con tools bien definidas.
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
def leer_csv(ruta: str) -> str:
    """
    Lee un archivo CSV y devuelve información sobre su estructura.
    Úsalo para entender qué datos contiene un CSV.
    
    Args:
        ruta: Ruta al archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        info = {
            "filas": len(df),
            "columnas": list(df.columns),
            "muestra": df.head(3).to_dict("records"),
        }
        return f"CSV tiene {info['filas']} filas y columnas: {info['columnas']}\nMuestra:\n{info['muestra']}"
    except Exception as e:
        return f"Error leyendo CSV: {e}"


@tool
def calcular_estadisticas(ruta: str, columna: str) -> str:
    """
    Calcula estadísticas básicas de una columna numérica en un CSV.
    
    Args:
        ruta: Ruta al archivo CSV.
        columna: Nombre de la columna a analizar.
    """
    try:
        df = pd.read_csv(ruta)
        if columna not in df.columns:
            return f"Error: La columna '{columna}' no existe. Columnas disponibles: {list(df.columns)}"
        
        if not pd.api.types.is_numeric_dtype(df[columna]):
            return f"Error: La columna '{columna}' no es numérica"
        
        stats = df[columna].describe()
        return f"Estadísticas de '{columna}':\n{stats.to_string()}"
    except Exception as e:
        return f"Error calculando estadísticas: {e}"


@tool
def filtrar_datos(ruta: str, columna: str, valor: str) -> str:
    """
    Filtra filas de un CSV donde una columna tiene un valor específico.
    
    Args:
        ruta: Ruta al archivo CSV.
        columna: Nombre de la columna para filtrar.
        valor: Valor a buscar (se convierte a string para comparación).
    """
    try:
        df = pd.read_csv(ruta)
        if columna not in df.columns:
            return f"Error: La columna '{columna}' no existe"
        
        filtrado = df[df[columna].astype(str) == str(valor)]
        if len(filtrado) == 0:
            return f"No se encontraron filas con {columna} = {valor}"
        
        return f"Se encontraron {len(filtrado)} filas:\n{filtrado.to_string()}"
    except Exception as e:
        return f"Error filtrando datos: {e}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 10: STRUCTURED CHAT AGENT EN LANGCHAIN 1.0+\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [leer_csv, calcular_estadisticas, filtrar_datos]
    
    # Crear el agente usando la nueva API de LangChain 1.0+
    # create_agent simplifica la creación y maneja todo automáticamente
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Eres un agente analista de datos. Tienes acceso a tools para analizar CSVs. "
            "Responde de forma clara y estructurada. Cuando uses una tool, explica qué estás haciendo y por qué."
        ),
    )
    
    # Asegurar que existe el CSV de ejemplo
    csv_path = Path("data/sales.csv")
    if not csv_path.exists():
        csv_path.parent.mkdir(exist_ok=True)
        datos_ejemplo = {
            "producto": ["Laptop", "Mouse", "Monitor", "Teclado"],
            "cantidad": [5, 50, 20, 30],
            "precio_unitario": [1200, 25, 300, 45],
        }
        pd.DataFrame(datos_ejemplo).to_csv(csv_path, index=False)
        print(f"✅ CSV de ejemplo creado: {csv_path}\n")
    
    print("=" * 60)
    print("EJEMPLO 1: Análisis básico de CSV")
    print("=" * 60)
    
    pregunta1 = f"Lee el archivo {csv_path} y dime qué columnas tiene y cuántas filas"
    print(f"\n🗣️ Pregunta: {pregunta1}\n")
    
    try:
        # En LangChain 1.0+, el agente se invoca directamente con mensajes
        respuesta1 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta1}]
        })
        # La respuesta viene en formato de mensajes
        if "messages" in respuesta1:
            ultimo_mensaje = respuesta1["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final: {ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final: {respuesta1}\n")
        else:
            print(f"\n🏁 Respuesta Final: {respuesta1}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Cálculo de estadísticas")
    print("=" * 60)
    
    pregunta2 = f"Calcula las estadísticas de la columna 'cantidad' en {csv_path}"
    print(f"\n🗣️ Pregunta: {pregunta2}\n")
    
    try:
        respuesta2 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta2}]
        })
        if "messages" in respuesta2:
            ultimo_mensaje = respuesta2["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final: {ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final: {respuesta2}\n")
        else:
            print(f"\n🏁 Respuesta Final: {respuesta2}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("💡 Observación:")
    print("   En LangChain 1.0+:")
    print("   - create_agent simplifica la creación de agentes")
    print("   - No necesitas AgentExecutor, el agente se invoca directamente")
    print("   - El formato de entrada es {'messages': [...]}")
    print("   - Las tools bien definidas funcionan automáticamente")
    print("=" * 60)


if __name__ == "__main__":
    main()
