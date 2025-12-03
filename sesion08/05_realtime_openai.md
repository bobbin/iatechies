# Audio en Tiempo Real con OpenAI Realtime API

## Objetivo
Implementar conversaciones de voz bidireccionales en tiempo real usando la **Realtime API de OpenAI**, permitiendo interacciones naturales con baja latencia.

## ¿Qué es OpenAI Realtime API?
La Realtime API permite conversaciones de voz en tiempo real con GPT-4o:
- Comunicación bidireccional vía WebSockets
- Audio streaming de entrada y salida
- Latencia ultra-baja (~320ms)
- Soporte para interrupciones naturales
- Detección automática de actividad de voz (VAD)

## Modelo
- **gpt-4o-realtime-preview-2024-10-01**: Modelo optimizado para tiempo real
- Soporta 6 voces: alloy, echo, fable, onyx, nova, shimmer
- Audio input: 24kHz PCM mono
- Audio output: 24kHz PCM mono

## Características Principales
✅ **Latencia Ultra-baja**: ~320ms end-to-end  
✅ **Interrupciones**: Detecta cuando el usuario interrumpe  
✅ **VAD Integrado**: Detección automática de voz  
✅ **Streaming**: Audio en chunks, no espera audio completo  
✅ **Funciones**: Puede llamar funciones como ChatGPT  
✅ **Conversación Natural**: Mantiene contexto de conversación  

## Arquitectura
```
Usuario (Micrófono) 
    ↓ WebSocket
OpenAI Realtime API
    ↓ WebSocket
Usuario (Altavoz)
```

## Casos de Uso
1. 🤖 **Asistentes de Voz**: Siri, Alexa-like
2. 📞 **Call Centers IA**: Atención al cliente automatizada
3. 🎓 **Tutores de Idiomas**: Práctica de conversación
4. 👴 **Compañía para Mayores**: Conversación natural
5. 🏥 **Asistentes Médicos**: Triage inicial
6. 🎮 **NPCs en Videojuegos**: Diálogos realistas
7. 🚗 **Asistentes de Conducción**: Manos libres

## Precios (2024)
- **Audio Input**: $100 / 1M tokens (~$0.06 / minuto)
- **Audio Output**: $200 / 1M tokens (~$0.24 / minuto)
- **Texto**: Similar a GPT-4o estándar

**Ejemplo**: 10 minutos de conversación ≈ $3.00 USD

## Componentes Necesarios

### Backend (Python)
- WebSocket server
- Manejo de eventos de audio
- Conexión a OpenAI Realtime API

### Frontend (JavaScript)
- Acceso al micrófono del navegador
- WebAudio API para captura de audio
- WebSocket client
- Reproducción de audio

## Ventajas sobre STT + LLM + TTS
| Característica | Pipeline Tradicional | Realtime API |
|----------------|---------------------|--------------|
| Latencia | 2-5 segundos | 0.32 segundos |
| Interrupciones | ❌ Difícil | ✅ Natural |
| Naturalidad | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup | Complejo (3 APIs) | Simple (1 API) |
| Costo | ~$0.50/min | ~$0.30/min |

## Limitaciones
- ⚠️ Requiere WebSocket (no REST)
- ⚠️ Solo audio (no video aún)
- ⚠️ Costo mayor que text-only
- ⚠️ Requiere frontend para micrófono

## Ejemplos Incluidos
1. **Conversación básica**: Setup mínimo
2. **Con interrupciones**: Detección de cuando el usuario habla
3. **Con funciones**: Llamar APIs durante conversación
4. **Frontend completo**: HTML/JS para navegador

## Referencias
- [OpenAI Realtime API Docs](https://platform.openai.com/docs/guides/realtime)
- [API Reference](https://platform.openai.com/docs/api-reference/realtime)
- [WebSocket Guide](https://platform.openai.com/docs/guides/realtime/websocket)

