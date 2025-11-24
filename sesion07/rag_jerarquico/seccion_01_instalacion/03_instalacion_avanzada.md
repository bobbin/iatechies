# Instalación Avanzada - Docker, Cloud y Producción

## Introducción

Esta guía cubre instalaciones avanzadas del Sistema de Gestión Multi-Agente para entornos de producción, contenedores Docker y despliegues en la nube.

**Nivel**: Avanzado  
**Audiencia**: DevOps, SysAdmins, Arquitectos de Software

## Instalación con Docker

### Dockerfile Optimizado

Crea un `Dockerfile` para tu aplicación CrewAI:

```dockerfile
FROM python:3.11-slim

# Metadata
LABEL maintainer="tu@email.com"
LABEL description="CrewAI Multi-Agent System"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para datos
RUN mkdir -p /app/data /app/logs

# Usuario no-root para seguridad
RUN useradd -m -u 1000 crewai && \
    chown -R crewai:crewai /app
USER crewai

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Puerto por defecto
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]
```

### Docker Compose para Desarrollo

Crea `docker-compose.yml`:

```yaml
version: '3.8'

services:
  crewai-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: crewai-system
    volumes:
      - ./:/app
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=development
      - LOG_LEVEL=INFO
    env_file:
      - .env
    ports:
      - "8000:8000"
    restart: unless-stopped
    networks:
      - crewai-network
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    container_name: crewai-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    networks:
      - crewai-network
    restart: unless-stopped

networks:
  crewai-network:
    driver: bridge

volumes:
  redis-data:
```

### Construcción y Ejecución

```bash
# Construir imagen
docker build -t crewai-system:latest .

# Ejecutar contenedor standalone
docker run -d \
  --name crewai-app \
  -e OPENAI_API_KEY=sk-tu-key \
  -v $(pwd)/data:/app/data \
  -p 8000:8000 \
  crewai-system:latest

# Con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f crewai-app

# Detener
docker-compose down
```

## Instalación en AWS

### AWS EC2 (Máquina Virtual)

**1. Crear instancia**:
```bash
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.large \
  --key-name mi-keypair \
  --security-group-ids sg-xxxxxxxx \
  --subnet-id subnet-xxxxxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=CrewAI-Production}]'
```

**2. Conectar y configurar**:
```bash
ssh -i mi-keypair.pem ubuntu@tu-ip-publica

# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Python y dependencias
sudo apt-get install -y python3.11 python3.11-venv python3-pip git

# Clonar proyecto
git clone https://github.com/tu-usuario/crewai-proyecto.git
cd crewai-proyecto

# Crear entorno virtual e instalar
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variables de entorno
echo "OPENAI_API_KEY=sk-tu-key" > .env

# Ejecutar como servicio con systemd
sudo nano /etc/systemd/system/crewai.service
```

**Archivo systemd** (`/etc/systemd/system/crewai.service`):
```ini
[Unit]
Description=CrewAI Multi-Agent System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/crewai-proyecto
Environment="PATH=/home/ubuntu/crewai-proyecto/venv/bin"
ExecStart=/home/ubuntu/crewai-proyecto/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Iniciar servicio**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable crewai
sudo systemctl start crewai
sudo systemctl status crewai
```

### AWS ECS (Elastic Container Service)

**1. Crear repositorio ECR**:
```bash
aws ecr create-repository --repository-name crewai-system
```

**2. Construir y subir imagen**:
```bash
# Login a ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Construir y etiquetar
docker build -t crewai-system .
docker tag crewai-system:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/crewai-system:latest

# Subir
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/crewai-system:latest
```

**3. Definir tarea ECS** (`task-definition.json`):
```json
{
  "family": "crewai-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "crewai-container",
      "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/crewai-system:latest",
      "essential": true,
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:crewai/openai-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/crewai",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

**4. Crear servicio**:
```bash
aws ecs create-service \
  --cluster crewai-cluster \
  --service-name crewai-service \
  --task-definition crewai-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## Instalación en Azure

### Azure Container Instances (ACI)

```bash
# Crear grupo de recursos
az group create --name crewai-rg --location eastus

# Crear contenedor
az container create \
  --resource-group crewai-rg \
  --name crewai-container \
  --image tu-registry/crewai:latest \
  --cpu 2 \
  --memory 4 \
  --environment-variables ENVIRONMENT=production \
  --secure-environment-variables OPENAI_API_KEY=sk-tu-key \
  --ports 8000 \
  --dns-name-label crewai-app
```

### Azure Kubernetes Service (AKS)

**Deployment** (`k8s-deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crewai-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crewai
  template:
    metadata:
      labels:
        app: crewai
    spec:
      containers:
      - name: crewai
        image: tu-registry/crewai:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: crewai-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

**Desplegar**:
```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

## Instalación en Google Cloud Platform

### Cloud Run

```bash
# Construir y subir imagen
gcloud builds submit --tag gcr.io/tu-proyecto/crewai:latest

# Desplegar en Cloud Run
gcloud run deploy crewai-service \
  --image gcr.io/tu-proyecto/crewai:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars ENVIRONMENT=production \
  --set-secrets OPENAI_API_KEY=crewai-openai-key:latest \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --allow-unauthenticated
```

## Optimizaciones de Producción

### 1. Caché de Respuestas

```python
from functools import lru_cache
import hashlib
import json

class ResponseCache:
    def __init__(self, max_size=1000):
        self.cache = {}
        self.max_size = max_size
    
    def get_key(self, prompt, model):
        data = f"{prompt}:{model}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get(self, prompt, model):
        key = self.get_key(prompt, model)
        return self.cache.get(key)
    
    def set(self, prompt, model, response):
        if len(self.cache) >= self.max_size:
            # Eliminar entrada más antigua
            self.cache.pop(next(iter(self.cache)))
        key = self.get_key(prompt, model)
        self.cache[key] = response
```

### 2. Connection Pooling

```python
from openai import OpenAI
import httpx

# Configurar cliente con connection pooling
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    http_client=httpx.Client(
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20
        )
    )
)
```

### 3. Rate Limiting

```python
from ratelimit import limits, sleep_and_retry

CALLS_PER_MINUTE = 60

@sleep_and_retry
@limits(calls=CALLS_PER_MINUTE, period=60)
def call_llm_with_rate_limit(prompt):
    # Tu lógica aquí
    pass
```

### 4. Monitoreo y Logging

```python
import logging
import structlog

# Configurar logging estructurado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Uso
logger.info("agent_started", agent_id="123", role="researcher")
```

## Seguridad en Producción

### 1. Gestión de Secretos

**AWS Secrets Manager**:
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret('crewai/api-keys')
openai_key = secrets['OPENAI_API_KEY']
```

**HashiCorp Vault**:
```python
import hvac

client = hvac.Client(url='http://vault:8200')
client.token = os.getenv('VAULT_TOKEN')
secret = client.secrets.kv.v2.read_secret_version(path='crewai')
openai_key = secret['data']['data']['openai_key']
```

### 2. Network Security

- Usar VPC privadas
- Configurar Security Groups/Firewall restrictivos
- Usar HTTPS con certificados válidos
- Implementar API Gateway para rate limiting
- Usar WAF (Web Application Firewall)

### 3. Encriptación

```python
from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data):
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()
```

## Auto-Scaling

### Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: crewai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: crewai-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Backup y Recuperación

```bash
# Script de backup automático
#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup de datos
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" /app/data

# Backup de configuración
cp /app/.env "$BACKUP_DIR/env_$DATE"

# Subir a S3
aws s3 cp "$BACKUP_DIR/data_$DATE.tar.gz" s3://mi-bucket/backups/

# Limpiar backups antiguos (> 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete
```

## Próximos Pasos

- Configurar monitoreo con Prometheus/Grafana
- Implementar CI/CD con GitHub Actions o GitLab CI
- Configurar alertas con PagerDuty o similar
- Revisar logs y métricas regularmente

