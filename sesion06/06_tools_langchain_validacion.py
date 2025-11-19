"""
Ejercicio 06 — Tools con validación y manejo de errores.

Demuestra cómo crear tools robustas que validan entradas
y manejan errores de forma predecible.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import List

from langchain_core.tools import tool


@tool
def calcular_edad(fecha_nacimiento: str) -> str:
    """
    Calcula la edad a partir de una fecha de nacimiento.
    La fecha debe estar en formato YYYY-MM-DD.
    
    Args:
        fecha_nacimiento: Fecha en formato YYYY-MM-DD (ej: "1990-05-15").
    """
    try:
        # Validar formato
        fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        hoy = datetime.now()
        
        # Validar que no sea futura
        if fecha > hoy:
            return "Error: La fecha de nacimiento no puede ser futura"
        
        # Calcular edad
        edad = hoy.year - fecha.year
        if (hoy.month, hoy.day) < (fecha.month, fecha.day):
            edad -= 1
        
        return f"La edad es {edad} años"
    except ValueError as e:
        return f"Error: Formato de fecha inválido. Usa YYYY-MM-DD. Detalle: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"


@tool
def dividir_numeros(a: float, b: float) -> str:
    """
    Divide dos números.
    Úsalo para realizar divisiones matemáticas.
    
    Args:
        a: Dividendo (número a dividir).
        b: Divisor (número por el que se divide).
    """
    try:
        # Validar división por cero
        if b == 0:
            return "Error: No se puede dividir por cero"
        
        resultado = a / b
        return f"El resultado de {a} / {b} = {resultado:.2f}"
    except Exception as e:
        return f"Error en la división: {e}"


@tool
def buscar_en_lista(lista: List[str], elemento: str) -> str:
    """
    Busca un elemento en una lista y devuelve su posición.
    Úsalo para encontrar elementos en colecciones.
    
    Args:
        lista: Lista de elementos donde buscar.
        elemento: Elemento a buscar.
    """
    try:
        if not lista:
            return "Error: La lista está vacía"
        
        if elemento not in lista:
            return f"'{elemento}' no se encontró en la lista"
        
        indice = lista.index(elemento)
        return f"'{elemento}' se encuentra en la posición {indice} (índice 0-based)"
    except Exception as e:
        return f"Error buscando en lista: {e}"


@tool
def validar_email(email: str) -> str:
    """
    Valida si un email tiene formato correcto.
    Úsalo para verificar direcciones de correo.
    
    Args:
        email: Dirección de email a validar.
    """
    try:
        if not email or "@" not in email:
            return "Error: Email inválido. Debe contener '@'"
        
        partes = email.split("@")
        if len(partes) != 2:
            return "Error: Email inválido. Formato incorrecto"
        
        local, dominio = partes
        if not local or not dominio:
            return "Error: Email inválido. Falta parte local o dominio"
        
        if "." not in dominio:
            return "Error: Email inválido. El dominio debe contener un punto"
        
        return f"✅ Email válido: {email}"
    except Exception as e:
        return f"Error validando email: {e}"


def main() -> None:
    print("🟦 EJERCICIO 6: TOOLS CON VALIDACIÓN Y MANEJO DE ERRORES\n")
    
    tools = [calcular_edad, dividir_numeros, buscar_en_lista, validar_email]
    
    print("📋 Tools con validación:\n")
    for i, tool_func in enumerate(tools, 1):
        print(f"{i}. {tool_func.name}")
        print(f"   {tool_func.description}\n")
    
    print("=" * 60)
    print("PRUEBAS: Casos válidos y errores\n")
    print("=" * 60)
    
    # Pruebas de calcular_edad
    print("\n1️⃣ calcular_edad:")
    print("   ✅ Caso válido:")
    resultado1 = calcular_edad.invoke({"fecha_nacimiento": "1990-05-15"})
    print(f"      {resultado1}")
    print("   ❌ Caso inválido (formato incorrecto):")
    resultado2 = calcular_edad.invoke({"fecha_nacimiento": "15-05-1990"})
    print(f"      {resultado2}")
    print("   ❌ Caso inválido (fecha futura):")
    resultado3 = calcular_edad.invoke({"fecha_nacimiento": "2030-01-01"})
    print(f"      {resultado3}")
    
    # Pruebas de dividir_numeros
    print("\n2️⃣ dividir_numeros:")
    print("   ✅ Caso válido:")
    resultado4 = dividir_numeros.invoke({"a": 10.0, "b": 2.0})
    print(f"      {resultado4}")
    print("   ❌ Caso inválido (división por cero):")
    resultado5 = dividir_numeros.invoke({"a": 10.0, "b": 0.0})
    print(f"      {resultado5}")
    
    # Pruebas de buscar_en_lista
    print("\n3️⃣ buscar_en_lista:")
    print("   ✅ Caso válido:")
    resultado6 = buscar_en_lista.invoke({"lista": ["a", "b", "c"], "elemento": "b"})
    print(f"      {resultado6}")
    print("   ❌ Caso inválido (no encontrado):")
    resultado7 = buscar_en_lista.invoke({"lista": ["a", "b", "c"], "elemento": "x"})
    print(f"      {resultado7}")
    print("   ❌ Caso inválido (lista vacía):")
    resultado8 = buscar_en_lista.invoke({"lista": [], "elemento": "a"})
    print(f"      {resultado8}")
    
    # Pruebas de validar_email
    print("\n4️⃣ validar_email:")
    print("   ✅ Caso válido:")
    resultado9 = validar_email.invoke({"email": "usuario@ejemplo.com"})
    print(f"      {resultado9}")
    print("   ❌ Caso inválido:")
    resultado10 = validar_email.invoke({"email": "usuario@ejemplo"})
    print(f"      {resultado10}")
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Las tools deben validar entradas y devolver mensajes")
    print("   de error claros. Esto ayuda al agente a entender qué salió mal")
    print("   y cómo corregirlo.")
    print("=" * 60)


if __name__ == "__main__":
    main()

