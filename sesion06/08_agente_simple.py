"""
Ejercicio 08 — Agente simple sin framework.

Crea un agente mínimo desde cero para entender los componentes
básicos: objetivo, razonamiento, tools y memoria opcional.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
import os


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


@tool
def buscar_en_diccionario(palabra: str) -> str:
    """Busca el significado de una palabra en un diccionario simple."""
    diccionario = {
        "agente": "Entidad que actúa en un entorno para lograr objetivos",
        "tool": "Función que un agente puede usar para realizar acciones",
        "llm": "Large Language Model - Modelo de lenguaje grande",
        "react": "Patrón Reasoning + Acting para agentes",
    }
    significado = diccionario.get(palabra.lower(), f"No se encontró '{palabra}' en el diccionario")
    return significado


@tool
def contar_caracteres(texto: str) -> str:
    """Cuenta el número de caracteres en un texto."""
    return f"El texto tiene {len(texto)} caracteres"


@tool
def convertir_a_mayusculas(texto: str) -> str:
    """Convierte un texto a mayúsculas."""
    return texto.upper()


class AgenteSimple:
    """
    Agente mínimo con los componentes básicos:
    - Objetivo
    - Razonamiento (LLM)
    - Tools
    - Memoria (opcional)
    """
    
    def __init__(
        self,
        llm: ChatOpenAI,
        tools: List,
        objetivo: str = "Ayudar al usuario a resolver problemas",
        memoria: Optional[List[str]] = None,
    ):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.objetivo = objetivo
        self.memoria = memoria or []
    
    def _crear_contexto(self) -> str:
        """Crea el contexto con objetivo, tools y memoria."""
        tools_info = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        
        memoria_str = "\n".join(self.memoria[-3:]) if self.memoria else "Sin historial previo"
        
        return f"""Eres un agente con el siguiente objetivo:
{self.objetivo}

Tienes acceso a estas tools:
{tools_info}

Historial reciente:
{memoria_str}

Responde de forma clara y útil. Si necesitas usar una tool, indícalo explícitamente."""
    
    def procesar(self, entrada: str) -> str:
        """Procesa una entrada del usuario."""
        contexto = self._crear_contexto()
        prompt = f"{contexto}\n\nUsuario: {entrada}\n\nAgente:"
        
        respuesta = self.llm.invoke(prompt)
        texto_respuesta = respuesta.content
        
        # Guardar en memoria
        self.memoria.append(f"Usuario: {entrada}\nAgente: {texto_respuesta}")
        
        # Limitar tamaño de memoria
        if len(self.memoria) > 10:
            self.memoria = self.memoria[-10:]
        
        return texto_respuesta
    
    def usar_tool(self, nombre_tool: str, parametros: Dict) -> str:
        """Ejecuta una tool específica."""
        if nombre_tool in self.tools:
            return self.tools[nombre_tool].invoke(parametros)
        return f"Error: Tool '{nombre_tool}' no encontrada"


def main() -> None:
    print("🟦 EJERCICIO 8: AGENTE SIMPLE SIN FRAMEWORK\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    tools = [buscar_en_diccionario, contar_caracteres, convertir_a_mayusculas]
    
    # Crear agente con objetivo específico
    agente = AgenteSimple(
        llm=llm,
        tools=tools,
        objetivo="Ayudar a entender conceptos de IA y procesar textos",
    )
    
    print("=" * 60)
    print("COMPONENTES DEL AGENTE")
    print("=" * 60)
    print(f"\n🎯 Objetivo: {agente.objetivo}")
    print(f"\n🔧 Tools disponibles:")
    for tool_func in tools:
        print(f"   - {tool_func.name}: {tool_func.description}")
    print(f"\n🧠 Memoria: {'Activa' if agente.memoria else 'Vacía'}")
    
    print("\n" + "=" * 60)
    print("INTERACCIÓN CON EL AGENTE")
    print("=" * 60)
    
    # Interacción 1
    print("\n1️⃣ Usuario: ¿Qué es un agente?")
    respuesta1 = agente.procesar("¿Qué es un agente?")
    print(f"   Agente: {respuesta1}")
    
    # Interacción 2 (con memoria)
    print("\n2️⃣ Usuario: ¿Y qué es una tool?")
    respuesta2 = agente.procesar("¿Y qué es una tool?")
    print(f"   Agente: {respuesta2}")
    
    # Interacción 3 (usando tool directamente)
    print("\n3️⃣ Usuario: Cuenta los caracteres de 'Hola mundo'")
    resultado_tool = agente.usar_tool("contar_caracteres", {"texto": "Hola mundo"})
    print(f"   Resultado de tool: {resultado_tool}")
    
    # Mostrar memoria
    print("\n" + "=" * 60)
    print("MEMORIA DEL AGENTE")
    print("=" * 60)
    print(f"\nÚltimas {len(agente.memoria)} interacciones guardadas:")
    for i, entrada in enumerate(agente.memoria[-3:], 1):
        print(f"\n{i}. {entrada[:100]}...")
    
    print("\n" + "=" * 60)
    print("💡 Observación:")
    print("   Este agente tiene los componentes básicos:")
    print("   - Objetivo: Define qué debe hacer")
    print("   - Razonamiento: El LLM que piensa")
    print("   - Tools: Acciones que puede ejecutar")
    print("   - Memoria: Recuerda interacciones previas")
    print("=" * 60)


if __name__ == "__main__":
    main()

