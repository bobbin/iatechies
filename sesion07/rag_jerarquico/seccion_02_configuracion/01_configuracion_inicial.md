# Configuración Inicial del Sistema CrewAI

## Introducción

Después de completar la instalación, es fundamental configurar correctamente el sistema para tu entorno específico. Esta guía te llevará paso a paso a través de la configuración inicial.

**Tiempo estimado**: 20-30 minutos  
**Nivel**: Intermedio  
**Prerrequisitos**: Instalación básica completada (`seccion_01_instalacion/02_instalacion_basica.md`)

## Estructura de Configuración

El sistema CrewAI utiliza una estructura de configuración en capas:

```
proyecto/
├── .env                      # Variables de entorno (secretos)
├── config.yaml              # Configuración principal
├── agents/
│   └── agents_config.yaml   # Configuración de agentes
├── logging/
│   └── logging_config.yaml  # Configuración de logs
└── data/
    └── cache/               # Caché de respuestas
```

## Paso 1: Configuración de Variables de Entorno (.env)

### 1.1 Crear Archivo .env

El archivo `.env` contiene información sensible y no debe versionarse.

```bash
# Crear .env si no existe
touch .env
```

### 1.2 Variables Obligatorias

```env
# ============================================
# CONFIGURACIÓN OBLIGATORIA
# ============================================

# API Keys
OPENAI_API_KEY=sk-tu-api-key-aqui

# Configuración del Sistema
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 1.3 Variables Recomendadas

```env
# ============================================
# CONFIGURACIÓN RECOMENDADA
# ============================================

# Modelos por Defecto
DEFAULT_MODEL=gpt-4-turbo-preview
DEFAULT_TEMPERATURE=0.7
MAX_TOKENS=4000

# Límites y Timeouts
REQUEST_TIMEOUT=60
MAX_RETRIES=3
MAX_AGENTS_CONCURRENT=10

# Caché
ENABLE_CACHE=true
CACHE_TTL=3600
CACHE_DIR=./data/cache

# Logging
LOG_FILE=./logs/crewai.log
LOG_FORMAT=json
LOG_ROTATION=daily
```

### 1.4 Variables Opcionales (Avanzadas)

```env
# ============================================
# CONFIGURACIÓN OPCIONAL
# ============================================

# Proveedores Alternativos
ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
OPENAI_ORG_ID=org-tu-organizacion

# Base de Datos Vectorial
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=./data/vectordb
VECTOR_DB_COLLECTION=crewai_docs

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
PROMETHEUS_ENABLED=false

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Seguridad
SECRET_KEY=tu-secret-key-aqui-generada
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## Paso 2: Configuración Principal (config.yaml)

### 2.1 Crear config.yaml

```yaml
# ============================================
# CONFIGURACIÓN GENERAL DEL SISTEMA
# ============================================
system:
  name: "Mi Sistema CrewAI"
  version: "1.0.0"
  environment: ${ENVIRONMENT}  # Referencia a variable de entorno
  debug: false

# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================
logging:
  level: ${LOG_LEVEL}
  format: ${LOG_FORMAT}
  file: ${LOG_FILE}
  rotation: ${LOG_ROTATION}
  max_size_mb: 100
  backup_count: 7
  console_output: true
  
# ============================================
# CONFIGURACIÓN DE AGENTES
# ============================================
agents:
  max_concurrent: ${MAX_AGENTS_CONCURRENT}
  default_timeout: 300
  retry_attempts: ${MAX_RETRIES}
  verbose: true
  allow_delegation: false
  
# ============================================
# CONFIGURACIÓN DE LLM
# ============================================
llm:
  provider: "openai"
  model: ${DEFAULT_MODEL}
  temperature: ${DEFAULT_TEMPERATURE}
  max_tokens: ${MAX_TOKENS}
  timeout: ${REQUEST_TIMEOUT}
  
  # Configuración de reintentos
  retry:
    max_attempts: ${MAX_RETRIES}
    backoff_factor: 2
    max_wait: 60
    
  # Fallback models
  fallback_models:
    - "gpt-4-turbo-preview"
    - "gpt-3.5-turbo"

# ============================================
# CONFIGURACIÓN DE CACHÉ
# ============================================
cache:
  enabled: ${ENABLE_CACHE}
  ttl: ${CACHE_TTL}
  directory: ${CACHE_DIR}
  max_size_mb: 500
  strategy: "lru"  # least-recently-used
  
# ============================================
# CONFIGURACIÓN DE HERRAMIENTAS
# ============================================
tools:
  web_search:
    enabled: true
    provider: "duckduckgo"
    max_results: 10
    
  file_operations:
    enabled: true
    allowed_paths:
      - "./data"
      - "./output"
    max_file_size_mb: 10
    
# ============================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================
security:
  api_key_rotation_days: 90
  max_request_size_mb: 10
  allowed_origins: ${ALLOWED_ORIGINS}
  rate_limiting:
    enabled: true
    per_minute: ${RATE_LIMIT_PER_MINUTE}
    per_hour: ${RATE_LIMIT_PER_HOUR}
```

## Paso 3: Configuración de Agentes

### 3.1 Crear agents_config.yaml

```yaml
# ============================================
# CONFIGURACIÓN DE AGENTES PREDEFINIDOS
# ============================================

agents:
  # Agente Investigador
  researcher:
    role: "Investigador Senior"
    goal: "Investigar y recopilar información precisa sobre temas asignados"
    backstory: |
      Eres un investigador con 20 años de experiencia en análisis de información.
      Tu especialidad es encontrar datos relevantes, verificar fuentes y 
      presentar hallazgos de forma estructurada.
    verbose: true
    allow_delegation: true
    max_iterations: 5
    tools:
      - web_search
      - file_read
    llm:
      model: "gpt-4-turbo-preview"
      temperature: 0.3  # Más factual
      
  # Agente Analista
  analyst:
    role: "Analista de Datos"
    goal: "Analizar información y extraer insights significativos"
    backstory: |
      Eres un analista experto en procesar grandes volúmenes de información.
      Identificas patrones, tendencias y anomalías con precisión.
    verbose: true
    allow_delegation: false
    max_iterations: 3
    tools:
      - data_analysis
      - visualization
    llm:
      model: "gpt-4-turbo-preview"
      temperature: 0.5
      
  # Agente Escritor
  writer:
    role: "Escritor Profesional"
    goal: "Crear contenido claro, bien estructurado y persuasivo"
    backstory: |
      Eres un escritor con experiencia en múltiples formatos y estilos.
      Transformas información compleja en contenido accesible y atractivo.
    verbose: true
    allow_delegation: false
    max_iterations: 3
    tools:
      - grammar_check
      - style_analysis
    llm:
      model: "gpt-4-turbo-preview"
      temperature: 0.7  # Más creativo
      
  # Agente Revisor
  reviewer:
    role: "Editor y Revisor"
    goal: "Asegurar la calidad, precisión y coherencia del contenido"
    backstory: |
      Eres un editor meticuloso con ojo crítico para detalles.
      Tu misión es elevar la calidad de todo contenido que revisas.
    verbose: true
    allow_delegation: false
    max_iterations: 2
    tools:
      - spell_check
      - fact_check
    llm:
      model: "gpt-4-turbo-preview"
      temperature: 0.2  # Muy objetivo

# ============================================
# TEMPLATES DE TAREAS
# ============================================

task_templates:
  research:
    description: "Investigar sobre {topic} y recopilar información relevante"
    expected_output: "Informe de investigación con fuentes citadas"
    
  analysis:
    description: "Analizar {data} y extraer insights clave"
    expected_output: "Análisis detallado con conclusiones"
    
  writing:
    description: "Escribir {content_type} sobre {topic}"
    expected_output: "Contenido completo y bien estructurado"
    
  review:
    description: "Revisar {content} para calidad y precisión"
    expected_output: "Versión revisada con mejoras sugeridas"
```

## Paso 4: Configuración de Logging

### 4.1 Crear logging_config.yaml

```yaml
# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================

version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    
  json:
    format: '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s"}'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
    
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: ./logs/crewai.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: ./logs/errors.log
    maxBytes: 10485760
    backupCount: 3
    
  json_file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: json
    filename: ./logs/crewai.json
    maxBytes: 10485760
    backupCount: 5

loggers:
  crewai:
    level: DEBUG
    handlers: [console, file, error_file]
    propagate: false
    
  openai:
    level: WARNING
    handlers: [file]
    propagate: false

root:
  level: INFO
  handlers: [console, file, json_file]
```

## Paso 5: Cargar Configuración en Python

### 5.1 Crear módulo config.py

```python
"""
Módulo de configuración para CrewAI
Carga y valida la configuración desde archivos
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# Cargar variables de entorno
load_dotenv()

# Directorio base
BASE_DIR = Path(__file__).parent
CONFIG_DIR = BASE_DIR / "config"

class ConfigLoader:
    """Cargador de configuración con expansión de variables de entorno"""
    
    def __init__(self):
        self.config = {}
        
    def load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Carga un archivo YAML"""
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def expand_env_vars(self, value: Any) -> Any:
        """Expande variables de entorno en formato ${VAR}"""
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]
            return os.getenv(var_name, value)
        elif isinstance(value, dict):
            return {k: self.expand_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.expand_env_vars(item) for item in value]
        return value
    
    def load_all(self):
        """Carga toda la configuración"""
        # Configuración principal
        main_config = self.load_yaml(BASE_DIR / "config.yaml")
        self.config = self.expand_env_vars(main_config)
        
        # Configuración de agentes
        agents_config = self.load_yaml(BASE_DIR / "agents" / "agents_config.yaml")
        self.config['agents_definitions'] = self.expand_env_vars(agents_config)
        
        return self.config

# Instancia global
config_loader = ConfigLoader()
config = config_loader.load_all()

# Acceso rápido a configuraciones comunes
SYSTEM_CONFIG = config.get('system', {})
LLM_CONFIG = config.get('llm', {})
CACHE_CONFIG = config.get('cache', {})
AGENTS_CONFIG = config.get('agents', {})
```

### 5.2 Usar configuración en tu aplicación

```python
from config import config, SYSTEM_CONFIG, LLM_CONFIG

# Acceder a configuración
print(f"Sistema: {SYSTEM_CONFIG['name']}")
print(f"Modelo: {LLM_CONFIG['model']}")
print(f"Temperatura: {LLM_CONFIG['temperature']}")

# Usar en agentes
from crewai import Agent

agent = Agent(
    role="Investigador",
    goal="Investigar temas",
    backstory="Experto en investigación",
    verbose=AGENTS_CONFIG['verbose']
)
```

## Paso 6: Inicialización del Sistema

### 6.1 Crear script de inicialización

```python
"""
Script de inicialización del sistema CrewAI
Ejecutar antes de usar el sistema
"""

import os
import sys
import logging
from pathlib import Path
from config import config, config_loader

def create_directories():
    """Crear directorios necesarios"""
    directories = [
        'logs',
        'data/cache',
        'data/vectordb',
        'output'
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {dir_path}")

def setup_logging():
    """Configurar sistema de logging"""
    import logging.config
    
    logging_config = config_loader.load_yaml(Path('logging/logging_config.yaml'))
    logging.config.dictConfig(logging_config)
    
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging inicializado")
    print("✅ Logging configurado")

def validate_config():
    """Validar configuración"""
    errors = []
    
    # Validar API Key
    if not os.getenv('OPENAI_API_KEY'):
        errors.append("OPENAI_API_KEY no configurada")
    
    # Validar archivos de configuración
    required_files = [
        'config.yaml',
        'agents/agents_config.yaml',
        'logging/logging_config.yaml'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Archivo faltante: {file_path}")
    
    if errors:
        print("\n❌ Errores de configuración:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✅ Configuración válida")

def initialize_cache():
    """Inicializar sistema de caché"""
    cache_config = config.get('cache', {})
    
    if cache_config.get('enabled'):
        cache_dir = Path(cache_config.get('directory', './data/cache'))
        cache_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Caché inicializado: {cache_dir}")

def main():
    """Función principal de inicialización"""
    print("\n" + "="*60)
    print("🚀 INICIALIZANDO SISTEMA CREWAI")
    print("="*60 + "\n")
    
    try:
        print("1. Creando directorios...")
        create_directories()
        
        print("\n2. Validando configuración...")
        validate_config()
        
        print("\n3. Configurando logging...")
        setup_logging()
        
        print("\n4. Inicializando caché...")
        initialize_cache()
        
        print("\n" + "="*60)
        print("✅ SISTEMA INICIALIZADO CORRECTAMENTE")
        print("="*60)
        print(f"\nSistema: {config['system']['name']}")
        print(f"Versión: {config['system']['version']}")
        print(f"Entorno: {config['system']['environment']}")
        print("\n¡Listo para usar!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 6.2 Ejecutar inicialización

```bash
python init_system.py
```

## Paso 7: Verificación Post-Configuración

### Script de verificación

```python
import os
from config import config

def verify_setup():
    checks = []
    
    # Verificar archivos
    checks.append(("Archivo .env", os.path.exists('.env')))
    checks.append(("Archivo config.yaml", os.path.exists('config.yaml')))
    checks.append(("API Key", bool(os.getenv('OPENAI_API_KEY'))))
    checks.append(("Directorio logs", os.path.exists('logs')))
    checks.append(("Directorio data", os.path.exists('data')))
    
    # Verificar configuración cargada
    checks.append(("Config cargada", bool(config)))
    checks.append(("LLM configurado", 'llm' in config))
    checks.append(("Agentes configurados", 'agents' in config))
    
    print("\n📋 VERIFICACIÓN DE CONFIGURACIÓN\n")
    for name, passed in checks:
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {name}")
    
    all_passed = all(passed for _, passed in checks)
    
    if all_passed:
        print("\n🎉 ¡Configuración completa y válida!")
    else:
        print("\n⚠️  Algunos checks fallaron. Revisa la configuración.")
    
    return all_passed

if __name__ == "__main__":
    verify_setup()
```

## Configuraciones por Entorno

### Desarrollo (.env.development)

```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEFAULT_MODEL=gpt-3.5-turbo
ENABLE_CACHE=false
MAX_AGENTS_CONCURRENT=3
```

### Producción (.env.production)

```env
ENVIRONMENT=production
LOG_LEVEL=INFO
DEFAULT_MODEL=gpt-4-turbo-preview
ENABLE_CACHE=true
MAX_AGENTS_CONCURRENT=20
REQUEST_TIMEOUT=120
ENABLE_METRICS=true
```

## Próximos Pasos

Después de completar la configuración inicial:

1. **Gestionar variables de entorno**: `02_variables_entorno.md`
2. **Comenzar a usar el sistema**: `seccion_03_uso/01_primeros_pasos.md`
3. **Configuraciones avanzadas**: Consultar documentación específica

¡Tu sistema está configurado y listo para usar!

