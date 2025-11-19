"""
Ejercicio MCP 01 — Servidor MCP mínimo.

Demuestra cómo crear un servidor MCP que expone herramientas
que cualquier cliente MCP puede descubrir y usar.
"""

from __future__ import annotations

import asyncio
import random
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Crear el servidor MCP
server = Server("demo-escape-room")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las tools disponibles en el servidor.
    El cliente MCP llama a esta función para descubrir qué tools hay.
    """
    return [
        Tool(
            name="get_random_fact",
            description="Obtiene un dato curioso aleatorio sobre ciencia, naturaleza o historia.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_weather",
            description="Obtiene el clima actual de una ciudad. Úsalo cuando necesites información meteorológica.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nombre de la ciudad (ej: 'Madrid', 'Barcelona')",
                    },
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="search_books",
            description="Busca libros por título o autor. Úsalo cuando necesites información sobre libros.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Término de búsqueda (título o autor)",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Ejecuta una tool cuando el cliente MCP la invoca.
    """
    if name == "get_random_fact":
        facts = [
            "Los pulpos tienen tres corazones.",
            "El ADN humano es 99.9% idéntico entre todas las personas.",
            "Las abejas pueden reconocer caras humanas.",
            "El sonido viaja 4 veces más rápido en el agua que en el aire.",
            "Los tiburones existen desde hace más de 400 millones de años.",
        ]
        fact = random.choice(facts)
        return [TextContent(type="text", text=f'{{"fact": "{fact}"}}')]
    
    elif name == "get_weather":
        city = arguments.get("city", "Desconocida")
        # Simulación de datos de clima
        weather_data = {
            "Madrid": {"temp": "22°C", "condition": "Soleado"},
            "Barcelona": {"temp": "24°C", "condition": "Parcialmente nublado"},
            "Valencia": {"temp": "26°C", "condition": "Soleado"},
            "Sevilla": {"temp": "28°C", "condition": "Soleado"},
        }
        
        if city in weather_data:
            data = weather_data[city]
        else:
            data = {"temp": f"{random.randint(15, 30)}°C", "condition": "Variable"}
        
        result = {
            "city": city,
            "temperature": data["temp"],
            "condition": data["condition"],
        }
        return [TextContent(type="text", text=str(result))]
    
    elif name == "search_books":
        query = arguments.get("query", "").lower()
        # Base de datos simulada de libros
        books_db = {
            "python": [
                {"title": "Python Crash Course", "author": "Eric Matthes", "year": 2019},
                {"title": "Fluent Python", "author": "Luciano Ramalho", "year": 2022},
            ],
            "ia": [
                {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "year": 2020},
                {"title": "Hands-On Machine Learning", "author": "Aurélien Géron", "year": 2022},
            ],
            "langchain": [
                {"title": "LangChain in Action", "author": "Various", "year": 2024},
            ],
        }
        
        results = []
        for keyword, books in books_db.items():
            if keyword in query:
                results.extend(books)
        
        if not results:
            results = [{"title": "No se encontraron libros", "author": "N/A", "year": "N/A"}]
        
        return [TextContent(type="text", text=str(results))]
    
    else:
        return [TextContent(type="text", text=f'{{"error": "Tool "{name}" no encontrada"}}')]


async def main() -> None:
    """
    Ejecuta el servidor MCP usando stdio (entrada/salida estándar).
    Esto permite que cualquier cliente MCP se conecte.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    print("🟦 SERVIDOR MCP MÍNIMO")
    print("=" * 60)
    print("\n📡 Servidor MCP iniciado: 'demo-escape-room'")
    print("🔧 Tools disponibles:")
    print("   - get_random_fact: Obtiene datos curiosos")
    print("   - get_weather: Obtiene clima de una ciudad")
    print("   - search_books: Busca libros")
    print("\n💡 Este servidor está listo para conectarse con:")
    print("   - VS Code (extensión MCP)")
    print("   - Claude Desktop")
    print("   - Cualquier cliente MCP compatible")
    print("\n⏳ Esperando conexiones...\n")
    
    asyncio.run(main())

