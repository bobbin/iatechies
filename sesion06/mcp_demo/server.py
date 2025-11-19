"""
Servidor MCP mínimo - Demostración del Model Context Protocol.

Este servidor expone herramientas simples que cualquier cliente MCP
puede descubrir y usar automáticamente.
"""

from __future__ import annotations

import asyncio
import json
import random
import sys
from typing import Any

import httpx

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


def log_error(message: str) -> None:
    """Registra errores en stderr sin interferir con stdio."""
    print(f"[MCP ERROR] {message}", file=sys.stderr, flush=True)


def log_debug(message: str) -> None:
    """Registra mensajes de depuración en stderr."""
    if sys.stdout.isatty():  # Solo en modo interactivo
        print(f"[MCP DEBUG] {message}", file=sys.stderr, flush=True)


# Crear el servidor MCP
server = Server("demo-escape-room")


# Registrar las tools disponibles
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista todas las tools disponibles en el servidor."""
    return [
        Tool(
            name="get_random_fact",
            description="Devuelve un dato curioso aleatorio. Úsalo cuando el usuario pida información interesante o datos curiosos.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_weather",
            description="Obtiene el clima actual de una ciudad. Úsalo cuando el usuario pregunte sobre el tiempo o clima.",
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
            description="Busca libros relacionados con un tema. Úsalo cuando el usuario pregunte sobre libros o recomendaciones de lectura.",
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
            description="Genera una palabra aleatoria de una categoría. Útil para inspirar elementos en puzzles o narrativas.",
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


# Manejar las llamadas a las tools
@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    """Ejecuta una tool específica cuando el cliente la invoca."""
    try:
        log_debug(f"Llamada a tool: {name} con argumentos: {arguments}")
        
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
            # Validar argumentos
            if not arguments or "city" not in arguments:
                error_msg = "El parámetro 'city' es requerido"
                log_error(f"get_weather: {error_msg}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": error_msg}, ensure_ascii=False)
                )]
            
            city = str(arguments.get("city", "Madrid")).strip()
            if not city:
                city = "Madrid"
            
            # Coordenadas de ciudades españolas principales
            ciudades_coords = {
                "Madrid": {"lat": 40.4168, "lon": -3.7038},
                "Barcelona": {"lat": 41.3851, "lon": 2.1734},
                "Valencia": {"lat": 39.4699, "lon": -0.3763},
                "Sevilla": {"lat": 37.3891, "lon": -5.9845},
                "Bilbao": {"lat": 43.2627, "lon": -2.9253},
                "Málaga": {"lat": 36.7213, "lon": -4.4214},
                "Zaragoza": {"lat": 41.6488, "lon": -0.8891},
                "Murcia": {"lat": 37.9922, "lon": -1.1307},
            }
            
            # Obtener coordenadas de la ciudad
            coords = ciudades_coords.get(city, ciudades_coords["Madrid"])
            
            try:
                # Llamar a la API de Open-Meteo (gratuita, sin API key)
                log_debug(f"Obteniendo clima para {city} (coords: {coords})")
                async with httpx.AsyncClient(timeout=10.0) as client:
                    url = "https://api.open-meteo.com/v1/forecast"
                    params = {
                        "latitude": coords["lat"],
                        "longitude": coords["lon"],
                        "current": "temperature_2m,relative_humidity_2m,weather_code",
                        "timezone": "Europe/Madrid",
                    }
                    
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()
                
                    current = data.get("current", {})
                    if not current:
                        raise ValueError("La API no devolvió datos de clima actuales")
                    
                    temp = current.get("temperature_2m", 0)
                    humidity = current.get("relative_humidity_2m", 0)
                    weather_code = current.get("weather_code", 0)
                    
                    # Mapear códigos de tiempo de Open-Meteo a descripciones
                    weather_descriptions = {
                        0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
                        3: "Nublado", 45: "Niebla", 48: "Niebla helada",
                        51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna densa",
                        56: "Llovizna helada ligera", 57: "Llovizna helada densa",
                        61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia intensa",
                        66: "Lluvia helada ligera", 67: "Lluvia helada intensa",
                        71: "Nieve ligera", 73: "Nieve moderada", 75: "Nieve intensa",
                        77: "Granos de nieve", 80: "Chubascos ligeros",
                        81: "Chubascos moderados", 82: "Chubascos intensos",
                        85: "Chubascos de nieve ligeros", 86: "Chubascos de nieve intensos",
                        95: "Tormenta", 96: "Tormenta con granizo", 99: "Tormenta intensa con granizo",
                    }
                    
                    condition = weather_descriptions.get(weather_code, "Desconocido")
                    
                    resultado = {
                        "city": city,
                        "temperature": f"{temp:.1f}°C",
                        "condition": condition,
                        "humidity": f"{humidity}%",
                        "source": "Open-Meteo API",
                    }
                    log_debug(f"Clima obtenido exitosamente para {city}")
                    
            except httpx.TimeoutException as e:
                error_msg = f"Timeout al conectar con la API de clima: {str(e)}"
                log_error(f"get_weather: {error_msg}")
                resultado = {
                    "city": city,
                    "error": error_msg,
                    "fallback": "Intenta más tarde o verifica tu conexión a internet",
                }
            except httpx.HTTPStatusError as e:
                error_msg = f"Error HTTP {e.response.status_code} al obtener el clima: {str(e)}"
                log_error(f"get_weather: {error_msg}")
                resultado = {
                    "city": city,
                    "error": error_msg,
                    "fallback": "La API de clima no está disponible temporalmente",
                }
            except (ValueError, KeyError) as e:
                error_msg = f"Error al procesar datos de la API: {str(e)}"
                log_error(f"get_weather: {error_msg}")
                resultado = {
                    "city": city,
                    "error": error_msg,
                    "fallback": "Los datos recibidos no son válidos",
                }
            except Exception as e:
                error_msg = f"Error inesperado al obtener el clima: {str(e)}"
                log_error(f"get_weather: {error_msg}")
                resultado = {
                    "city": city,
                    "error": error_msg,
                    "fallback": "Intenta con otra ciudad o verifica tu conexión a internet",
                }
            
            return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False))]
        
        elif name == "search_books":
            # Validar argumentos
            if not arguments or "query" not in arguments:
                error_msg = "El parámetro 'query' es requerido"
                log_error(f"search_books: {error_msg}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": error_msg}, ensure_ascii=False)
                )]
            
            query = str(arguments.get("query", "")).strip()
            if not query:
                error_msg = "El parámetro 'query' no puede estar vacío"
                log_error(f"search_books: {error_msg}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": error_msg}, ensure_ascii=False)
                )]
            
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
            category = str(arguments.get("category", "general")).strip() if arguments else "general"
            if not category:
                category = "general"
            
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
            error_msg = f"Tool '{name}' no encontrada"
            log_error(error_msg)
            return [TextContent(type="text", text=json.dumps({"error": error_msg}, ensure_ascii=False))]
    
    except Exception as e:
        # Capturar cualquier error no esperado
        error_msg = f"Error inesperado al ejecutar tool '{name}': {str(e)}"
        log_error(error_msg)
        return [TextContent(
            type="text",
            text=json.dumps({"error": error_msg, "tool": name}, ensure_ascii=False)
        )]


async def main() -> None:
    """
    Ejecuta el servidor MCP usando stdio (entrada/salida estándar).
    Esto permite que cualquier cliente MCP se conecte.
    """
    try:
        log_debug("Iniciando servidor MCP...")
        async with stdio_server() as (read_stream, write_stream):
            log_debug("Servidor MCP conectado, esperando solicitudes...")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    except Exception as e:
        log_error(f"Error fatal en el servidor MCP: {str(e)}")
        raise


if __name__ == "__main__":
    # Los mensajes de print solo se muestran cuando se ejecuta directamente
    # Cuando se ejecuta a través de MCP stdio, estos mensajes no se muestran
    # para evitar problemas de encoding con emojis
    import sys
    if sys.stdout.isatty():  # Solo imprimir si hay una terminal interactiva
        print("Iniciando servidor MCP 'demo-escape-room'...")
        print("Tools disponibles:")
        print("   - get_random_fact()")
        print("   - get_weather(city)")
        print("   - search_books(query)")
        print("   - get_random_word(category)")
        print("\nEste servidor esta listo para conectarse con clientes MCP")
        print("   (VS Code, Claude Desktop, Cursor, etc.)\n")
    
    asyncio.run(main())
