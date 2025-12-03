# Audio en Tiempo Real con Gemini Live API

## Objetivo
Implementar conversaciones de voz bidireccionales en tiempo real usando **Gemini Multimodal Live API**, con soporte para audio, video y baja latencia.

## ¿Qué es Gemini Multimodal Live API?
API de Google para conversaciones en tiempo real con capacidades multimodales:
- Audio bidireccional en vivo
- Video streaming (opcional)
- Baja latencia (~300-500ms)
- Comunicación vía WebSocket (BidiGenerateContent)
- Detección de actividad de voz
- Soporte para interrupciones

## Modelos Disponibles
- **gemini-2.0-flash-exp**: Modelo experimental optimizado para tiempo real
- **gemini-2.0-flash**: Modelo estable con capacidades multimodales
- Soporta audio input/output simultáneo
- Configuración de voces y parámetros de generación

## Características Principales
✅ **Multimodal**: Audio + Video + Texto simultáneo  
✅ **Baja Latencia**: ~300-500ms  
✅ **Streaming**: Respuestas en tiempo real  
✅ **Interrupciones**: Soporte natural  
✅ **Gratuito**: Durante preview (con límites)  
✅ **Funciones**: Puede llamar tools/funciones  

## Arquitectura
```
Usuario (Micrófono/Cámara)
    ↓ WebSocket
Gemini Live API
    ↓ WebSocket  
Usuario (Altavoz/Pantalla)
```

## Casos de Uso
1. 🤖 **Asistentes Multimodales**: Voz + visión
2. 📹 **Videollamadas IA**: Interacción con video
3. 🎓 **Tutores Interactivos**: Explicaciones visuales
4. 🏥 **Telemedicina**: Consultas con análisis visual
5. 🔍 **Análisis en Vivo**: Streaming de video con IA
6. 🎮 **Juegos Interactivos**: NPCs con IA multimodal
7. 👁️ **Accesibilidad**: Descripción de entorno en vivo

## Precios
Durante el periodo de preview:
- ✅ **Gratuito** con límites razonables
- Límites de rate: 15 RPM, 1M TPM, 8M TPD
- Audio: PCM 16kHz mono

## Ventajas sobre OpenAI Realtime
| Característica | Gemini Live | OpenAI Realtime |
|----------------|-------------|-----------------|
| **Multimodal** | ✅ Audio+Video | ❌ Solo Audio |
| **Costo** | ✅ Gratis (preview) | 💰 ~$0.30/min |
| **Latencia** | ~400ms | ~320ms |
| **Voces** | Configurables | 6 predefinidas |
| **Video** | ✅ Soportado | ❌ No |

## Formato de Audio
- Input: PCM 16-bit, 16kHz, mono
- Output: PCM 16-bit, 24kHz, mono
- Codificación: Base64 en mensajes JSON

## Configuración de Voz
```python
voice_config = {
    "prebuiltVoiceConfig": {
        "voiceName": "Charon"  # u otras voces disponibles
    }
}
```

Voces disponibles: Puck, Charon, Kore, Fenrir, Aoede

## Ejemplos Incluidos
1. **Conversación básica**: Setup mínimo con audio
2. **Con interrupciones**: Detección de usuario hablando
3. **Multimodal**: Audio + Video simultáneo
4. **Con funciones**: Llamar APIs durante conversación
5. **Frontend completo**: Interfaz web con cámara y micrófono

## Limitaciones
- ⚠️ En preview (puede cambiar)
- ⚠️ Requiere WebSocket
- ⚠️ Rate limits durante preview
- ⚠️ Voces menos naturales que OpenAI

## Referencias
- [Gemini Live API Docs](https://ai.google.dev/gemini-api/docs/live)
- [BidiGenerateContent](https://ai.google.dev/api/generate-content#method:-models.streamgeneratecontent)
- [Multimodal Guide](https://ai.google.dev/gemini-api/docs/audio)

