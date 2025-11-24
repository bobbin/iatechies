# Problemas Comunes y Soluciones - Guía de Troubleshooting

## Introducción

Esta guía cubre los problemas más frecuentes al trabajar con CrewAI y sus soluciones paso a paso.

## Problemas de Instalación

### Error: "No module named 'crewai'"

**Síntomas**:
```python
ModuleNotFoundError: No module named 'crewai'
```

**Causas comunes**:
1. CrewAI no instalado
2. Entorno virtual no activado
3. Instalado en otro entorno de Python

**Soluciones**:

```bash
# 1. Verificar que el entorno virtual está activado
# Deberías ver (venv_nombre) en tu prompt

# Windows:
.\venv_crewai\Scripts\Activate.ps1

# Linux/macOS:
source venv_crewai/bin/activate

# 2. Reinstalar CrewAI
pip install --upgrade crewai crewai-tools

# 3. Verificar instalación
pip show crewai

# 4. Verificar que usas el Python correcto
which python  # Linux/macOS
where python  # Windows
```

### Error: "Microsoft Visual C++ 14.0 is required"

**Síntomas** (Windows):
```
error: Microsoft Visual C++ 14.0 is required
```

**Causa**: Faltan herramientas de compilación

**Solución**:

1. Descargar Visual Studio Build Tools:
   https://visualstudio.microsoft.com/downloads/

2. Durante instalación, seleccionar:
   - "Desktop development with C++"
   - Windows 10 SDK

3. Reiniciar terminal y reinstalar:
   ```bash
   pip install crewai
   ```

## Problemas de Configuración

### Error: "OPENAI_API_KEY not found"

**Síntomas**:
```python
OpenAIError: OPENAI_API_KEY not found
```

**Soluciones**:

```python
# 1. Verificar que .env existe
import os
print(os.path.exists('.env'))  # Debe ser True

# 2. Verificar contenido de .env
# Debe tener: OPENAI_API_KEY=sk-...

# 3. Verificar que load_dotenv() se llama
from dotenv import load_dotenv
load_dotenv()

# 4. Verificar que la variable se carga
import os
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key presente: {bool(api_key)}")
print(f"Empieza con sk-: {api_key.startswith('sk-') if api_key else False}")

# 5. Si persiste, establecer manualmente
os.environ['OPENAI_API_KEY'] = 'sk-tu-key-aqui'
```

### Error: "Invalid API key"

**Síntomas**:
```python
AuthenticationError: Incorrect API key provided
```

**Verificaciones**:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Verificar formato
print(f"Longitud: {len(api_key) if api_key else 0}")  # Debe ser ~50+
print(f"Empieza con 'sk-': {api_key.startswith('sk-') if api_key else False}")
print(f"Tiene espacios: {' ' in api_key if api_key else False}")  # Debe ser False

# Verificar conectividad
import openai
client = openai.OpenAI(api_key=api_key)
try:
    models = client.models.list()
    print("✅ API Key válida")
except openai.AuthenticationError:
    print("❌ API Key inválida")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Soluciones**:
1. Regenerar API key en https://platform.openai.com/api-keys
2. Verificar que no hay espacios ni comillas extra en .env
3. Verificar que la cuenta tiene créditos activos

## Problemas de Ejecución

### Error: "Rate limit exceeded"

**Síntomas**:
```python
RateLimitError: Rate limit reached for requests
```

**Causa**: Demasiadas peticiones en poco tiempo

**Soluciones**:

```python
# 1. Implementar rate limiting
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
def call_with_retry(prompt):
    # Tu llamada aquí
    pass

# 2. Agregar delays entre llamadas
import time

for task in tasks:
    result = crew.kickoff()
    time.sleep(2)  # 2 segundos entre tareas

# 3. Reducir agentes concurrentes
# En config.yaml:
agents:
  max_concurrent: 3  # Reducir de 10 a 3

# 4. Verificar límites de tu plan
# https://platform.openai.com/account/limits
```

### Error: "Context length exceeded"

**Síntomas**:
```python
InvalidRequestError: This model's maximum context length is 8192 tokens
```

**Causa**: El prompt + historial excede el límite del modelo

**Soluciones**:

```python
# 1. Usar modelo con más contexto
from crewai import LLM

llm = LLM(
    model="gpt-4-turbo-preview",  # 128k tokens
    # vs "gpt-3.5-turbo"  # 4k tokens
)

agent = Agent(..., llm=llm)

# 2. Reducir tamaño de descripciones
# ❌ Mal
description = """
    [Descripción muy larga de 1000 palabras...]
"""

# ✅ Bien
description = "Resumir el documento en 3 puntos clave"

# 3. Limitar contexto de tareas
tarea = Task(
    description="...",
    context=[tarea_1]  # Solo 1 tarea anterior, no todas
)

# 4. Usar max_tokens
llm = LLM(
    model="gpt-4",
    max_tokens=2000  # Limitar respuesta
)
```

### Error: "Agent stuck in infinite loop"

**Síntomas**: El agente nunca termina su tarea

**Causa**: Tarea mal definida o sin criterio de salida

**Soluciones**:

```python
# 1. Agregar límite de iteraciones
agent = Agent(
    role="Investigador",
    goal="...",
    backstory="...",
    max_iterations=5,  # ← Máximo 5 intentos
    verbose=True
)

# 2. Definir criterios claros de éxito
# ❌ Mal
description = "Investiga todo sobre IA"

# ✅ Bien
description = """Investiga sobre IA y proporciona exactamente:
- 3 aplicaciones principales
- 2 desafíos actuales
Limita tu respuesta a 200 palabras."""

# 3. Usar expected_output específico
expected_output = "Lista numerada con exactamente 5 puntos"
```

### Error: "Timeout"

**Síntomas**:
```python
TimeoutError: Request timed out after 60 seconds
```

**Soluciones**:

```python
# 1. Aumentar timeout
from crewai import LLM

llm = LLM(
    model="gpt-4",
    timeout=120  # 2 minutos
)

# 2. Simplificar tareas complejas
# Dividir 1 tarea grande en varias pequeñas

# 3. Usar tareas asíncronas (avanzado)
import asyncio

async def ejecutar_equipos_paralelos():
    resultados = await asyncio.gather(
        equipo1.kickoff_async(),
        equipo2.kickoff_async()
    )
    return resultados
```

## Problemas de Rendimiento

### Problema: Respuestas muy lentas

**Causas y soluciones**:

```python
# 1. Modelo muy grande - Usar modelo más rápido
llm = LLM(model="gpt-3.5-turbo")  # Más rápido que gpt-4

# 2. Demasiado contexto - Limitar información
task = Task(
    description="...",
    context=[tarea_reciente]  # Solo la más reciente
)

# 3. Sin caché - Habilitar caché
# En config.yaml:
cache:
  enabled: true
  ttl: 3600

# 4. Verbose muy detallado - Reducir
agent = Agent(
    ...,
    verbose=False  # Solo resultados finales
)
```

### Problema: Costos muy altos

**Monitorear y optimizar**:

```python
# 1. Usar modelo más económico cuando sea posible
# gpt-3.5-turbo: ~$0.0015 por 1K tokens
# gpt-4: ~$0.03 por 1K tokens (20x más caro)

# 2. Implementar contador de tokens
import tiktoken

def contar_tokens(texto, modelo="gpt-4"):
    encoding = tiktoken.encoding_for_model(modelo)
    return len(encoding.encode(texto))

prompt = "Tu prompt aquí"
tokens = contar_tokens(prompt)
costo_estimado = tokens / 1000 * 0.03  # $0.03 por 1K
print(f"Tokens: {tokens}, Costo estimado: ${costo_estimado:.4f}")

# 3. Habilitar caché agresivo
cache:
  enabled: true
  ttl: 86400  # 24 horas

# 4. Establecer límites
llm = LLM(
    model="gpt-4",
    max_tokens=500  # Limitar respuesta
)
```

## Problemas de Herramientas (Tools)

### Error: "Tool execution failed"

**Síntomas**:
```python
ToolExecutionError: Error executing tool 'nombre_tool'
```

**Soluciones**:

```python
# 1. Agregar manejo de errores en la herramienta
from crewai.tools import tool

@tool("Mi Herramienta")
def mi_herramienta(parametro: str) -> str:
    """Descripción de la herramienta"""
    try:
        # Tu lógica aquí
        resultado = hacer_algo(parametro)
        return f"✅ Éxito: {resultado}"
    except ValueError as e:
        return f"❌ Error de valor: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 2. Validar parámetros
@tool("Calculadora")
def calculadora(operacion: str) -> str:
    """Realiza operaciones matemáticas"""
    # Validar entrada
    if not operacion or not isinstance(operacion, str):
        return "❌ Error: Se requiere una operación válida"
    
    # Validar caracteres permitidos
    permitidos = set("0123456789+-*/().")
    if not set(operacion.replace(" ", "")).issubset(permitidos):
        return "❌ Error: Caracteres no permitidos en la operación"
    
    try:
        resultado = eval(operacion)
        return f"Resultado: {resultado}"
    except Exception as e:
        return f"❌ Error al calcular: {str(e)}"

# 3. Logging detallado
import logging

@tool("Mi Tool")
def mi_tool(param: str) -> str:
    logger = logging.getLogger(__name__)
    logger.info(f"Ejecutando tool con parámetro: {param}")
    
    try:
        result = proceso(param)
        logger.info(f"Tool exitoso: {result}")
        return result
    except Exception as e:
        logger.error(f"Tool falló: {e}", exc_info=True)
        return f"Error: {e}"
```

## Problemas de Memoria

### Error: "Out of memory"

**Síntomas**: El proceso se cierra o se vuelve muy lento

**Soluciones**:

```python
# 1. Limpiar historial de tareas
import gc

# Después de cada ejecución
resultado = crew.kickoff()
# Procesar resultado
gc.collect()  # Forzar recolección de basura

# 2. Limitar agentes concurrentes
agents:
  max_concurrent: 3  # Reducir

# 3. Descargar modelos no usados
# Evitar cargar múltiples modelos grandes simultáneamente

# 4. Usar generadores en lugar de listas grandes
def procesar_documentos():
    for doc in documentos:
        yield procesar(doc)  # Genera uno a la vez
```

## Problemas de Logs

### Problema: Logs no aparecen

**Soluciones**:

```python
# 1. Verificar configuración de logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 2. Habilitar verbose en agentes
agent = Agent(
    ...,
    verbose=True  # ← Importante
)

# 3. Verificar nivel de log
import os
os.environ['LOG_LEVEL'] = 'DEBUG'

# 4. Forzar flush de logs
import sys
sys.stdout.flush()
```

## Checklist de Diagnóstico Rápido

Cuando algo falla, verifica en orden:

- [ ] ¿Está activado el entorno virtual?
- [ ] ¿Existe el archivo .env con OPENAI_API_KEY?
- [ ] ¿La API key es válida?
- [ ] ¿Hay créditos en la cuenta de OpenAI?
- [ ] ¿Hay conexión a internet?
- [ ] ¿El firewall permite HTTPS saliente?
- [ ] ¿Los agentes tienen verbose=True para debugging?
- [ ] ¿Las tareas tienen expected_output claro?
- [ ] ¿Los nombres de variables/funciones son correctos?
- [ ] ¿Hay errores en los logs?

## Recursos Adicionales

- Logs detallados: Habilitar `verbose=True` en todo
- Documentación oficial: https://docs.crewai.com
- Issues de GitHub: https://github.com/joaomdmoura/crewAI/issues
- Discord de CrewAI: Para soporte de la comunidad

## Próximos Pasos

Si el problema persiste:
1. Consulta `02_diagnostico_sistema.md` para herramientas de diagnóstico avanzadas
2. Revisa `03_mantenimiento_rutinario.md` para prevención de problemas
3. Consulta `04_recuperacion_errores.md` para recuperación ante fallos críticos

