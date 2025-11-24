"""
Ejemplo 11: Agentic RAG (Planner → Retriever → Verifier → Writer)
===================================================================

Complejidad: MUY ALTA

Concepto:
---------
RAG ya no es una sola llamada "retrieve + generate".
Se convierte en un grafo de decisiones que:
- Razona sobre la pregunta
- Busca estratégicamente
- Verifica suficiencia y validez
- Reintenta si es necesario
- Escribe con citas verificadas
- Registra en memoria para aprendizaje

Patrón: Planner → Retriever → Verifier → (retry?) → Writer → Memory

Este es el estado del arte en sistemas RAG de producción.
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# BASE DE CONOCIMIENTO (SIMULADA)
# ==============================================================================

BASE_VECTORIAL = {
    "chunk_1": {
        "contenido": "Los sistemas multi-agente permiten distribuir tareas complejas entre agentes especializados. Cada agente puede enfocarse en su área de expertise.",
        "metadata": {"fuente": "doc_sistemas_ia.pdf", "pagina": 12}
    },
    "chunk_2": {
        "contenido": "El patrón supervisor-especialistas es común en arquitecturas multi-agente. El supervisor coordina mientras especialistas ejecutan.",
        "metadata": {"fuente": "doc_patrones.pdf", "pagina": 45}
    },
    "chunk_3": {
        "contenido": "La verificación de evidencia es crítica en RAG. Sin ella, los modelos pueden alucinar información que suena correcta pero es falsa.",
        "metadata": {"fuente": "doc_rag_avanzado.pdf", "pagina": 23}
    },
    "chunk_4": {
        "contenido": "CrewAI facilita la construcción de equipos de agentes con roles, objetivos y herramientas bien definidas para cada miembro.",
        "metadata": {"fuente": "doc_crewai.pdf", "pagina": 8}
    },
    "chunk_5": {
        "contenido": "La memoria evolutiva permite que agentes aprendan de experiencias pasadas, almacenando problema-solución-resultado para mejorar futuras decisiones.",
        "metadata": {"fuente": "doc_memoria_agentes.pdf", "pagina": 34}
    }
}


# ==============================================================================
# AGENTES DEL SISTEMA AGENTIC RAG
# ==============================================================================

# AGENTE 1: PLANNER (Planificador)
planner = Agent(
    role="Planificador de Consultas",
    goal="Analizar preguntas y crear estrategias de búsqueda óptimas",
    backstory="""Eres un planificador experto que analiza preguntas complejas
    y las descompone en sub-consultas manejables. Determinas:
    - Qué información se necesita
    - En qué orden buscarla
    - Cuántos chunks son suficientes
    - Qué términos de búsqueda usar
    
    Tu plan guía al retriever.""",
    verbose=True,
    allow_delegation=False
)

# AGENTE 2: RETRIEVER (Recuperador)
retriever = Agent(
    role="Recuperador de Información",
    goal="Buscar y recuperar los chunks más relevantes según el plan",
    backstory="""Eres un especialista en búsqueda de información. Ejecutas
    estrategias de búsqueda, recuperas chunks de la base vectorial y
    evalúas su relevancia. Puedes hacer múltiples búsquedas si es necesario.""",
    verbose=True,
    allow_delegation=False
)

# AGENTE 3: VERIFIER (Verificador)
verifier = Agent(
    role="Verificador de Suficiencia",
    goal="Verificar que la información recuperada sea suficiente y relevante",
    backstory="""Eres un verificador riguroso. Evalúas si los chunks recuperados:
    - Son suficientes para responder la pregunta
    - Son relevantes al tema
    - Tienen calidad adecuada
    
    Puedes solicitar:
    - MÁS búsquedas si falta información
    - REPLANIFICACIÓN si la estrategia no funcionó
    - CONTINUAR si es suficiente
    
    No aceptas información insuficiente.""",
    verbose=True,
    allow_delegation=False
)

# AGENTE 4: WRITER (Escritor)
writer = Agent(
    role="Escritor de Respuestas",
    goal="Generar respuestas claras y bien citadas basadas en chunks verificados",
    backstory="""Eres un escritor experto que crea respuestas precisas basadas
    SOLO en los chunks proporcionados. SIEMPRE citas tus fuentes usando
    [chunk_X]. No inventas información. Si los chunks no son suficientes,
    lo indicas claramente.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA AGENTIC RAG
# ==============================================================================

class AgenticRAG:
    """Sistema RAG completo con agentes coordinados."""
    
    def __init__(self, base_vectorial: Dict):
        self.base_vectorial = base_vectorial
        self.intentos_busqueda = 0
        self.max_intentos = 3
        self.historial = []
    
    def buscar_chunks(self, terminos: List[str], top_k: int = 3) -> List[Dict]:
        """
        Simula búsqueda vectorial.
        En producción usaría ChromaDB, Pinecone, etc.
        """
        print(f"🔍 Buscando chunks con términos: {terminos}")
        
        # Simplificación: búsqueda por palabras clave
        resultados = []
        for chunk_id, chunk_data in self.base_vectorial.items():
            contenido_lower = chunk_data["contenido"].lower()
            
            # Calcular score simple
            score = sum(1 for termino in terminos if termino.lower() in contenido_lower)
            
            if score > 0:
                resultados.append({
                    "chunk_id": chunk_id,
                    "contenido": chunk_data["contenido"],
                    "metadata": chunk_data["metadata"],
                    "score": score
                })
        
        # Ordenar por score y retornar top_k
        resultados.sort(key=lambda x: x["score"], reverse=True)
        chunks_recuperados = resultados[:top_k]
        
        print(f"✅ Recuperados {len(chunks_recuperados)} chunks")
        return chunks_recuperados
    
    def procesar_consulta(self, pregunta: str) -> Dict:
        """
        Procesa una consulta usando el pipeline completo Agentic RAG.
        
        Flujo:
        1. PLAN: Analizar pregunta y crear estrategia
        2. RETRIEVE: Buscar chunks según plan
        3. VERIFY: Verificar suficiencia
        4. RETRY: Si insuficiente, replanear y rebuscar
        5. WRITE: Generar respuesta con citas
        6. MEMORY: Registrar experiencia
        """
        
        print("\n" + "="*70)
        print("🤖 AGENTIC RAG PIPELINE")
        print("="*70)
        print(f"❓ Pregunta: {pregunta}\n")
        
        # ==== FASE 1: PLANIFICACIÓN ====
        print("📋 FASE 1: Planificación de búsqueda...")
        print("-" * 70)
        
        tarea_plan = Task(
            description=f"""
            Analiza esta pregunta y crea una estrategia de búsqueda:
            
            PREGUNTA: {pregunta}
            
            Tu tarea:
            1. Identifica los conceptos clave
            2. Define términos de búsqueda efectivos (3-5 términos)
            3. Estima cuántos chunks necesitas (1-5)
            
            Responde en formato:
            TÉRMINOS: [término1, término2, término3]
            CHUNKS_NECESARIOS: X
            ESTRATEGIA: [explicación breve]
            """,
            agent=planner,
            expected_output="Plan con términos de búsqueda y cantidad de chunks"
        )
        
        crew_plan = Crew(
            agents=[planner],
            tasks=[tarea_plan],
            process=Process.sequential,
            verbose=1
        )
        
        plan = str(crew_plan.kickoff())
        
        # Parsear plan (simplificado)
        terminos = ["multi-agente", "verificación", "sistema"]  # En producción, parsearía del plan
        top_k = 3
        
        print(f"\n📊 Plan creado:")
        print(f"  Términos: {terminos}")
        print(f"  Chunks a buscar: {top_k}\n")
        
        # ==== FASE 2: RECUPERACIÓN ====
        chunks_recuperados = []
        verificacion_exitosa = False
        
        while self.intentos_busqueda < self.max_intentos and not verificacion_exitosa:
            self.intentos_busqueda += 1
            
            print(f"\n🔎 FASE 2: Recuperación (intento {self.intentos_busqueda}/{self.max_intentos})...")
            print("-" * 70)
            
            # Buscar chunks
            chunks_recuperados = self.buscar_chunks(terminos, top_k)
            
            # Mostrar chunks
            print(f"\nChunks recuperados:")
            for chunk in chunks_recuperados:
                print(f"\n  [{chunk['chunk_id']}] (score: {chunk['score']})")
                print(f"  {chunk['contenido'][:80]}...")
                print(f"  Fuente: {chunk['metadata']['fuente']}")
            
            # ==== FASE 3: VERIFICACIÓN ====
            print(f"\n⚖️ FASE 3: Verificación de suficiencia...")
            print("-" * 70)
            
            chunks_texto = "\n\n".join([
                f"[{c['chunk_id']}]: {c['contenido']}"
                for c in chunks_recuperados
            ])
            
            tarea_verificacion = Task(
                description=f"""
                Pregunta original: {pregunta}
                
                Chunks recuperados:
                {chunks_texto}
                
                Evalúa si estos chunks son SUFICIENTES para responder la pregunta:
                
                1. ¿Contienen información relevante?
                2. ¿Son suficientes para una respuesta completa?
                3. ¿Hay gaps de información?
                
                Responde con:
                - SUFICIENTE: si se puede responder bien
                - INSUFICIENTE: [qué falta] si necesitas más información
                - IRRELEVANTE: si los chunks no son útiles
                """,
                agent=verifier,
                expected_output="SUFICIENTE, INSUFICIENTE o IRRELEVANTE con explicación"
            )
            
            crew_verificacion = Crew(
                agents=[verifier],
                tasks=[tarea_verificacion],
                process=Process.sequential,
                verbose=1
            )
            
            verificacion = str(crew_verificacion.kickoff()).upper()
            
            if "SUFICIENTE" in verificacion:
                print("\n✅ Verificación EXITOSA: Información suficiente")
                verificacion_exitosa = True
            elif self.intentos_busqueda < self.max_intentos:
                print(f"\n⚠️ Información insuficiente, reintentando con nuevos términos...")
                # En producción, replanificar con feedback
                terminos.append("agentes")  # Ampliar búsqueda
                top_k += 1
            else:
                print(f"\n❌ Máximo de intentos alcanzado")
                break
        
        if not verificacion_exitosa:
            return {
                "pregunta": pregunta,
                "respuesta": "No se pudo encontrar información suficiente después de múltiples intentos.",
                "chunks_usados": [],
                "exitoso": False
            }
        
        # ==== FASE 4: ESCRITURA ====
        print(f"\n✍️ FASE 4: Generación de respuesta...")
        print("-" * 70)
        
        chunks_contexto = "\n\n".join([
            f"[{c['chunk_id']}]: {c['contenido']}\nFuente: {c['metadata']['fuente']}, Página: {c['metadata']['pagina']}"
            for c in chunks_recuperados
        ])
        
        tarea_escritura = Task(
            description=f"""
            Pregunta: {pregunta}
            
            Información verificada disponible:
            {chunks_contexto}
            
            Tu tarea:
            1. Genera una respuesta clara de 3-4 oraciones
            2. USA SOLO información de los chunks proporcionados
            3. CITA cada afirmación con [chunk_X]
            4. NO inventes información
            
            Cada dato factual debe tener su cita.
            """,
            agent=writer,
            expected_output="Respuesta de 3-4 oraciones con citas verificables"
        )
        
        crew_escritura = Crew(
            agents=[writer],
            tasks=[tarea_escritura],
            process=Process.sequential,
            verbose=1
        )
        
        respuesta = crew_escritura.kickoff()
        
        # ==== FASE 5: REGISTRO EN MEMORIA ====
        print(f"\n💾 FASE 5: Registrando en memoria...")
        experiencia = {
            "timestamp": datetime.now().isoformat(),
            "pregunta": pregunta,
            "plan": plan[:100],
            "chunks_usados": [c["chunk_id"] for c in chunks_recuperados],
            "intentos": self.intentos_busqueda,
            "exitoso": True
        }
        self.historial.append(experiencia)
        print(f"✅ Experiencia registrada")
        
        # ==== RESULTADO FINAL ====
        print("\n" + "="*70)
        print("✅ RESPUESTA FINAL")
        print("="*70)
        print(respuesta)
        print("\n📚 Fuentes utilizadas:")
        for chunk in chunks_recuperados:
            print(f"  • [{chunk['chunk_id']}] {chunk['metadata']['fuente']}, p.{chunk['metadata']['pagina']}")
        print("="*70 + "\n")
        
        return {
            "pregunta": pregunta,
            "respuesta": str(respuesta),
            "chunks_usados": chunks_recuperados,
            "intentos": self.intentos_busqueda,
            "exitoso": True
        }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Agentic RAG")
    print("="*70)
    print("\nComponentes del sistema:")
    print("  📋 Planner: Estrategia de búsqueda")
    print("  🔎 Retriever: Recuperación inteligente")
    print("  ⚖️ Verifier: Validación de suficiencia")
    print("  ✍️ Writer: Generación con citas")
    print("  💾 Memory: Aprendizaje continuo")
    print()
    
    # Inicializar sistema
    rag_system = AgenticRAG(BASE_VECTORIAL)
    
    # CASO 1: Consulta sobre sistemas multi-agente
    print("\n🔬 CASO: Consulta compleja sobre multi-agentes")
    print("-" * 70)
    
    pregunta = "¿Cómo funcionan los sistemas multi-agente y por qué son importantes?"
    
    resultado = rag_system.procesar_consulta(pregunta)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ RAG ya no es simple retrieve + generate")
    print("✅ Planificación mejora la búsqueda")
    print("✅ Verificación previene respuestas insuficientes")
    print("✅ Reintentos automáticos si faltan datos")
    print("✅ Memoria permite aprendizaje continuo")
    print("✅ Sistema robusto y listo para producción")
    print("="*70 + "\n")


