"""
Ejercicio 12 — Pipelines con Runnables en LangChain.

Demuestra cómo usar Runnables para crear pipelines
componibles sin necesidad de un agente completo.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent.parent / "sesion03" / ".env", override=False)


def extraer_tema(texto: str) -> str:
    """Extrae el tema principal de un texto."""
    palabras = texto.lower().split()
    # Simulación simple: contar palabras más frecuentes
    from collections import Counter
    comunes = Counter(palabras).most_common(3)
    temas = [palabra for palabra, _ in comunes if len(palabra) > 4]
    return temas[0] if temas else "general"


def formatear_respuesta(resultado: Dict) -> str:
    """Formatea la respuesta final."""
    return f"""
📝 Resumen:
{resultado['resumen']}

🎯 Tema principal: {resultado['tema']}

💬 Opinión del modelo:
{resultado['opinion']}
"""


def main() -> None:
    print("🟦 EJERCICIO 12: PIPELINES CON RUNNABLES EN LANGCHAIN\n")
    
    load_env()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: Configura OPENAI_API_KEY en el archivo .env")
        return
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    parser = StrOutputParser()
    
    # Pipeline 1: Resumen simple
    print("=" * 60)
    print("PIPELINE 1: Resumen de texto")
    print("=" * 60)
    
    prompt_resumen = ChatPromptTemplate.from_template(
        "Resume el siguiente texto en 2-3 frases:\n\n{texto}"
    )
    
    pipeline_resumen = prompt_resumen | llm | parser
    
    texto_ejemplo = """
    La inteligencia artificial está transformando la forma en que trabajamos.
    Los agentes de IA pueden automatizar tareas complejas que antes requerían
    intervención humana. Sin embargo, también plantean desafíos éticos y
    de privacidad que debemos abordar.
    """
    
    print(f"\n📄 Texto original:\n{texto_ejemplo}\n")
    resultado1 = pipeline_resumen.invoke({"texto": texto_ejemplo})
    print(f"📝 Resumen:\n{resultado1}\n")
    
    # Pipeline 2: Procesamiento en cadena
    print("=" * 60)
    print("PIPELINE 2: Procesamiento en cadena")
    print("=" * 60)
    
    prompt_tema = ChatPromptTemplate.from_template(
        "¿Cuál es el tema principal de este texto? Responde con una sola palabra:\n\n{texto}"
    )
    
    prompt_opinion = ChatPromptTemplate.from_template(
        "Da tu opinión breve sobre el tema '{tema}' en una frase."
    )
    
    # Pipeline compuesto: texto -> tema -> opinión
    pipeline_compuesto = (
        {"tema": prompt_tema | llm | parser}
        | prompt_opinion
        | llm
        | parser
    )
    
    tema_resultado = (prompt_tema | llm | parser).invoke({"texto": texto_ejemplo})
    print(f"\n🎯 Tema extraído: {tema_resultado}\n")
    
    opinion_resultado = pipeline_compuesto.invoke({"texto": texto_ejemplo})
    print(f"💬 Opinión: {opinion_resultado}\n")
    
    # Pipeline 3: Con funciones personalizadas
    print("=" * 60)
    print("PIPELINE 3: Con funciones personalizadas")
    print("=" * 60)
    
    prompt_resumen2 = ChatPromptTemplate.from_template(
        "Resume este texto:\n\n{texto}"
    )
    
    # Pipeline que combina LLM + función personalizada + otro LLM
    # Explicación: RunnablePassthrough() pasa los datos sin modificar
    # RunnableLambda permite ejecutar funciones Python personalizadas
    pipeline_complejo = (
        RunnableLambda(lambda x: {
            "resumen": (prompt_resumen2 | llm | parser).invoke({"texto": x["texto"]}),
            "texto_original": x["texto"],  # Extraer el texto del diccionario de entrada
        })
        | RunnableLambda(lambda x: {
            **x,
            "tema": extraer_tema(x["texto_original"]),
        })
        | RunnableLambda(lambda x: {
            "resumen": x["resumen"],
            "tema": x["tema"],
            "opinion": (prompt_opinion | llm | parser).invoke({"tema": x["tema"]}),
        })
    )
    
    resultado_completo = pipeline_complejo.invoke({"texto": texto_ejemplo})
    print(f"\n📊 Resultado completo:\n{resultado_completo}\n")
    
    # Formatear resultado final
    resultado_formateado = formatear_respuesta(resultado_completo)
    print("=" * 60)
    print("RESULTADO FORMATEADO")
    print("=" * 60)
    print(resultado_formateado)
    
    print("=" * 60)
    print("💡 ¿QUÉ SON LOS RUNNABLES?")
    print("=" * 60)
    print("""
   Los Runnables son componentes en LangChain que pueden ejecutarse y
   componerse entre sí usando el operador pipe (|).

   Tipos principales:
   - Prompts: Preparan el input para el LLM
   - LLMs: Modelos de lenguaje
   - Parsers: Procesan la salida del LLM
   - RunnableLambda: Funciones Python personalizadas
   - RunnablePassthrough: Pasa datos sin modificar

   Ventajas:
   ✅ Composición fácil con |
   ✅ Flujos deterministas y predecibles
   ✅ Eficientes (sin sobrecarga de agentes)
   ✅ Reutilizables en múltiples pipelines

   Cuándo usar Runnables:
   - Flujo determinista (siempre el mismo proceso)
   - No necesitas decisiones dinámicas
   - Procesamiento rápido y eficiente
   - Transformaciones secuenciales de datos

   Cuándo usar Agentes:
   - Necesitas decisiones dinámicas
   - El orden de acciones no está claro
   - El modelo debe decidir qué tool usar
   """)
    print("=" * 60)


if __name__ == "__main__":
    main()

