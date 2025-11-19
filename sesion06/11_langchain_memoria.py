"""
Ejercicio 11 — Agente con memoria en LangChain.

Demuestra cómo usar memoria en LangChain 1.0+ para que el agente
recuerde contexto entre interacciones manteniendo el historial de mensajes.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


@tool
def guardar_nota(titulo: str, contenido: str) -> str:
    """
    Guarda una nota con título y contenido en memoria.
    Úsalo para recordar información importante.
    
    Args:
        titulo: Título de la nota.
        contenido: Contenido de la nota.
    """
    return f"✅ Nota guardada: '{titulo}' - {contenido[:50]}..."


@tool
def obtener_fecha_actual() -> str:
    """Obtiene la fecha y hora actual."""
    from datetime import datetime
    return f"Fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


@tool
def calcular_edad(fecha_nacimiento: str) -> str:
    """
    Calcula la edad a partir de una fecha de nacimiento (YYYY-MM-DD).
    
    Args:
        fecha_nacimiento: Fecha en formato YYYY-MM-DD.
    """
    from datetime import datetime
    try:
        fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        hoy = datetime.now()
        edad = hoy.year - fecha.year
        if (hoy.month, hoy.day) < (fecha.month, fecha.day):
            edad -= 1
        return f"La edad es {edad} años"
    except Exception as e:
        return f"Error: {e}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 11: AGENTE CON MEMORIA EN LANGCHAIN 1.0+\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [guardar_nota, obtener_fecha_actual, calcular_edad]
    
    # Crear el agente
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Eres un asistente útil que recuerda el contexto de la conversación. "
            "Puedes usar las tools disponibles para ayudar al usuario."
        ),
    )
    
    # Mantener el historial de mensajes manualmente para simular memoria
    # En producción, podrías usar un checkpointer o base de datos
    historial_mensajes = []
    
    print("=" * 60)
    print("INTERACCIÓN 1: Guardar información")
    print("=" * 60)
    
    pregunta1 = "Guarda una nota con título 'Reunión' y contenido 'Reunión mañana a las 10am'"
    print(f"\n🗣️ Pregunta: {pregunta1}\n")
    
    # Agregar el mensaje del usuario al historial
    historial_mensajes.append({"role": "user", "content": pregunta1})
    
    try:
        respuesta1 = agent.invoke({"messages": historial_mensajes})
        
        # Extraer la respuesta y agregarla al historial
        if "messages" in respuesta1:
            # Agregar todos los mensajes nuevos al historial
            for msg in respuesta1["messages"]:
                if msg not in historial_mensajes:
                    historial_mensajes.append(msg)
            
            # Mostrar la última respuesta
            ultimo_mensaje = respuesta1["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta: {ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta: {ultimo_mensaje}\n")
        else:
            print(f"\n🏁 Respuesta: {respuesta1}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("INTERACCIÓN 2: Usar información previa")
    print("=" * 60)
    
    pregunta2 = "¿Qué nota guardé antes sobre la reunión?"
    print(f"\n🗣️ Pregunta: {pregunta2}\n")
    
    # Agregar el nuevo mensaje del usuario al historial
    historial_mensajes.append({"role": "user", "content": pregunta2})
    
    try:
        # El agente recuerda la conversación anterior porque pasamos todo el historial
        respuesta2 = agent.invoke({"messages": historial_mensajes})
        
        if "messages" in respuesta2:
            # Agregar todos los mensajes nuevos al historial
            for msg in respuesta2["messages"]:
                if msg not in historial_mensajes:
                    historial_mensajes.append(msg)
            
            ultimo_mensaje = respuesta2["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta: {ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta: {respuesta2}\n")
        else:
            print(f"\n🏁 Respuesta: {respuesta2}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("INTERACCIÓN 3: Contexto continuo")
    print("=" * 60)
    
    pregunta3 = "Calcula mi edad si nací el 15 de mayo de 1990"
    print(f"\n🗣️ Pregunta: {pregunta3}\n")
    
    # Agregar el nuevo mensaje del usuario al historial
    historial_mensajes.append({"role": "user", "content": pregunta3})
    
    try:
        respuesta3 = agent.invoke({"messages": historial_mensajes})
        
        if "messages" in respuesta3:
            # Agregar todos los mensajes nuevos al historial
            for msg in respuesta3["messages"]:
                if msg not in historial_mensajes:
                    historial_mensajes.append(msg)
            
            ultimo_mensaje = respuesta3["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta: {ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta: {respuesta3}\n")
        else:
            print(f"\n🏁 Respuesta: {respuesta3}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("MEMORIA DEL AGENTE")
    print("=" * 60)
    print(f"\n📝 Historial de mensajes ({len(historial_mensajes)} mensajes):")
    for i, msg in enumerate(historial_mensajes[-6:], 1):  # Mostrar últimos 6 mensajes
        if isinstance(msg, dict):
            role = msg.get("role", "unknown")
            content = msg.get("content", str(msg))[:100]
            print(f"   {i}. [{role}]: {content}...")
        else:
            print(f"   {i}. {str(msg)[:100]}...")
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   En LangChain 1.0+:")
    print("   - La memoria se maneja pasando el historial completo de mensajes")
    print("   - Cada invocación incluye todos los mensajes anteriores")
    print("   - El agente recuerda automáticamente el contexto")
    print("   - En producción, podrías usar un checkpointer o base de datos")
    print("   - Este enfoque manual funciona bien para demostraciones")
    print("=" * 60)


if __name__ == "__main__":
    main()
