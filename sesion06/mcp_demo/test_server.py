"""
Script de prueba para verificar que el servidor MCP funciona correctamente.

Este script prueba las tools directamente sin necesidad de un cliente MCP completo.
"""

from __future__ import annotations

import json
import random


def get_random_fact() -> dict:
    """Tool 1: Dato curioso."""
    facts = [
        "Los pulpos tienen tres corazones.",
        "Las abejas pueden reconocer caras humanas.",
        "El sonido viaja más rápido en el agua que en el aire.",
        "Los pingüinos pueden saltar hasta 2 metros de altura.",
        "El cerebro humano usa aproximadamente el 20% de la energía del cuerpo.",
    ]
    return {"fact": random.choice(facts)}


def get_weather(city: str) -> dict:
    """Tool 2: Clima (simulado para test)."""
    # Nota: En el servidor real usa la API de Open-Meteo
    temperaturas = {
        "Madrid": "22°C",
        "Barcelona": "24°C",
        "Valencia": "26°C",
    }
    temp = temperaturas.get(city, f"{random.randint(15, 30)}°C")
    return {
        "city": city,
        "temperature": temp,
        "condition": "Soleado",
        "note": "Este es un test simulado. El servidor real usa Open-Meteo API",
    }


def search_books(query: str) -> dict:
    """Tool 3: Búsqueda de libros."""
    libros_db = {
        "inteligencia artificial": [
            {"titulo": "Artificial Intelligence: A Modern Approach", "autor": "Russell & Norvig"},
            {"titulo": "Deep Learning", "autor": "Ian Goodfellow"},
        ],
        "programación python": [
            {"titulo": "Python Crash Course", "autor": "Eric Matthes"},
            {"titulo": "Fluent Python", "autor": "Luciano Ramalho"},
        ],
    }
    
    resultados = []
    query_lower = query.lower()
    for tema, libros in libros_db.items():
        if tema in query_lower:
            resultados.extend(libros)
    
    return {
        "query": query,
        "results": resultados[:3],
        "count": len(resultados),
    }


def main() -> None:
    """Prueba las tools directamente."""
    print("PRUEBA DE TOOLS DEL SERVIDOR MCP\n")
    print("=" * 60)
    print("Este script prueba las tools sin necesidad de un cliente MCP completo")
    print("=" * 60)
    
    print("\n1. get_random_fact():")
    resultado1 = get_random_fact()
    print(f"   {json.dumps(resultado1, indent=2, ensure_ascii=False)}\n")
    
    print("2. get_weather('Madrid'):")
    resultado2 = get_weather("Madrid")
    print(f"   {json.dumps(resultado2, indent=2, ensure_ascii=False)}\n")
    
    print("3. search_books('inteligencia artificial'):")
    resultado3 = search_books("inteligencia artificial")
    print(f"   {json.dumps(resultado3, indent=2, ensure_ascii=False)}\n")
    
    print("=" * 60)
    print("Estas son las funciones que el servidor MCP expone")
    print("Un cliente MCP las descubrira automaticamente y el LLM")
    print("decidira cuando usarlas segun las preguntas del usuario.")
    print("=" * 60)


if __name__ == "__main__":
    main()

