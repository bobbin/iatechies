"""
Ejercicio 07 — Implementación manual del patrón ReAct.

Demuestra el ciclo ReAct (Reasoning + Acting) sin usar frameworks,
para entender cómo funciona internamente.
"""

from __future__ import annotations

import json
from typing import Callable, Dict, List, Optional

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
import os


# Tools simples
@tool
def sumar(a: float, b: float) -> str:
    """Suma dos números."""
    return f"Resultado: {a + b}"


@tool
def multiplicar(a: float, b: float) -> str:
    """Multiplica dos números."""
    return f"Resultado: {a * b}"


@tool
def obtener_factorial(n: int) -> str:
    """Calcula el factorial de un número entero."""
    if n < 0:
        return "Error: El factorial no está definido para números negativos"
    if n == 0:
        return "Resultado: 1"
    
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return f"Resultado: {resultado}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


class AgenteReActManual:
    """
    Implementación manual del patrón ReAct.
    Ciclo: Pensar → Decidir → Actuar → Observar → Repetir
    """
    
    def __init__(self, llm: ChatOpenAI, tools: List, max_iteraciones: int = 5):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.max_iteraciones = max_iteraciones
        self.historial: List[str] = []
    
    def _crear_prompt(self, pregunta: str) -> str:
        """Crea el prompt con el formato ReAct."""
        tools_desc = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        historial_str = "\n".join(self.historial) if self.historial else "Ninguna acción previa."
        
        return f"""Eres un agente que resuelve problemas paso a paso.

Tienes acceso a estas tools:
{tools_desc}

Formato de respuesta (usa EXACTAMENTE este formato):
Thought: [tu razonamiento]
Action: [nombre de la tool]
Action Input: [parámetros en JSON]
Observation: [resultado de la acción]

Historial previo:
{historial_str}

Pregunta: {pregunta}

Responde siguiendo el formato Thought/Action/Action Input/Observation.
Si ya tienes la respuesta final, escribe:
Thought: Tengo la respuesta final
Final Answer: [tu respuesta]"""
    
    def ejecutar(self, pregunta: str) -> str:
        """Ejecuta el ciclo ReAct."""
        print(f"\n🤔 Pregunta: {pregunta}\n")
        print("=" * 60)
        
        for iteracion in range(self.max_iteraciones):
            print(f"\n--- Iteración {iteracion + 1} ---\n")
            
            # 1. PENSAR: Generar respuesta del LLM
            prompt = self._crear_prompt(pregunta)
            respuesta = self.llm.invoke(prompt)
            texto = respuesta.content
            
            print(f"Thought/Action del modelo:\n{texto}\n")
            
            # 2. DECIDIR: Parsear la respuesta
            if "Final Answer:" in texto:
                # Extraer respuesta final
                final_answer = texto.split("Final Answer:")[-1].strip()
                print(f"✅ Respuesta final: {final_answer}")
                return final_answer
            
            # 3. ACTUAR: Extraer acción y ejecutarla
            if "Action:" in texto and "Action Input:" in texto:
                try:
                    # Extraer nombre de la tool
                    action_line = [l for l in texto.split("\n") if "Action:" in l][0]
                    action_name = action_line.split("Action:")[-1].strip()
                    
                    # Extraer parámetros
                    input_line = [l for l in texto.split("\n") if "Action Input:" in l][0]
                    input_json = input_line.split("Action Input:")[-1].strip()
                    params = json.loads(input_json)
                    
                    print(f"🔧 Ejecutando: {action_name}({params})")
                    
                    # Ejecutar tool
                    if action_name in self.tools:
                        resultado = self.tools[action_name].invoke(params)
                        print(f"📊 Observación: {resultado}")
                        
                        # 4. OBSERVAR: Guardar en historial
                        self.historial.append(
                            f"Action: {action_name}\n"
                            f"Action Input: {input_json}\n"
                            f"Observation: {resultado}"
                        )
                    else:
                        error = f"Tool '{action_name}' no encontrada"
                        print(f"❌ {error}")
                        self.historial.append(f"Error: {error}")
                except Exception as e:
                    error = f"Error parseando o ejecutando: {e}"
                    print(f"❌ {error}")
                    self.historial.append(f"Error: {error}")
            else:
                print("⚠️  No se pudo parsear la respuesta del modelo")
                break
        
        return "Error: Se alcanzó el máximo de iteraciones sin respuesta final"


def main() -> None:
    print("🟦 EJERCICIO 7: PATRÓN REACT MANUAL\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [sumar, multiplicar, obtener_factorial]
    
    agente = AgenteReActManual(llm, tools, max_iteraciones=5)
    
    # Ejemplo 1: Cálculo simple
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Cálculo simple")
    print("=" * 60)
    resultado1 = agente.ejecutar("¿Cuánto es 15 + 27?")
    
    # Resetear historial para el siguiente ejemplo
    agente.historial = []
    
    # Ejemplo 2: Cálculo más complejo
    print("\n\n" + "=" * 60)
    print("EJEMPLO 2: Cálculo más complejo")
    print("=" * 60)
    resultado2 = agente.ejecutar("Calcula el factorial de 5 y luego multiplícalo por 10")
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Este es el ciclo ReAct básico que LangChain y CrewAI")
    print("   implementan internamente. El modelo:")
    print("   1. Piensa (Thought)")
    print("   2. Decide qué tool usar (Action)")
    print("   3. Ejecuta la tool (Acting)")
    print("   4. Observa el resultado (Observation)")
    print("   5. Repite hasta tener la respuesta final")
    print("=" * 60)


if __name__ == "__main__":
    main()

