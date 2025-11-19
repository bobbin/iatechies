"""
Ejercicio 15 — Manejo de errores y límites en LangChain.

Demuestra cómo manejar errores comunes en tools y cómo
el agente puede explicar errores al usuario.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


@tool
def dividir_numeros(a: float, b: float) -> str:
    """
    Divide dos números. Maneja el error de división por cero.
    
    Args:
        a: Dividendo.
        b: Divisor.
    """
    if b == 0:
        return "Error: No se puede dividir por cero. Por favor, usa un divisor diferente."
    return f"Resultado: {a / b:.2f}"


@tool
def buscar_archivo(ruta: str) -> str:
    """
    Busca un archivo y devuelve su contenido si existe.
    
    Args:
        ruta: Ruta al archivo.
    """
    from pathlib import Path
    archivo = Path(ruta)
    if not archivo.exists():
        return f"Error: El archivo '{ruta}' no existe. Verifica la ruta."
    try:
        contenido = archivo.read_text(encoding="utf-8")
        return f"Contenido del archivo:\n{contenido[:200]}..."  # Limitar tamaño
    except Exception as e:
        return f"Error leyendo archivo: {e}"


@tool
def calcular_raiz_cuadrada(numero: float) -> str:
    """
    Calcula la raíz cuadrada de un número.
    
    Args:
        numero: Número positivo.
    """
    if numero < 0:
        return "Error: No se puede calcular la raíz cuadrada de un número negativo."
    import math
    resultado = math.sqrt(numero)
    return f"Raíz cuadrada de {numero}: {resultado:.2f}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def main() -> None:
    print("🟦 EJERCICIO 15: MANEJO DE ERRORES Y LÍMITES EN LANGCHAIN\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [dividir_numeros, buscar_archivo, calcular_raiz_cuadrada]
    
    # Crear el agente usando la nueva API de LangChain 1.0+
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=(
            "Eres un asistente útil. Si encuentras errores al usar las tools, "
            "intenta explicar el problema al usuario de forma clara y amigable. "
            "Las tools pueden devolver mensajes de error que debes interpretar y explicar."
        ),
    )
    
    print("=" * 60)
    print("EJEMPLO 1: Error manejado por la tool")
    print("=" * 60)
    
    pregunta1 = "Divide 10 entre 0"
    print(f"\n🗣️ Pregunta: {pregunta1}\n")
    
    try:
        respuesta1 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta1}]
        })
        
        if "messages" in respuesta1:
            ultimo_mensaje = respuesta1["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final:\n{ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final:\n{respuesta1}\n")
        else:
            print(f"\n🏁 Respuesta Final:\n{respuesta1}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Error de archivo no encontrado")
    print("=" * 60)
    
    pregunta2 = "Lee el archivo 'archivo_inexistente.txt'"
    print(f"\n🗣️ Pregunta: {pregunta2}\n")
    
    try:
        respuesta2 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta2}]
        })
        
        if "messages" in respuesta2:
            ultimo_mensaje = respuesta2["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final:\n{ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final:\n{respuesta2}\n")
        else:
            print(f"\n🏁 Respuesta Final:\n{respuesta2}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Error de validación")
    print("=" * 60)
    
    pregunta3 = "Calcula la raíz cuadrada de -5"
    print(f"\n🗣️ Pregunta: {pregunta3}\n")
    
    try:
        respuesta3 = agent.invoke({
            "messages": [{"role": "user", "content": pregunta3}]
        })
        
        if "messages" in respuesta3:
            ultimo_mensaje = respuesta3["messages"][-1]
            if hasattr(ultimo_mensaje, "content"):
                print(f"\n🏁 Respuesta Final:\n{ultimo_mensaje.content}\n")
            else:
                print(f"\n🏁 Respuesta Final:\n{respuesta3}\n")
        else:
            print(f"\n🏁 Respuesta Final:\n{respuesta3}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)
    print("CONFIGURACIONES DE SEGURIDAD")
    print("=" * 60)
    print("""
✅ Buenas prácticas implementadas:
   - Tools devuelven mensajes de error claros y estructurados
   - El agente puede interpretar y explicar errores al usuario
   - Validación en las tools previene errores peligrosos
   - Mensajes de error descriptivos ayudan al agente a entender qué salió mal

✅ En LangChain 1.0+:
   - create_agent maneja automáticamente el flujo de herramientas
   - Los errores de tools se pasan al agente para que los explique
   - No necesitas configurar max_iterations manualmente (el modelo decide)
   - El sistema de prompts ayuda al agente a manejar errores correctamente

⚠️ Errores típicos a evitar (slides B14):
   - Dar demasiadas tools (confunde al modelo)
   - Tools mal definidas (sin descripciones claras)
   - No testear las responses (errores en producción)
   - No controlar qué pasa si una API falla
   - Tools que no devuelven mensajes de error claros
""")
    print("=" * 60)


if __name__ == "__main__":
    main()
