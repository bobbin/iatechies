"""
Ejercicio 05 — Tool con validación y manejo de errores.

Aquí se introduce algo muy productivo en la vida real: la tool valida parámetros
y devuelve errores controlados, que el modelo puede explicar al usuario.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def transferir_dinero(origen: str, destino: str, importe: float) -> dict:
    """
    Transfiere dinero entre cuentas internas.
    
    Args:
        origen: Cuenta origen.
        destino: Cuenta destino.
        importe: Cantidad a transferir en EUR.
    """
    # Validación 1: Misma cuenta
    if origen == destino:
        return {
            "status": "error",
            "message": "La cuenta origen y destino no pueden ser la misma.",
        }
    
    # Validación 2: Límite diario
    if importe > 1000:
        return {
            "status": "error",
            "message": "Límite diario excedido para transferencias (1000 EUR).",
        }
    
    # Validación 3: Importe mínimo
    if importe < 0.01:
        return {
            "status": "error",
            "message": "El importe mínimo es 0.01 EUR.",
        }
    
    # Aquí iría lógica real contra tu sistema bancario
    return {
        "status": "ok",
        "message": f"Transferidos {importe} EUR de {origen} a {destino}.",
    }


def run() -> None:
    print("🟦 EJERCICIO 5: TOOL CON VALIDACIÓN Y MANEJO DE ERRORES\n")
    
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
                "name": "transferir_dinero",
                "description": "Transfiere dinero entre cuentas internas.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origen": {"type": "string", "description": "Cuenta origen"},
                        "destino": {"type": "string", "description": "Cuenta destino"},
                        "importe": {
                            "type": "number",
                            "minimum": 0.01,
                            "description": "Cantidad a transferir en EUR",
                        },
                    },
                    "required": ["origen", "destino", "importe"],
                },
            },
        }
    ]
    
    # Ejemplo 1: Transferencia válida
    print("=" * 60)
    print("EJEMPLO 1: Transferencia válida")
    print("=" * 60)
    
    messages1 = [
        {"role": "user", "content": "Quiero transferir 100 euros de mi cuenta A a mi cuenta B."},
    ]
    
    print(f"\n👤 Usuario: {messages1[0]['content']}\n")
    
    first1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages1,
        tools=tools,
        tool_choice="auto",
    )
    
    msg1 = first1.choices[0].message
    messages1.append(msg1)
    
    if msg1.tool_calls:
        call1 = msg1.tool_calls[0]
        args1 = json.loads(call1.function.arguments)
        result1 = transferir_dinero(**args1)
        
        messages1.append(
            {
                "role": "tool",
                "tool_call_id": call1.id,
                "name": call1.function.name,
                "content": json.dumps(result1),
            }
        )
        
        second1 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages1,
        )
        
        print(f"🤖 Respuesta final:\n{second1.choices[0].message.content}\n")
    
    # Ejemplo 2: Error (límite excedido)
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Error - Límite excedido")
    print("=" * 60)
    
    messages2 = [
        {"role": "user", "content": "Quiero pasar 1500 euros de mi cuenta A a mi cuenta B."},
    ]
    
    print(f"\n👤 Usuario: {messages2[0]['content']}\n")
    
    first2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages2,
        tools=tools,
        tool_choice="auto",
    )
    
    msg2 = first2.choices[0].message
    messages2.append(msg2)
    
    if msg2.tool_calls:
        call2 = msg2.tool_calls[0]
        args2 = json.loads(call2.function.arguments)
        result2 = transferir_dinero(**args2)
        
        print(f"   ⚠️  Resultado de la tool: {json.dumps(result2, indent=2, ensure_ascii=False)}\n")
        
        messages2.append(
            {
                "role": "tool",
                "tool_call_id": call2.id,
                "name": call2.function.name,
                "content": json.dumps(result2),
            }
        )
        
        second2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages2,
        )
        
        print(f"🤖 Respuesta final (el modelo explica el error):\n{second2.choices[0].message.content}\n")
    
    print("=" * 60)
    print("💡 PUNTOS CLAVE:")
    print("=" * 60)
    print("   ✅ La lógica de negocio vive en tu tool, no en el modelo")
    print("   ✅ El modelo solo traduce: intención → llamada → mensaje amigable")
    print("   ✅ Los errores se devuelven estructurados y el modelo los explica")
    print("   ✅ Validación en la tool, no en el prompt")
    print("=" * 60)


if __name__ == "__main__":
    run()

