# Ejercicio 14: Agente que usa APIs externas

## Objetivo
Crear un agente que combina información de múltiples APIs externas para responder preguntas complejas, siguiendo el ejemplo de las slides B10.

## Conceptos Clave (Slides B10)
- **APIs externas**: Los agentes pueden llamar a servicios externos para obtener datos en tiempo real.
- **Composición de información**: El agente combina resultados de múltiples APIs.
- **Síntesis**: El agente sintetiza la información en una respuesta coherente.

## Qué vamos a hacer
1. Crear 3 tools que simulan APIs externas:
   - `get_weather`: API meteorológica
   - `get_news`: API de noticias
   - `get_prices`: API financiera
2. Configurar un agente que puede usar estas tools.
3. Ejecutar preguntas que requieren combinar información de múltiples fuentes.
4. Observar cómo el agente decide qué APIs llamar.

## Instrucciones
Ejecuta el script:
```bash
python 14_langchain_api_externa.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Las APIs están simuladas; en producción usarías llamadas HTTP reales.

