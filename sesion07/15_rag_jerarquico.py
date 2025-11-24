"""
Ejemplo: RAG Agéntico Jerárquico
==================================

Este ejemplo demuestra un sistema RAG (Retrieval Augmented Generation) jerárquico
donde un agente navega una estructura de documentos en tres niveles:

1. Índice Maestro: Contiene la estructura general del manual
2. Índices de Sección: Cada sección tiene su propio índice
3. Documentos Específicos: Documentos detallados dentro de cada sección

El agente consulta primero el índice maestro, luego navega al índice de sección
apropiado, y finalmente lee el documento específico necesario para responder la consulta.
"""

import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# Directorio base del manual
BASE_DIR = Path(__file__).parent / "rag_jerarquico"

# ==============================================================================
# HERRAMIENTAS PARA NAVEGACIÓN JERÁRQUICA
# ==============================================================================

@tool("Leer Índice Maestro")
def leer_indice_maestro() -> str:
    """
    Lee el índice maestro que contiene la estructura general del manual.
    Este índice referencia todas las secciones disponibles y sus contenidos.
    
    Returns:
        Contenido completo del índice maestro.
    """
    ruta = BASE_DIR / "indice_maestro.md"
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ Error: No se encontró el índice maestro en {ruta}"
    except Exception as e:
        return f"❌ Error al leer índice maestro: {str(e)}"

@tool("Leer Índice de Sección")
def leer_indice_seccion(numero_seccion: int) -> str:
    """
    Lee el índice de una sección específica del manual.
    
    Args:
        numero_seccion: Número de la sección (1-5)
            - 1: Instalación y Requisitos
            - 2: Configuración y Setup
            - 3: Uso y Operación
            - 4: Troubleshooting
            - 5: Referencia Técnica
    
    Returns:
        Contenido del índice de la sección especificada.
    """
    secciones = {
        1: "seccion_01_instalacion",
        2: "seccion_02_configuracion",
        3: "seccion_03_uso",
        4: "seccion_04_troubleshooting",
        5: "seccion_05_referencia"
    }
    
    if numero_seccion not in secciones:
        return f"❌ Error: Número de sección inválido. Debe ser entre 1 y 5."
    
    nombre_seccion = secciones[numero_seccion]
    ruta = BASE_DIR / nombre_seccion / f"indice_seccion_{numero_seccion:02d}.md"
    
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ Error: No se encontró el índice de la sección {numero_seccion} en {ruta}"
    except Exception as e:
        return f"❌ Error al leer índice de sección: {str(e)}"

@tool("Leer Documento Específico")
def leer_documento(seccion: int, nombre_documento: str) -> str:
    """
    Lee un documento específico dentro de una sección.
    
    Args:
        seccion: Número de la sección (1-5)
        nombre_documento: Nombre del archivo del documento (ej: "01_requisitos_sistema.md")
    
    Returns:
        Contenido completo del documento solicitado.
    """
    secciones = {
        1: "seccion_01_instalacion",
        2: "seccion_02_configuracion",
        3: "seccion_03_uso",
        4: "seccion_04_troubleshooting",
        5: "seccion_05_referencia"
    }
    
    if seccion not in secciones:
        return f"❌ Error: Número de sección inválido. Debe ser entre 1 y 5."
    
    nombre_seccion = secciones[seccion]
    ruta = BASE_DIR / nombre_seccion / nombre_documento
    
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            return f"📄 Contenido de {nombre_documento}:\n\n{contenido}"
    except FileNotFoundError:
        # Intentar listar archivos disponibles
        dir_seccion = BASE_DIR / nombre_seccion
        if dir_seccion.exists():
            archivos = [f.name for f in dir_seccion.glob("*.md") if f.is_file()]
            return f"❌ Documento '{nombre_documento}' no encontrado.\n\nArchivos disponibles en sección {seccion}:\n" + "\n".join(f"  - {f}" for f in sorted(archivos))
        return f"❌ Error: Sección {seccion} no existe."
    except Exception as e:
        return f"❌ Error al leer documento: {str(e)}"

@tool("Listar Documentos de Sección")
def listar_documentos_seccion(seccion: int) -> str:
    """
    Lista todos los documentos disponibles en una sección.
    
    Args:
        seccion: Número de la sección (1-5)
    
    Returns:
        Lista de documentos disponibles en la sección.
    """
    secciones = {
        1: "seccion_01_instalacion",
        2: "seccion_02_configuracion",
        3: "seccion_03_uso",
        4: "seccion_04_troubleshooting",
        5: "seccion_05_referencia"
    }
    
    if seccion not in secciones:
        return f"❌ Error: Número de sección inválido. Debe ser entre 1 y 5."
    
    nombre_seccion = secciones[seccion]
    dir_seccion = BASE_DIR / nombre_seccion
    
    if not dir_seccion.exists():
        return f"❌ Error: Sección {seccion} no existe."
    
    archivos = [f.name for f in dir_seccion.glob("*.md") if f.is_file()]
    archivos.sort()
    
    return f"📚 Documentos disponibles en Sección {seccion}:\n\n" + "\n".join(f"  - {f}" for f in archivos)

# ==============================================================================
# AGENTE RAG JERÁRQUICO
# ==============================================================================

agente_rag = Agent(
    role="Especialista en Documentación Jerárquica",
    goal="Navegar eficientemente la estructura jerárquica de documentos para encontrar y proporcionar información precisa",
    backstory="""Eres un experto en sistemas de documentación jerárquica. 
    Tu especialidad es navegar estructuras de documentos complejas de forma eficiente.
    
    Tu proceso de trabajo es:
    1. Primero consultas el ÍNDICE MAESTRO para entender la estructura general
    2. Identificas qué SECCIÓN es relevante para la consulta del usuario
    3. Consultas el ÍNDICE DE SECCIÓN para ver qué documentos están disponibles
    4. Seleccionas y lees el DOCUMENTO ESPECÍFICO más relevante
    5. Proporcionas una respuesta completa basada en la información encontrada
    
    Siempre sigues esta jerarquía: Índice Maestro → Índice de Sección → Documento Específico.
    Nunca lees documentos directamente sin consultar primero los índices.""",
    tools=[leer_indice_maestro, leer_indice_seccion, leer_documento, listar_documentos_seccion],
    verbose=True,
    allow_delegation=False
)

# ==============================================================================
# FUNCIÓN PARA CREAR TAREAS DE CONSULTA
# ==============================================================================

def crear_tarea_consulta(consulta: str):
    """
    Crea una tarea para que el agente RAG responda una consulta.
    
    Args:
        consulta: La pregunta o consulta del usuario sobre el manual.
    
    Returns:
        Task configurada para el agente RAG.
    """
    return Task(
        description=f"""
        El usuario tiene la siguiente consulta sobre el manual:
        
        "{consulta}"
        
        Para responder esta consulta, debes seguir este proceso jerárquico:
        
        1. PRIMERO: Usa la herramienta 'Leer Índice Maestro' para entender la estructura general del manual.
        
        2. SEGUNDO: Basándote en el índice maestro, identifica qué sección (1-5) es más relevante para la consulta.
        
        3. TERCERO: Usa 'Leer Índice de Sección' con el número de sección identificado para ver qué documentos están disponibles.
        
        4. CUARTO: Selecciona el documento más relevante y úsalo con 'Leer Documento Específico'.
        
        5. QUINTO: Si necesitas información adicional, puedes consultar otros documentos o secciones.
        
        6. FINALMENTE: Proporciona una respuesta completa y precisa basada en la información encontrada en los documentos.
        
        IMPORTANTE: 
        - Siempre sigue la jerarquía: Índice Maestro → Índice de Sección → Documento Específico
        - No leas documentos directamente sin consultar primero los índices
        - Si la información no está en un documento, consulta otros documentos relacionados
        - Proporciona referencias específicas (sección y documento) en tu respuesta
        """,
        agent=agente_rag,
        expected_output="Una respuesta completa y precisa basada en la información encontrada en los documentos del manual, con referencias específicas a las secciones y documentos consultados."
    )

# ==============================================================================
# EJECUCIÓN
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔍 SISTEMA RAG JERÁRQUICO - Consulta de Documentación")
    print("="*80)
    print("\nEste sistema navega una estructura jerárquica de documentos:")
    print("  1. Índice Maestro (estructura general)")
    print("  2. Índices de Sección (contenido por sección)")
    print("  3. Documentos Específicos (información detallada)")
    print("="*80 + "\n")
    
    # Ejemplos de consultas
    consultas_ejemplo = [
        "¿Cuáles son los requisitos del sistema para instalar el software?",
        "¿Cómo configuro las variables de entorno?",
        "Necesito ayuda para crear mi primer agente, ¿dónde encuentro información?",
        "¿Qué hago si tengo un error de API key?"
    ]
    
    print("Consultas de ejemplo disponibles:")
    for i, consulta in enumerate(consultas_ejemplo, 1):
        print(f"  {i}. {consulta}")
    
    print("\n" + "-"*80)
    
    # Permitir al usuario elegir o ingresar su propia consulta
    print("\nOpciones:")
    print("  1-4: Seleccionar consulta de ejemplo")
    print("  5: Ingresar consulta personalizada")
    
    try:
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion in ["1", "2", "3", "4"]:
            consulta = consultas_ejemplo[int(opcion) - 1]
        elif opcion == "5":
            consulta = input("\nIngresa tu consulta: ").strip()
            if not consulta:
                print("❌ Consulta vacía. Usando consulta por defecto.")
                consulta = consultas_ejemplo[0]
        else:
            print("❌ Opción inválida. Usando consulta por defecto.")
            consulta = consultas_ejemplo[0]
        
        print(f"\n📋 Consulta seleccionada: {consulta}\n")
        print("🚀 Iniciando búsqueda jerárquica...\n")
        
        # Crear tarea y equipo
        tarea = crear_tarea_consulta(consulta)
        equipo = Crew(
            agents=[agente_rag],
            tasks=[tarea],
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        resultado = equipo.kickoff()
        
        print("\n" + "="*80)
        print("📄 RESPUESTA FINAL")
        print("="*80)
        print(resultado)
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\n❌ Consulta cancelada por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()

