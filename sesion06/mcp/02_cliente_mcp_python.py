"""
Ejercicio MCP 02 — Cliente MCP en Python.

Demuestra cómo un cliente Python puede conectarse a un servidor MCP,
descubrir las tools disponibles e invocarlas.
"""

from __future__ import annotations

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    print("🟦 CLIENTE MCP EN PYTHON\n")
    print("=" * 60)
    print("DEMOSTRACIÓN: Descubrir y usar tools de un servidor MCP")
    print("=" * 60)
    
    # Configurar el servidor MCP
    # Nota: En producción, esto apuntaría a un servidor MCP real
    # Aquí usamos el servidor local que creamos en el ejercicio 01
    server_params = StdioServerParameters(
        command="python",
        args=["01_servidor_mcp_minimo.py"],
    )
    
    print("\n📡 Conectando al servidor MCP...\n")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar la conexión
            await session.initialize()
            
            print("✅ Conexión establecida\n")
            
            # 1. DESCUBRIR TOOLS DISPONIBLES
            print("=" * 60)
            print("PASO 1: Descubrir tools disponibles")
            print("=" * 60)
            
            tools = await session.list_tools()
            
            print(f"\n🔧 Tools descubiertas: {len(tools.tools)}\n")
            for tool in tools.tools:
                print(f"   📌 {tool.name}")
                print(f"      {tool.description}")
                if tool.inputSchema:
                    print(f"      Parámetros: {json.dumps(tool.inputSchema.get('properties', {}), indent=8, ensure_ascii=False)}")
                print()
            
            # 2. INVOCAR TOOLS
            print("=" * 60)
            print("PASO 2: Invocar tools")
            print("=" * 60)
            
            # Tool 1: get_random_fact
            print("\n1️⃣ Invocando: get_random_fact()\n")
            result1 = await session.call_tool("get_random_fact", {})
            print(f"   📊 Resultado: {result1.content[0].text}\n")
            
            # Tool 2: get_weather
            print("2️⃣ Invocando: get_weather(city='Madrid')\n")
            result2 = await session.call_tool("get_weather", {"city": "Madrid"})
            print(f"   📊 Resultado: {result2.content[0].text}\n")
            
            # Tool 3: search_books
            print("3️⃣ Invocando: search_books(query='python')\n")
            result3 = await session.call_tool("search_books", {"query": "python"})
            print(f"   📊 Resultado: {result3.content[0].text}\n")
            
            print("=" * 60)
            print("💡 OBSERVACIONES")
            print("=" * 60)
            print("""
   Este cliente demuestra:
   ✅ Cómo un cliente descubre las tools disponibles (list_tools)
   ✅ Cómo invoca tools remotas (call_tool)
   ✅ Cómo recibe resultados estructurados
   ✅ Que MCP es un protocolo estándar (no específico de un framework)
   
   En producción:
   - El servidor MCP puede estar en otro proceso/máquina
   - Múltiples clientes pueden conectarse al mismo servidor
   - Las tools pueden ser dinámicas (agregarse/eliminarse sin reiniciar)
   - El protocolo es independiente del lenguaje (Python, TypeScript, etc.)
            """)
            print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Cliente interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

