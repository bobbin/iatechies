"""
Ejercicio 09 — Tools avanzadas en LangChain.

Demuestra cómo crear tools más complejas con validación,
tipos personalizados y mejor integración con LangChain.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Modelo Pydantic para validación avanzada
class FiltroBusqueda(BaseModel):
    """Filtros para búsqueda de productos."""
    categoria: Optional[str] = Field(None, description="Categoría del producto")
    precio_min: Optional[float] = Field(None, ge=0, description="Precio mínimo")
    precio_max: Optional[float] = Field(None, ge=0, description="Precio máximo")
    stock_minimo: Optional[int] = Field(None, ge=0, description="Stock mínimo requerido")


@tool
def buscar_productos(filtros: str) -> str:
    """
    Busca productos en un catálogo aplicando filtros.
    Los filtros deben ser un JSON con: categoria, precio_min, precio_max, stock_minimo.
    
    Args:
        filtros: JSON string con los filtros a aplicar.
    """
    try:
        filtros_dict = json.loads(filtros)
        
        # Base de datos simulada
        productos = [
            {"nombre": "Laptop", "categoria": "Electrónica", "precio": 1200, "stock": 5},
            {"nombre": "Mouse", "categoria": "Electrónica", "precio": 25, "stock": 50},
            {"nombre": "Monitor", "categoria": "Electrónica", "precio": 300, "stock": 20},
            {"nombre": "Silla", "categoria": "Muebles", "precio": 150, "stock": 10},
            {"nombre": "Mesa", "categoria": "Muebles", "precio": 200, "stock": 8},
        ]
        
        # Aplicar filtros
        resultados = productos
        if "categoria" in filtros_dict and filtros_dict["categoria"]:
            resultados = [p for p in resultados if p["categoria"] == filtros_dict["categoria"]]
        if "precio_min" in filtros_dict and filtros_dict["precio_min"]:
            resultados = [p for p in resultados if p["precio"] >= filtros_dict["precio_min"]]
        if "precio_max" in filtros_dict and filtros_dict["precio_max"]:
            resultados = [p for p in resultados if p["precio"] <= filtros_dict["precio_max"]]
        if "stock_minimo" in filtros_dict and filtros_dict["stock_minimo"]:
            resultados = [p for p in resultados if p["stock"] >= filtros_dict["stock_minimo"]]
        
        if not resultados:
            return "No se encontraron productos con esos filtros"
        
        return json.dumps(resultados, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return "Error: Los filtros deben ser un JSON válido"
    except Exception as e:
        return f"Error en búsqueda: {e}"


@tool
def analizar_sentimiento(texto: str) -> str:
    """
    Analiza el sentimiento de un texto (positivo, negativo, neutro).
    Úsalo para entender la opinión expresada en un texto.
    
    Args:
        texto: El texto a analizar.
    """
    texto_lower = texto.lower()
    
    palabras_positivas = ["bueno", "excelente", "genial", "me gusta", "perfecto", "fantástico"]
    palabras_negativas = ["malo", "terrible", "horrible", "no me gusta", "pésimo", "odio"]
    
    positivos = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
    negativos = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
    
    if positivos > negativos:
        sentimiento = "positivo"
        score = min(0.9, 0.5 + (positivos * 0.1))
    elif negativos > positivos:
        sentimiento = "negativo"
        score = min(0.9, 0.5 + (negativos * 0.1))
    else:
        sentimiento = "neutro"
        score = 0.5
    
    return json.dumps({
        "sentimiento": sentimiento,
        "score": round(score, 2),
        "razon": f"Encontradas {positivos} palabras positivas y {negativos} negativas"
    }, ensure_ascii=False)


@tool
def procesar_archivo(ruta: str, operacion: str) -> str:
    """
    Procesa un archivo de texto con diferentes operaciones.
    
    Args:
        ruta: Ruta al archivo a procesar.
        operacion: Tipo de operación: 'contar_lineas', 'contar_palabras', 'extraer_primera_linea'.
    """
    try:
        archivo = Path(ruta)
        if not archivo.exists():
            return f"Error: El archivo '{ruta}' no existe"
        
        contenido = archivo.read_text(encoding="utf-8")
        
        if operacion == "contar_lineas":
            lineas = contenido.split("\n")
            return f"El archivo tiene {len(lineas)} líneas"
        elif operacion == "contar_palabras":
            palabras = contenido.split()
            return f"El archivo tiene {len(palabras)} palabras"
        elif operacion == "extraer_primera_linea":
            primera = contenido.split("\n")[0]
            return f"Primera línea: {primera}"
        else:
            return f"Error: Operación '{operacion}' no válida. Usa: contar_lineas, contar_palabras, extraer_primera_linea"
    except Exception as e:
        return f"Error procesando archivo: {e}"


def main() -> None:
    print("🟦 EJERCICIO 9: TOOLS AVANZADAS EN LANGCHAIN\n")
    
    tools = [buscar_productos, analizar_sentimiento, procesar_archivo]
    
    print("📋 Tools avanzadas:\n")
    for i, tool_func in enumerate(tools, 1):
        print(f"{i}. {tool_func.name}")
        print(f"   {tool_func.description}\n")
    
    print("=" * 60)
    print("PRUEBAS DE TOOLS AVANZADAS\n")
    print("=" * 60)
    
    # Prueba 1: Búsqueda con filtros
    print("\n1️⃣ buscar_productos con filtros:")
    filtros = json.dumps({"categoria": "Electrónica", "precio_max": 500})
    resultado1 = buscar_productos.invoke({"filtros": filtros})
    print(f"   Filtros: {filtros}")
    print(f"   Resultado:\n{resultado1}\n")
    
    # Prueba 2: Análisis de sentimiento
    print("2️⃣ analizar_sentimiento:")
    texto1 = "Este producto es excelente, me gusta mucho"
    resultado2 = analizar_sentimiento.invoke({"texto": texto1})
    print(f"   Texto: '{texto1}'")
    print(f"   Resultado: {resultado2}\n")
    
    texto2 = "Este producto es terrible, no me gusta nada"
    resultado3 = analizar_sentimiento.invoke({"texto": texto2})
    print(f"   Texto: '{texto2}'")
    print(f"   Resultado: {resultado3}\n")
    
    # Prueba 3: Procesar archivo
    print("3️⃣ procesar_archivo:")
    # Crear archivo de ejemplo
    archivo_ejemplo = Path("data/ejemplo_procesar.txt")
    archivo_ejemplo.parent.mkdir(exist_ok=True)
    archivo_ejemplo.write_text("Línea 1\nLínea 2\nLínea 3", encoding="utf-8")
    
    resultado4 = procesar_archivo.invoke({"ruta": str(archivo_ejemplo), "operacion": "contar_lineas"})
    print(f"   {resultado4}")
    
    resultado5 = procesar_archivo.invoke({"ruta": str(archivo_ejemplo), "operacion": "contar_palabras"})
    print(f"   {resultado5}\n")
    
    print("=" * 60)
    print("💡 Observación:")
    print("   Estas tools son más complejas:")
    print("   - Aceptan parámetros estructurados (JSON)")
    print("   - Realizan procesamiento más sofisticado")
    print("   - Devuelven resultados estructurados")
    print("   - Tienen mejor manejo de errores")
    print("=" * 60)
    
    # Mostrar schemas
    print("\n📊 Schemas de las tools:\n")
    for tool_func in tools:
        print(f"{tool_func.name}:")
        print(json.dumps(tool_func.args, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()

