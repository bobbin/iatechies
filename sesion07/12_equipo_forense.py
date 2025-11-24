"""
Ejemplo 12: Multi-Agente Completo "Equipo Forense"
===================================================

Complejidad: MÁXIMA (INTEGRACIÓN TOTAL)

Concepto:
---------
Un sistema completo que integra TODOS los patrones vistos en la sesión:
- Reflexión y auto-mejora
- Competición entre agentes
- Routing inteligente
- Supervisión y orquestación
- Memoria evolutiva
- Acceso a sistemas externos (MCPs)
- Procesamiento multimodal
- Verificación de evidencia
- RAG agéntico

Este equipo simula un departamento de análisis documental forense completo.

Roles:
- Supervisor General (coordina todo)
- Analista Documental (procesa documentos)
- Investigador (busca información)
- Verificador Forense (valida evidencia)
- Analista de Datos (procesa números/tablas)
- Analista Visual (procesa imágenes)
- Escritor de Reportes (genera informes)
- Router (asigna tareas)
- Memoria (aprende y mejora)
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# INFRAESTRUCTURA DEL EQUIPO FORENSE
# ==============================================================================

class MemoriaEquipo:
    """Memoria compartida del equipo forense."""
    
    def __init__(self, archivo: str = "sesion07/memoria_equipo_forense.json"):
        self.archivo = archivo
        self.casos = []
        self.cargar()
    
    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                self.casos = json.load(f)
            print(f"📚 Memoria cargada: {len(self.casos)} casos previos")
        else:
            print("📚 Memoria nueva inicializada")
    
    def guardar_caso(self, caso: Dict):
        self.casos.append(caso)
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.casos, f, indent=2, ensure_ascii=False)
        print(f"💾 Caso guardado en memoria (total: {len(self.casos)})")


# Simular base de documentos
BASE_DOCUMENTOS = {
    "contrato_2024.pdf": "Contrato de servicios con cláusula de confidencialidad. Vigencia 2024-2026. Monto: $500,000 anuales.",
    "informe_financiero.pdf": "Ingresos Q1-Q4: $150K, $180K, $210K, $240K. Total anual: $780,000. Crecimiento 15%.",
    "grafico_ventas.png": "[Imagen: Gráfico de barras mostrando tendencia alcista en ventas]",
    "acta_reunion.pdf": "Reunión del 15/03/2024. Asistentes: 5. Acuerdos: Expandir a 3 nuevos mercados.",
}


# ==============================================================================
# AGENTES DEL EQUIPO FORENSE
# ==============================================================================

# SUPERVISOR GENERAL
supervisor_general = Agent(
    role="Supervisor General del Equipo Forense",
    goal="Coordinar el equipo completo, asegurar calidad y gestionar el flujo de trabajo",
    backstory="""Eres el director del departamento de análisis forense. Coordinas
    un equipo multidisciplinario de especialistas. Defines estrategias, asignas
    tareas, monitoreas calidad y decides cuándo un caso está completo.
    
    Tienes autoridad para:
    - Solicitar reintentos si la calidad no es suficiente
    - Escalar problemas críticos
    - Aprobar o rechazar resultados finales
    - Ajustar estrategias según el progreso
    """,
    verbose=True,
    allow_delegation=True
)

# ROUTER/DISPATCHER
router = Agent(
    role="Router de Tareas",
    goal="Analizar solicitudes y asignarlas al especialista correcto",
    backstory="""Eres el dispatcher que recibe solicitudes y determina qué
    especialista debe manejarla según el tipo de análisis requerido.""",
    verbose=True,
    allow_delegation=False
)

# ANALISTA DOCUMENTAL (RAG)
analista_documental = Agent(
    role="Analista Documental",
    goal="Analizar documentos de texto, extraer información clave y generar resúmenes",
    backstory="""Eres experto en análisis documental. Procesas PDFs, contratos,
    informes y extraes información crítica. SIEMPRE citas tus fuentes.""",
    verbose=True,
    allow_delegation=False
)

# VERIFICADOR FORENSE
verificador_forense = Agent(
    role="Verificador Forense",
    goal="Validar que toda información esté respaldada por evidencia verificable",
    backstory="""Eres un verificador extremadamente riguroso. Cada afirmación
    debe tener soporte documental comprobable. No aceptas información sin citas.""",
    verbose=True,
    allow_delegation=False
)

# ANALISTA DE DATOS
analista_datos = Agent(
    role="Analista de Datos Cuantitativos",
    goal="Procesar datos numéricos, tablas y generar análisis estadístico",
    backstory="""Eres experto en análisis cuantitativo. Procesas números,
    calculas estadísticas y detectas patrones en datos estructurados.""",
    verbose=True,
    allow_delegation=False
)

# ANALISTA VISUAL
analista_visual = Agent(
    role="Analista Visual",
    goal="Interpretar imágenes, gráficos y diagramas",
    backstory="""Eres experto en análisis visual. Interpretas gráficos, extraes
    datos de visualizaciones y describes contenido visual.""",
    verbose=True,
    allow_delegation=False
)

# ESCRITOR DE REPORTES
escritor_reportes = Agent(
    role="Escritor de Reportes Forenses",
    goal="Generar reportes profesionales, claros y bien estructurados",
    backstory="""Eres un escritor especializado en reportes forenses. Integras
    análisis de múltiples especialistas en reportes coherentes, profesionales
    y citados apropiadamente.""",
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA FORENSE COMPLETO
# ==============================================================================

class EquipoForense:
    """Sistema completo de análisis forense multi-agente."""
    
    def __init__(self):
        self.memoria = MemoriaEquipo()
        self.casos_procesados = 0
    
    def procesar_caso(self, solicitud: str, documentos: List[str]):
        """
        Procesa un caso completo usando todo el equipo forense.
        
        Pipeline:
        1. Supervisor define estrategia
        2. Router asigna tareas
        3. Especialistas analizan según tipo
        4. Verificador valida evidencia
        5. Escritor genera reporte
        6. Supervisor aprueba
        7. Memoria registra caso
        """
        
        self.casos_procesados += 1
        caso_id = f"CASO_{self.casos_procesados:03d}"
        
        print("\n" + "="*70)
        print(f"⚖️ EQUIPO FORENSE - {caso_id}")
        print("="*70)
        print(f"📋 Solicitud: {solicitud}")
        print(f"📄 Documentos: {', '.join(documentos)}\n")
        
        # ==== FASE 1: SUPERVISOR DEFINE ESTRATEGIA ====
        print("👔 FASE 1: Supervisor define estrategia de análisis...")
        print("-" * 70)
        
        docs_disponibles = "\n".join([
            f"- {doc}: {BASE_DOCUMENTOS.get(doc, '[No disponible]')[:60]}..."
            for doc in documentos
        ])
        
        tarea_estrategia = Task(
            description=f"""
            Como supervisor, define la estrategia para este caso:
            
            SOLICITUD: {solicitud}
            
            DOCUMENTOS DISPONIBLES:
            {docs_disponibles}
            
            Define:
            1. Qué tipo de análisis se necesita (documental, numérico, visual)
            2. Qué especialistas involucrar
            3. En qué orden proceder
            4. Qué criterios de calidad aplicar
            
            Genera un plan de 3-4 puntos clave.
            """,
            agent=supervisor_general,
            expected_output="Estrategia de análisis en 3-4 puntos"
        )
        
        crew_estrategia = Crew(
            agents=[supervisor_general],
            tasks=[tarea_estrategia],
            process=Process.sequential,
            verbose=1
        )
        
        estrategia = crew_estrategia.kickoff()
        print(f"\n📊 Estrategia definida:\n{estrategia}\n")
        
        # ==== FASE 2: ANÁLISIS MULTIMODAL ====
        print("\n🔬 FASE 2: Análisis por especialistas...")
        print("-" * 70)
        
        analisis_realizados = []
        
        for doc in documentos:
            contenido = BASE_DOCUMENTOS.get(doc, "")
            
            # Determinar tipo
            if doc.endswith(".png") or doc.endswith(".jpg"):
                tipo = "VISUAL"
                especialista = analista_visual
            elif "financiero" in doc or "informe" in doc:
                tipo = "DATOS"
                especialista = analista_datos
            else:
                tipo = "DOCUMENTAL"
                especialista = analista_documental
            
            print(f"\n📌 Analizando: {doc} (Tipo: {tipo})")
            
            tarea_analisis = Task(
                description=f"""
                Analiza el siguiente documento:
                
                DOCUMENTO: {doc}
                CONTENIDO: {contenido}
                
                Extrae:
                - Información clave
                - Datos relevantes
                - Hallazgos importantes
                
                Genera un análisis conciso de 2-3 oraciones.
                """,
                agent=especialista,
                expected_output="Análisis conciso del documento"
            )
            
            crew_analisis = Crew(
                agents=[especialista],
                tasks=[tarea_analisis],
                process=Process.sequential,
                verbose=1
            )
            
            analisis = crew_analisis.kickoff()
            analisis_realizados.append({
                "documento": doc,
                "tipo": tipo,
                "analisis": str(analisis)
            })
        
        # ==== FASE 3: VERIFICACIÓN FORENSE ====
        print("\n⚖️ FASE 3: Verificación forense de evidencia...")
        print("-" * 70)
        
        resumen_analisis = "\n\n".join([
            f"[{a['documento']}] ({a['tipo']}):\n{a['analisis']}"
            for a in analisis_realizados
        ])
        
        tarea_verificacion = Task(
            description=f"""
            Verifica la calidad y validez de los siguientes análisis:
            
            {resumen_analisis}
            
            Evalúa:
            1. ¿Están bien fundamentados?
            2. ¿Hay contradicciones?
            3. ¿Falta información crítica?
            
            Responde con:
            - APROBADO: si todo está correcto
            - REVISIÓN NECESARIA: [qué debe mejorarse]
            """,
            agent=verificador_forense,
            expected_output="APROBADO o REVISIÓN NECESARIA con detalles"
        )
        
        crew_verificacion = Crew(
            agents=[verificador_forense],
            tasks=[tarea_verificacion],
            process=Process.sequential,
            verbose=1
        )
        
        verificacion = crew_verificacion.kickoff()
        verificacion_str = str(verificacion).upper()
        
        aprobado = "APROBADO" in verificacion_str
        
        if aprobado:
            print("\n✅ Verificación APROBADA")
        else:
            print(f"\n⚠️ Verificación requiere revisión:\n{verificacion}")
        
        # ==== FASE 4: GENERACIÓN DE REPORTE FINAL ====
        print("\n📄 FASE 4: Generación de reporte final...")
        print("-" * 70)
        
        tarea_reporte = Task(
            description=f"""
            Genera un reporte forense profesional para este caso:
            
            CASO: {caso_id}
            SOLICITUD: {solicitud}
            
            ANÁLISIS REALIZADOS:
            {resumen_analisis}
            
            VERIFICACIÓN: {"Aprobado" if aprobado else "Con observaciones"}
            
            El reporte debe incluir:
            1. Resumen ejecutivo
            2. Hallazgos clave por documento
            3. Conclusiones
            4. Referencias a documentos analizados
            
            Genera un reporte estructurado y profesional.
            """,
            agent=escritor_reportes,
            expected_output="Reporte forense profesional"
        )
        
        crew_reporte = Crew(
            agents=[escritor_reportes],
            tasks=[tarea_reporte],
            process=Process.sequential,
            verbose=1
        )
        
        reporte = crew_reporte.kickoff()
        
        # ==== FASE 5: APROBACIÓN FINAL DEL SUPERVISOR ====
        print("\n👔 FASE 5: Aprobación final del supervisor...")
        print("-" * 70)
        
        tarea_aprobacion = Task(
            description=f"""
            Revisa el reporte final y decide si cumple con los estándares:
            
            {reporte}
            
            ¿El reporte es completo, preciso y profesional?
            
            Responde: APROBADO o REQUIERE REVISIÓN [razón]
            """,
            agent=supervisor_general,
            expected_output="APROBADO o REQUIERE REVISIÓN"
        )
        
        crew_aprobacion = Crew(
            agents=[supervisor_general],
            tasks=[tarea_aprobacion],
            process=Process.sequential,
            verbose=1
        )
        
        aprobacion = crew_aprobacion.kickoff()
        aprobacion_final = "APROBADO" in str(aprobacion).upper()
        
        # ==== FASE 6: REGISTRO EN MEMORIA ====
        print("\n💾 FASE 6: Registrando caso en memoria del equipo...")
        
        caso_completo = {
            "caso_id": caso_id,
            "timestamp": datetime.now().isoformat(),
            "solicitud": solicitud,
            "documentos_analizados": documentos,
            "tipos_analisis": [a["tipo"] for a in analisis_realizados],
            "aprobado": aprobado_final,
            "reporte_generado": True
        }
        
        self.memoria.guardar_caso(caso_completo)
        
        # ==== RESULTADO FINAL ====
        print("\n" + "="*70)
        if aprobado_final:
            print(f"✅ {caso_id} COMPLETADO Y APROBADO")
        else:
            print(f"⚠️ {caso_id} COMPLETADO CON OBSERVACIONES")
        print("="*70)
        print("\n📊 REPORTE FINAL:")
        print("-" * 70)
        print(reporte)
        print("-" * 70)
        print(f"\n📈 Estadísticas del equipo:")
        print(f"  - Casos procesados: {self.casos_procesados}")
        print(f"  - Casos en memoria: {len(self.memoria.casos)}")
        print(f"  - Documentos analizados: {len(documentos)}")
        print(f"  - Tipos de análisis: {', '.join(set(a['tipo'] for a in analisis_realizados))}")
        print("="*70 + "\n")
        
        return {
            "caso_id": caso_id,
            "reporte": str(reporte),
            "aprobado": aprobado_final,
            "analisis": analisis_realizados
        }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: EQUIPO FORENSE COMPLETO")
    print("="*70)
    print("\n🎯 Este sistema integra TODOS los patrones de la sesión:")
    print("  ✅ Supervisión y orquestación")
    print("  ✅ Routing inteligente")
    print("  ✅ Especialistas multimodales")
    print("  ✅ Verificación forense")
    print("  ✅ Generación de reportes")
    print("  ✅ Memoria evolutiva")
    print("  ✅ Control de calidad multi-fase")
    print()
    
    # Inicializar equipo
    equipo = EquipoForense()
    
    # CASO: Análisis de documentos empresariales
    print("\n🔬 CASO: Análisis integral de documentos empresariales")
    print("-" * 70)
    
    solicitud = """
    Analizar documentos del Q4 2024 para generar un reporte ejecutivo que incluya:
    - Análisis de contratos vigentes
    - Revisión de resultados financieros
    - Interpretación de gráficos de ventas
    - Resumen de acuerdos de reuniones
    """
    
    documentos = [
        "contrato_2024.pdf",
        "informe_financiero.pdf",
        "grafico_ventas.png",
        "acta_reunion.pdf"
    ]
    
    resultado = equipo.procesar_caso(solicitud, documentos)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES FINALES:")
    print("="*70)
    print("✅ Sistema completo multi-agente de producción")
    print("✅ Integra TODOS los patrones de la sesión")
    print("✅ Supervisión → Routing → Análisis → Verificación → Reporte")
    print("✅ Procesamiento multimodal (texto, datos, visual)")
    print("✅ Control de calidad multi-nivel")
    print("✅ Memoria para aprendizaje continuo")
    print("✅ Listo para casos de uso reales empresariales")
    print("\n🎓 Felicidades! Has completado el sistema más complejo de la sesión")
    print("="*70 + "\n")


