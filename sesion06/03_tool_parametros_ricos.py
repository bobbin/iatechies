"""
Ejercicio 03 — Tool con parámetros más ricos.

Subimos nivel: una tool con enum, parámetro opcional y descripción más detallada.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def get_report(periodo: str, formato: str, incluir_grafico: bool = False) -> dict:
    """
    Genera un informe de ventas.
    
    Args:
        periodo: Rango de tiempo del informe.
        formato: Nivel de detalle del informe.
        incluir_grafico: Si es True, incluye datos para gráfico.
    """
    # Demo: en realidad aquí consultarías BD, etc.
    return {
        "periodo": periodo,
        "formato": formato,
        "timestamp": datetime.utcnow().isoformat(),
        "ventas_totales": 12345.67,
        "incluir_grafico": incluir_grafico,
        "datos_grafico": [10, 20, 30] if incluir_grafico else [],
    }


def run() -> None:
    print("🟦 EJERCICIO 3: TOOL CON PARÁMETROS MÁS RICOS\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Tool con enums, parámetros opcionales y validación
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_report",
                "description": "Devuelve un pequeño informe sobre ventas.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "periodo": {
                            "type": "string",
                            "enum": ["hoy", "semana", "mes"],
                            "description": "Rango de tiempo del informe",
                        },
                        "formato": {
                            "type": "string",
                            "enum": ["resumen", "detallado"],
                            "description": "Nivel de detalle del informe",
                        },
                        "incluir_grafico": {
                            "type": "boolean",
                            "description": "Si es true, incluye datos para gráfico.",
                        },
                    },
                    "required": ["periodo", "formato"],
                },
            },
        }
    ]
    
    print("=" * 60)
    print("TOOL CON PARÁMETROS AVANZADOS")
    print("=" * 60)
    print("\n📋 Tool definida:")
    print(json.dumps(tools, indent=2, ensure_ascii=False))
    
    user_message = "Dame un informe de ventas de este mes, detallado y con gráfico."
    print(f"\n👤 Usuario: {user_message}\n")
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": user_message,
            },
        ],
        tools=tools,
        tool_choice="auto",
    )
    
    msg = completion.choices[0].message
    
    if not msg.tool_calls:
        print("⚠️  El modelo no ha llamado a ninguna tool.")
        print(f"   Respuesta directa: {msg.content}")
        return
    
    call = msg.tool_calls[0]
    args = json.loads(call.function.arguments)
    
    print("=" * 60)
    print("TOOL LLAMADA CON ARGUMENTOS")
    print("=" * 60)
    print(f"   Tool: {call.function.name}")
    print(f"   Argumentos parseados: {json.dumps(args, indent=2, ensure_ascii=False)}\n")
    
    result = get_report(**args)
    
    print("=" * 60)
    print("RESULTADO DE LA FUNCIÓN")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("💡 PUNTOS DIDÁCTICOS:")
    print("=" * 60)
    print("   ✅ enums: Ayudan al modelo a no inventarse valores")
    print("   ✅ parámetros opcionales: Evitan obligar al usuario a decir todo")
    print("   ✅ required: Define qué parámetros son obligatorios")
    print("   ✅ La tool devuelve un objeto Python, que luego puedes serializar")
    print("=" * 60)


if __name__ == "__main__":
    run()

