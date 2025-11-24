# Requisitos del Sistema - CrewAI Multi-Agente

## Introducción

Antes de instalar el Sistema de Gestión Multi-Agente con CrewAI, es fundamental verificar que tu entorno cumple con los requisitos necesarios. Este documento detalla todos los requisitos de hardware, software y conectividad.

## Requisitos de Hardware

### Procesador (CPU)

**Mínimo**: 
- 4 núcleos físicos a 2.0 GHz
- Arquitectura x86_64 (64-bit)
- Compatible con SSE4.2 o superior

**Recomendado**: 
- 8+ núcleos físicos a 3.0 GHz o superior
- Procesadores Intel Core i7/i9 o AMD Ryzen 7/9
- Soporte para virtualización (Intel VT-x / AMD-V)

**Producción**: 
- 16+ núcleos con soporte para threading
- Procesadores XEON o EPYC para servidores
- Mínimo 3.5 GHz en modo turbo

**Justificación**: El sistema multi-agente ejecuta múltiples procesos en paralelo. Cada agente puede consumir un hilo de CPU independiente, especialmente durante el procesamiento de tareas concurrentes. Un CPU con más núcleos permite ejecutar más agentes simultáneamente sin degradación de rendimiento.

### Memoria RAM

**Mínimo**: 8 GB RAM
- Suficiente para 2-3 agentes concurrentes
- Desarrollo y pruebas básicas

**Recomendado**: 16 GB RAM
- Permite ejecutar 5-10 agentes simultáneamente
- Incluye margen para el sistema operativo y otras aplicaciones

**Producción**: 32 GB RAM o superior
- Soporta 15+ agentes concurrentes
- Permite caché de modelos y datos en memoria
- Margen para picos de carga

**Consideraciones importantes**:
- Cada agente consume aproximadamente 500 MB - 2 GB de RAM dependiendo de:
  - Complejidad de las tareas asignadas
  - Cantidad de herramientas (tools) que utiliza
  - Tamaño del contexto de conversación
  - Uso de memoria caché
- Los modelos de lenguaje grandes (LLMs) pueden requerir memoria adicional si se ejecutan localmente
- Se recomienda tener al menos 4 GB libres para el sistema operativo
- Considera usar swap/pagefile de al menos 8 GB adicionales

### Almacenamiento

**Mínimo**: 20 GB de espacio libre
- 5 GB para instalación base
- 10 GB para logs y datos temporales
- 5 GB de margen operativo

**Recomendado**: 50 GB de espacio libre (SSD recomendado)
- Instalación base: ~5 GB
- Modelos de lenguaje locales (opcional): 10-50 GB
- Logs y datos de sesión: Variable
- Base de datos vectorial: Variable según volumen
- Caché de respuestas: 2-5 GB

**Producción**: 100 GB+ con SSD NVMe
- Mayor velocidad de lectura/escritura reduce latencia
- Espacio para backups locales
- Logs históricos y auditoría

**Desglose detallado del uso**:
```
/opt/crewai/
├── venv/              (2-3 GB)    - Entorno virtual Python
├── models/            (0-50 GB)   - Modelos locales opcionales
├── logs/              (1-10 GB)   - Logs del sistema
├── cache/             (2-5 GB)    - Caché de respuestas
├── data/              (Variable)  - Datos de usuario
└── backups/           (Variable)  - Copias de seguridad
```

**Recomendación de tipo de disco**:
- **HDD**: Aceptable para desarrollo, puede causar lentitud en I/O
- **SATA SSD**: Bueno para producción pequeña-mediana
- **NVMe SSD**: Recomendado para producción de alto rendimiento

### Requisitos de Red

**Ancho de banda mínimo**: 10 Mbps
- Suficiente para llamadas API básicas
- Puede experimentar lentitud con tareas complejas

**Recomendado**: 100 Mbps o superior
- Permite múltiples llamadas API simultáneas
- Reduce latencia en respuestas
- Soporta streaming de respuestas

**Latencia**: 
- < 100ms para APIs externas (OpenAI, Anthropic)
- < 50ms para bases de datos locales
- < 20ms para comunicación entre nodos en cluster

**Requisitos de conectividad**:
- Acceso a internet para APIs de modelos de lenguaje
- Conexión estable (uptime > 99%)
- Firewall configurado para permitir:
  - Conexiones HTTPS salientes (puerto 443)
  - Conexiones HTTP salientes (puerto 80)
  - WebSocket si se usa streaming
- IPs de APIs permitidas en whitelist

## Requisitos de Software

### Sistema Operativo

**Sistemas soportados**:

**Windows**:
- Windows 10 (64-bit) - Build 1903 o superior
- Windows 11 (64-bit)
- Windows Server 2019 o 2022

**Linux** (Recomendado para producción):
- Ubuntu 20.04 LTS / 22.04 LTS / 24.04 LTS
- Debian 11 (Bullseye) / 12 (Bookworm)
- CentOS Stream 8 / 9
- Red Hat Enterprise Linux (RHEL) 8+
- Amazon Linux 2 / Amazon Linux 2023
- Arch Linux (rolling release)

**macOS**:
- macOS 11 (Big Sur) o superior
- macOS 12 (Monterey)
- macOS 13 (Ventura)
- macOS 14 (Sonoma)

**Nota**: Los comandos y paths pueden variar según el sistema operativo. La documentación proporciona ejemplos para cada plataforma.

### Python

**Versión requerida**: Python 3.9 o superior
**Versión recomendada**: Python 3.11 o Python 3.12

**Por qué estas versiones**:
- Python 3.9+: Requerido por CrewAI y sus dependencias
- Python 3.11: Ofrece mejoras de rendimiento (10-25% más rápido)
- Python 3.12: Última versión estable con características modernas

**Verificación**:
```bash
python --version  # Debe mostrar 3.9 o superior
python3 --version # En sistemas con múltiples versiones
```

**Gestor de paquetes**:
- **pip**: Versión 23.0+ requerida
- **uv**: Alternativa moderna más rápida (opcional)

```bash
pip --version     # Debe mostrar 23.0 o superior
python -m pip install --upgrade pip  # Actualizar pip
```

### Dependencias del Sistema

**Build Tools** (Requeridos para compilar algunas dependencias):

**Windows**:
- Visual Studio Build Tools 2019 o superior
- Windows SDK
- Descargar desde: https://visualstudio.microsoft.com/downloads/

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev
```

**Linux (CentOS/RHEL)**:
```bash
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

**macOS**:
```bash
xcode-select --install
```

**Otras dependencias del sistema**:

**Git** (Requerido):
- Versión 2.30+ para control de versiones
- Instalación:
  - Windows: https://git-scm.com/download/win
  - Linux: `sudo apt-get install git`
  - macOS: `brew install git`

**OpenSSL** (Requerido):
- Versión 1.1.1+ para conexiones seguras HTTPS
- Generalmente ya instalado en sistemas modernos
- Verificar: `openssl version`

**curl** (Recomendado):
- Para descargas y verificación de conectividad
- Instalado por defecto en la mayoría de sistemas

## Dependencias de Python

### Librerías Core (Obligatorias)

Estas librerías se instalan automáticamente con CrewAI:

```
crewai >= 0.28.8        # Framework principal multi-agente
crewai-tools >= 0.1.6   # Herramientas para agentes
openai >= 1.12.0        # Cliente oficial OpenAI API
python-dotenv >= 1.0.0  # Gestión de variables de entorno
pydantic >= 2.0.0       # Validación de datos y modelos
httpx >= 0.25.0         # Cliente HTTP asíncrono
tenacity >= 8.2.0       # Reintentos automáticos
jsonschema >= 4.17.0    # Validación de esquemas JSON
```

**Instalación básica**:
```bash
pip install crewai crewai-tools openai python-dotenv pydantic
```

### Librerías Opcionales (Según Caso de Uso)

**Para usar Claude (Anthropic)**:
```bash
pip install anthropic>=0.18.0
```

**Para RAG y búsqueda vectorial**:
```bash
pip install chromadb>=0.4.22        # Base de datos vectorial local
pip install faiss-cpu>=1.7.4        # Alternativa FAISS
pip install sentence-transformers   # Embeddings
```

**Para herramientas avanzadas**:
```bash
pip install langchain>=0.1.10       # Herramientas adicionales
pip install beautifulsoup4          # Web scraping
pip install requests                # HTTP requests
```

**Para procesamiento de documentos**:
```bash
pip install pypdf                   # Leer PDFs
pip install python-docx             # Leer Word
pip install openpyxl               # Leer Excel
```

**Para conteo de tokens**:
```bash
pip install tiktoken>=0.6.0
```

## APIs y Servicios Externos

### OpenAI API (Recomendado)

**Requisitos**:
- Cuenta activa en https://platform.openai.com
- API Key válida
- Créditos o método de pago configurado

**Modelos soportados**:
- `gpt-4-turbo-preview` (Recomendado)
- `gpt-4` (Más potente, más costoso)
- `gpt-3.5-turbo` (Más económico)

**Costo estimado** (a fecha de redacción):
- GPT-4 Turbo: ~$0.01 por cada 1K tokens entrada, ~$0.03 salida
- GPT-3.5 Turbo: ~$0.0005 por cada 1K tokens entrada, ~$0.0015 salida

**Obtener API Key**:
1. Registrarse en https://platform.openai.com
2. Ir a "API Keys"
3. Click en "Create new secret key"
4. Copiar la key (se muestra solo una vez)
5. Configurar créditos o método de pago

### Anthropic Claude API (Alternativa)

**Requisitos**:
- Cuenta en https://console.anthropic.com
- API Key de Claude
- Acceso aprobado (puede requerir lista de espera)

**Modelos soportados**:
- `claude-3-opus-20240229` (Más potente)
- `claude-3-sonnet-20240229` (Balanceado)
- `claude-3-haiku-20240307` (Más rápido)

### Otros Servicios Opcionales

**Bases de datos vectoriales en la nube**:
- Pinecone: https://www.pinecone.io
- Weaviate: https://weaviate.io
- Qdrant: https://qdrant.tech

**Almacenamiento en la nube**:
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

## Requisitos de Seguridad

### Certificados SSL/TLS

- Certificados válidos para conexiones HTTPS
- Certificados de cliente si se requiere autenticación mutua
- Sistema de gestión de certificados actualizado

### Gestión de Secretos

**Requerido**:
- Sistema para almacenar API keys de forma segura
- Variables de entorno o gestor de secretos
- Permisos de archivo restringidos

**Opciones**:
- Archivo `.env` con permisos 600 (desarrollo)
- HashiCorp Vault (producción)
- AWS Secrets Manager (cloud)
- Azure Key Vault (cloud)
- Google Secret Manager (cloud)

### Firewall y Seguridad de Red

**Puertos requeridos**:
- 443 (HTTPS) - Salida para APIs
- 80 (HTTP) - Salida opcional para redirecciones

**Configuraciones**:
- Permitir conexiones salientes a:
  - api.openai.com
  - api.anthropic.com
  - Otros servicios utilizados
- Reglas de firewall para comunicación interna en clusters
- VPN si se requiere acceso a recursos privados

## Verificación Rápida de Requisitos

Ejecuta este script para verificar tu sistema:

```python
import sys
import platform
import subprocess

print("=== VERIFICACIÓN DE REQUISITOS ===\n")

# Python
print(f"✓ Python: {sys.version}")
print(f"✓ SO: {platform.system()} {platform.release()}")
print(f"✓ Arquitectura: {platform.machine()}")

# Memoria (requiere psutil)
try:
    import psutil
    mem = psutil.virtual_memory()
    print(f"✓ RAM Total: {mem.total / (1024**3):.2f} GB")
    print(f"✓ RAM Disponible: {mem.available / (1024**3):.2f} GB")
except ImportError:
    print("⚠ Instala psutil para ver info de RAM: pip install psutil")

# Verificar pip
try:
    result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
    print(f"✓ {result.stdout.strip()}")
except:
    print("✗ pip no encontrado")

print("\n=== VERIFICACIÓN COMPLETADA ===")
```

## Próximos Pasos

Si tu sistema cumple con todos los requisitos:
1. Continúa con la **Instalación Básica**: `02_instalacion_basica.md`
2. Si necesitas configuración avanzada: `03_instalacion_avanzada.md`
3. Verifica tu instalación: `04_verificacion_instalacion.md`

Si NO cumples algún requisito:
- Actualiza tu hardware/software según sea necesario
- Consulta la sección de Troubleshooting para alternativas
- Considera usar entornos cloud si tu hardware local es insuficiente

