"""
Ejercicio 04 — Flujo completo de tool: modelo → tool → modelo (dos turnos).

Aquí se enseña cómo se cierra el ciclo: el modelo pide una tool, tú la ejecutas,
luego le mandas el resultado como mensaje de tool para que genere la respuesta
final al usuario.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def get_weather(city: str) -> dict:
    """
    Obtiene el tiempo actual en una ciudad.
    
    Args:
        city: Nombre de la ciudad.
    """
    # DEMO: podrías usar una API real aquí
    # r = requests.get("https://api.weatherapi.com/v1/current.json", params={...})
    # return r.json()
    
    # Simulación de datos de clima
    datos_clima = {
        "Madrid": {"temp_c": 21.3, "condition": "Soleado con nubes"},
        "Barcelona": {"temp_c": 24.1, "condition": "Soleado"},
        "Valencia": {"temp_c": 26.5, "condition": "Parcialmente nublado"},
    }
    
    clima = datos_clima.get(city, {"temp_c": 20.0, "condition": "Desconocido"})
    
    return {
        "city": city,
        "temp_c": clima["temp_c"],
        "condition": clima["condition"],
    }


def run() -> None:
    print("🟦 EJERCICIO 4: FLUJO COMPLETO DE TOOL (DOS TURNOS)\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    client = OpenAI(api_key=api_key)
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Obtiene el tiempo actual en una ciudad.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "Nombre de la ciudad"},
                    },
                    "required": ["city"],
                },
            },
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": "¿Qué tiempo hace ahora en Madrid y explícamelo de forma sencilla?",
        },
    ]
    
    print("=" * 60)
    print("FLUJO COMPLETO: MODELO → TOOL → MODELO")
    print("=" * 60)
    print(f"\n👤 Usuario: {messages[0]['content']}\n")
    
    # 1) Primer llamado: el modelo decide si usar la tool y con qué argumentos
    print("🔄 TURNO 1: Modelo decide usar tool\n")
    first = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    msg = first.choices[0].message
    messages.append(msg)  # Añadimos el mensaje del modelo al historial
    
    if msg.tool_calls:
        call = msg.tool_calls[0]
        args = json.loads(call.function.arguments)
        
        print(f"   ✅ Modelo decidió usar tool: {call.function.name}")
        print(f"   📋 Argumentos: {args}\n")
        
        # 2) Ejecutamos la tool
        print("🔧 Ejecutando tool...\n")
        weather = get_weather(**args)
        print(f"   📊 Resultado de la tool: {json.dumps(weather, indent=2, ensure_ascii=False)}\n")
        
        # 3) Enviamos el resultado de la tool como un nuevo mensaje
        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "name": call.function.name,
                "content": json.dumps(weather),
            }
        )
        
        # 4) Segundo llamado: ahora el modelo ya tiene el resultado de la tool
        print("🔄 TURNO 2: Modelo genera respuesta final\n")
        second = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        
        final_msg = second.choices[0].message.content
        print("=" * 60)
        print("RESPUESTA FINAL AL USUARIO")
        print("=" * 60)
        print(f"\n{final_msg}\n")
    else:
        # El modelo ha decidido no usar tools
        print("⚠️  El modelo decidió no usar tools")
        print(f"   Respuesta directa: {msg.content}")
    
    print("=" * 60)
    print("💡 CICLO COMPLETO:")
    print("=" * 60)
    print("   1️⃣ Turno 1 → El modelo pide la tool")
    print("   2️⃣ Tu código ejecuta la tool")
    print("   3️⃣ Turno 2 → Le das el resultado y el modelo construye la respuesta final")
    print("\n   Este es el bucle fundamental de herramientas en OpenAI.")
    print("=" * 60)


if __name__ == "__main__":
    run()

