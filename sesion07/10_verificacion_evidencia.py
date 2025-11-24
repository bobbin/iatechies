"""
Ejemplo 10: Verificación de Evidencia (Evidence Checking Agents)
=================================================================

Complejidad: ALTA

Concepto:
---------
Agentes que verifican si las citas son reales y si la evidencia soporta
las afirmaciones realizadas.

Este es el antídoto contra la "alucinación elegante": 
respuestas que suenan convincentes pero no tienen soporte factual.

Patrón: Afirmación → Extraer citas → Verificar existencia → 
        Validar soporte → Aprobar/Rechazar
"""

import os
import re
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# BASE DE DOCUMENTOS (GROUND TRUTH)
# ==============================================================================

# En producción, esto sería una base vectorial (ChromaDB, Pinecone, etc.)
DOCUMENTOS_BASE = {
    "doc_1": """
Los sistemas multi-agente permiten coordinar múltiples agentes de IA para
resolver problemas complejos. Según el estudio de Stanford 2023, estos sistemas
pueden mejorar la eficiencia en un 40% comparado con agentes individuales.
    """,
    "doc_2": """
CrewAI es un framework que facilita la construcción de equipos de agentes.
Permite definir roles, objetivos y herramientas para cada agente. La
documentación oficial indica que es especialmente útil para tareas que
requieren especialización.
    """,
    "doc_3": """
La verificación de evidencia es crítica en sistemas RAG (Retrieval Augmented
Generation). Sin verificación, los modelos pueden generar respuestas que suenan
correctas pero carecen de soporte factual, fenómeno conocido como "alucinación".
    """,
    "doc_4": """
El patrón supervisor-especialistas es común en arquitecturas multi-agente.
El supervisor coordina mientras los especialistas ejecutan tareas específicas.
Este patrón reduce la complejidad y mejora la mantenibilidad del sistema.
    """
}


# ==============================================================================
# MOTOR DE VERIFICACIÓN
# ==============================================================================

class VerificadorEvidencia:
    """
    Motor de verificación de citas y evidencia.
    """
    
    def __init__(self, documentos: Dict[str, str]):
        self.documentos = documentos
    
    def extraer_citas(self, texto: str) -> List[str]:
        """
        Extrae referencias en formato [doc_X] del texto.
        """
        patron = r'\[doc_(\d+)\]'
        citas = re.findall(patron, texto)
        return [f"doc_{c}" for c in citas]
    
    def verificar_existencia_citas(self, citas: List[str]) -> Tuple[bool, List[str]]:
        """
        Verifica que todas las citas apunten a documentos existentes.
        """
        errores = []
        for cita in citas:
            if cita not in self.documentos:
                errores.append(f"❌ Cita {cita} no existe en la base de documentos")
        
        return len(errores) == 0, errores
    
    def verificar_soporte_afirmacion(
        self,
        afirmacion: str,
        cita: str
    ) -> Tuple[bool, str]:
        """
        Verifica si el documento citado realmente soporta la afirmación.
        
        En producción, esto usaría:
        - Embeddings para similitud semántica
        - Entailment models
        - LLMs con prompts especializados
        
        Aquí usamos búsqueda simple de palabras clave.
        """
        if cita not in self.documentos:
            return False, f"Documento {cita} no existe"
        
        documento = self.documentos[cita].lower()
        afirmacion_lower = afirmacion.lower()
        
        # Extraer palabras clave de la afirmación
        palabras_clave = set(afirmacion_lower.split()) - {
            'el', 'la', 'los', 'las', 'un', 'una', 'es', 'son', 'de', 'del', 
            'en', 'y', 'a', 'que', 'por', 'para', 'con'
        }
        
        # Verificar cuántas palabras clave aparecen en el documento
        palabras_encontradas = [p for p in palabras_clave if p in documento]
        ratio_soporte = len(palabras_encontradas) / len(palabras_clave) if palabras_clave else 0
        
        if ratio_soporte >= 0.5:  # Al menos 50% de las palabras clave deben aparecer
            return True, f"✅ {cita} soporta la afirmación ({ratio_soporte*100:.0f}% match)"
        else:
            return False, f"❌ {cita} NO soporta suficientemente la afirmación ({ratio_soporte*100:.0f}% match)"
    
    def generar_reporte_verificacion(
        self,
        texto: str,
        afirmaciones: List[str]
    ) -> Dict:
        """
        Genera un reporte completo de verificación.
        """
        # Extraer citas
        citas = self.extraer_citas(texto)
        
        # Verificar existencia
        citas_existen, errores_existencia = self.verificar_existencia_citas(citas)
        
        # Verificar soporte (solo si las citas existen)
        verificaciones_soporte = []
        if citas_existen:
            for afirmacion in afirmaciones:
                # Buscar qué citas acompañan esta afirmación
                # (simplificación: asumimos que las citas están cerca)
                citas_afirmacion = self.extraer_citas(afirmacion)
                if not citas_afirmacion:
                    citas_afirmacion = citas  # Usar todas las citas si no hay específicas
                
                for cita in citas_afirmacion:
                    soporta, razon = self.verificar_soporte_afirmacion(afirmacion, cita)
                    verificaciones_soporte.append({
                        "afirmacion": afirmacion,
                        "cita": cita,
                        "soporta": soporta,
                        "razon": razon
                    })
        
        todas_soportadas = all(v["soporta"] for v in verificaciones_soporte)
        
        return {
            "citas_extraidas": citas,
            "citas_validas": citas_existen,
            "errores_existencia": errores_existencia,
            "verificaciones_soporte": verificaciones_soporte,
            "todas_soportadas": todas_soportadas,
            "aprobado": citas_existen and todas_soportadas
        }


# ==============================================================================
# AGENTES
# ==============================================================================

generador_respuestas = Agent(
    role="Generador de Respuestas con Citas",
    goal="Generar respuestas bien fundamentadas con citas a documentos",
    backstory="""Eres un agente que genera respuestas basadas en documentos.
    SIEMPRE debes citar tus fuentes usando el formato [doc_X] donde X es el
    número del documento. Cada afirmación factual debe tener una cita.""",
    verbose=True,
    allow_delegation=False
)

verificador_estricto = Agent(
    role="Verificador de Evidencia",
    goal="Verificar rigurosamente que todas las afirmaciones tengan soporte documental",
    backstory="""Eres un verificador extremadamente estricto. Tu trabajo es
    asegurar que cada afirmación esté respaldada por evidencia real de los
    documentos citados. No aceptas afirmaciones sin soporte.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA CON VERIFICACIÓN
# ==============================================================================

def generar_respuesta_verificada(pregunta: str):
    """
    Genera una respuesta con verificación estricta de evidencia.
    
    Flujo:
    1. Generar respuesta con citas
    2. Extraer afirmaciones
    3. Verificar existencia de citas
    4. Verificar que citas soporten afirmaciones
    5. Aprobar/Rechazar
    """
    
    print("\n" + "="*70)
    print("🔍 SISTEMA DE VERIFICACIÓN DE EVIDENCIA")
    print("="*70)
    print(f"❓ Pregunta: {pregunta}\n")
    
    verificador = VerificadorEvidencia(DOCUMENTOS_BASE)
    
    # Mostrar documentos disponibles
    print("📚 Documentos disponibles en la base:")
    for doc_id, contenido in DOCUMENTOS_BASE.items():
        print(f"\n[{doc_id}]:")
        print(f"  {contenido[:100]}...")
    print()
    
    # ==== FASE 1: GENERAR RESPUESTA CON CITAS ====
    print("\n📝 FASE 1: Generando respuesta con citas...")
    print("-" * 70)
    
    docs_contexto = "\n\n".join([
        f"[{doc_id}]: {contenido}"
        for doc_id, contenido in DOCUMENTOS_BASE.items()
    ])
    
    tarea_generacion = Task(
        description=f"""
        Responde la siguiente pregunta basándote en los documentos proporcionados:
        
        PREGUNTA: {pregunta}
        
        DOCUMENTOS DISPONIBLES:
        {docs_contexto}
        
        REQUISITOS CRÍTICOS:
        1. TODA afirmación factual debe incluir una cita [doc_X]
        2. Solo usa información que esté en los documentos
        3. Si un documento soporta una afirmación, cítalo
        4. No inventes información
        
        Formato de cita: [doc_1], [doc_2], etc.
        
        Genera una respuesta de 3-4 oraciones con citas apropiadas.
        """,
        agent=generador_respuestas,
        expected_output="Respuesta de 3-4 oraciones con citas en formato [doc_X]"
    )
    
    crew_generacion = Crew(
        agents=[generador_respuestas],
        tasks=[tarea_generacion],
        process=Process.sequential,
        verbose=1
    )
    
    respuesta = crew_generacion.kickoff()
    respuesta_str = str(respuesta)
    
    print(f"\n📄 Respuesta generada:\n{respuesta_str}\n")
    
    # ==== FASE 2: EXTRAER AFIRMACIONES ====
    print("\n🔎 FASE 2: Extrayendo afirmaciones a verificar...")
    print("-" * 70)
    
    # Dividir respuesta en oraciones (afirmaciones)
    afirmaciones = [s.strip() for s in respuesta_str.split('.') if s.strip()]
    
    print(f"Afirmaciones encontradas: {len(afirmaciones)}")
    for i, af in enumerate(afirmaciones, 1):
        print(f"  {i}. {af}")
    print()
    
    # ==== FASE 3: VERIFICACIÓN AUTOMÁTICA ====
    print("\n⚖️ FASE 3: Verificación automática de evidencia...")
    print("-" * 70)
    
    reporte = verificador.generar_reporte_verificacion(respuesta_str, afirmaciones)
    
    print(f"\n📊 Citas encontradas: {reporte['citas_extraidas']}")
    print(f"✅ Citas válidas: {reporte['citas_validas']}")
    
    if not reporte['citas_validas']:
        print("\n❌ ERRORES DE EXISTENCIA:")
        for error in reporte['errores_existencia']:
            print(f"  {error}")
    
    print(f"\n🔍 Verificaciones de soporte:")
    for verif in reporte['verificaciones_soporte']:
        print(f"\n  Afirmación: {verif['afirmacion'][:60]}...")
        print(f"  Cita: {verif['cita']}")
        print(f"  {verif['razon']}")
    
    # ==== FASE 4: DECISIÓN FINAL ====
    print("\n" + "="*70)
    if reporte['aprobado']:
        print("✅ RESPUESTA APROBADA")
        print("="*70)
        print("Todas las afirmaciones están respaldadas por evidencia verificada.")
        print(f"\nRespuesta final:\n{respuesta_str}")
    else:
        print("❌ RESPUESTA RECHAZADA")
        print("="*70)
        print("Razones:")
        if not reporte['citas_validas']:
            print("  - Citas a documentos inexistentes")
        if not reporte['todas_soportadas']:
            print("  - Afirmaciones sin soporte documental adecuado")
        print("\n⚠️ En producción, esto activaría un re-generación con feedback")
    
    print("="*70 + "\n")
    
    return {
        "pregunta": pregunta,
        "respuesta": respuesta_str,
        "reporte_verificacion": reporte,
        "aprobado": reporte['aprobado']
    }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Verificación de Evidencia")
    print("="*70)
    
    # CASO 1: Pregunta que debería generar respuesta válida
    print("\n🔬 CASO 1: Pregunta sobre sistemas multi-agente")
    print("-" * 70)
    
    pregunta1 = "¿Qué ventajas tienen los sistemas multi-agente?"
    resultado1 = generar_respuesta_verificada(pregunta1)
    
    # CASO 2: Otra pregunta
    # print("\n\n🔬 CASO 2: Pregunta sobre verificación")
    # print("-" * 70)
    
    # pregunta2 = "¿Por qué es importante verificar evidencia en sistemas RAG?"
    # resultado2 = generar_respuesta_verificada(pregunta2)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ Cada afirmación debe tener soporte documental")
    print("✅ Verificación automática previene alucinaciones")
    print("✅ Citas deben existir Y soportar las afirmaciones")
    print("✅ Antídoto contra 'alucinación elegante'")
    print("✅ Crítico para Agentic RAG de producción")
    print("="*70 + "\n")


