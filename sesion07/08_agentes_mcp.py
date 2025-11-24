"""
Ejemplo 8: Agentes con MCP Real (Airbnb Live)
=============================================

Complejidad: ALTA

Concepto:
---------
Este ejemplo utiliza el servidor MCP REAL de Airbnb (@openbnb/mcp-server-airbnb).
A diferencia del ejemplo anterior (que usaba una base de datos SQLite simulada),
este script conecta el Agente con el servidor MCP que navega la web de Airbnb en tiempo real.

Requisitos:
-----------
1. Node.js y NPM instalados (para ejecutar npx).
2. Paquete Python `mcp` instalado.

Arquitectura:
-------------
Agente (CrewAI) <--> MCPServerAdapter <--> Servidor MCP (NodeJS) <--> Airbnb.com

El servidor MCP expone herramientas como `search` y `get_listing` que el agente
descubrirá y usará automáticamente.
"""

import os
import sys
import io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ==============================================================================
# CONFIGURACIÓN DEL SERVIDOR MCP (Vía NPM/Node)
# ==============================================================================

def crear_servidor_mcp_airbnb():
    """
    Configura los parámetros para lanzar el servidor MCP de Airbnb oficial.
    Usamos 'npx' para ejecutar el paquete Node.js sin instalarlo globalmente.
    """
    # Verificamos si npx está disponible
    try:
        import subprocess
        # npx suele ser un script cmd en windows (npx.cmd)
        npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"
        subprocess.run([npx_cmd, "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ ERROR CRÍTICO: 'npx' (Node.js) no está instalado o no está en el PATH.")
        sys.exit(1)

    print("🔌 Configurando servidor MCP: @openbnb/mcp-server-airbnb")
    
    # Parámetros para StdioServerParameters
    # Es crucial usar npx.cmd en Windows para que Python pueda invocarlo
    command = "npx.cmd" if sys.platform == "win32" else "npx"
    args = ["-y", "@openbnb/mcp-server-airbnb"]

    server_params = StdioServerParameters(
        command=command, 
        args=args,
        env=None
    )
    
    return server_params

# ==============================================================================
# AGENTE Y TAREA
# ==============================================================================

def ejecutar_agente_airbnb_real():
    print("\n" + "="*80)
    print("🌍 AGENTE DE VIAJES CON ACCESO A AIRBNB (LIVE)")
    print("="*80)
    
    # 1. Configurar Servidor
    server_params = crear_servidor_mcp_airbnb()
    
    # 2. Monkeypatch para evitar bug de confirmación interactiva en crewai_tools
    import click
    if hasattr(click, "confirm"):
        original_confirm = click.confirm
        def mock_confirm(text, *args, **kwargs):
            if "missing the 'mcp' package" in text:
                return False
            return original_confirm(text, *args, **kwargs)
        click.confirm = mock_confirm

    # 3. Conectar Agente
    try:
        with MCPServerAdapter(server_params) as mcp_tools:
            # Listar herramientas descubiertas
            nombres_tools = [t.name for t in mcp_tools]
            print(f"🛠️  Herramientas MCP descubiertas: {nombres_tools}")
            
            if not nombres_tools:
                print("⚠️  No se detectaron herramientas. El servidor MCP podría estar fallando al iniciar.")
                return

            # Agente: Planner de Viajes
            agente_planner = Agent(
                role="Planner de Escapadas",
                goal="Encontrar alojamientos reales en Airbnb que cumplan criterios específicos",
                backstory="""Eres un experto en encontrar los mejores alojamientos. 
                Usas herramientas conectadas a Airbnb en tiempo real para buscar opciones.
                No inventas datos; usas lo que el sistema te devuelve.""",
                tools=mcp_tools,
                verbose=True,
                allow_delegation=False
            )
            
            # Tarea: Buscar alojamiento real
            tarea_busqueda = Task(
                description="""
                Busca 3 opciones de alojamiento en 'Mallorca, Spain' para 2 personas.
                Fechas flexibles (próximo mes).
                
                Usa las herramientas disponibles (probablemente 'search' o similar).
                
                Para cada opción encontrada, extrae:
                1. Nombre
                2. Precio (si está disponible)
                3. Una característica destacada
                
                Si la herramienta devuelve muchos resultados, selecciona solo los 3 primeros.
                """,
                agent=agente_planner,
                expected_output="Lista de 3 opciones de alojamiento reales encontradas en Airbnb."
            )
            
            # Equipo
            crew = Crew(
                agents=[agente_planner],
                tasks=[tarea_busqueda],
                process=Process.sequential,
                verbose=True
            )
            
            print("\n🚀 Iniciando búsqueda en Airbnb real...")
            resultado = crew.kickoff()
            
            print("\n" + "="*80)
            print("✅ RESULTADO FINAL")
            print("="*80)
            print(resultado)

    except Exception as e:
        print(f"\n❌ Error durante la ejecución del MCP: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_agente_airbnb_real()
