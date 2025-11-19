"""
Ejercicio 02 — Tool básica con OpenAI.

Aquí ya usamos tools de verdad. El modelo devuelve una estructura JSON
con el nombre de la función y los argumentos; tú solo la ejecutas.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def sumar(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b


def run() -> None:
    print("🟦 EJERCICIO 2: TOOL BÁSICA CON OPENAI\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Definición de la tool (JSON Schema)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "sumar",
                "description": "Suma dos números.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "Primer número"},
                        "b": {"type": "number", "description": "Segundo número"},
                    },
                    "required": ["a", "b"],
                },
            },
        }
    ]
    
    print("=" * 60)
    print("ENFOQUE CON TOOLS OFICIALES")
    print("=" * 60)
    print("\n📋 Tool definida:")
    print(json.dumps(tools, indent=2, ensure_ascii=False))
    
    user_message = "¿Puedes sumar 23.5 y 7, por favor?"
    print(f"\n👤 Usuario: {user_message}\n")
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_message},
        ],
        tools=tools,
        tool_choice="auto",  # El modelo decide si usar la tool
    )
    
    message = completion.choices[0].message
    print(f"🤖 Mensaje del modelo completo:\n{message}\n")
    
    # Si el modelo decidió usar una tool
    if message.tool_calls:
        call = message.tool_calls[0]
        func_name = call.function.name
        args = json.loads(call.function.arguments)
        
        print("=" * 60)
        print("TOOL LLAMADA POR EL MODELO")
        print("=" * 60)
        print(f"   Nombre de la tool: {func_name}")
        print(f"   Argumentos: {args}")
        
        # Ejecutar la función real
        if func_name == "sumar":
            result = sumar(**args)
            print(f"\n✅ Resultado de la función: {result}")
    else:
        print("⚠️  El modelo no ha llamado a ninguna tool")
        print(f"   Respuesta directa: {message.content}")
    
    print("\n" + "=" * 60)
    print("💡 CONCEPTOS CLAVE:")
    print("=" * 60)
    print("   ✅ tools: La definición (JSON Schema)")
    print("   ✅ tool_calls: El pedido del modelo")
    print("   ✅ arguments: Viene en JSON, lo parseas y ejecutas")
    print("   ✅ El modelo decide cuándo usar la tool (tool_choice='auto')")
    print("=" * 60)


if __name__ == "__main__":
    run()

