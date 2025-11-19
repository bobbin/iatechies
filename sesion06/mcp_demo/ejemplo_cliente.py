"""
Cliente MCP de ejemplo - Demuestra cómo un cliente puede usar el servidor MCP.

Este es un ejemplo educativo. En producción, usarías VS Code o Claude Desktop.
"""

from __future__ import annotations

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    """Ejemplo de cómo un cliente MCP se conecta y usa las tools."""
    
    print("🟦 EJEMPLO: CLIENTE MCP\n")
    print("=" * 60)
    print("Este es un ejemplo educativo de cómo funciona un cliente MCP")
    print("En producción, usarías VS Code o Claude Desktop\n")
    
    # Configuración del servidor
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None,
    )
    
    print("📡 Conectando al servidor MCP...\n")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la conexión
            await session.initialize()
            
            print("✅ Conectado al servidor MCP\n")
            
            # Listar las tools disponibles
            tools_result = await session.list_tools()
            
            print("=" * 60)
            print("TOOLS DISPONIBLES")
            print("=" * 60)
            for tool in tools_result.tools:
                print(f"\n🔧 {tool.name}")
                print(f"   {tool.description}")
                if tool.inputSchema:
                    print(f"   Parámetros: {json.dumps(tool.inputSchema, indent=6, ensure_ascii=False)}")
            
            print("\n" + "=" * 60)
            print("EJEMPLO 1: get_random_fact")
            print("=" * 60)
            
            # Llamar a get_random_fact
            try:
                result = await session.call_tool("get_random_fact", {})
                print(f"\n📊 Resultado: {json.dumps(result.content, indent=2, ensure_ascii=False)}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
            
            print("=" * 60)
            print("EJEMPLO 2: get_weather")
            print("=" * 60)
            
            # Llamar a get_weather
            try:
                result = await session.call_tool("get_weather", {"city": "Madrid"})
                print(f"\n📊 Resultado: {json.dumps(result.content, indent=2, ensure_ascii=False)}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
            
            print("=" * 60)
            print("EJEMPLO 3: search_books")
            print("=" * 60)
            
            # Llamar a search_books
            try:
                result = await session.call_tool("search_books", {"query": "inteligencia artificial"})
                print(f"\n📊 Resultado: {json.dumps(result.content, indent=2, ensure_ascii=False)}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
            
            print("=" * 60)
            print("💡 OBSERVACIONES")
            print("=" * 60)
            print("""
   Este ejemplo muestra:
   ✅ Cómo un cliente se conecta al servidor MCP
   ✅ Cómo descubre las tools disponibles (list_tools)
   ✅ Cómo invoca las tools (call_tool)
   ✅ Cómo recibe los resultados
   
   En un cliente real (VS Code, Claude Desktop):
   - El LLM decide qué tool usar
   - El cliente muestra la llamada en tiempo real
   - El usuario ve todo el proceso transparentemente
            """)


if __name__ == "__main__":
    print("⚠️  NOTA: Este ejemplo requiere que el servidor MCP esté configurado correctamente.")
    print("   Para una demo real, usa VS Code o Claude Desktop.\n")
    asyncio.run(main())

