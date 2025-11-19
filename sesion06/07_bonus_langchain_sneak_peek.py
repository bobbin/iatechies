"""
Ejercicio 07 — Bonus: Cómo encaja esto con LangChain (mini sneak peek).

Para conectar luego con la parte de LangChain, este ejercicio muestra
la misma idea de tool, pero usando el decorador @tool y un agente.
"""

from __future__ import annotations

import os
from pathlib import Path

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


@tool
def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return a + b


def main() -> None:
    print("🟦 EJERCICIO 7: BONUS - LANGCHAIN SNEAK PEEK\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    print("=" * 60)
    print("LANGCHAIN SIMPLIFICA EL TRABAJO")
    print("=" * 60)
    print("\n📋 Tool definida con decorador @tool:")
    print(f"   {sumar.name}: {sumar.description}")
    print(f"   Schema: {sumar.args}\n")
    
    # LangChain se ocupa de:
    # - La definición JSON de la tool
    # - Leer la docstring como descripción
    # - Hacer el ciclo ReAct por ti
    
    template = """Eres un asistente útil. Responde las preguntas del usuario.

Tienes acceso a estas tools:
{tools}

Usa el siguiente formato:
Question: {input}
Thought: {agent_scratchpad}
Action: [nombre de la tool]
Action Input: [parámetros]
Observation: [resultado]
... (repetir si es necesario)
Thought: Tengo la respuesta final
Final Answer: [tu respuesta]

Begin!

Question: {input}
Thought:"""
    
    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, [sumar], prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=[sumar],
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,
    )
    
    pregunta = "Por favor, suma 12.5 y 3.7."
    print(f"👤 Usuario: {pregunta}\n")
    
    try:
        respuesta = agent_executor.invoke({"input": pregunta})
        print("\n" + "=" * 60)
        print("RESPUESTA DEL AGENTE")
        print("=" * 60)
        print(f"\n{respuesta['output']}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
    
    print("=" * 60)
    print("💡 VENTAJAS DE LANGCHAIN:")
    print("=" * 60)
    print("   ✅ Se ocupa de la definición JSON de la tool")
    print("   ✅ Lee la docstring como descripción automáticamente")
    print("   ✅ Hace el ciclo ReAct por ti")
    print("   ✅ Maneja el bucle modelo → tool → modelo")
    print("   ✅ Gestiona errores y reintentos")
    print("\n   Esto es solo un sneak peek. Verás más en los ejercicios siguientes.")
    print("=" * 60)


if __name__ == "__main__":
    main()

