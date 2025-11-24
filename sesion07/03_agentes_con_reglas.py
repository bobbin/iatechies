"""
Ejemplo 3: Agentes con Reglas Híbridas (Simbólico + LLM)
=========================================================

Complejidad: MEDIA

Concepto:
---------
El agente mezcla:
- Decisiones DURAS (deterministas, basadas en reglas)
- Razonamiento BLANDO (LLM, probabilístico)

No todo debe depender del LLM. Las reglas aportan:
- Estabilidad
- Límites claros
- Decisiones críticas predecibles
- Validación estricta

Patrón: Reglas → Validación → LLM (si pasa) → Reglas finales
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# MOTOR DE REGLAS (SIMBÓLICO)
# ==============================================================================

class MotorReglas:
    """
    Motor de reglas deterministas para validación.
    Estas reglas NO dependen del LLM, son lógica pura.
    """
    
    @staticmethod
    def validar_solicitud(solicitud: Dict) -> Tuple[bool, List[str]]:
        """
        Valida una solicitud de análisis antes de enviarla al LLM.
        
        Reglas duras:
        1. Debe tener fecha
        2. La fuente debe estar en lista blanca
        3. El texto debe tener longitud mínima
        4. No debe contener palabras prohibidas
        """
        errores = []
        
        # REGLA 1: Fecha obligatoria
        if not solicitud.get("fecha"):
            errores.append("❌ REGLA_001: Falta fecha en la solicitud")
        
        # REGLA 2: Fuente en lista blanca
        fuentes_validas = ["informe_oficial", "paper_cientifico", "documento_interno", "estudio_mercado"]
        if solicitud.get("tipo_fuente") not in fuentes_validas:
            errores.append(f"❌ REGLA_002: Fuente '{solicitud.get('tipo_fuente')}' no autorizada")
        
        # REGLA 3: Longitud mínima
        texto = solicitud.get("texto", "")
        if len(texto) < 50:
            errores.append(f"❌ REGLA_003: Texto demasiado corto ({len(texto)} caracteres, mínimo 50)")
        
        # REGLA 4: Palabras prohibidas
        palabras_prohibidas = ["hack", "exploit", "bypass", "crack"]
        texto_lower = texto.lower()
        palabras_encontradas = [p for p in palabras_prohibidas if p in texto_lower]
        if palabras_encontradas:
            errores.append(f"❌ REGLA_004: Contiene palabras prohibidas: {palabras_encontradas}")
        
        es_valida = len(errores) == 0
        return es_valida, errores
    
    @staticmethod
    def validar_citas(respuesta: str, documentos: List[str]) -> Tuple[bool, List[str]]:
        """
        Valida que todas las citas en la respuesta existan en los documentos.
        
        Busca patrones como [1], [Ref:2], etc.
        """
        # Buscar citas en formato [número]
        patron_citas = r'\[(\d+)\]|\[Ref:(\d+)\]'
        citas_encontradas = re.findall(patron_citas, respuesta)
        
        # Extraer números de citas
        numeros_citas = []
        for match in citas_encontradas:
            num = match[0] if match[0] else match[1]
            numeros_citas.append(int(num))
        
        errores = []
        
        # Validar que cada cita apunte a un documento existente
        for num_cita in numeros_citas:
            if num_cita < 1 or num_cita > len(documentos):
                errores.append(f"❌ REGLA_005: Cita [{num_cita}] no corresponde a ningún documento")
        
        es_valida = len(errores) == 0
        return es_valida, errores
    
    @staticmethod
    def aplicar_restricciones_finales(respuesta: str) -> str:
        """
        Aplica formato y restricciones finales de forma determinista.
        """
        # Agregar timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        respuesta_final = f"[Generado: {timestamp}]\n\n{respuesta}"
        
        # Agregar disclaimer si no existe
        if "disclaimer" not in respuesta.lower():
            respuesta_final += "\n\n⚠️ Disclaimer: Esta respuesta fue generada por IA y debe ser revisada por un experto."
        
        return respuesta_final


# ==============================================================================
# AGENTES (PARTE LLM)
# ==============================================================================

analizador = Agent(
    role="Analizador de Documentos",
    goal="Analizar documentos y generar resúmenes con citas verificables",
    backstory="""Eres un analista experto que examina documentos y genera 
    resúmenes precisos. SIEMPRE debes citar tus fuentes usando el formato [número] 
    donde número corresponde al documento de referencia.""",
    verbose=True,
    allow_delegation=False
)

revisor = Agent(
    role="Revisor de Calidad",
    goal="Verificar que los análisis cumplan con estándares de calidad",
    backstory="""Eres un revisor meticuloso. Verificas que las respuestas 
    tengan sentido, estén bien estructuradas y sean coherentes.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# FLUJO HÍBRIDO (REGLAS + LLM)
# ==============================================================================

def procesar_solicitud_hibrida(solicitud: Dict):
    """
    Procesa una solicitud usando enfoque híbrido: Reglas + LLM.
    
    Flujo:
    1. Validación inicial (REGLAS)
    2. Análisis con LLM
    3. Validación de citas (REGLAS)
    4. Revisión de calidad (LLM)
    5. Aplicación de restricciones finales (REGLAS)
    """
    print("\n" + "="*70)
    print("🔬 PROCESAMIENTO HÍBRIDO: REGLAS + LLM")
    print("="*70 + "\n")
    
    motor = MotorReglas()
    
    # ===== FASE 1: VALIDACIÓN INICIAL (REGLAS) =====
    print("📋 FASE 1: Validación con reglas deterministas...")
    es_valida, errores = motor.validar_solicitud(solicitud)
    
    if not es_valida:
        print("\n❌ SOLICITUD RECHAZADA POR REGLAS:")
        for error in errores:
            print(f"  {error}")
        return None
    
    print("✅ Solicitud pasa todas las reglas iniciales\n")
    
    # ===== FASE 2: ANÁLISIS CON LLM =====
    print("🤖 FASE 2: Análisis con LLM...")
    
    documentos = solicitud.get("documentos", [])
    docs_enumerados = "\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(documentos)])
    
    tarea_analisis = Task(
        description=f"""
        Analiza el siguiente texto y genera un resumen de 3-4 oraciones.
        
        Texto a analizar:
        {solicitud['texto']}
        
        Documentos de referencia:
        {docs_enumerados}
        
        IMPORTANTE: Debes citar las fuentes usando [número]. Por ejemplo: [1] o [2].
        Cada afirmación debe tener una cita.
        """,
        agent=analizador,
        expected_output="Resumen con citas en formato [número]"
    )
    
    crew_analisis = Crew(
        agents=[analizador],
        tasks=[tarea_analisis],
        process=Process.sequential,
        verbose=1
    )
    
    respuesta_llm = crew_analisis.kickoff()
    print(f"\n📄 Respuesta del LLM:\n{respuesta_llm}\n")
    
    # ===== FASE 3: VALIDACIÓN DE CITAS (REGLAS) =====
    print("🔍 FASE 3: Validación de citas con reglas...")
    
    citas_validas, errores_citas = motor.validar_citas(str(respuesta_llm), documentos)
    
    if not citas_validas:
        print("\n❌ RESPUESTA RECHAZADA: Citas inválidas")
        for error in errores_citas:
            print(f"  {error}")
        print("\n⚠️ En producción, aquí se reiniciaria el proceso o se solicitaría corrección")
        # En un sistema real, podrías reintentar o pedir corrección
        # Por simplicidad, continuamos con warning
    else:
        print("✅ Todas las citas son válidas\n")
    
    # ===== FASE 4: REVISIÓN DE CALIDAD (LLM) =====
    print("👁️ FASE 4: Revisión de calidad con LLM...")
    
    tarea_revision = Task(
        description=f"""
        Revisa el siguiente análisis:
        
        {respuesta_llm}
        
        Verifica:
        1. ¿Es coherente?
        2. ¿Las afirmaciones tienen sentido?
        3. ¿Está bien estructurado?
        
        Si encuentras problemas, indica qué debería mejorarse.
        Si está bien, di "APROBADO".
        """,
        agent=revisor,
        expected_output="APROBADO o lista de mejoras necesarias"
    )
    
    crew_revision = Crew(
        agents=[revisor],
        tasks=[tarea_revision],
        process=Process.sequential,
        verbose=1
    )
    
    revision = crew_revision.kickoff()
    print(f"\n📊 Revisión: {revision}\n")
    
    # ===== FASE 5: RESTRICCIONES FINALES (REGLAS) =====
    print("🔒 FASE 5: Aplicando restricciones finales...")
    
    respuesta_final = motor.aplicar_restricciones_finales(str(respuesta_llm))
    
    print("\n" + "="*70)
    print("✅ RESULTADO FINAL (después de flujo híbrido)")
    print("="*70)
    print(respuesta_final)
    print("="*70 + "\n")
    
    return respuesta_final


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    # CASO 1: Solicitud válida
    print("\n🧪 CASO 1: Solicitud válida (debería procesarse)")
    print("-" * 70)
    
    solicitud_valida = {
        "fecha": "2024-01-15",
        "tipo_fuente": "paper_cientifico",
        "texto": """
        Los sistemas multi-agente permiten coordinar múltiples agentes de IA 
        para resolver problemas complejos. Estos sistemas pueden dividir tareas, 
        colaborar y alcanzar objetivos que serían difíciles para un solo agente.
        """,
        "documentos": [
            "CrewAI es un framework para multi-agentes",
            "Los agentes pueden tener roles especializados",
            "La colaboración mejora los resultados"
        ]
    }
    
    procesar_solicitud_hibrida(solicitud_valida)
    
    
    # CASO 2: Solicitud inválida (sin fecha)
    print("\n\n🧪 CASO 2: Solicitud inválida (falta fecha)")
    print("-" * 70)
    
    solicitud_invalida = {
        # "fecha": None,  # ← Falta fecha (violará REGLA_001)
        "tipo_fuente": "paper_cientifico",
        "texto": "Este es un texto de ejemplo que tiene la longitud suficiente para pasar la validación de caracteres mínimos.",
        "documentos": ["Doc 1", "Doc 2"]
    }
    
    procesar_solicitud_hibrida(solicitud_invalida)
    
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ Reglas duras proveen estabilidad y predicibilidad")
    print("✅ LLM aporta flexibilidad y razonamiento")
    print("✅ Combinarlos es más robusto que solo LLM")
    print("✅ Validaciones críticas NUNCA deben depender 100% del LLM")
    print("="*70 + "\n")


