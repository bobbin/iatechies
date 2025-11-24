# Referencia API - CrewAI

## Introducción

Esta es la referencia completa de la API de CrewAI con todos los parámetros, métodos y ejemplos de uso.

## Clase: Agent

### Constructor

```python
from crewai import Agent

agent = Agent(
    role: str,
    goal: str,
    backstory: str,
    llm: Optional[LLM] = None,
    tools: Optional[List[Tool]] = None,
    verbose: bool = False,
    allow_delegation: bool = False,
    step_callback: Optional[Callable] = None,
    cache: bool = True,
    max_iterations: int = 15,
    max_execution_time: Optional[int] = None,
    memory: bool = False
)
```

### Parámetros

#### `role` (str, obligatorio)
**Descripción**: El rol o título del agente.  
**Ejemplo**: `"Investigador Senior"`, `"Analista de Datos"`  
**Mejores prácticas**: Ser específico y descriptivo

```python
# ❌ Malo
role="Agente"

# ✅ Bueno
role="Investigador Científico especializado en IA"
```

#### `goal` (str, obligatorio)
**Descripción**: El objetivo principal del agente.  
**Ejemplo**: `"Investigar y sintetizar información técnica"`

```python
goal="Analizar datos financieros y generar insights accionables"
```

#### `backstory` (str, obligatorio)
**Descripción**: Contexto y personalidad del agente.  
**Longitud recomendada**: 2-5 oraciones

```python
backstory="""Eres un analista financiero con 15 años de experiencia en Wall Street.
Tu especialidad es identificar tendencias de mercado antes que la competencia.
Eres conocido por tu precisión y pensamiento analítico riguroso."""
```

#### `llm` (LLM, opcional)
**Descripción**: Modelo de lenguaje específico para este agente.  
**Por defecto**: Usa el LLM global configurado

```python
from crewai import LLM

custom_llm = LLM(
    model="gpt-4-turbo-preview",
    temperature=0.3
)

agent = Agent(
    role="Analista",
    goal="...",
    backstory="...",
    llm=custom_llm
)
```

#### `tools` (List[Tool], opcional)
**Descripción**: Lista de herramientas que el agente puede usar.  
**Por defecto**: `[]` (sin herramientas)

```python
from crewai.tools import tool

@tool("Buscar Web")
def buscar_web(query: str) -> str:
    """Busca información en internet"""
    return f"Resultados para: {query}"

agent = Agent(
    role="Investigador",
    goal="...",
    backstory="...",
    tools=[buscar_web]
)
```

#### `verbose` (bool, opcional)
**Descripción**: Mostrar logs detallados del proceso del agente.  
**Por defecto**: `False`  
**Recomendado**: `True` para desarrollo, `False` para producción

```python
agent = Agent(
    ...,
    verbose=True  # Ver proceso de pensamiento
)
```

#### `allow_delegation` (bool, opcional)
**Descripción**: Permitir que el agente delegue tareas a otros agentes.  
**Por defecto**: `False`

```python
# Agente supervisor que puede delegar
supervisor = Agent(
    role="Supervisor",
    goal="Coordinar el equipo",
    backstory="...",
    allow_delegation=True
)

# Agente especializado que no delega
especialista = Agent(
    role="Especialista",
    goal="Ejecutar tareas específicas",
    backstory="...",
    allow_delegation=False
)
```

#### `max_iterations` (int, opcional)
**Descripción**: Número máximo de iteraciones para completar una tarea.  
**Por defecto**: `15`  
**Rango recomendado**: 3-20

```python
agent = Agent(
    ...,
    max_iterations=10  # Máximo 10 intentos
)
```

### Métodos

#### `execute_task(task: Task) -> str`
Ejecuta una tarea asignada.

```python
resultado = agent.execute_task(tarea)
```

## Clase: Task

### Constructor

```python
from crewai import Task

task = Task(
    description: str,
    agent: Agent,
    expected_output: str,
    tools: Optional[List[Tool]] = None,
    context: Optional[List[Task]] = None,
    async_execution: bool = False,
    output_file: Optional[str] = None,
    callback: Optional[Callable] = None
)
```

### Parámetros

#### `description` (str, obligatorio)
**Descripción**: Descripción detallada de lo que debe hacerse.

```python
description="""Analiza el documento adjunto y extrae:
1. Los 3 puntos principales
2. Cualquier dato estadístico relevante
3. Conclusiones clave

Presenta los resultados en formato markdown con secciones claras."""
```

#### `agent` (Agent, obligatorio)
**Descripción**: Agente asignado para ejecutar esta tarea.

```python
tarea = Task(
    description="...",
    agent=investigador  # Agente previamente creado
)
```

#### `expected_output` (str, obligatorio)
**Descripción**: Descripción del resultado esperado.

```python
expected_output="Lista numerada con 3-5 hallazgos clave, cada uno con evidencia de respaldo"
```

#### `context` (List[Task], opcional)
**Descripción**: Tareas cuyo output se usará como contexto.  
**Por defecto**: `None`

```python
tarea_1 = Task(description="Investigar tema", ...)
tarea_2 = Task(description="Analizar investigación", ...)

tarea_3 = Task(
    description="Escribir artículo basado en el análisis",
    agent=escritor,
    context=[tarea_1, tarea_2]  # Usa resultados de ambas tareas
)
```

#### `async_execution` (bool, opcional)
**Descripción**: Ejecutar tarea de forma asíncrona.  
**Por defecto**: `False`

```python
tarea_async = Task(
    description="Tarea que puede ejecutarse en paralelo",
    agent=agente,
    async_execution=True
)
```

#### `output_file` (str, opcional)
**Descripción**: Ruta donde guardar el resultado.

```python
tarea = Task(
    description="Generar informe",
    agent=redactor,
    output_file="./output/informe.md"
)
```

## Clase: Crew

### Constructor

```python
from crewai import Crew, Process

crew = Crew(
    agents: List[Agent],
    tasks: List[Task],
    process: Process = Process.sequential,
    verbose: Union[int, bool] = False,
    manager_llm: Optional[LLM] = None,
    function_calling_llm: Optional[LLM] = None,
    memory: bool = False,
    cache: bool = True,
    max_rpm: Optional[int] = None,
    share_crew: bool = False
)
```

### Parámetros

#### `agents` (List[Agent], obligatorio)
**Descripción**: Lista de agentes que forman el equipo.

```python
crew = Crew(
    agents=[investigador, analista, escritor],
    tasks=[...]
)
```

#### `tasks` (List[Task], obligatorio)
**Descripción**: Lista de tareas a ejecutar.

```python
crew = Crew(
    agents=[...],
    tasks=[tarea_1, tarea_2, tarea_3]
)
```

#### `process` (Process, opcional)
**Descripción**: Tipo de proceso de ejecución.  
**Por defecto**: `Process.sequential`  
**Opciones**:
- `Process.sequential`: Tareas en orden secuencial
- `Process.hierarchical`: Con agente manager

```python
from crewai import Process

# Secuencial
crew_seq = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential
)

# Jerárquico (requiere manager_llm)
crew_hier = Crew(
    agents=[...],
    tasks=[...],
    process=Process.hierarchical,
    manager_llm=LLM(model="gpt-4")
)
```

#### `verbose` (Union[int, bool], opcional)
**Descripción**: Nivel de detalle en logs.  
**Opciones**:
- `False` o `0`: Sin logs
- `True` o `1`: Logs básicos
- `2`: Logs detallados

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=2  # Máximo detalle
)
```

### Métodos

#### `kickoff() -> str`
Inicia la ejecución del equipo.

```python
resultado = crew.kickoff()
print(resultado)
```

#### `kickoff_async() -> Awaitable[str]`
Inicia la ejecución de forma asíncrona.

```python
import asyncio

async def main():
    resultado = await crew.kickoff_async()
    print(resultado)

asyncio.run(main())
```

## Clase: LLM

### Constructor

```python
from crewai import LLM

llm = LLM(
    model: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    timeout: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
)
```

### Parámetros

#### `model` (str, obligatorio)
**Modelos disponibles**:
- OpenAI: `"gpt-4-turbo-preview"`, `"gpt-4"`, `"gpt-3.5-turbo"`
- Anthropic: `"claude-3-opus"`, `"claude-3-sonnet"`

```python
llm = LLM(model="gpt-4-turbo-preview")
```

#### `temperature` (float, opcional)
**Rango**: 0.0 - 2.0  
**Por defecto**: 0.7

- `0.0-0.3`: Muy determinista (análisis, código)
- `0.4-0.7`: Balanceado (general)
- `0.8-2.0`: Muy creativo (escritura creativa)

```python
# Para análisis preciso
llm_analytical = LLM(model="gpt-4", temperature=0.2)

# Para escritura creativa
llm_creative = LLM(model="gpt-4", temperature=0.9)
```

#### `max_tokens` (int, opcional)
**Descripción**: Máximo de tokens en la respuesta.

```python
llm = LLM(
    model="gpt-4",
    max_tokens=2000  # Limitar respuesta
)
```

## Decorador: @tool

### Uso Básico

```python
from crewai.tools import tool

@tool("Nombre de la Herramienta")
def mi_herramienta(parametro: str) -> str:
    """
    Descripción de lo que hace la herramienta.
    
    Args:
        parametro: Descripción del parámetro
        
    Returns:
        Descripción del valor de retorno
    """
    # Implementación
    return f"Resultado: {parametro}"
```

### Ejemplo Completo

```python
@tool("Buscar en Base de Datos")
def buscar_db(query: str, limite: int = 10) -> str:
    """
    Busca registros en la base de datos.
    
    Args:
        query: Término de búsqueda
        limite: Número máximo de resultados (default: 10)
        
    Returns:
        Lista de resultados encontrados
    """
    try:
        # Tu lógica de búsqueda
        resultados = ejecutar_query(query, limite)
        return f"Encontrados {len(resultados)} resultados"
    except Exception as e:
        return f"Error en búsqueda: {str(e)}"

# Usar en agente
agente = Agent(
    role="Analista de Datos",
    goal="Analizar información de la BD",
    backstory="...",
    tools=[buscar_db]
)
```

## Enum: Process

```python
from crewai import Process

# Valores disponibles
Process.sequential    # Tareas ejecutadas una tras otra
Process.hierarchical  # Con agente manager coordinando
```

## Ejemplos de Uso Combinado

### Ejemplo Completo

```python
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# Configurar LLM personalizado
llm_preciso = LLM(
    model="gpt-4-turbo-preview",
    temperature=0.3,
    max_tokens=2000
)

# Crear herramienta
@tool("Analizar Datos")
def analizar_datos(datos: str) -> str:
    """Analiza un conjunto de datos"""
    return f"Análisis completado de: {datos}"

# Crear agentes
analista = Agent(
    role="Analista de Datos Senior",
    goal="Extraer insights de datos complejos",
    backstory="Experto en análisis con 10 años de experiencia",
    llm=llm_preciso,
    tools=[analizar_datos],
    verbose=True,
    max_iterations=10
)

reportero = Agent(
    role="Generador de Reportes",
    goal="Crear reportes claros y visuales",
    backstory="Especialista en comunicación de datos",
    llm=LLM(model="gpt-4", temperature=0.5),
    verbose=True
)

# Crear tareas
tarea_analisis = Task(
    description="Analiza el dataset de ventas del Q1",
    agent=analista,
    expected_output="Análisis con 5 insights clave"
)

tarea_reporte = Task(
    description="Crea un reporte ejecutivo del análisis",
    agent=reportero,
    expected_output="Reporte de 1 página en markdown",
    context=[tarea_analisis],
    output_file="reporte_q1.md"
)

# Crear equipo
equipo = Crew(
    agents=[analista, reportero],
    tasks=[tarea_analisis, tarea_reporte],
    process=Process.sequential,
    verbose=2,
    cache=True
)

# Ejecutar
resultado = equipo.kickoff()
print(resultado)
```

## Configuración Global

### Variables de Entorno

```python
import os

# Configurar API keys
os.environ['OPENAI_API_KEY'] = 'sk-...'
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'

# Configurar comportamiento
os.environ['CREWAI_CACHE_ENABLED'] = 'true'
os.environ['CREWAI_VERBOSE'] = 'true'
```

## Próximos Pasos

- Estructuras de datos: `02_estructuras_datos.md`
- Configuración avanzada: `03_configuracion_avanzada.md`
- Arquitectura: `04_arquitectura_sistema.md`

