"""
Ejercicio 05 — Tools que llaman APIs externas.

Demuestra cómo crear tools que interactúan con servicios externos,
simulando llamadas a APIs reales.
"""

from __future__ import annotations

import json
import random
import time
from typing import Dict

from langchain_core.tools import tool


# Simulación de una API de clima (sin necesidad de API key real)
def _simular_api_clima(ciudad: str) -> Dict[str, str]:
    """Simula una llamada a una API de clima."""
    time.sleep(0.5)  # Simula latencia de red
    temperaturas = {
        "Madrid": "22°C",
        "Barcelona": "24°C",
        "Valencia": "26°C",
        "Sevilla": "28°C",
    }
    return {
        "ciudad": ciudad,
        "temperatura": temperaturas.get(ciudad, f"{random.randint(15, 30)}°C"),
        "condicion": random.choice(["Soleado", "Nublado", "Parcialmente nublado"]),
    }


@tool
def obtener_clima(ciudad: str) -> str:
    """
    Obtiene el clima actual de una ciudad.
    Úsalo cuando necesites información meteorológica.
    
    Args:
        ciudad: Nombre de la ciudad (ej: "Madrid", "Barcelona").
    """
    try:
        datos = _simular_api_clima(ciudad)
        return (
            f"Clima en {datos['ciudad']}: "
            f"{datos['temperatura']}, {datos['condicion']}"
        )
    except Exception as e:
        return f"Error obteniendo clima: {e}"


# Simulación de una API de precios
def _simular_api_precios(simbolo: str) -> Dict[str, str]:
    """Simula una llamada a una API de precios de acciones."""
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
    }


@tool
def obtener_precio_accion(simbolo: str) -> str:
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
            f"(variación: {datos['variacion']})"
        )
    except Exception as e:
        return f"Error obteniendo precio: {e}"


# Simulación de búsqueda web
def _simular_busqueda_web(query: str) -> str:
    """Simula una búsqueda web."""
    time.sleep(0.4)
    resultados = [
        f"Artículo sobre '{query}' - fuente1.com",
        f"Noticia reciente: {query} - fuente2.com",
        f"Análisis de {query} - fuente3.com",
    ]
    return "\n".join(resultados[:2])


@tool
def buscar_web(query: str) -> str:
    """
    Busca información en la web sobre un tema.
    Úsalo cuando necesites información actualizada o datos externos.
    
    Args:
        query: Términos de búsqueda.
    """
    try:
        return _simular_busqueda_web(query)
    except Exception as e:
        return f"Error en búsqueda web: {e}"


def main() -> None:
    print("🟦 EJERCICIO 5: TOOLS QUE LLAMAN APIs EXTERNAS\n")
    
    tools = [obtener_clima, obtener_precio_accion, buscar_web]
    
    print("📋 Tools disponibles (simulando APIs externas):\n")
    for i, tool_func in enumerate(tools, 1):
        print(f"{i}. {tool_func.name}")
        print(f"   {tool_func.description}\n")
    
    print("=" * 60)
    print("PRUEBAS DE TOOLS EXTERNAS\n")
    print("=" * 60)
    
    # Prueba 1: Clima
    print("\n1️⃣ Obteniendo clima de Madrid...")
    resultado1 = obtener_clima.invoke({"ciudad": "Madrid"})
    print(f"   {resultado1}")
    
    # Prueba 2: Precio de acción
    print("\n2️⃣ Obteniendo precio de AAPL...")
    resultado2 = obtener_precio_accion.invoke({"simbolo": "AAPL"})
    print(f"   {resultado2}")
    
    # Prueba 3: Búsqueda web
    print("\n3️⃣ Buscando información sobre 'inteligencia artificial'...")
    resultado3 = buscar_web.invoke({"query": "inteligencia artificial"})
    print(f"   {resultado3}")
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Estas tools simulan llamadas a APIs reales.")
    print("   En producción, reemplazarías las funciones simuladas")
    print("   con llamadas HTTP reales usando 'requests' o 'httpx'.")
    print("=" * 60)
    
    # Mostrar schemas
    print("\n📊 Schemas de las tools:\n")
    for tool_func in tools:
        print(f"{tool_func.name}:")
        print(json.dumps(tool_func.args, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()

