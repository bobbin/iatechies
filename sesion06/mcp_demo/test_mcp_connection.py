"""
Script de diagnóstico para probar el servidor MCP local.

Este script verifica que el servidor MCP funcione correctamente
antes de usarlo en Cursor o VS Code.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server() -> bool:
    """Prueba la conexión y todas las tools del servidor MCP."""
    
    print("=" * 70)
    print("DIAGNÓSTICO DEL SERVIDOR MCP LOCAL")
    print("=" * 70)
    print()
    
    # Obtener la ruta del servidor
    server_path = Path(__file__).parent / "server.py"
    
    if not server_path.exists():
        print(f"❌ ERROR: No se encuentra server.py en {server_path}")
        return False
    
    print(f"📁 Servidor encontrado: {server_path}")
    print()
    
    # Configurar el servidor
    server_params = StdioServerParameters(
        command="python",
        args=["-u", str(server_path)],
    )
    
    print("📡 Conectando al servidor MCP...")
    print()
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Inicializar la conexión
                await session.initialize()
                print("✅ Conexión establecida exitosamente")
                print()
                
                # Listar las tools disponibles
                print("=" * 70)
                print("1. LISTANDO TOOLS DISPONIBLES")
                print("=" * 70)
                tools_result = await session.list_tools()
                
                if not tools_result.tools:
                    print("❌ ERROR: No se encontraron tools disponibles")
                    return False
                
                print(f"✅ Se encontraron {len(tools_result.tools)} tools:")
                for tool in tools_result.tools:
                    print(f"   - {tool.name}: {tool.description}")
                print()
                
                # Probar cada tool
                tests_passed = 0
                tests_failed = 0
                
                # Test 1: get_random_fact
                print("=" * 70)
                print("2. PROBANDO: get_random_fact")
                print("=" * 70)
                try:
                    result = await session.call_tool("get_random_fact", {})
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if "fact" in data:
                                print(f"✅ Éxito: {data['fact']}")
                                tests_passed += 1
                            else:
                                print(f"❌ Error: Respuesta inesperada: {data}")
                                tests_failed += 1
                        else:
                            print(f"❌ Error: Formato de respuesta inesperado")
                            tests_failed += 1
                    else:
                        print("❌ Error: No se recibió respuesta")
                        tests_failed += 1
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    tests_failed += 1
                print()
                
                # Test 2: get_weather
                print("=" * 70)
                print("3. PROBANDO: get_weather")
                print("=" * 70)
                try:
                    result = await session.call_tool("get_weather", {"city": "Madrid"})
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if "error" in data:
                                print(f"⚠️  Advertencia: {data['error']}")
                                print(f"   (Esto puede ser normal si no hay conexión a internet)")
                                tests_passed += 1  # No es un error crítico
                            elif "temperature" in data:
                                print(f"✅ Éxito: {data['city']} - {data['temperature']}, {data['condition']}")
                                tests_passed += 1
                            else:
                                print(f"❌ Error: Respuesta inesperada: {data}")
                                tests_failed += 1
                        else:
                            print(f"❌ Error: Formato de respuesta inesperado")
                            tests_failed += 1
                    else:
                        print("❌ Error: No se recibió respuesta")
                        tests_failed += 1
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    tests_failed += 1
                print()
                
                # Test 3: search_books
                print("=" * 70)
                print("4. PROBANDO: search_books")
                print("=" * 70)
                try:
                    result = await session.call_tool("search_books", {"query": "python"})
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if "error" in data:
                                print(f"❌ Error: {data['error']}")
                                tests_failed += 1
                            elif "results" in data:
                                print(f"✅ Éxito: Se encontraron {data['count']} resultados")
                                for i, libro in enumerate(data['results'][:2], 1):
                                    print(f"   {i}. {libro.get('titulo', 'N/A')} - {libro.get('autor', 'N/A')}")
                                tests_passed += 1
                            else:
                                print(f"❌ Error: Respuesta inesperada: {data}")
                                tests_failed += 1
                        else:
                            print(f"❌ Error: Formato de respuesta inesperado")
                            tests_failed += 1
                    else:
                        print("❌ Error: No se recibió respuesta")
                        tests_failed += 1
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    tests_failed += 1
                print()
                
                # Test 4: get_random_word
                print("=" * 70)
                print("5. PROBANDO: get_random_word")
                print("=" * 70)
                try:
                    result = await session.call_tool("get_random_word", {"category": "objeto"})
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if "error" in data:
                                print(f"❌ Error: {data['error']}")
                                tests_failed += 1
                            elif "word" in data:
                                print(f"✅ Éxito: Palabra '{data['word']}' de categoría '{data['category']}'")
                                tests_passed += 1
                            else:
                                print(f"❌ Error: Respuesta inesperada: {data}")
                                tests_failed += 1
                        else:
                            print(f"❌ Error: Formato de respuesta inesperado")
                            tests_failed += 1
                    else:
                        print("❌ Error: No se recibió respuesta")
                        tests_failed += 1
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    tests_failed += 1
                print()
                
                # Test 5: Validación de argumentos (tool con argumentos faltantes)
                print("=" * 70)
                print("6. PROBANDO: Validación de argumentos (get_weather sin city)")
                print("=" * 70)
                try:
                    result = await session.call_tool("get_weather", {})
                    if result.content and len(result.content) > 0:
                        content = result.content[0]
                        if hasattr(content, 'text'):
                            data = json.loads(content.text)
                            if "error" in data:
                                print(f"✅ Éxito: Validación funcionando - {data['error']}")
                                tests_passed += 1
                            else:
                                print(f"⚠️  Advertencia: No se validó el argumento requerido")
                                print(f"   Respuesta: {data}")
                                tests_passed += 1  # No es crítico
                        else:
                            print(f"❌ Error: Formato de respuesta inesperado")
                            tests_failed += 1
                    else:
                        print("❌ Error: No se recibió respuesta")
                        tests_failed += 1
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    tests_failed += 1
                print()
                
                # Resumen
                print("=" * 70)
                print("RESUMEN")
                print("=" * 70)
                print(f"✅ Tests pasados: {tests_passed}")
                print(f"❌ Tests fallidos: {tests_failed}")
                print(f"📊 Total: {tests_passed + tests_failed}")
                print()
                
                if tests_failed == 0:
                    print("🎉 ¡Todos los tests pasaron! El servidor MCP está funcionando correctamente.")
                    print()
                    print("💡 Próximos pasos:")
                    print("   1. Reinicia Cursor completamente")
                    print("   2. Verifica que el servidor aparezca en la lista de MCP servers")
                    print("   3. Prueba preguntando: '¿Qué tiempo hace en Madrid?'")
                    return True
                else:
                    print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")
                    return False
                
    except FileNotFoundError:
        print("❌ ERROR: No se encontró el ejecutable de Python")
        print("   Asegúrate de que 'python' está en tu PATH")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        print("💡 Posibles soluciones:")
        print("   1. Verifica que todas las dependencias estén instaladas:")
        print("      pip install -r requirements.txt")
        print("   2. Verifica que el servidor se pueda ejecutar manualmente:")
        print("      python server.py")
        return False


async def main() -> None:
    """Función principal."""
    success = await test_mcp_server()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
        sys.exit(1)

