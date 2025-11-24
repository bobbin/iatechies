# Primeros Pasos - Tutorial Práctico con CrewAI

## Introducción

Este tutorial te guiará paso a paso para crear y ejecutar tus primeros agentes y equipos con CrewAI. Al final, habrás creado sistemas multi-agente funcionales.

**Tiempo estimado**: 30-45 minutos  
**Nivel**: Principiante  
**Prerrequisitos**: Instalación y configuración completadas

## Conceptos Fundamentales

### ¿Qué es un Agente?

Un **agente** es una entidad autónoma que:
- Tiene un **rol** específico (ej: "Investigador", "Escritor")
- Persigue un **objetivo** (goal)
- Tiene un **contexto** (backstory) que define su personalidad
- Puede usar **herramientas** (tools) para realizar acciones
- Toma **decisiones** basándose en su rol y contexto

### ¿Qué es una Tarea?

Una **tarea** es una unidad de trabajo que:
- Define **qué debe hacerse** (description)
- Se asigna a un **agente específico**
- Especifica el **resultado esperado** (expected_output)
- Puede depender de **otras tareas** (context)

### ¿Qué es un Equipo (Crew)?

Un **equipo** es un conjunto de agentes que:
- **Colaboran** en tareas relacionadas
- Siguen un **proceso** definido (secuencial, jerárquico, etc.)
- Comparten información entre tareas
- Producen un **resultado final** conjunto

## Ejemplo 1: Tu Primer Agente

### Script Básico

Crea un archivo `ejemplo_01_primer_agente.py`:

```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno
load_dotenv()

print("="*60)
print("🤖 EJEMPLO 1: TU PRIMER AGENTE")
print("="*60 + "\n")

# Paso 1: Crear un agente
asistente = Agent(
    role="Asistente Personal",
    goal="Ayudar al usuario respondiendo preguntas de forma clara y útil",
    backstory="""Eres un asistente amigable y competente.
    Tu prioridad es ser útil, claro y conciso en tus respuestas.
    Siempre intentas proporcionar información precisa.""",
    verbose=True,  # Muestra el proceso de pensamiento
    allow_delegation=False  # No delega a otros agentes
)

# Paso 2: Crear una tarea
tarea = Task(
    description="Explica qué es la inteligencia artificial en 2-3 oraciones simples",
    agent=asistente,
    expected_output="Una explicación breve y clara de IA"
)

# Paso 3: Crear un equipo con el agente
equipo = Crew(
    agents=[asistente],
    tasks=[tarea],
    process=Process.sequential,  # Ejecuta tareas en orden
    verbose=True
)

# Paso 4: Ejecutar
print("📋 Ejecutando tarea...\n")
resultado = equipo.kickoff()

print("\n" + "="*60)
print("✅ RESULTADO:")
print("="*60)
print(resultado)
print("="*60)
```

### Ejecutar

```bash
python ejemplo_01_primer_agente.py
```

### Resultado Esperado

Verás:
1. El agente "pensando" sobre la tarea
2. El proceso de razonamiento (si verbose=True)
3. La respuesta final con una explicación de IA

## Ejemplo 2: Equipo de Dos Agentes

### Script con Colaboración

Crea `ejemplo_02_equipo_basico.py`:

```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

print("="*60)
print("👥 EJEMPLO 2: EQUIPO DE DOS AGENTES")
print("="*60 + "\n")

# Agente 1: Investigador
investigador = Agent(
    role="Investigador de Tecnología",
    goal="Investigar y recopilar información precisa sobre temas tecnológicos",
    backstory="""Eres un investigador experto en tecnología con 10 años de experiencia.
    Te especializas en explicar conceptos complejos de forma clara.
    Siempre citas fuentes confiables y verificas la información.""",
    verbose=True,
    allow_delegation=False
)

# Agente 2: Escritor
escritor = Agent(
    role="Escritor Técnico",
    goal="Transformar información técnica en contenido accesible y bien estructurado",
    backstory="""Eres un escritor técnico profesional.
    Tu especialidad es tomar información compleja y convertirla en artículos
    claros, bien organizados y fáciles de entender.
    Usas ejemplos y analogías cuando es apropiado.""",
    verbose=True,
    allow_delegation=False
)

# Tarea 1: Investigar
tarea_investigacion = Task(
    description="""Investiga sobre los modelos de lenguaje GPT-4.
    Incluye: qué son, cómo funcionan (de forma simple), y sus aplicaciones principales.
    Proporciona 3-4 puntos clave.""",
    agent=investigador,
    expected_output="Información estructurada sobre GPT-4 con 3-4 puntos clave"
)

# Tarea 2: Escribir artículo
# IMPORTANTE: context=[tarea_investigacion] hace que esta tarea reciba 
# el resultado de la tarea anterior como contexto
tarea_redaccion = Task(
    description="""Usando la información investigada, escribe un artículo breve (200-250 palabras)
    sobre GPT-4 dirigido a personas no técnicas.
    
    El artículo debe tener:
    - Un título atractivo
    - Una introducción enganchadora
    - 2-3 párrafos explicativos
    - Una conclusión breve
    
    Usa un tono amigable y accesible.""",
    agent=escritor,
    expected_output="Artículo completo de 200-250 palabras sobre GPT-4",
    context=[tarea_investigacion]  # ← Usa el resultado de la tarea anterior
)

# Crear equipo
equipo = Crew(
    agents=[investigador, escritor],
    tasks=[tarea_investigacion, tarea_redaccion],
    process=Process.sequential,  # Ejecuta en orden: primero investigación, luego redacción
    verbose=True
)

# Ejecutar
print("🚀 Iniciando equipo de trabajo...\n")
resultado = equipo.kickoff()

print("\n" + "="*60)
print("📄 ARTÍCULO FINAL:")
print("="*60)
print(resultado)
print("="*60)
```

### Observa el Flujo

1. El **investigador** ejecuta primero su tarea
2. Su resultado se pasa automáticamente al **escritor**
3. El escritor usa esa información para crear el artículo
4. El resultado final es el artículo completo

## Ejemplo 3: Agente con Herramientas

### Definir una Herramienta Personalizada

Crea `ejemplo_03_herramientas.py`:

```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

load_dotenv()

print("="*60)
print("🔧 EJEMPLO 3: AGENTE CON HERRAMIENTAS")
print("="*60 + "\n")

# Definir herramientas personalizadas
@tool("Calculadora")
def calculadora(operacion: str) -> str:
    """
    Realiza operaciones matemáticas básicas.
    
    Args:
        operacion: Una operación matemática como string (ej: "25 + 17")
        
    Returns:
        El resultado de la operación
    """
    try:
        # ADVERTENCIA: En producción, usar una librería segura para evaluar expresiones
        resultado = eval(operacion)
        return f"El resultado de {operacion} es: {resultado}"
    except Exception as e:
        return f"Error en la operación: {str(e)}"

@tool("Contador de Palabras")
def contar_palabras(texto: str) -> str:
    """
    Cuenta las palabras en un texto.
    
    Args:
        texto: El texto a analizar
        
    Returns:
        El número de palabras
    """
    palabras = len(texto.split())
    return f"El texto tiene {palabras} palabras"

# Agente con herramientas
asistente_matematico = Agent(
    role="Asistente Matemático",
    goal="Ayudar con cálculos y análisis de texto",
    backstory="""Eres un asistente que puede realizar cálculos matemáticos
    y analizar texto. Tienes acceso a una calculadora y un contador de palabras.""",
    tools=[calculadora, contar_palabras],  # ← Asignar herramientas
    verbose=True,
    allow_delegation=False
)

# Tarea que requiere usar herramientas
tarea = Task(
    description="""Realiza las siguientes operaciones:
    1. Calcula cuánto es 156 * 23
    2. Luego calcula cuánto es ese resultado dividido entre 4
    3. Finalmente, cuenta cuántas palabras hay en este texto:
       "La inteligencia artificial está transformando múltiples industrias"
       
    Presenta los resultados de forma clara.""",
    agent=asistente_matematico,
    expected_output="Resultados de las operaciones y conteo de palabras"
)

# Crear y ejecutar equipo
equipo = Crew(
    agents=[asistente_matematico],
    tasks=[tarea],
    process=Process.sequential,
    verbose=True
)

print("🧮 Ejecutando operaciones...\n")
resultado = equipo.kickoff()

print("\n" + "="*60)
print("✅ RESULTADOS:")
print("="*60)
print(resultado)
print("="*60)
```

### Observa

El agente **decide cuándo usar** cada herramienta:
- Usa `calculadora` para las operaciones matemáticas
- Usa `contar_palabras` para analizar el texto
- Combina los resultados en una respuesta coherente

## Ejemplo 4: Equipo Complejo (3+ Agentes)

### Proyecto: Crear un Informe de Mercado

Crea `ejemplo_04_proyecto_completo.py`:

```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

print("="*60)
print("📊 EJEMPLO 4: PROYECTO COMPLETO - INFORME DE MERCADO")
print("="*60 + "\n")

# Agente 1: Investigador de Mercado
investigador_mercado = Agent(
    role="Investigador de Mercado",
    goal="Recopilar datos sobre tendencias de mercado y competencia",
    backstory="""Eres un analista de mercado con 15 años de experiencia.
    Identificas tendencias, analizas competidores y evalúas oportunidades de mercado.""",
    verbose=True,
    allow_delegation=False
)

# Agente 2: Analista Financiero
analista_financiero = Agent(
    role="Analista Financiero",
    goal="Analizar la viabilidad financiera y proyecciones",
    backstory="""Eres un analista financiero especializado en proyecciones y ROI.
    Evalúas riesgos, calculas márgenes y determinas viabilidad económica.""",
    verbose=True,
    allow_delegation=False
)

# Agente 3: Estratega de Negocio
estratega = Agent(
    role="Estratega de Negocio",
    goal="Desarrollar recomendaciones estratégicas basadas en análisis",
    backstory="""Eres un estratega de negocio senior.
    Sintetizas información de múltiples fuentes para crear planes de acción concretos.""",
    verbose=True,
    allow_delegation=False
)

# Agente 4: Redactor Ejecutivo
redactor = Agent(
    role="Redactor de Informes Ejecutivos",
    goal="Crear informes ejecutivos claros y persuasivos",
    backstory="""Eres un redactor especializado en comunicación ejecutiva.
    Transformas análisis complejos en informes ejecutivos concisos.""",
    verbose=True,
    allow_delegation=False
)

# Definir tareas
tarea_1 = Task(
    description="""Analiza el mercado de software de gestión de proyectos.
    Identifica: 3 competidores principales, tendencias actuales, tamaño de mercado estimado.""",
    agent=investigador_mercado,
    expected_output="Análisis de mercado con competidores, tendencias y tamaño"
)

tarea_2 = Task(
    description="""Basándote en el análisis de mercado, evalúa la viabilidad financiera
    de lanzar un nuevo producto. Estima costos iniciales, ingresos potenciales y ROI a 2 años.""",
    agent=analista_financiero,
    expected_output="Análisis financiero con proyecciones",
    context=[tarea_1]
)

tarea_3 = Task(
    description="""Usando el análisis de mercado y financiero, desarrolla 3 recomendaciones
    estratégicas concretas para el lanzamiento del producto.""",
    agent=estratega,
    expected_output="3 recomendaciones estratégicas específicas",
    context=[tarea_1, tarea_2]
)

tarea_4 = Task(
    description="""Crea un informe ejecutivo de 1 página que sintetice:
    - Hallazgos clave del mercado
    - Viabilidad financiera
    - 3 recomendaciones estratégicas prioritarias
    
    Usa un formato ejecutivo profesional con bullet points.""",
    agent=redactor,
    expected_output="Informe ejecutivo de 1 página",
    context=[tarea_1, tarea_2, tarea_3]
)

# Crear equipo
equipo_proyecto = Crew(
    agents=[investigador_mercado, analista_financiero, estratega, redactor],
    tasks=[tarea_1, tarea_2, tarea_3, tarea_4],
    process=Process.sequential,
    verbose=True
)

# Ejecutar
print("🚀 Iniciando proyecto de análisis de mercado...\n")
print("⏳ Esto puede tardar varios minutos...\n")

resultado = equipo_proyecto.kickoff()

print("\n" + "="*60)
print("📋 INFORME EJECUTIVO FINAL:")
print("="*60)
print(resultado)
print("="*60)

# Opcional: Guardar resultado
with open("informe_mercado.md", "w", encoding="utf-8") as f:
    f.write(f"# Informe de Análisis de Mercado\n\n")
    f.write(resultado)

print("\n💾 Informe guardado en: informe_mercado.md")
```

## Consejos y Mejores Prácticas

### 1. Define Roles Claros

❌ **Mal**:
```python
role="Agente"
goal="Hacer cosas"
```

✅ **Bien**:
```python
role="Investigador Científico Senior"
goal="Investigar papers académicos y sintetizar hallazgos clave"
```

### 2. Backstories Específicos

❌ **Mal**:
```python
backstory="Eres un experto."
```

✅ **Bien**:
```python
backstory="""Eres un investigador con PhD en Ciencias de la Computación
y 10 años de experiencia en ML. Tu especialidad es resumir papers
técnicos para audiencias no técnicas."""
```

### 3. Expected Outputs Claros

❌ **Mal**:
```python
expected_output="Un resultado"
```

✅ **Bien**:
```python
expected_output="Lista de 5 hallazgos clave con fuentes citadas en formato: 
[Hallazgo] - [Fuente]"
```

### 4. Usa Context Apropiadamente

```python
# Tarea que depende de resultados anteriores
tarea_final = Task(
    description="Sintetiza los hallazgos anteriores",
    agent=sintetizador,
    context=[tarea_1, tarea_2, tarea_3]  # ← Recibe resultados de 3 tareas
)
```

## Ejercicios Prácticos

### Ejercicio 1: Blog Post Generator
Crea un equipo con:
- Investigador que busca información sobre un tema
- Escritor que crea un blog post
- Editor que revisa y mejora

### Ejercicio 2: Análisis de Sentimiento
Crea un agente que:
- Recibe una lista de comentarios de clientes
- Analiza el sentimiento (positivo/negativo/neutral)
- Genera un resumen con insights

### Ejercicio 3: Generador de Ideas
Crea un equipo con:
- Generador creativo (muchas ideas)
- Evaluador crítico (filtra las mejores)
- Desarrollador (expande la mejor idea)

## Troubleshooting Común

### Problema: El agente no termina su tarea

**Causa**: Descripción de tarea poco clara o sin límites

**Solución**:
```python
# Agrega límites claros
description="""Investiga sobre IA.
LÍMITE: Máximo 3 párrafos, enfócate solo en aplicaciones médicas."""
```

### Problema: Resultados inconsistentes

**Causa**: Temperature muy alta

**Solución**:
```python
# Reduce temperature para más consistencia
from crewai import LLM

llm = LLM(model="gpt-4", temperature=0.3)
agent = Agent(..., llm=llm)
```

## Próximos Pasos

Ahora que dominas los conceptos básicos:

1. **Explora herramientas avanzadas**: Web scraping, APIs, bases de datos
2. **Aprende patrones avanzados**: `seccion_03_uso/02_casos_uso_avanzados.md`
3. **Optimiza tu sistema**: Caché, logging, monitoreo

¡Felicidades! Ya sabes crear sistemas multi-agente con CrewAI 🎉

