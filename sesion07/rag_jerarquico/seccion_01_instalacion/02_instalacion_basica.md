# Instalación Básica - Guía Paso a Paso

## Introducción

Esta guía te llevará paso a paso a través de la instalación básica del Sistema de Gestión Multi-Agente con CrewAI. Está diseñada para usuarios que instalan el sistema por primera vez y buscan una configuración funcional rápidamente.

**Tiempo estimado**: 15-30 minutos  
**Nivel**: Principiante  
**Prerrequisitos**: Haber verificado los requisitos del sistema (`01_requisitos_sistema.md`)

## Paso 1: Preparación del Entorno

### 1.1 Verificar Python

Primero, verifica que tienes Python 3.9+ instalado:

```bash
python --version
```

**Resultado esperado**: `Python 3.9.x`, `3.10.x`, `3.11.x` o `3.12.x`

**Si no tienes Python instalado**:

**Windows**:
1. Descarga Python desde https://www.python.org/downloads/
2. Ejecuta el instalador
3. ✅ **IMPORTANTE**: Marca "Add Python to PATH"
4. Selecciona "Install Now"
5. Reinicia el terminal después de instalar

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

**macOS**:
```bash
# Usando Homebrew
brew install python3
```

### 1.2 Crear Directorio del Proyecto

Crea un directorio para tu proyecto:

```bash
# Windows PowerShell
New-Item -ItemType Directory -Path C:\Users\TuUsuario\crewai_proyecto
cd C:\Users\TuUsuario\crewai_proyecto

# Linux/macOS
mkdir ~/crewai_proyecto
cd ~/crewai_proyecto
```

### 1.3 Crear Entorno Virtual (Recomendado)

Un entorno virtual aísla las dependencias de tu proyecto:

```bash
# Crear entorno virtual
python -m venv venv_crewai

# Activar entorno virtual
# Windows PowerShell:
.\venv_crewai\Scripts\Activate.ps1

# Windows CMD:
venv_crewai\Scripts\activate.bat

# Linux/macOS:
source venv_crewai/bin/activate
```

**Verificar activación**: Verás `(venv_crewai)` al inicio de tu prompt.

**Si hay error de permisos en Windows**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.4 Actualizar pip

Asegúrate de tener la última versión de pip:

```bash
python -m pip install --upgrade pip
```

**Resultado esperado**: `Successfully installed pip-23.x.x`

## Paso 2: Instalación de Dependencias Base

### 2.1 Instalar CrewAI y Herramientas

Instala los paquetes principales:

```bash
pip install crewai crewai-tools
```

**Esto instalará**:
- `crewai`: Framework principal
- `crewai-tools`: Herramientas para agentes
- Todas las dependencias necesarias (openai, pydantic, etc.)

**Tiempo estimado**: 2-5 minutos

**Verificar instalación**:
```bash
pip list | grep crewai
# O en Windows:
pip list | Select-String "crewai"
```

**Resultado esperado**:
```
crewai            0.28.8
crewai-tools      0.1.6
```

### 2.2 Instalar Cliente OpenAI (ya incluido)

El cliente de OpenAI se instala automáticamente con CrewAI, pero puedes verificar:

```bash
pip show openai
```

### 2.3 Instalar Utilidades Adicionales

Instala herramientas útiles:

```bash
pip install python-dotenv pydantic
```

- `python-dotenv`: Para gestionar variables de entorno desde archivo .env
- `pydantic`: Para validación de datos (ya incluido con CrewAI)

### 2.4 Guardar Dependencias

Guarda las dependencias instaladas:

```bash
pip freeze > requirements.txt
```

Esto crea un archivo `requirements.txt` que lista todas las librerías instaladas.

## Paso 3: Configuración Inicial

### 3.1 Crear Archivo de Configuración

Crea un archivo llamado `.env` en el directorio raíz de tu proyecto:

```bash
# Windows PowerShell
New-Item -ItemType File -Path .env

# Linux/macOS
touch .env
```

### 3.2 Configurar API Key de OpenAI

Edita el archivo `.env` y agrega tu API key:

```env
# Archivo .env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

**Reemplaza** `sk-tu-api-key-aqui` con tu API key real de OpenAI.

**⚠️ IMPORTANTE**: 
- Nunca compartas tu API key públicamente
- No subas el archivo .env a repositorios públicos
- Guárdalo de forma segura

### 3.3 Obtener API Key de OpenAI

**Si no tienes una API key**:

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Haz clic en "Create new secret key"
4. Dale un nombre descriptivo (ej: "CrewAI Development")
5. **Copia la key inmediatamente** (se muestra solo una vez)
6. Pégala en tu archivo `.env`

**Configurar método de pago**:
- Ve a https://platform.openai.com/account/billing
- Agrega créditos o una tarjeta de crédito
- Configura límites de gasto para evitar sorpresas

### 3.4 Proteger el Archivo .env

**Linux/macOS**:
```bash
chmod 600 .env
```

**Windows**:
```powershell
# Ocultar el archivo
attrib +h .env
```

### 3.5 Crear .gitignore

Si usas Git, crea un archivo `.gitignore`:

```bash
# Archivo .gitignore
.env
venv_crewai/
__pycache__/
*.pyc
.DS_Store
```

## Paso 4: Crear Proyecto de Prueba

### 4.1 Estructura de Directorios

Tu proyecto debería verse así:

```
crewai_proyecto/
├── .env                 # Variables de entorno (API keys)
├── .gitignore          # Archivos a ignorar en Git
├── requirements.txt    # Dependencias
├── main.py            # Script principal (crearemos ahora)
└── venv_crewai/       # Entorno virtual
```

### 4.2 Script de Prueba Básico

Crea un archivo `main.py` con el siguiente contenido:

```python
"""
Script de prueba básico para verificar instalación de CrewAI
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Cargar variables de entorno desde .env
load_dotenv()

# Verificar que la API key está configurada
if not os.getenv('OPENAI_API_KEY'):
    print("❌ ERROR: OPENAI_API_KEY no configurada en .env")
    exit(1)

print("✅ API Key cargada correctamente")
print("\n" + "="*60)
print("🚀 Iniciando prueba de CrewAI")
print("="*60 + "\n")

# Crear un agente simple
agente_prueba = Agent(
    role="Asistente de Prueba",
    goal="Responder preguntas de forma útil y concisa",
    backstory="""Eres un asistente amigable que ayuda a los usuarios.
    Tu especialidad es proporcionar información clara y precisa.""",
    verbose=True,  # Muestra el proceso de pensamiento del agente
    allow_delegation=False
)

# Crear una tarea simple
tarea_prueba = Task(
    description="Explica qué es un sistema multi-agente en una oración breve y clara.",
    agent=agente_prueba,
    expected_output="Una oración explicando sistemas multi-agente"
)

# Crear el equipo (crew)
equipo = Crew(
    agents=[agente_prueba],
    tasks=[tarea_prueba],
    process=Process.sequential,  # Las tareas se ejecutan en orden
    verbose=True
)

# Ejecutar
if __name__ == "__main__":
    print("📋 Tarea asignada al agente...\n")
    
    try:
        resultado = equipo.kickoff()
        
        print("\n" + "="*60)
        print("✅ PRUEBA EXITOSA")
        print("="*60)
        print(f"\n📄 Resultado:\n{resultado}\n")
        print("="*60)
        print("\n🎉 ¡CrewAI está instalado y funcionando correctamente!")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR EN LA EJECUCIÓN")
        print("="*60)
        print(f"\nError: {str(e)}\n")
        print("Verifica:")
        print("1. Tu API key en .env es correcta")
        print("2. Tienes créditos en tu cuenta de OpenAI")
        print("3. Tu conexión a internet funciona")
```

### 4.3 Ejecutar el Script de Prueba

Ejecuta el script:

```bash
python main.py
```

**Resultado esperado**:

```
✅ API Key cargada correctamente

============================================================
🚀 Iniciando prueba de CrewAI
============================================================

📋 Tarea asignada al agente...

[Verás aquí el proceso del agente pensando y ejecutando]

============================================================
✅ PRUEBA EXITOSA
============================================================

📄 Resultado:
Un sistema multi-agente es un conjunto de agentes autónomos que colaboran para resolver tareas complejas.

============================================================

🎉 ¡CrewAI está instalado y funcionando correctamente!
```

## Paso 5: Verificación de Instalación

### 5.1 Verificar Imports

Crea un script `verificar.py`:

```python
import sys

print("Verificando imports...")

try:
    from crewai import Agent, Task, Crew, Process
    print("✅ crewai")
except ImportError as e:
    print(f"❌ crewai: {e}")
    sys.exit(1)

try:
    from crewai.tools import tool
    print("✅ crewai.tools")
except ImportError as e:
    print(f"❌ crewai.tools: {e}")

try:
    import openai
    print("✅ openai")
except ImportError as e:
    print(f"❌ openai: {e}")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv")
except ImportError as e:
    print(f"❌ python-dotenv: {e}")

try:
    import pydantic
    print("✅ pydantic")
except ImportError as e:
    print(f"❌ pydantic: {e}")

print("\n✅ Todas las importaciones exitosas")
```

Ejecuta:
```bash
python verificar.py
```

### 5.2 Verificar Conexión con OpenAI

Crea `verificar_openai.py`:

```python
import os
from dotenv import load_dotenv
import openai

load_dotenv()

print("Verificando conexión con OpenAI...")

try:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Listar modelos disponibles
    models = client.models.list()
    print(f"✅ Conexión exitosa con OpenAI")
    print(f"   Modelos disponibles: {len(list(models.data))}")
    
except openai.AuthenticationError:
    print("❌ API Key inválida")
    print("   Verifica tu OPENAI_API_KEY en .env")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

### 5.3 Checklist de Verificación

Verifica que has completado todo:

- [ ] Python 3.9+ instalado y verificado
- [ ] Entorno virtual creado y activado
- [ ] pip actualizado a versión 23+
- [ ] CrewAI y crewai-tools instalados
- [ ] Archivo .env creado con OPENAI_API_KEY
- [ ] Script de prueba ejecutado exitosamente
- [ ] Todas las importaciones funcionan
- [ ] Conexión con OpenAI verificada

## Solución de Problemas Comunes

### Error: "No module named 'crewai'"

**Causa**: El entorno virtual no está activado o CrewAI no está instalado.

**Solución**:
```bash
# 1. Activar entorno virtual
# Windows:
.\venv_crewai\Scripts\Activate.ps1
# Linux/macOS:
source venv_crewai/bin/activate

# 2. Reinstalar CrewAI
pip install --upgrade crewai crewai-tools
```

### Error: "OPENAI_API_KEY not found"

**Causa**: El archivo .env no existe o no contiene la API key.

**Solución**:
1. Verifica que el archivo `.env` existe en el directorio actual
2. Verifica que contiene: `OPENAI_API_KEY=sk-...`
3. Verifica que `load_dotenv()` se llama antes de usar la key

### Error: "Rate limit exceeded"

**Causa**: Has excedido el límite de requests de tu cuenta de OpenAI.

**Solución**:
1. Espera unos minutos antes de reintentar
2. Verifica tu plan en https://platform.openai.com/account/limits
3. Considera actualizar tu plan si lo necesitas

### Error: "Connection timeout"

**Causa**: Problemas de conectividad a internet o firewall.

**Solución**:
1. Verifica tu conexión a internet
2. Verifica que el firewall permite conexiones HTTPS salientes
3. Si usas proxy, configúralo:
   ```bash
   export HTTPS_PROXY=http://proxy:puerto
   ```

### Error: "Invalid API key"

**Causa**: La API key en .env es incorrecta.

**Solución**:
1. Verifica que copiaste la key completa
2. Verifica que no hay espacios extra
3. Regenera una nueva key en OpenAI si es necesario

## Próximos Pasos

Una vez completada la instalación básica:

1. **Configura tu entorno**: Lee `seccion_02_configuracion/01_configuracion_inicial.md`
2. **Aprende a usar el sistema**: Consulta `seccion_03_uso/01_primeros_pasos.md`
3. **Explora ejemplos avanzados**: Revisa los ejemplos en el repositorio

**Para instalaciones avanzadas**:
- Docker: `03_instalacion_avanzada.md`
- Producción: `03_instalacion_avanzada.md`
- Clusters: `03_instalacion_avanzada.md`

## Recursos Adicionales

- Documentación oficial de CrewAI: https://docs.crewai.com
- API de OpenAI: https://platform.openai.com/docs
- Comunidad en Discord: https://discord.gg/crewai
- Ejemplos en GitHub: https://github.com/joaomdmoura/crewAI-examples

---

**¡Felicidades!** Has completado la instalación básica de CrewAI. Ahora estás listo para crear tus propios sistemas multi-agente.

