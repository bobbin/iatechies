"""
Ejemplo 7: Agentes con Memoria Evolutiva (Memory Vector + Episodios)
=====================================================================

Complejidad: ALTA

Concepto:
---------
El agente almacena experiencias previas (problema→solución) y las usa
para mejorar decisiones futuras.

Diferencias con RAG tradicional:
- RAG: Memoria de documentos externos
- Memoria evolutiva: Memoria de experiencias del propio agente

El sistema aprende de casos pasados, no solo del input actual.

Patrón: Problema → Buscar experiencias similares → Aplicar aprendizaje → 
        Guardar nueva experiencia
"""

import os
import json
import sys
import io
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Configurar encoding UTF-8 para consola en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# SISTEMA DE MEMORIA EVOLUTIVA
# ==============================================================================

class MemoriaEvolutiva:
    """
    Almacena experiencias del agente y permite buscar casos similares.
    
    Cada experiencia contiene:
    - problema: Descripción del problema enfrentado
    - solucion: Solución aplicada
    - resultado: ¿Funcionó? (éxito/fallo)
    - aprendizaje: Qué se aprendió
    - timestamp: Cuándo ocurrió
    """
    
    def __init__(self, archivo_memoria: str = "memoria_agente.json"):
        self.archivo_memoria = archivo_memoria
        self.experiencias: List[Dict] = []
        self.cargar_memoria()
    
    def cargar_memoria(self):
        """Carga experiencias desde archivo."""
        if os.path.exists(self.archivo_memoria):
            try:
                with open(self.archivo_memoria, 'r', encoding='utf-8') as f:
                    self.experiencias = json.load(f)
                print(f"📚 Memoria cargada: {len(self.experiencias)} experiencias")
            except json.JSONDecodeError:
                print("⚠️ Error al leer memoria (JSON corrupto). Iniciando memoria vacía.")
                self.experiencias = []
        else:
            print("📚 Memoria nueva creada (no se encontró archivo previo)")
    
    def guardar_memoria(self):
        """Persiste experiencias a archivo."""
        with open(self.archivo_memoria, 'w', encoding='utf-8') as f:
            json.dump(self.experiencias, f, indent=2, ensure_ascii=False)
        print(f"💾 Memoria guardada: {len(self.experiencias)} experiencias")
    
    def agregar_experiencia(
        self,
        problema: str,
        solucion: str,
        resultado: str,
        aprendizaje: str
    ):
        """Agrega una nueva experiencia a la memoria."""
        experiencia = {
            "id": len(self.experiencias) + 1,
            "problema": problema,
            "solucion": solucion,
            "resultado": resultado,
            "aprendizaje": aprendizaje,
            "timestamp": datetime.now().isoformat()
        }
        self.experiencias.append(experiencia)
        self.guardar_memoria()
        print(f"✅ Nueva experiencia guardada (ID: {experiencia['id']})")
    
    def buscar_experiencias_similares(
        self,
        problema_actual: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Busca experiencias similares al problema actual.
        
        En producción, usarías embeddings y búsqueda vectorial.
        Aquí usamos búsqueda por palabras clave (simplificado).
        """
        if not self.experiencias:
            return []
        
        # Simplificación: buscar por palabras clave comunes
        problema_actual_lower = problema_actual.lower()
        palabras_clave = set(problema_actual_lower.split())
        
        # Calcular "similitud" simple
        experiencias_con_score = []
        for exp in self.experiencias:
            problema_exp_lower = exp["problema"].lower()
            palabras_exp = set(problema_exp_lower.split())
            
            # Intersección de palabras
            coincidencias = palabras_clave & palabras_exp
            score = len(coincidencias)
            
            if score > 0:
                experiencias_con_score.append((score, exp))
        
        # Ordenar por score y retornar top_k
        experiencias_con_score.sort(reverse=True, key=lambda x: x[0])
        experiencias_relevantes = [exp for _, exp in experiencias_con_score[:top_k]]
        
        print(f"🔍 Encontradas {len(experiencias_relevantes)} experiencias similares")
        return experiencias_relevantes
    
    def obtener_resumen_memoria(self) -> str:
        """Genera un resumen de la memoria."""
        if not self.experiencias:
            return "Memoria vacía"
        
        exitosas = sum(1 for e in self.experiencias if e["resultado"] == "éxito")
        fallidas = len(self.experiencias) - exitosas
        
        return f"""
        📊 Resumen de Memoria:
        - Total experiencias: {len(self.experiencias)}
        - Exitosas: {exitosas}
        - Fallidas: {fallidas}
        - Tasa de éxito: {exitosas/len(self.experiencias)*100:.1f}%
        """


# ==============================================================================
# AGENTE CON MEMORIA
# ==============================================================================

solucionador = Agent(
    role="Solucionador de Problemas",
    goal="Resolver problemas usando experiencias pasadas cuando sea posible",
    backstory="""Eres un agente que aprende de la experiencia. Antes de 
    abordar un problema, consultas tu memoria para ver si ya resolviste 
    algo similar. Si existe experiencia previa, la usas como guía. 
    Si no, creas una solución nueva. SIEMPRE guardas lo que aprendes.""",
    verbose=True,
    allow_delegation=False
)

evaluador = Agent(
    role="Evaluador de Soluciones",
    goal="Evaluar si las soluciones propuestas son correctas y efectivas",
    backstory="""Eres un evaluador crítico. Analizas soluciones y determinas 
    si son correctas, efectivas y bien fundamentadas. Das feedback claro.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA CON MEMORIA EVOLUTIVA
# ==============================================================================

def resolver_con_memoria(problema: str, memoria: MemoriaEvolutiva):
    """
    Resuelve un problema usando memoria evolutiva.
    
    Flujo:
    1. Buscar experiencias similares en memoria
    2. Si hay experiencias, usarlas como contexto
    3. Generar solución (informada por experiencias)
    4. Evaluar solución
    5. Guardar nueva experiencia
    """
    
    print("\n" + "="*70)
    print("🧠 RESOLUCIÓN CON MEMORIA EVOLUTIVA")
    print("="*70)
    print(f"❓ Problema: {problema}\n")
    
    # ==== PASO 1: BUSCAR EXPERIENCIAS SIMILARES ====
    print("📚 PASO 1: Buscando en memoria de experiencias...")
    experiencias_similares = memoria.buscar_experiencias_similares(problema)
    
    contexto_memoria = ""
    if experiencias_similares:
        print(f"\n✅ Encontradas {len(experiencias_similares)} experiencias relevantes:\n")
        for i, exp in enumerate(experiencias_similares, 1):
            print(f"   Experiencia {i}:")
            print(f"   - Problema: {exp['problema']}")
            print(f"   - Solución: {exp['solucion'][:80]}...")
            print(f"   - Resultado: {exp['resultado']}")
            print(f"   - Aprendizaje: {exp['aprendizaje'][:80]}...")
            print()
        
        # Construir contexto de memoria
        contexto_memoria = "\n\n".join([
            f"Experiencia previa {i}:\n"
            f"Problema: {exp['problema']}\n"
            f"Solución aplicada: {exp['solucion']}\n"
            f"Resultado: {exp['resultado']}\n"
            f"Aprendizaje: {exp['aprendizaje']}"
            for i, exp in enumerate(experiencias_similares, 1)
        ])
    else:
        print("ℹ️ No hay experiencias previas similares. Generando solución desde cero.\n")
    
    # ==== PASO 2: GENERAR SOLUCIÓN (CON CONTEXTO DE MEMORIA) ====
    print("💡 PASO 2: Generando solución...")
    
    prompt_solucion = f"""
    Problema a resolver:
    {problema}
    
    {f"Tu memoria de experiencias similares:{chr(10)}{contexto_memoria}{chr(10)}" if contexto_memoria else "No hay experiencias previas similares."}
    
    Tu tarea:
    1. Si hay experiencias previas, úsalas como guía (aprende de éxitos y fallos)
    2. Genera una solución clara y específica
    3. Explica tu razonamiento
    
    Proporciona tu solución en 3-4 oraciones.
    """
    
    tarea_solucion = Task(
        description=prompt_solucion,
        agent=solucionador,
        expected_output="Solución propuesta en 3-4 oraciones"
    )
    
    crew_solucion = Crew(
        agents=[solucionador],
        tasks=[tarea_solucion],
        process=Process.sequential,
        verbose=1
    )
    
    solucion = crew_solucion.kickoff()
    print(f"\n📄 Solución propuesta:\n{solucion}\n")
    
    # ==== PASO 3: EVALUAR SOLUCIÓN ====
    print("⚖️ PASO 3: Evaluando solución...")
    
    tarea_evaluacion = Task(
        description=f"""
        Evalúa la siguiente solución:
        
        Problema: {problema}
        Solución propuesta: {solucion}
        
        Determina:
        1. ¿Es correcta?
        2. ¿Es práctica y aplicable?
        3. ¿Qué tan efectiva es?
        
        Responde con:
        - RESULTADO: éxito o fallo
        - APRENDIZAJE: Una lección clave (1-2 oraciones)
        """,
        agent=evaluador,
        expected_output="RESULTADO y APRENDIZAJE"
    )
    
    crew_evaluacion = Crew(
        agents=[evaluador],
        tasks=[tarea_evaluacion],
        process=Process.sequential,
        verbose=1
    )
    
    evaluacion = crew_evaluacion.kickoff()
    evaluacion_str = str(evaluacion)
    
    # Parsear resultado
    resultado = "éxito" if "éxito" in evaluacion_str.lower() else "fallo"
    aprendizaje = evaluacion_str  # En producción, parsearías mejor
    
    print(f"\n📊 Evaluación: {resultado}")
    
    # ==== PASO 4: GUARDAR EXPERIENCIA ====
    print("\n💾 PASO 4: Guardando experiencia en memoria...")
    
    memoria.agregar_experiencia(
        problema=problema,
        solucion=str(solucion),
        resultado=resultado,
        aprendizaje=aprendizaje
    )
    
    print("\n" + "="*70)
    print("✅ PROCESO COMPLETADO")
    print("="*70)
    print(memoria.obtener_resumen_memoria())
    print("="*70 + "\n")
    
    return {
        "problema": problema,
        "experiencias_usadas": len(experiencias_similares),
        "solucion": str(solucion),
        "resultado": resultado,
        "aprendizaje": aprendizaje
    }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    # Inicializar memoria con ruta absoluta basada en la ubicación del script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_memoria = os.path.join(base_dir, "memoria_agente.json")
    
    memoria = MemoriaEvolutiva(ruta_memoria)
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Agente con Memoria Evolutiva")
    print("="*70)
    
    # PROBLEMA 1: Primera vez (sin memoria previa)
    print("\n\n🔬 CASO 1: Problema nuevo (sin experiencia previa)")
    print("-" * 70)
    problema1 = "Cómo implementar un sistema de cache para mejorar performance de una API"
    resolver_con_memoria(problema1, memoria)
    
    # PROBLEMA 2: Relacionado (debería usar memoria del problema 1)
    print("\n\n🔬 CASO 2: Problema similar (debería usar experiencia previa)")
    print("-" * 70)
    problema2 = "Qué estrategia de cache usar para reducir latencia en una API REST"
    resolver_con_memoria(problema2, memoria)
    
    # PROBLEMA 3: Diferente
    # print("\n\n🔬 CASO 3: Problema diferente")
    # print("-" * 70)
    # problema3 = "Cómo diseñar un sistema de autenticación seguro con JWT"
    # resolver_con_memoria(problema3, memoria)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ El agente aprende de experiencias pasadas")
    print("✅ La memoria persiste entre ejecuciones")
    print("✅ Soluciones futuras mejoran con el tiempo")
    print("✅ Diferente a RAG: memoria del agente, no docs externos")
    print("="*70 + "\n")


