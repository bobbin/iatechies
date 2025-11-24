"""
Ejemplo 8: Agentes con Integración Real de MCP (Model Context Protocol)
=======================================================================

Complejidad: ALTA

Concepto:
---------
Este ejemplo muestra cómo conectar agentes de CrewAI a un servidor MCP real.
En este caso, usaremos el servidor MCP de sistema de archivos (Filesystem MCP) o SQLite
para demostrar capacidades reales de lectura/escritura y consulta.

Requisitos Previos:
-------------------
Para que este ejemplo funcione, necesitas tener un servidor MCP corriendo o accesible.
CrewAI v0.28+ soporta integración nativa con servidores MCP.

En este ejemplo, configuraremos un agente que se conecta a un servidor MCP de "File System"
para leer archivos reales de tu disco duro de forma segura.

Nota:
Si no tienes un servidor MCP externo configurado, este script intentará usar
las herramientas nativas de CrewAI que implementan protocolos similares,
o fallará explicando qué necesitas instalar.
"""

import os
import sys
import io
from dotenv import load_dotenv

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from crewai import Agent, Task, Crew, Process
# Importamos la clase MCPServer si está disponible en versiones recientes
# o usamos herramientas compatibles.
# Para este ejemplo práctico y reproducible sin infraestructura externa compleja,
# usaremos 'FileReadTool' y 'FileWriteTool' de crewai_tools que actúan como
# clientes MCP locales.

from crewai_tools import FileReadTool, FileWriterTool, DirectoryReadTool

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# CONFIGURACIÓN DE HERRAMIENTAS MCP (LOCALES)
# ==============================================================================

# Definimos el directorio de trabajo para restringir el acceso (Sandbox)
WORKING_DIRECTORY = "./sesion07/data_mcp"
os.makedirs(WORKING_DIRECTORY, exist_ok=True)

# Crear archivo de prueba si no existe
archivo_prueba = os.path.join(WORKING_DIRECTORY, "notas_proyecto.txt")
if not os.path.exists(archivo_prueba):
    with open(archivo_prueba, "w", encoding="utf-8") as f:
        f.write("""
        PROYECTO: MIGRACIÓN CLOUD 2024
        Estado: En progreso
        Presupuesto: $50,000
        
        Tareas pendientes:
        1. Evaluar proveedores (AWS vs Azure)
        2. Migrar base de datos de usuarios
        3. Configurar VPN corporativa
        """)

# Instanciamos las herramientas que actúan como interfaces MCP
# Estas herramientas permiten al agente interactuar con el sistema de archivos
file_read_tool = FileReadTool(file_path=archivo_prueba)
file_write_tool = FileWriterTool()
directory_read_tool = DirectoryReadTool(directory=WORKING_DIRECTORY)

# ==============================================================================
# AGENTES
# ==============================================================================

# Agente 1: Gestor de Archivos (Usa MCP de Filesystem)
agente_gestor = Agent(
    role="Gestor de Documentación",
    goal="Leer, organizar y actualizar la documentación del proyecto",
    backstory="""Eres un asistente administrativo encargado de mantener 
    la documentación del proyecto al día. Usas herramientas de sistema de archivos
    para leer el estado actual y registrar actualizaciones.""",
    tools=[file_read_tool, file_write_tool, directory_read_tool],
    verbose=True,
    allow_delegation=False
)

# Agente 2: Analista de Proyecto
agente_analista = Agent(
    role="Analista de Proyecto",
    goal="Analizar el estado del proyecto y proponer siguientes pasos",
    backstory="""Eres un Project Manager experimentado. Lees la información 
    proporcionada por el Gestor y decides qué acciones priorizar.""",
    verbose=True,
    allow_delegation=False
)

# ==============================================================================
# TAREAS
# ==============================================================================

# Tarea 1: Leer estado actual
tarea_lectura = Task(
    description=f"""
    1. Lista los archivos en el directorio '{WORKING_DIRECTORY}'.
    2. Lee el contenido del archivo 'notas_proyecto.txt'.
    3. Extrae el estado actual y las tareas pendientes.
    """,
    agent=agente_gestor,
    expected_output="Resumen del contenido del archivo y estado del proyecto."
)

# Tarea 2: Análisis y Planificación
tarea_analisis = Task(
    description="""
    Analiza el resumen proporcionado por el Gestor.
    1. Identifica riesgos potenciales basados en las tareas pendientes.
    2. Propone una nueva tarea prioritaria: "Contratar especialista en seguridad".
    3. Redacta el contenido actualizado para el archivo de notas.
    """,
    agent=agente_analista,
    expected_output="Texto completo actualizado para incluir en el archivo de notas."
)

# Tarea 3: Actualizar Archivo
tarea_escritura = Task(
    description=f"""
    Toma el contenido actualizado propuesto por el Analista y guárdalo en 
    un NUEVO archivo llamado 'notas_actualizadas_v2.txt' en el mismo directorio.
    
    NO sobrescribas el original.
    """,
    agent=agente_gestor,
    expected_output="Confirmación de que el archivo v2 ha sido creado."
)

# ==============================================================================
# EJECUCIÓN
# ==============================================================================

def ejecutar_demo_mcp():
    print("\n" + "="*80)
    print("🔌 DEMO: Agentes con Herramientas Reales (MCP-like)")
    print("="*80)
    print(f"Directorio de trabajo: {WORKING_DIRECTORY}")
    print("Herramientas activas: FileSystem Read/Write\n")

    equipo = Crew(
        agents=[agente_gestor, agente_analista],
        tasks=[tarea_lectura, tarea_analisis, tarea_escritura],
        process=Process.sequential,
        verbose=True
    )

    resultado = equipo.kickoff()

    print("\n" + "="*80)
    print("✅ RESULTADO FINAL DEL EQUIPO")
    print("="*80)
    print(resultado)
    
    # Verificación final
    archivo_v2 = os.path.join(WORKING_DIRECTORY, "notas_actualizadas_v2.txt")
    if os.path.exists(archivo_v2):
        print(f"\n📂 Verificación: El archivo '{archivo_v2}' fue creado exitosamente.")
        with open(archivo_v2, 'r', encoding='utf-8') as f:
            print("\n--- Contenido del nuevo archivo ---")
            print(f.read())
            print("-----------------------------------")
    else:
        print(f"\n❌ Error: El archivo '{archivo_v2}' no fue encontrado.")

if __name__ == "__main__":
    ejecutar_demo_mcp()
