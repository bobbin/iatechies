"""
Servidor MCP simple - Versión simplificada para demostración.

Este servidor expone herramientas usando la API estándar de MCP.
"""

from __future__ import annotations

import asyncio
import json
import random
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Crear el servidor MCP
server = Server("demo-escape-room")


# Tool 1: Obtener un dato curioso
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las tools disponibles."""
    return [
        Tool(
            name="get_random_fact",
            description="Devuelve un dato curioso aleatorio. Úsalo cuando el usuario pida información interesante.",
        ),
        Tool(
            name="get_weather",
            description="Obtiene el clima actual de una ciudad. Úsalo cuando el usuario pregunte sobre el tiempo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nombre de la ciudad (ej: 'Madrid', 'Barcelona')",
                    }
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="search_books",
            description="Busca libros relacionados con un tema. Úsalo cuando el usuario pregunte sobre libros.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Términos de búsqueda (ej: 'inteligencia artificial', 'programación Python')",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_random_word",
            description="Genera una palabra aleatoria de una categoría. Útil para inspirar elementos en puzzles.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Categoría de la palabra (ej: 'objeto', 'lugar', 'animal', 'general')",
                        "default": "general",
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Ejecuta una tool específica."""
    
    if name == "get_random_fact":
        facts = [
            "Los pulpos tienen tres corazones.",
            "Las abejas pueden reconocer caras humanas.",
            "El sonido viaja más rápido en el agua que en el aire.",
            "Los pingüinos pueden saltar hasta 2 metros de altura.",
            "El cerebro humano usa aproximadamente el 20% de la energía del cuerpo.",
            "Los tiburones existen desde hace más de 400 millones de años.",
            "Las mariposas saborean con sus patas.",
        ]
        resultado = {"fact": random.choice(facts)}
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]
    
    elif name == "get_weather":
        city = arguments.get("city", "Madrid") if arguments else "Madrid"
        temperaturas = {
            "Madrid": "22°C",
            "Barcelona": "24°C",
            "Valencia": "26°C",
            "Sevilla": "28°C",
            "Bilbao": "20°C",
        }
        temp = temperaturas.get(city, f"{random.randint(15, 30)}°C")
        condiciones = ["Soleado", "Nublado", "Parcialmente nublado", "Lluvioso"]
        resultado = {
            "city": city,
            "temperature": temp,
            "condition": random.choice(condiciones),
            "humidity": f"{random.randint(40, 80)}%",
        }
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]
    
    elif name == "search_books":
        query = arguments.get("query", "") if arguments else ""
        libros_db = {
            "inteligencia artificial": [
                {"titulo": "Artificial Intelligence: A Modern Approach", "autor": "Russell & Norvig"},
                {"titulo": "Deep Learning", "autor": "Ian Goodfellow"},
                {"titulo": "Pattern Recognition and Machine Learning", "autor": "Christopher Bishop"},
            ],
            "programación python": [
                {"titulo": "Python Crash Course", "autor": "Eric Matthes"},
                {"titulo": "Fluent Python", "autor": "Luciano Ramalho"},
                {"titulo": "Effective Python", "autor": "Brett Slatkin"},
            ],
            "agentes": [
                {"titulo": "Building AI Agents", "autor": "Various"},
                {"titulo": "LangChain in Action", "autor": "Various"},
            ],
        }
        
        resultados = []
        query_lower = query.lower()
        for tema, libros in libros_db.items():
            if tema in query_lower or any(palabra in query_lower for palabra in tema.split()):
                resultados.extend(libros)
        
        if not resultados:
            resultados = [{"titulo": f"Libros sobre {query}", "autor": "Varios autores"}]
        
        resultado = {
            "query": query,
            "results": resultados[:5],
            "count": len(resultados),
        }
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]
    
    elif name == "get_random_word":
        category = arguments.get("category", "general") if arguments else "general"
        palabras = {
            "objeto": ["llave", "candado", "código", "mapa", "piedra", "espejo", "reloj", "libro"],
            "lugar": ["biblioteca", "laboratorio", "mazmorra", "torre", "cripta", "templo", "castillo"],
            "animal": ["león", "águila", "serpiente", "lobo", "búho", "delfín", "tigre"],
            "general": ["misterio", "aventura", "secreto", "tesoro", "puzzle", "enigmas", "desafío"],
        }
        opciones = palabras.get(category.lower(), palabras["general"])
        palabra = random.choice(opciones)
        resultado = {
            "word": palabra,
            "category": category,
            "suggestion": f"Palabra '{palabra}' de la categoría '{category}'",
        }
        return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]
    
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Tool '{name}' no encontrada"}))]


async def main() -> None:
    """Ejecuta el servidor MCP."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP 'demo-escape-room'...")
    print("📋 Tools disponibles:")
    print("   - get_random_fact()")
    print("   - get_weather(city)")
    print("   - search_books(query)")
    print("   - get_random_word(category)")
    print("\n💡 Este servidor está listo para conectarse con clientes MCP")
    print("   (VS Code, Claude Desktop, etc.)\n")
    
    asyncio.run(main())

