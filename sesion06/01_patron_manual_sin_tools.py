"""
Ejercicio 01 — Patrón "manual" sin tools oficiales.

Este ejemplo muestra por qué las tools oficiales son mejores:
el modelo responde con texto y tú parseas a mano.
"""

from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def run() -> None:
    print("🟦 EJERCICIO 1: PATRÓN MANUAL SIN TOOLS OFICIALES\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    client = OpenAI(api_key=api_key)
    
    prompt = """
    Eres un asistente con dos acciones:
    
    - SEARCH: cuando el usuario te pide buscar algo en la web.
    - CALC: cuando el usuario te pide hacer un cálculo numérico.
    
    Responde SOLO con:
    - "SEARCH: <query>" o
    - "CALC: <expresion>"
    """
    
    user = "¿Cuánto es 23 * 7?"
    
    print("=" * 60)
    print("ENFOQUE MANUAL (SIN TOOLS OFICIALES)")
    print("=" * 60)
    print(f"\n📝 Prompt del sistema:\n{prompt}\n")
    print(f"👤 Usuario: {user}\n")
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user},
        ],
    )
    
    text = completion.choices[0].message.content
    print(f"🤖 Modelo responde: {text}\n")
    
    # Parseo manual (frágil)
    if text.startswith("CALC:"):
        expr = text.replace("CALC:", "").strip()
        try:
            result = eval(expr)  # ⚠️ Solo como demo, nunca en producción
            print(f"✅ Resultado calculado: {result}")
        except Exception as e:
            print(f"❌ Error al calcular: {e}")
    elif text.startswith("SEARCH:"):
        query = text.replace("SEARCH:", "").strip()
        print(f"🔍 Búsqueda solicitada: {query}")
    else:
        print("⚠️  Respuesta no reconocida, no se puede parsear")
    
    print("\n" + "=" * 60)
    print("💡 PROBLEMAS DE ESTE ENFOQUE:")
    print("=" * 60)
    print("   ❌ Todo es texto frágil")
    print("   ❌ El parseo puede romperse fácilmente")
    print("   ❌ No hay validación de estructura")
    print("   ❌ El modelo puede responder en formatos inesperados")
    print("   ❌ Difícil de mantener y escalar")
    print("\n   ✅ Solución: Usar tools oficiales (ver siguiente ejercicio)")
    print("=" * 60)


if __name__ == "__main__":
    run()

