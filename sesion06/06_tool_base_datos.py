"""
Ejercicio 06 — Tool conectada a base de datos / capa de dominio.

Ejemplo conceptual de tool que consulta datos de usuario.
Esto ya se parece mucho a un caso de negocio real.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


# Simulación de "base de datos"
USERS = {
    "u123": {"nombre": "Laura", "plan": "Pro", "activo": True},
    "u456": {"nombre": "Jorge", "plan": "Free", "activo": False},
    "u789": {"nombre": "Ana", "plan": "Premium", "activo": True},
}


def get_user_profile(user_id: str) -> dict:
    """
    Obtiene el perfil básico de un usuario por ID interno.
    
    Args:
        user_id: ID interno del usuario.
    """
    user = USERS.get(user_id)
    if not user:
        return {"found": False, "message": f"Usuario {user_id} no encontrado"}
    
    return {"found": True, "user": user}


def run() -> None:
    print("🟦 EJERCICIO 6: TOOL CONECTADA A BASE DE DATOS\n")
    
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
                "name": "get_user_profile",
                "description": "Obtiene el perfil básico de un usuario por ID interno.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID interno del usuario"},
                    },
                    "required": ["user_id"],
                },
            },
        }
    ]
    
    print("=" * 60)
    print("TOOL CONECTADA A CAPA DE DOMINIO")
    print("=" * 60)
    print("\n📊 Base de datos simulada:")
    for user_id, user_data in USERS.items():
        print(f"   {user_id}: {user_data}")
    
    messages = [
        {
            "role": "user",
            "content": "Dime si el usuario u456 tiene una cuenta activa y qué plan tiene.",
        },
    ]
    
    print(f"\n👤 Usuario: {messages[0]['content']}\n")
    
    first = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    
    msg = first.choices[0].message
    messages.append(msg)
    
    if not msg.tool_calls:
        print("⚠️  El modelo no ha llamado a ninguna tool.")
        print(f"   Respuesta directa: {msg.content}")
        return
    
    call = msg.tool_calls[0]
    args = json.loads(call.function.arguments)
    
    print(f"🔧 Tool llamada: {call.function.name}")
    print(f"📋 Argumentos: {args}\n")
    
    result = get_user_profile(**args)
    
    print(f"📊 Resultado de la tool: {json.dumps(result, indent=2, ensure_ascii=False)}\n")
    
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.function.name,
            "content": json.dumps(result),
        }
    )
    
    second = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    
    print("=" * 60)
    print("RESPUESTA FINAL AL USUARIO")
    print("=" * 60)
    print(f"\n{second.choices[0].message.content}\n")
    
    print("=" * 60)
    print("💡 CASO DE NEGOCIO REAL:")
    print("=" * 60)
    print("   ✅ LLM entiende la pregunta del usuario")
    print("   ✅ Tool accede a tu dominio (DB / microservicio)")
    print("   ✅ LLM genera una respuesta bien explicada")
    print("\n   En producción, reemplazarías USERS con:")
    print("   - Consulta SQL real")
    print("   - Llamada a API REST")
    print("   - Acceso a base de datos NoSQL")
    print("   - Microservicio interno")
    print("=" * 60)


if __name__ == "__main__":
    run()

