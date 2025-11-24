"""
Ejemplo 9: Multi-Agente Multimodal Ligero
==========================================

Complejidad: ALTA

Concepto:
---------
Agentes que combinan texto, imágenes, diagramas o PDFs en un mismo flujo.

El sistema decide dinámicamente:
- Si el input es texto → RAG textual
- Si el input es imagen → Visión
- Si el input es PDF escaneado → OCR
- Si el input tiene gráficos → Análisis visual

Patrón: Router → Detecta tipo → Especialista adecuado → Integra resultados
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool

# Cargar variables de entorno
load_dotenv()

# ==============================================================================
# HERRAMIENTAS MULTIMODALES (SIMULADAS)
# ==============================================================================

@tool("Analizar Imagen")
def analizar_imagen(imagen_path: str) -> str:
    """
    Analiza una imagen y extrae información visual.
    
    En producción usaría GPT-4V, Claude 3, o Gemini Vision.
    
    Args:
        imagen_path: Ruta a la imagen
    
    Returns:
        Descripción de lo encontrado en la imagen
    """
    print(f"🖼️ Analizando imagen: {imagen_path}")
    
    # Simulación basada en el nombre del archivo
    if "grafico" in imagen_path.lower():
        return """
Análisis de imagen (gráfico detectado):
- Tipo: Gráfico de barras
- Datos: Ventas mensuales 2024
- Tendencia: Crecimiento del 15%
- Valores destacados: 
  * Enero: $50K
  * Junio: $75K
  * Diciembre: $95K
- Conclusión visual: Tendencia alcista clara
        """
    elif "diagrama" in imagen_path.lower():
        return """
Análisis de imagen (diagrama detectado):
- Tipo: Diagrama de arquitectura
- Componentes identificados:
  * Frontend (React)
  * API Gateway
  * Microservicios (3)
  * Base de datos (PostgreSQL)
- Flujo: Cliente → API → Servicios → DB
        """
    else:
        return f"""
Análisis de imagen: {imagen_path}
- Contenido: [Descripción general de la imagen]
- Elementos detectados: [Lista de elementos]
- Contexto: [Interpretación del contenido]
        """


@tool("Extraer Texto PDF")
def extraer_texto_pdf(pdf_path: str) -> str:
    """
    Extrae texto de un PDF (OCR si es necesario).
    
    En producción usaría PyPDF2, pdf2image + Tesseract, o APIs especializadas.
    
    Args:
        pdf_path: Ruta al PDF
    
    Returns:
        Texto extraído del PDF
    """
    print(f"📄 Extrayendo texto de PDF: {pdf_path}")
    
    # Simulación
    return f"""
Texto extraído de {pdf_path}:

REPORTE FINANCIERO 2024
=======================

Resumen Ejecutivo:
La empresa alcanzó ingresos de $780,000 en 2024, representando 
un crecimiento del 15% respecto al año anterior.

Principales logros:
- Expansión a 3 nuevos mercados
- Lanzamiento de 5 productos nuevos
- Incremento del 20% en satisfacción del cliente

Desafíos:
- Competencia en mercado X
- Costos operativos aumentaron 8%

Proyección 2025:
Se espera un crecimiento adicional del 18-20%.
    """


@tool("Analizar Tabla")
def analizar_tabla(tabla_descripcion: str) -> str:
    """
    Analiza datos tabulares y extrae insights.
    
    Args:
        tabla_descripcion: Descripción o datos de la tabla
    
    Returns:
        Análisis de los datos
    """
    print(f"📊 Analizando tabla de datos")
    
    return """
Análisis de tabla:
- Filas: 12 (meses)
- Columnas: Ventas, Costos, Ganancia
- Estadísticas:
  * Promedio ventas: $65,000/mes
  * Promedio ganancia: $18,000/mes
  * Mejor mes: Diciembre ($95K ventas)
  * Peor mes: Febrero ($42K ventas)
- Tendencias:
  * Estacionalidad clara (picos en Q4)
  * Margen de ganancia estable (~28%)
    """


@tool("Sintetizar Información")
def sintetizar_informacion(fuentes: str) -> str:
    """
    Sintetiza información de múltiples fuentes y formatos.
    
    Args:
        fuentes: Descripción de las fuentes analizadas
    
    Returns:
        Síntesis integrada
    """
    print(f"🔄 Sintetizando información multimodal")
    
    return """
Síntesis integrada de fuentes multimodales:

La información visual (gráficos) confirma los datos textuales (PDF).
Hay consistencia entre:
- Cifras en documentos
- Tendencias en gráficos
- Estructura en diagramas

Conclusión consolidada basada en texto + visual + datos.
    """


# ==============================================================================
# AGENTES MULTIMODALES
# ==============================================================================

router_multimodal = Agent(
    role="Router Multimodal",
    goal="Detectar el tipo de contenido y dirigirlo al especialista correcto",
    backstory="""Eres un router que identifica si el contenido es:
    - TEXTO: Documentos, reportes escritos
    - IMAGEN: Fotos, gráficos, diagramas
    - PDF: Documentos PDF (pueden requerir OCR)
    - TABLA: Datos estructurados, hojas de cálculo
    
    Decides qué herramienta usar según el tipo.""",
    verbose=True,
    allow_delegation=False
)

especialista_visual = Agent(
    role="Especialista en Análisis Visual",
    goal="Analizar contenido visual (imágenes, gráficos, diagramas)",
    backstory="""Eres experto en interpretar información visual. Analizas
    imágenes, gráficos, diagramas y extraes insights. Puedes detectar tendencias
    en visualizaciones y describir estructuras en diagramas.""",
    tools=[analizar_imagen],
    verbose=True,
    allow_delegation=False
)

especialista_documentos = Agent(
    role="Especialista en Documentos",
    goal="Extraer y analizar información de documentos PDF y texto",
    backstory="""Eres experto en procesar documentos. Extraes texto de PDFs,
    incluso si están escaneados (OCR), y analizas el contenido textual.""",
    tools=[extraer_texto_pdf],
    verbose=True,
    allow_delegation=False
)

especialista_datos = Agent(
    role="Especialista en Datos Estructurados",
    goal="Analizar tablas, hojas de cálculo y datos estructurados",
    backstory="""Eres experto en análisis de datos. Procesas tablas,
    calculas estadísticas y detectas patrones en datos estructurados.""",
    tools=[analizar_tabla],
    verbose=True,
    allow_delegation=False
)

integrador = Agent(
    role="Integrador de Información",
    goal="Sintetizar información de múltiples formatos en una respuesta coherente",
    backstory="""Eres experto en integrar información de diferentes fuentes
    y formatos. Tomas análisis de texto, visual y datos, y creas una síntesis
    coherente y completa.""",
    tools=[sintetizar_informacion],
    verbose=True,
    allow_delegation=False
)


# ==============================================================================
# SISTEMA MULTIMODAL
# ==============================================================================

def procesar_input_multimodal(inputs: List[Dict[str, str]]):
    """
    Procesa múltiples inputs de diferentes tipos (texto, imagen, PDF, tabla).
    
    Args:
        inputs: Lista de diccionarios con 'tipo' y 'contenido'
        
    Ejemplo:
        [
            {"tipo": "imagen", "contenido": "grafico_ventas.png"},
            {"tipo": "pdf", "contenido": "reporte_2024.pdf"},
            {"tipo": "tabla", "contenido": "datos mensuales"}
        ]
    """
    
    print("\n" + "="*70)
    print("🎨 SISTEMA MULTIMODAL")
    print("="*70)
    print(f"📥 Procesando {len(inputs)} inputs de diferentes tipos\n")
    
    resultados = []
    
    # ==== FASE 1: PROCESAR CADA INPUT SEGÚN SU TIPO ====
    for i, input_item in enumerate(inputs, 1):
        tipo = input_item["tipo"]
        contenido = input_item["contenido"]
        
        print(f"\n📌 INPUT {i}/{len(inputs)}: {tipo.upper()}")
        print("-" * 70)
        
        if tipo == "imagen":
            # Usar especialista visual
            tarea = Task(
                description=f"""
                Analiza la siguiente imagen: {contenido}
                
                Extrae toda la información visual relevante.
                Usa la herramienta 'analizar_imagen'.
                """,
                agent=especialista_visual,
                expected_output="Análisis detallado de la imagen"
            )
            
            crew = Crew(
                agents=[especialista_visual],
                tasks=[tarea],
                process=Process.sequential,
                verbose=1
            )
            
            resultado = crew.kickoff()
            resultados.append({"tipo": "imagen", "resultado": str(resultado)})
        
        elif tipo == "pdf":
            # Usar especialista documentos
            tarea = Task(
                description=f"""
                Extrae y analiza el contenido del PDF: {contenido}
                
                Usa la herramienta 'extraer_texto_pdf' y luego analiza
                el contenido extraído.
                """,
                agent=especialista_documentos,
                expected_output="Contenido extraído y analizado del PDF"
            )
            
            crew = Crew(
                agents=[especialista_documentos],
                tasks=[tarea],
                process=Process.sequential,
                verbose=1
            )
            
            resultado = crew.kickoff()
            resultados.append({"tipo": "pdf", "resultado": str(resultado)})
        
        elif tipo == "tabla":
            # Usar especialista datos
            tarea = Task(
                description=f"""
                Analiza la siguiente tabla de datos: {contenido}
                
                Usa la herramienta 'analizar_tabla' para extraer insights
                estadísticos y tendencias.
                """,
                agent=especialista_datos,
                expected_output="Análisis estadístico de la tabla"
            )
            
            crew = Crew(
                agents=[especialista_datos],
                tasks=[tarea],
                process=Process.sequential,
                verbose=1
            )
            
            resultado = crew.kickoff()
            resultados.append({"tipo": "tabla", "resultado": str(resultado)})
    
    # ==== FASE 2: INTEGRAR RESULTADOS ====
    print("\n" + "="*70)
    print("🔄 FASE 2: Integrando información multimodal...")
    print("="*70 + "\n")
    
    # Preparar resumen de todos los análisis
    resumen_fuentes = "\n\n".join([
        f"Fuente {i} ({r['tipo'].upper()}):\n{r['resultado']}"
        for i, r in enumerate(resultados, 1)
    ])
    
    tarea_integracion = Task(
        description=f"""
        Has recibido análisis de múltiples fuentes en diferentes formatos:
        
        {resumen_fuentes}
        
        Tu tarea:
        1. Identifica información complementaria entre fuentes
        2. Detecta consistencias o inconsistencias
        3. Genera una síntesis coherente que integre todas las fuentes
        
        Crea un resumen ejecutivo de 4-5 puntos clave.
        """,
        agent=integrador,
        expected_output="Síntesis integrada de todas las fuentes multimodales"
    )
    
    crew_integracion = Crew(
        agents=[integrador],
        tasks=[tarea_integracion],
        process=Process.sequential,
        verbose=1
    )
    
    sintesis_final = crew_integracion.kickoff()
    
    print("\n" + "="*70)
    print("✅ SÍNTESIS FINAL MULTIMODAL")
    print("="*70)
    print(sintesis_final)
    print("="*70 + "\n")
    
    return {
        "resultados_individuales": resultados,
        "sintesis_final": str(sintesis_final)
    }


# ==============================================================================
# EJEMPLOS DE USO
# ==============================================================================

if __name__ == "__main__":
    
    print("="*70)
    print("🧪 DEMOSTRACIÓN: Sistema Multi-Agente Multimodal")
    print("="*70)
    
    # CASO: Análisis empresarial con múltiples fuentes
    print("\n🔬 CASO: Análisis empresarial multimodal")
    print("-" * 70)
    print("Inputs: Gráfico + PDF + Tabla de datos\n")
    
    inputs_multimodales = [
        {
            "tipo": "imagen",
            "contenido": "grafico_ventas_2024.png"
        },
        {
            "tipo": "pdf",
            "contenido": "reporte_financiero_2024.pdf"
        },
        {
            "tipo": "tabla",
            "contenido": "datos_mensuales_ventas_costos_ganancias"
        }
    ]
    
    resultado = procesar_input_multimodal(inputs_multimodales)
    
    print("\n\n" + "="*70)
    print("💡 APRENDIZAJES:")
    print("="*70)
    print("✅ Agentes procesan múltiples tipos de datos (texto, imagen, PDF)")
    print("✅ Router decide qué especialista usar según el tipo")
    print("✅ Cada especialista usa herramientas específicas")
    print("✅ Integrador sintetiza información de todas las fuentes")
    print("✅ Razonamiento híbrido: visual + textual + datos")
    print("="*70 + "\n")


