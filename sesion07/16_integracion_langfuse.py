"""
Ejemplo 16: Integración con Langfuse para Observabilidad
========================================================

Este ejercicio demuestra cómo integrar CrewAI con Langfuse para obtener
trazas detalladas de la ejecución de agentes, incluyendo:
- Trazas completas de conversaciones
- Métricas de uso de tokens
- Comparación entre modelos (GPT-4.1 vs GPT-4.1-mini)
- Monitoreo de costes
- Análisis de rendimiento

Modelos Usados:
--------------
- GPT-4.1: Modelo principal, más potente ($2.50/$10.00 por 1M tokens)
- GPT-4.1-mini: Versión económica y rápida ($0.15/$0.60 por 1M tokens)

Requisitos:
-----------
1. Cuenta en Langfuse Cloud (https://cloud.langfuse.com)
2. API Keys de Langfuse (Public Key, Secret Key)
3. pip install langfuse
4. Configurar modelos en Langfuse: Settings → Model Definitions
"""

import os
import sys
import io
from dotenv import load_dotenv
from langfuse import Langfuse, observe
from crewai import Agent, Task, Crew, Process, LLM

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

# ==============================================================================
# CONFIGURACIÓN DE LANGFUSE
# ==============================================================================

def inicializar_langfuse():
    """
    Inicializa la conexión con Langfuse Cloud.
    
    Necesitas configurar en tu .env:
    - LANGFUSE_PUBLIC_KEY=pk-lf-...
    - LANGFUSE_SECRET_KEY=sk-lf-...
    - LANGFUSE_HOST=https://cloud.langfuse.com (opcional, es el default)
    """
    public_key = os.getenv('LANGFUSE_PUBLIC_KEY')
    secret_key = os.getenv('LANGFUSE_SECRET_KEY')
    host = os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')
    
    if not public_key or not secret_key:
        print("\n" + "="*70)
        print("❌ ERROR: Credenciales de Langfuse no configuradas")
        print("="*70)
        print("\nPara usar este ejercicio necesitas:")
        print("\n1. Crear cuenta en https://cloud.langfuse.com")
        print("2. Obtener tus API keys en Settings > API Keys")
        print("3. Agregar a tu .env:")
        print("\n   LANGFUSE_PUBLIC_KEY=pk-lf-...")
        print("   LANGFUSE_SECRET_KEY=sk-lf-...")
        print("   LANGFUSE_HOST=https://cloud.langfuse.com")
        print("\n" + "="*70)
        sys.exit(1)
    
    # Cliente de Langfuse
    langfuse = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host
    )
    
    print("✅ Langfuse inicializado correctamente")
    print(f"   Host: {host}\n")
    
    return langfuse

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def crear_agente(role: str, model: str, temperature: float):
    """
    Crea un agente con configuración específica.
    """
    llm = LLM(
        model=model,
        temperature=temperature
    )
    
    backstories = {
        "Investigador": """Eres un investigador meticuloso con experiencia en análisis de información.
        Tu especialidad es encontrar datos relevantes y verificar fuentes.
        Siempre proporcionas información precisa y bien fundamentada.""",
        
        "Analista": """Eres un analista experto en identificar patrones y tendencias.
        Tu habilidad es sintetizar grandes cantidades de información en insights accionables.
        Eres conocido por tu claridad y profundidad de análisis.""",
        
        "Escritor": """Eres un escritor profesional que transforma información técnica en contenido accesible.
        Tu estilo es claro, conciso y atractivo.
        Sabes adaptar el tono según la audiencia."""
    }
    
    goals = {
        "Investigador": "Investigar y recopilar información precisa y verificada",
        "Analista": "Analizar información y extraer insights significativos",
        "Escritor": "Crear contenido claro y bien estructurado"
    }
    
    agent = Agent(
        role=role,
        goal=goals.get(role, "Completar la tarea asignada"),
        backstory=backstories.get(role, "Eres un agente especializado."),
        verbose=False,
        allow_delegation=False,
        llm=llm
    )
    
    return agent

def crear_tarea(descripcion: str, agente: Agent, nombre: str):
    """
    Crea una tarea para un agente.
    """
    return Task(
        description=descripcion,
        agent=agente,
        expected_output=f"Resultado de: {nombre}"
    )

# ==============================================================================
# EXPERIMENTO 1: COMPARACIÓN DE MODELOS
# ==============================================================================

@observe(name="Experimento 1: Comparación de Modelos")
def experimento_comparacion_modelos(langfuse):
    """
    Compara gpt-4.1 vs gpt-4.1-mini en la misma tarea.
    
    Observa en Langfuse:
    - Diferencia de tokens consumidos
    - Diferencia de latencia
    - Diferencia de coste
    - Calidad de las respuestas
    """
    print("\n" + "="*70)
    print("🔬 EXPERIMENTO 1: COMPARACIÓN DE MODELOS")
    print("="*70)
    
    tema = "inteligencia artificial en medicina"
    
    # Experimento 1: gpt-4.1 (más potente, más caro)
    print("\n📊 Test 1: gpt-4.1")
    generation_gpt4 = langfuse.start_generation(
        name="Test gpt-4.1",
        model="gpt-4.1",
        model_parameters={"temperature": 0.3},
        input=f"Investiga sobre {tema}. Proporciona 3 hallazgos clave con fuentes."
    )
    
    agente_gpt4 = crear_agente("Investigador", "gpt-4.1", 0.3)
    tarea_gpt4 = crear_tarea(
        f"Investiga sobre {tema}. Proporciona 3 hallazgos clave con fuentes.",
        agente_gpt4,
        "Investigación gpt-4.1"
    )
    
    crew_gpt4 = Crew(
        agents=[agente_gpt4],
        tasks=[tarea_gpt4],
        process=Process.sequential,
        verbose=False
    )
    
    resultado_gpt4 = crew_gpt4.kickoff()
    
    # Obtener el uso de tokens de CrewAI si está disponible
    usage_metadata = getattr(crew_gpt4, 'usage_metrics', None)
    if usage_metadata and hasattr(usage_metadata, 'total_tokens'):
        generation_gpt4.update(
            output=str(resultado_gpt4),
            usage={
                "input": getattr(usage_metadata, 'prompt_tokens', 0),
                "output": getattr(usage_metadata, 'completion_tokens', 0),
                "total": getattr(usage_metadata, 'total_tokens', 0)
            }
        )
    else:
        generation_gpt4.update(output=str(resultado_gpt4))
    
    generation_gpt4.end()
    print(f"\n✅ gpt-4.1 completado: {len(str(resultado_gpt4))} caracteres")
    
    # Experimento 2: gpt-4.1-mini (más rápido, más económico)
    print("\n📊 Test 2: gpt-4.1-mini")
    generation_mini = langfuse.start_generation(
        name="Test gpt-4.1-mini",
        model="gpt-4.1-mini",
        model_parameters={"temperature": 0.3},
        input=f"Investiga sobre {tema}. Proporciona 3 hallazgos clave con fuentes."
    )
    
    agente_mini = crear_agente("Investigador", "gpt-4.1-mini", 0.3)
    tarea_mini = crear_tarea(
        f"Investiga sobre {tema}. Proporciona 3 hallazgos clave con fuentes.",
        agente_mini,
        "Investigación gpt-4.1-mini"
    )
    
    crew_mini = Crew(
        agents=[agente_mini],
        tasks=[tarea_mini],
        process=Process.sequential,
        verbose=False
    )
    
    resultado_mini = crew_mini.kickoff()
    
    # Obtener el uso de tokens si está disponible
    usage_metadata = getattr(crew_mini, 'usage_metrics', None)
    if usage_metadata and hasattr(usage_metadata, 'total_tokens'):
        generation_mini.update(
            output=str(resultado_mini),
            usage={
                "input": getattr(usage_metadata, 'prompt_tokens', 0),
                "output": getattr(usage_metadata, 'completion_tokens', 0),
                "total": getattr(usage_metadata, 'total_tokens', 0)
            }
        )
    else:
        generation_mini.update(output=str(resultado_mini))
    
    generation_mini.end()
    print(f"\n✅ gpt-4.1-mini completado: {len(str(resultado_mini))} caracteres")
    
    print("\n💡 Ve a Langfuse para comparar tokens, latencia y costes")
    print("\n📝 NOTA: Si no ves costes en Langfuse, asegúrate de que los modelos")
    print("   'gpt-4.1' y 'gpt-4.1-mini' estén configurados en:")
    print("   Langfuse Dashboard → Settings → Model Definitions")
    
    return {
        "gpt4o_length": len(str(resultado_gpt4)),
        "gpt4o_mini_length": len(str(resultado_mini))
    }

# ==============================================================================
# EXPERIMENTO 2: CREW MULTI-AGENTE
# ==============================================================================

@observe(name="Experimento 2: Crew Multi-Agente")
def experimento_crew_multiagente(langfuse):
    """
    Crea un workflow de 3 agentes secuenciales.
    
    Observa en Langfuse:
    - Flujo completo de información entre agentes
    - Tokens acumulados por cada paso
    - Tiempo de ejecución por agente
    - Costes totales del crew
    """
    print("\n" + "="*70)
    print("🤝 EXPERIMENTO 2: CREW MULTI-AGENTE")
    print("="*70)
    
    # Crear span principal
    span_crew = langfuse.start_span(
        name="Crew: IA en Educación",
        metadata={"num_agentes": 3, "proceso": "sequential"}
    )
    
    # Agente 1: Investigador (gpt-4.1)
    investigador = crear_agente("Investigador", "gpt-4.1", 0.3)
    
    # Agente 2: Analista (gpt-4.1)
    analista = crear_agente("Analista", "gpt-4.1", 0.5)
    
    # Agente 3: Escritor (gpt-4.1-mini - más económico para redacción)
    escritor = crear_agente("Escritor", "gpt-4.1-mini", 0.7)
    
    # Tareas
    tarea_investigacion = crear_tarea(
        """Investiga sobre el impacto de la IA en la educación.
        Enfócate en: personalización del aprendizaje, accesibilidad y desafíos éticos.
        Proporciona datos concretos y ejemplos reales.""",
        investigador,
        "Investigación"
    )
    
    tarea_analisis = crear_tarea(
        """Analiza la información investigada e identifica:
        1. Las 3 tendencias más prometedoras
        2. Los 2 principales riesgos
        3. Recomendaciones para educadores
        
        Usa el contexto de la investigación previa.""",
        analista,
        "Análisis"
    )
    
    tarea_redaccion = crear_tarea(
        """Redacta un artículo divulgativo de 300 palabras sobre IA en educación.
        Usa un tono accesible pero informado.
        Estructura: Introducción, Desarrollo (tendencias + riesgos), Conclusión.
        
        Basa tu artículo en el análisis previo.""",
        escritor,
        "Redacción"
    )
    
    # Crear crew
    crew = Crew(
        agents=[investigador, analista, escritor],
        tasks=[tarea_investigacion, tarea_analisis, tarea_redaccion],
        process=Process.sequential,
        verbose=True
    )
    
    # Ejecutar
    print("\n🚀 Iniciando crew multi-agente...")
    resultado = crew.kickoff()
    
    # Actualizar span
    span_crew.update(output=str(resultado))
    span_crew.end()
    
    print("\n✅ Crew completado")
    print(f"\n📄 Artículo final ({len(str(resultado))} caracteres):")
    print("-" * 70)
    print(resultado)
    print("-" * 70)
    
    print("\n💡 Ve a Langfuse para ver el flujo completo de 3 agentes")
    
    return {"length": len(str(resultado))}

# ==============================================================================
# EXPERIMENTO 3: EFECTO DE TEMPERATURA
# ==============================================================================

@observe(name="Experimento 3: Efecto de Temperatura")
def experimento_temperatura(langfuse):
    """
    Compara el mismo agente con diferentes temperaturas.
    
    Observa en Langfuse:
    - Variabilidad en las respuestas
    - Creatividad vs consistencia
    - Diferencia de tokens (a veces la temperatura alta genera más texto)
    """
    print("\n" + "="*70)
    print("🌡️  EXPERIMENTO 3: EFECTO DE TEMPERATURA")
    print("="*70)
    
    prompt = "Escribe un eslogan creativo para una startup de IA en salud"
    
    # Temperatura baja (más determinista)
    print("\n🌡️  Test 1: Temperatura 0.1 (Determinista)")
    span_frio = langfuse.start_span(
        name="Temperatura 0.1",
        metadata={"temperatura": 0.1, "modelo": "gpt-4.1"}
    )
    
    agente_frio = crear_agente("Escritor", "gpt-4.1", 0.1)
    tarea_frio = crear_tarea(prompt, agente_frio, "Eslogan Determinista")
    
    crew_frio = Crew(
        agents=[agente_frio],
        tasks=[tarea_frio],
        process=Process.sequential,
        verbose=False
    )
    
    resultado_frio = crew_frio.kickoff()
    span_frio.update(output=str(resultado_frio))
    span_frio.end()
    print(f"   Resultado: {resultado_frio}")
    
    # Temperatura alta (más creativo)
    print("\n🌡️  Test 2: Temperatura 0.9 (Creativo)")
    span_caliente = langfuse.start_span(
        name="Temperatura 0.9",
        metadata={"temperatura": 0.9, "modelo": "gpt-4.1"}
    )
    
    agente_caliente = crear_agente("Escritor", "gpt-4.1", 0.9)
    tarea_caliente = crear_tarea(prompt, agente_caliente, "Eslogan Creativo")
    
    crew_caliente = Crew(
        agents=[agente_caliente],
        tasks=[tarea_caliente],
        process=Process.sequential,
        verbose=False
    )
    
    resultado_caliente = crew_caliente.kickoff()
    span_caliente.update(output=str(resultado_caliente))
    span_caliente.end()
    print(f"   Resultado: {resultado_caliente}")
    
    print("\n💡 Ve a Langfuse para comparar la variabilidad y creatividad")
    
    return {
        "temperatura_baja": str(resultado_frio),
        "temperatura_alta": str(resultado_caliente)
    }

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """
    Ejecuta los 3 experimentos de observabilidad con Langfuse.
    """
    print("\n" + "="*70)
    print("🔍 INTEGRACIÓN CREWAI + LANGFUSE")
    print("="*70)
    print("\nEste script ejecuta 3 experimentos para demostrar observabilidad:")
    print("1. Comparación de modelos (gpt-4.1 vs gpt-4.1-mini)")
    print("2. Crew multi-agente (3 agentes secuenciales)")
    print("3. Efecto de temperatura (0.1 vs 0.9)")
    print("\nTodas las trazas se enviarán a Langfuse Cloud.")
    
    # Inicializar Langfuse
    langfuse = inicializar_langfuse()
    
    # Ejecutar experimentos
    experimento_comparacion_modelos(langfuse)
    experimento_crew_multiagente(langfuse)
    experimento_temperatura(langfuse)
    
    # Flush para asegurar que todas las trazas se envíen
    langfuse.flush()
    
    print("\n" + "="*70)
    print("✅ TODOS LOS EXPERIMENTOS COMPLETADOS")
    print("="*70)
    print("\n📊 Ahora ve a tu dashboard de Langfuse:")
    print(f"   {os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')}")
    print("\n💡 Busca las trazas por nombre de experimento")
    print("💡 Compara tokens, latencias y costes entre modelos")
    print("💡 Explora el flujo del crew multi-agente")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
