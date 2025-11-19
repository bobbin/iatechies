"""
Ejercicio 04 — Múltiples Tools trabajando juntas.

Demuestra cómo definir varias tools y cómo un agente puede decidir
cuál usar según el contexto.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from langchain_core.tools import tool


@tool
def leer_archivo(ruta: str) -> str:
    """
    Lee el contenido de un archivo de texto.
    Úsalo cuando necesites leer datos de un archivo.
    
    Args:
        ruta: La ruta al archivo a leer.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta}'"
    except Exception as e:
        return f"Error leyendo archivo: {e}"


@tool
def contar_palabras(texto: str) -> str:
    """
    Cuenta el número de palabras en un texto.
    Úsalo para analizar la longitud de un documento.
    
    Args:
        texto: El texto a analizar.
    """
    palabras = texto.split()
    return f"El texto tiene {len(palabras)} palabras"


@tool
def buscar_palabra(texto: str, palabra: str) -> str:
    """
    Busca una palabra en un texto y cuenta cuántas veces aparece.
    Úsalo para encontrar términos específicos.
    
    Args:
        texto: El texto donde buscar.
        palabra: La palabra a buscar (case-insensitive).
    """
    texto_lower = texto.lower()
    palabra_lower = palabra.lower()
    ocurrencias = texto_lower.split().count(palabra_lower)
    return f"La palabra '{palabra}' aparece {ocurrencias} veces"


@tool
def extraer_lineas(texto: str, inicio: int, fin: int) -> str:
    """
    Extrae un rango de líneas de un texto.
    Úsalo para obtener secciones específicas de un documento.
    
    Args:
        texto: El texto completo.
        inicio: Número de línea inicial (1-indexed).
        fin: Número de línea final (1-indexed, inclusive).
    """
    lineas = texto.split("\n")
    if inicio < 1 or fin > len(lineas) or inicio > fin:
        return f"Error: Rango inválido. El texto tiene {len(lineas)} líneas"
    
    seleccion = "\n".join(lineas[inicio - 1 : fin])
    return f"Líneas {inicio}-{fin}:\n{seleccion}"


def main() -> None:
    print("🟦 EJERCICIO 4: MÚLTIPLES TOOLS TRABAJANDO JUNTAS\n")
    
    # Crear un archivo de ejemplo
    archivo_ejemplo = Path("data/ejemplo.txt")
    archivo_ejemplo.parent.mkdir(exist_ok=True)
    contenido = """Python es un lenguaje de programación.
Es muy popular para ciencia de datos.
Python tiene muchas librerías útiles.
La comunidad de Python es grande.
Python se usa en muchas empresas."""
    
    archivo_ejemplo.write_text(contenido, encoding="utf-8")
    print(f"✅ Archivo de ejemplo creado: {archivo_ejemplo}\n")
    
    # Lista de todas las tools
    tools = [leer_archivo, contar_palabras, buscar_palabra, extraer_lineas]
    
    print("📋 Tools disponibles:\n")
    for i, tool_func in enumerate(tools, 1):
        print(f"{i}. {tool_func.name}")
        print(f"   {tool_func.description}\n")
    
    # Simulación de un flujo de trabajo
    print("=" * 60)
    print("SIMULACIÓN: Análisis de un documento\n")
    print("=" * 60)
    
    # Paso 1: Leer archivo
    print("\n1️⃣ Paso 1: Leer archivo")
    resultado1 = leer_archivo.invoke({"ruta": str(archivo_ejemplo)})
    print(f"   Resultado: {resultado1[:100]}...\n")
    
    # Paso 2: Contar palabras
    print("2️⃣ Paso 2: Contar palabras")
    resultado2 = contar_palabras.invoke({"texto": resultado1})
    print(f"   {resultado2}\n")
    
    # Paso 3: Buscar palabra
    print("3️⃣ Paso 3: Buscar palabra 'Python'")
    resultado3 = buscar_palabra.invoke({"texto": resultado1, "palabra": "Python"})
    print(f"   {resultado3}\n")
    
    # Paso 4: Extraer líneas
    print("4️⃣ Paso 4: Extraer primeras 2 líneas")
    resultado4 = extraer_lineas.invoke({"texto": resultado1, "inicio": 1, "fin": 2})
    print(f"   {resultado4}\n")
    
    print("=" * 60)
    print("💡 Observación:")
    print("   Un agente podría usar estas tools en cualquier orden")
    print("   según lo que necesite. El modelo decide cuál usar.")
    print("=" * 60)
    
    # Mostrar schemas
    print("\n📊 Schemas de las tools (lo que ve el LLM):\n")
    for tool_func in tools:
        print(f"{tool_func.name}:")
        print(json.dumps(tool_func.args, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()

