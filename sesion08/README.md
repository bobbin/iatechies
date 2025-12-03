# Sesión 08 - Audio Generativo: Speech & Text-to-Speech

## 🎯 Objetivos de Aprendizaje

Esta sesión se enfoca en técnicas de **generación y procesamiento de audio** usando modelos de IA:
- **Speech-to-Text (STT)**: Convertir audio a texto
- **Text-to-Speech (TTS)**: Convertir texto a audio

### Temas Cubiertos:
1. 🏠 **Modelos Locales**: Faster-Whisper (STT) y pyttsx3/Coqui TTS (TTS)
2. ☁️ **APIs Cloud**: OpenAI Whisper y OpenAI TTS
3. 🎙️ **Procesamiento de Audio**: Diferentes formatos y calidades
4. ⏱️ **Timestamps y Subtítulos**: Generación de SRT
5. 🌍 **Multiidioma**: Soporte para 99+ idiomas
6. 🎵 **Voces Múltiples**: Diferentes estilos y géneros

---

## 📚 Ejemplos Incluidos

### 📥 Speech-to-Text (STT)

### 01. Speech-to-Text Local con Faster-Whisper
**Archivos:** `01_stt_local_faster_whisper.md` / `.py`

Aprende a transcribir audio usando Faster-Whisper completamente en local:
- ✅ 100% Gratuito y privado
- ✅ Sin necesidad de APIs
- ✅ Múltiples modelos (tiny a large-v3)
- ✅ Timestamps y subtítulos SRT
- ✅ Procesamiento en batch

**Ejemplos incluidos:**
1. Transcripción básica
2. Timestamps detallados
3. Generación de subtítulos SRT
4. Detección automática de idioma
5. Procesamiento en batch
6. Configuración avanzada (velocidad vs precisión)

---

### 02. Speech-to-Text con OpenAI Whisper API
**Archivos:** `02_stt_openai_whisper.md` / `.py`

Aprende a usar la API profesional de Whisper de OpenAI:
- ⭐ Máxima precisión (modelo large-v3)
- ⚡ Procesamiento rápido en la nube
- 🌍 99+ idiomas soportados
- 💰 Bajo costo ($0.006/minuto)

**Ejemplos incluidos:**
1. Transcripción básica
2. Formato detallado con metadata
3. Traducción automática a inglés
4. Generación de subtítulos SRT
5. Múltiples formatos de audio
6. Manejo de archivos grandes
7. Detección automática de idioma
8. Calculadora de costos

---

### 📤 Text-to-Speech (TTS)

### 03. Text-to-Speech Local Offline
**Archivos:** `03_tts_local_offline.md` / `.py`

Aprende a generar voz desde texto completamente en local:
- ✅ 100% Gratuito y offline
- ✅ pyttsx3: Voces del sistema (rápido y simple)
- ✅ Coqui TTS: Modelos IA de alta calidad
- ✅ Control de velocidad, volumen y voces
- ✅ Múltiples formatos de salida

**Ejemplos incluidos:**
1. Síntesis básica con pyttsx3
2. Listar voces disponibles
3. Configurar velocidad y volumen
4. Guardar audio en archivos
5. TTS de alta calidad con Coqui
6. Generación multilingüe con XTTS v2
7. Convertir archivos de texto completos
8. Listar modelos disponibles
9. Comparación de calidad

---

### 04. Text-to-Speech con OpenAI TTS API
**Archivos:** `04_tts_openai.md` / `.py`

Aprende a generar voces ultra-realistas con OpenAI TTS:
- ⭐ Calidad profesional indistinguible de humanos
- 🎤 6 voces diferentes con estilos únicos
- ⚡ Modelos TTS-1 (rápido) y TTS-1-HD (calidad)
- 🎵 Múltiples formatos: MP3, Opus, AAC, FLAC, WAV
- 💰 Bajo costo: $15/1M caracteres

**Ejemplos incluidos:**
1. Síntesis básica
2. Comparar las 6 voces disponibles
3. Comparar TTS-1 vs TTS-1-HD
4. Diferentes formatos de audio
5. Control de velocidad de habla
6. Generar audiolibro completo
7. Streaming en tiempo real
8. Calculadora de costos
9. Caso real: Tutorial de YouTube

---

### 🔊 Audio en Tiempo Real (Realtime)

### 05. Audio en Tiempo Real con OpenAI
**Archivos:** `05_realtime_openai.md` / `.py` / `_server.py` / `_frontend.html`

Conversación de voz bidireccional en tiempo real:
- ⚡ Latencia ultra-baja (~320ms)
- 🎤 Detección automática de voz (VAD)
- ⚠️ Soporte para interrupciones naturales
- 🔄 Streaming bidireccional
- 💬 Audio + Texto simultáneo
- 🌐 Frontend web completo con micrófono

**Ejemplos incluidos:**
1. Conversación básica (modo texto)
2. Conversación interactiva multi-turno
3. Conversación con funciones
4. Servidor WebSocket relay
5. Frontend HTML/JS completo

---

### 06. Audio en Tiempo Real con Gemini
**Archivos:** `06_realtime_gemini.md` / `.py` / `_server.py` / `_frontend.html`

Conversación multimodal en tiempo real con Gemini:
- 🎥 Multimodal: Audio + Video + Texto
- ⚡ Baja latencia (~400ms)
- ✅ Gratis durante preview
- 🔄 Streaming bidireccional
- 🛠️ Soporte para funciones
- 🌐 Frontend web con acceso a cámara

**Ejemplos incluidos:**
1. Conversación con texto
2. Conversación interactiva
3. Conversación con funciones  
4. Info sobre audio realtime
5. Capacidades de audio
6. Servidor WebSocket relay
7. Frontend HTML/JS multimodal

---

## 🚀 Instalación

```bash
# Navegar a la carpeta
cd sesion08

# Instalar dependencias
pip install -r requirements.txt

# Para OpenAI Whisper API, crear archivo .env
echo "OPENAI_API_KEY=sk-tu-key-aqui" > .env
```

---

## 📊 Comparaciones

### Speech-to-Text (STT)

| Característica | Faster-Whisper | OpenAI Whisper API |
|----------------|----------------|-------------------|
| **Costo** | ✅ Gratis | 💰 $0.006/min |
| **Privacidad** | ✅ 100% Local | ❌ Cloud |
| **Precisión** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **GPU** | ⚠️ Opcional | ❌ No necesaria |
| **Límite** | ✅ Sin límite | ⚠️ 25 MB |
| **Internet** | ❌ No | ✅ Sí |

### Text-to-Speech (TTS)

| Característica | pyttsx3 | Coqui TTS | OpenAI TTS |
|----------------|---------|-----------|------------|
| **Costo** | ✅ Gratis | ✅ Gratis | 💰 $15/1M chars |
| **Calidad** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Naturalidad** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Setup** | Muy fácil | Complejo | Fácil |
| **Voces** | Sistema | Muchas | 6 premium |
| **Internet** | ❌ No | ❌ No | ✅ Sí |

### Audio en Tiempo Real (Realtime)

| Característica | OpenAI Realtime | Gemini Live |
|----------------|-----------------|-------------|
| **Latencia** | ~320ms ⚡⚡⚡⚡⚡ | ~400ms ⚡⚡⚡⚡ |
| **Costo** | 💰 ~$0.30/min | ✅ Gratis (preview) |
| **Interrupciones** | ✅ Natural | ✅ Natural |
| **Multimodal** | ❌ Solo audio | ✅ Audio + Video |
| **Voces** | 6 predefinidas | 5 configurables |
| **Calidad voz** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Setup** | WebSocket | WebSocket |
| **Funciones** | ✅ Soportado | ✅ Soportado |

---

## 🎯 Casos de Uso Reales

### Speech-to-Text (STT)
1. **📝 Transcripción de Reuniones** - Actas automáticas
2. **🎬 Subtitulado de Videos** - YouTube, accesibilidad
3. **📞 Análisis de Llamadas** - Atención al cliente
4. **🎙️ Podcasts a Texto** - SEO y búsqueda
5. **⚖️ Transcripciones Legales** - Entrevistas, deposiciones
6. **🔍 Búsqueda en Audio** - Indexación de contenido

### Text-to-Speech (TTS)
1. **📚 Audiolibros** - Conversión de libros completos
2. **🎓 E-Learning** - Narración de cursos online
3. **🎬 Voiceovers** - Videos de YouTube, TikTok
4. **🤖 Asistentes Virtuales** - IVR, chatbots con voz
5. **📻 Podcasts Automatizados** - Noticias, resúmenes
6. **♿ Accesibilidad** - Lectores de pantalla premium
7. **📱 Apps Móviles** - Notificaciones habladas
8. **🎮 Videojuegos** - Diálogos dinámicos NPCs

### Audio en Tiempo Real
1. **🤖 Asistentes de Voz** - Siri, Alexa-like
2. **📞 Call Centers IA** - Atención al cliente automatizada
3. **🎓 Tutores de Idiomas** - Práctica de conversación
4. **👴 Compañía para Mayores** - Conversación natural
5. **🏥 Asistentes Médicos** - Triage inicial
6. **🎮 NPCs Inteligentes** - Diálogos realistas en juegos
7. **🚗 Asistentes de Conducción** - Manos libres
8. **📹 Videollamadas IA** - Interacción multimodal

---

## 💡 Tips y Mejores Prácticas

### Calidad del Audio
- 🎤 Usa micrófonos de buena calidad
- 🔇 Minimiza ruido de fondo
- 📏 Frecuencia de muestreo: 16kHz o superior
- 🎚️ Normaliza el volumen

### Optimización
- ⚡ Para velocidad → Usar modelo `tiny` o `base`
- 🎯 Para precisión → Usar modelo `large-v3`
- 💾 Para archivos grandes → Dividir en chunks
- 🌍 Especificar idioma mejora la precisión

### Privacidad y Seguridad
- 🔒 Datos sensibles → Usar Faster-Whisper local
- ☁️ Datos no sensibles → OpenAI API es más rápido
- 📜 Revisar políticas de retención de datos

---

## 🛠️ Requisitos del Sistema

### Para Modelos Locales (Faster-Whisper, Coqui TTS):
- Python 3.8+
- 4-8GB RAM (8GB+ recomendado para Coqui TTS)
- GPU opcional (mejora velocidad 4x)
- FFmpeg instalado
- Espacio en disco: 500MB - 3GB para modelos

### Para pyttsx3:
- Python 3.8+
- Voces del sistema instaladas
  - Windows: SAPI5 voices (incluidas)
  - macOS: NSSpeechSynthesizer (incluido)
  - Linux: espeak o festival

### Para OpenAI APIs:
- Python 3.8+
- Conexión a internet estable
- API Key de OpenAI
- Créditos en cuenta OpenAI

---

## 📖 Recursos Adicionales

### Documentación Oficial:

**Speech-to-Text:**
- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Whisper Original](https://github.com/openai/whisper)

**Text-to-Speech:**
- [pyttsx3 Docs](https://pyttsx3.readthedocs.io/)
- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [OpenAI TTS API](https://platform.openai.com/docs/guides/text-to-speech)

### Herramientas Útiles:
- [FFmpeg](https://ffmpeg.org/) - Conversión de formatos de audio
- [Audacity](https://www.audacityteam.org/) - Editor de audio gratuito
- [gTTS](https://gtts.readthedocs.io/) - Text-to-Speech simple para testing
- [XTTS Playground](https://huggingface.co/spaces/coqui/xtts) - Demo online

### Formatos de Audio Soportados:
- **Input (STT)**: WAV, MP3, M4A, FLAC, OGG, WebM, MP4
- **Output (TTS)**: MP3, WAV, Opus, AAC, FLAC, PCM

---

## 🏃 Inicio Rápido

### Speech-to-Text

```bash
# STT Local (gratis, offline)
python 01_stt_local_faster_whisper.py

# STT OpenAI (requiere API key)
python 02_stt_openai_whisper.py
```

### Text-to-Speech

```bash
# TTS Local (gratis, offline)
python 03_tts_local_offline.py

# TTS OpenAI (requiere API key)
python 04_tts_openai.py
```

### Audio en Tiempo Real

```bash
# Realtime OpenAI (ejemplos de consola)
python 05_realtime_openai.py

# Realtime OpenAI (con frontend web + micrófono)
python 05_realtime_openai_server.py
# Abrir en navegador: http://localhost:8000/05_realtime_openai_frontend.html

# Realtime Gemini (ejemplos de consola)
python 06_realtime_gemini.py

# Realtime Gemini (con frontend web + micrófono/cámara)
python 06_realtime_gemini_server.py
# Abrir en navegador: http://localhost:8001/06_realtime_gemini_frontend.html
```

---

## 💰 Resumen de Costos

| Servicio | Modelo | Costo | Ejemplo |
|----------|--------|-------|---------|
| **STT OpenAI** | Whisper | $0.006/min | 1h audio = $0.36 |
| **TTS OpenAI** | TTS-1 | $15/1M chars | 1000 palabras = $0.075 |
| **TTS OpenAI** | TTS-1-HD | $30/1M chars | 1000 palabras = $0.15 |
| **Realtime OpenAI** | gpt-4o-realtime | ~$0.30/min | 10 min conversación = $3.00 |
| **Realtime Gemini** | gemini-2.0-flash | ✅ Gratis (preview) | Ilimitado (con rate limits) |
| **Local** | Todos | ✅ Gratis | Ilimitado |

---

## 📈 Próximos Pasos

Después de completar esta sesión, estarás listo para:
- 🎼 **Generación de Música**: MusicGen, AudioCraft
- 🔊 **Separación de Audio**: Demucs, Spleeter (voces/instrumentos)
- 🎚️ **Mejora de Audio**: Reducción de ruido, upsampling
- 🎭 **Clonación de Voz**: XTTS v2, RVC
- 🎵 **Efectos de Audio**: Cambio de tono, tempo
- 🔄 **Pipeline Completo**: STT → Procesamiento → TTS

---

## 🎓 Conclusión

Esta sesión te ha proporcionado:
- ✅ Herramientas para convertir audio a texto (STT)
- ✅ Herramientas para convertir texto a audio (TTS)
- ✅ Opciones locales (gratis) y cloud (premium)
- ✅ Casos de uso reales y ejemplos prácticos
- ✅ Control total sobre calidad vs costo vs velocidad

**¡Ahora puedes construir aplicaciones completas de audio generativo!** 🎙️✨

