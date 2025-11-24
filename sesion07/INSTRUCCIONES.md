# Instrucciones de Instalación y Uso - Sesión 07

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
cd sesion07
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar claves de API

Crea un archivo `.env` en la carpeta `sesion07` con tus claves:

```env
OPENAI_API_KEY=tu_clave_openai_aqui
ANTHROPIC_API_KEY=tu_clave_anthropic_aqui  # Opcional
```

**¿Dónde obtener las claves?**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/ (opcional)

## 📚 Orden de Ejecución Recomendado

### Nivel 1: Fundamentos (Complejidad Baja)

```bash
# 1. Agentes Reflexivos
python 01_agentes_reflexivos.py

# 2. Self-Prompt Editing
python 02_self_prompt_editing.py

# 3. Agentes con Reglas
python 03_agentes_con_reglas.py
```

### Nivel 2: Colaboración (Complejidad Media)

```bash
# 4. Agentes Competitivos
python 04_agentes_competitivos.py

# 5. Router Agents
python 05_router_agents.py

# 6. Supervisor/Orquestador
python 06_supervisor_orquestador.py
```

### Nivel 3: Sistemas Avanzados (Complejidad Alta)

```bash
# 7. Memoria Evolutiva
python 07_memoria_evolutiva.py

# 8. Agentes con MCPs
python 08_agentes_mcp.py

# 9. Multimodal Ligero
python 09_multimodal_ligero.py
```

### Nivel 4: Sistemas de Producción (Complejidad Muy Alta)

```bash
# 10. Verificación de Evidencia
python 10_verificacion_evidencia.py

# 11. Agentic RAG
python 11_agentic_rag.py

# 12. Equipo Forense Completo
python 12_equipo_forense.py
```

## 📖 Estructura de Cada Ejemplo

Cada ejemplo incluye:
- **`.py`**: Código ejecutable con comentarios detallados
- **`.md`**: Documentación completa con conceptos, diagramas y explicaciones

## ⚙️ Configuración Opcional

### Ajustar Verbosidad

En cada script, puedes ajustar el nivel de detalle:

```python
# Menos verboso
verbose=0  # Solo resultados finales

# Normal
verbose=1  # Información importante

# Muy verboso
verbose=2  # Todo el detalle
```

### Cambiar Modelo

Por defecto usa `gpt-4-turbo-preview`. Para usar otro:

```python
# En tu archivo .env
DEFAULT_MODEL=gpt-3.5-turbo
```

## 🐛 Solución de Problemas

### Error: "No module named 'crewai'"

```bash
pip install crewai crewai-tools
```

### Error: "API key not found"

Verifica que tu archivo `.env` esté en la carpeta `sesion07` y tenga:
```env
OPENAI_API_KEY=sk-...
```

### Error: "Rate limit exceeded"

Estás haciendo demasiadas llamadas a la API. Espera unos minutos o:
- Reduce el número de agentes
- Usa `verbose=0` para menos llamadas
- Agrega delays entre ejecuciones

### Los ejemplos tardan mucho

Es normal. Los sistemas multi-agente hacen múltiples llamadas a la API.
- Ejemplo simple: 1-2 minutos
- Ejemplo complejo: 3-5 minutos
- Equipo forense: 5-10 minutos

## 💡 Consejos

1. **Lee el .md antes de ejecutar**: Cada `.md` explica qué esperar
2. **Empieza por el principio**: Los ejemplos son progresivos
3. **Experimenta**: Modifica parámetros, roles y objetivos
4. **Observa los logs**: CrewAI muestra cómo los agentes se coordinan
5. **No te apures**: Algunos ejemplos necesitan tiempo para ejecutar

## 📊 Uso de API

**Estimación de costos** (con GPT-4):
- Ejemplo simple (01-03): ~$0.10 - $0.20
- Ejemplo medio (04-06): ~$0.20 - $0.40
- Ejemplo avanzado (07-09): ~$0.30 - $0.60
- Ejemplo complejo (10-12): ~$0.50 - $1.00

Para reducir costos durante aprendizaje, usa `gpt-3.5-turbo`.

## 🎓 Recursos Adicionales

- **CrewAI Docs**: https://docs.crewai.com
- **LangChain Tools**: https://python.langchain.com/docs/modules/tools/
- **OpenAI API**: https://platform.openai.com/docs

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar modelos locales?**  
R: Sí, pero necesitas configurar Ollama u otro servidor local. Los ejemplos asumen API de OpenAI por simplicidad.

**P: ¿Funcionan sin internet?**  
R: No, requieren conexión para llamar a las APIs de modelos.

**P: ¿Puedo modificar los ejemplos?**  
R: ¡Absolutamente! Están diseñados para experimentar.

**P: ¿Cuál es el orden ideal?**  
R: Secuencial (01→02→...→12). Cada uno construye sobre anteriores.

## 🎯 Objetivo de la Sesión

Al completar los 12 ejemplos, serás capaz de:
- ✅ Diseñar arquitecturas multi-agente profesionales
- ✅ Implementar patrones de coordinación avanzados
- ✅ Construir sistemas robustos anti-alucinación
- ✅ Integrar múltiples modalidades (texto, datos, visual)
- ✅ Crear soluciones empresariales de producción

---

**¡Disfruta construyendo sistemas multi-agente de clase mundial!** 🚀


