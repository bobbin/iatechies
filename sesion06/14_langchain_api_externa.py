"""
Ejercicio 14 — Agente que usa APIs externas.

Demuestra cómo crear un agente que combina información de
múltiples APIs externas para responder preguntas complejas.
"""

from __future__ import annotations

import os
import random
import time
from pathlib import Path
from typing import Dict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


# Simulación de APIs externas
def _simular_api_clima(ciudad: str) -> Dict[str, str]:
    """Simula una API de clima."""
    time.sleep(0.3)
    temperaturas = {
        "Madrid": "22°C",
        "Barcelona": "24°C",
        "Valencia": "26°C",
        "Sevilla": "28°C",
        "Bilbao": "20°C",
    }
    return {
        "ciudad": ciudad,
        "temperatura": temperaturas.get(ciudad, f"{random.randint(15, 30)}°C"),
        "condicion": random.choice(["Soleado", "Nublado", "Parcialmente nublado"]),
        "humedad": f"{random.randint(40, 80)}%",
    }


def _simular_api_noticias(tema: str) -> str:
    """Simula una API de noticias."""
    time.sleep(0.3)
    noticias = {
        "tecnologia": "Nueva actualización de IA revoluciona el sector",
        "deportes": "Equipo local gana campeonato regional",
        "economia": "Mercados muestran tendencia alcista",
        "salud": "Nuevo estudio sobre beneficios del ejercicio",
    }
    return noticias.get(tema.lower(), f"Noticias recientes sobre {tema}")


def _simular_api_precios(simbolo: str) -> Dict[str, str]:
    """Simula una API de precios de acciones."""
    time.sleep(0.3)
    precios_base = {
        "AAPL": 175.50,
        "GOOGL": 142.30,
        "MSFT": 378.20,
        "TSLA": 248.90,
    }
    precio_base = precios_base.get(simbolo.upper(), 100.0)
    variacion = random.uniform(-2.0, 2.0)
    precio_actual = precio_base + variacion
    
    return {
        "simbolo": simbolo.upper(),
        "precio": f"${precio_actual:.2f}",
        "variacion": f"{variacion:+.2f}",
        "tendencia": "alcista" if variacion > 0 else "bajista",
    }


@tool
def get_weather(ciudad: str) -> str:
    """
    Obtiene el clima actual de una ciudad.
    Úsalo cuando necesites información meteorológica.
    
    Args:
        ciudad: Nombre de la ciudad (ej: "Madrid", "Barcelona").
    """
    try:
        datos = _simular_api_clima(ciudad)
        return (
            f"Clima en {datos['ciudad']}: {datos['temperatura']}, "
            f"{datos['condicion']}, Humedad: {datos['humedad']}"
        )
    except Exception as e:
        return f"Error obteniendo clima: {e}"


@tool
def get_news(tema: str) -> str:
    """
    Obtiene noticias recientes sobre un tema.
    Úsalo cuando necesites información actualizada.
    
    Args:
        tema: Tema de las noticias (ej: "tecnologia", "deportes", "economia").
    """
    try:
        return _simular_api_noticias(tema)
    except Exception as e:
        return f"Error obteniendo noticias: {e}"


@tool
def get_prices(simbolo: str) -> str:
    """
    Obtiene el precio actual de una acción.
    Úsalo cuando necesites información financiera.
    
    Args:
        simbolo: Símbolo de la acción (ej: "AAPL", "GOOGL", "MSFT").
    """
    try:
        datos = _simular_api_precios(simbolo)
        return (
            f"{datos['simbolo']}: {datos['precio']} "
            f"(variación: {datos['variacion']}, tendencia: {datos['tendencia']})"
        )
    except Exception as e:
        return f"Error obteniendo precio: {e}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 14: AGENTE QUE USA APIs EXTERNAS\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [get_weather, get_news, get_prices]
    
    # Crear el agente usando la nueva API de LangChain 1.0+
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Eres un asistente que combina información de múltiples fuentes. "
            "Tienes acceso a tools para obtener clima, noticias y precios de acciones. "
            "Cuando el usuario pregunta sobre múltiples temas, usa las tools necesarias "
            "y sintetiza la información en una respuesta coherente."
        ),
    )
    
    print("=" * 60)
    print("EJEMPLO 1: Información combinada")
    print("=" * 60)
    
    pregunta1 = "¿Qué tiempo hace en Madrid y qué noticias hay sobre tecnología?"
    print(f"\n🗣️ Pregunta: {pregunta1}\n")
    
    try:
        respuesta1 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta1}]
        })
        
        if "messages" in respuesta1:
            ultimo_mensaje = respuesta1["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final:\n{ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final:\n{respuesta1}\n")
        else:
            print(f"\n🏁 Respuesta Final:\n{respuesta1}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Análisis financiero")
    print("=" * 60)
    
    pregunta2 = "Obtén el precio de AAPL y las noticias de economía, luego dame un resumen"
    print(f"\n🗣️ Pregunta: {pregunta2}\n")
    
    try:
        respuesta2 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta2}]
        })
        
        if "messages" in respuesta2:
            ultimo_mensaje = respuesta2["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final:\n{ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final:\n{respuesta2}\n")
        else:
            print(f"\n🏁 Respuesta Final:\n{respuesta2}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("💡 Observación:")
    print("   Este agente:")
    print("   - Combina información de múltiples APIs")
    print("   - Decide qué APIs llamar según la pregunta")
    print("   - Sintetiza la información en una respuesta coherente")
    print("   - Sigue el ejemplo de las slides B10")
    print("\n   En producción, reemplazarías las funciones simuladas")
    print("   con llamadas HTTP reales usando 'requests' o 'httpx'.")
    print("=" * 60)


if __name__ == "__main__":
    main()
