---
marp: true
theme: default
paginate: true
backgroundColor: #1a1a2e
color: #ffffff
style: |
  section {
    font-family: 'Segoe UI', system-ui, sans-serif;
  }
  h1 {
    color: #00d9ff;
  }
  h2 {
    color: #00ff88;
  }
  code {
    background: rgba(0,217,255,0.1);
  }
  table {
    font-size: 0.8em;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# 🎙️ Audio Generativo

## Speech-to-Text & Text-to-Speech con IA

**Sesión 08**

---

# 📋 Agenda

1. **Introducción** - ¿Qué es Audio Generativo?
2. **Speech-to-Text (STT)** - Audio → Texto
   - Faster-Whisper (Local)
   - OpenAI Whisper API (Cloud)
3. **Text-to-Speech (TTS)** - Texto → Audio
   - pyttsx3 + Coqui TTS (Local)
   - OpenAI TTS API (Cloud)
4. **Audio en Tiempo Real** - Conversaciones bidireccionales
   - OpenAI Realtime API
   - Gemini Live API
5. **Demos, Casos de Uso y Costos**

---

# 🎯 Objetivos de Aprendizaje

Al finalizar esta sesión podrás:

✅ Convertir **audio a texto** con modelos locales y cloud
✅ Generar **voz desde texto** con voces naturales
✅ Crear **subtítulos automáticos** en formato SRT
✅ Implementar **conversaciones de voz** en tiempo real
✅ Elegir la solución correcta según **costo/calidad/privacidad**
✅ Integrar audio en tus **aplicaciones de IA**

---

# 🤔 ¿Qué es Audio Generativo?

Tecnologías de IA para **procesar y generar audio**:

| Tecnología | Descripción | Ejemplo |
|------------|-------------|---------|
| **STT** | Audio → Texto | Transcribir reuniones |
| **TTS** | Texto → Audio | Crear audiolibros |
| **Realtime** | Conversación bidireccional | Asistente de voz |
| **Music Gen** | Texto → Música | Crear canciones |
| **Voice Clone** | Clonar voces | Doblaje automático |

> En esta sesión nos enfocamos en **STT, TTS y Realtime**

---

<!-- _class: lead -->
<!-- _backgroundColor: #16213e -->

# 📥 Speech-to-Text (STT)

## Convertir Audio en Texto

---

# 🎤 Speech-to-Text - Conceptos

**¿Qué es?**
Tecnología que convierte audio hablado en texto escrito.

**¿Cómo funciona?**
1. 🎵 Captura señal de audio
2. 🔊 Procesamiento de señal (normalización, filtrado)
3. 🧠 Modelo de IA analiza patrones
4. 📝 Genera texto transcrito

**Modelo estrella: Whisper de OpenAI**
- Entrenado con 680,000 horas de audio
- 99+ idiomas soportados
- Open source (septiembre 2022)

---

# 🏠 STT Local: Faster-Whisper

**¿Qué es?**
Implementación optimizada de Whisper (4x más rápido)

**Ventajas:**
✅ 100% Gratuito
✅ 100% Offline y privado
✅ Sin límites de uso
✅ Control total

**Instalación:**
```bash
pip install faster-whisper
```

---

# 🏠 Faster-Whisper: Modelos

| Modelo | Tamaño | RAM | Velocidad | Precisión |
|--------|--------|-----|-----------|-----------|
| `tiny` | 39 MB | ~1 GB | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| `base` | 74 MB | ~1 GB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| `small` | 244 MB | ~2 GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| `medium` | 769 MB | ~5 GB | ⚡⚡ | ⭐⭐⭐⭐ |
| `large-v3` | 1550 MB | ~10 GB | ⚡ | ⭐⭐⭐⭐⭐ |

> 💡 **Recomendación:** Usa `base` para desarrollo, `large-v3` para producción

---

# 🏠 Faster-Whisper: Ejemplos

```python
from faster_whisper import WhisperModel

# Cargar modelo
model = WhisperModel("base", device="cpu")

# Transcribir
segments, info = model.transcribe("audio.mp3")

# Resultado
for segment in segments:
    print(f"[{segment.start:.1f}s] {segment.text}")
```

**Scripts disponibles:**
- `01a` - Transcripción básica
- `01b` - Con timestamps
- `01c` - Generar subtítulos SRT
- `01d` - Detectar idioma
- `01e` - Batch (múltiples archivos)
- `01f` - Configuración velocidad/precisión

---

# ☁️ STT Cloud: OpenAI Whisper API

**¿Qué es?**
API de OpenAI que usa el modelo Whisper large-v3

**Ventajas:**
✅ Máxima precisión (large-v3)
✅ Sin configuración de hardware
✅ Muy rápido
✅ 99+ idiomas

**Costo:**
💰 **$0.006 por minuto** (~$0.36/hora)

---

# ☁️ OpenAI Whisper: Ejemplo

```python
from openai import OpenAI

client = OpenAI()

# Transcribir
with open("audio.mp3", "rb") as audio:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio,
        language="es"
    )

print(transcript.text)
```

**Scripts disponibles:**
- `02a` - Básico | `02b` - Timestamps
- `02c` - Traducción a inglés
- `02d` - Subtítulos SRT
- `02e` - Múltiples formatos
- `02f` - Archivos grandes (chunks)
- `02g` - Detectar idioma | `02h` - Costos

---

# 📊 Comparación STT

| Característica | Faster-Whisper | OpenAI API |
|----------------|----------------|------------|
| **Costo** | ✅ Gratis | 💰 $0.006/min |
| **Privacidad** | ✅ 100% Local | ❌ Cloud |
| **Precisión** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **GPU** | ⚠️ Opcional | ❌ No necesaria |
| **Límite archivo** | ✅ Sin límite | ⚠️ 25 MB |
| **Internet** | ❌ No | ✅ Sí |

> 💡 **Usa Faster-Whisper** para datos sensibles, **OpenAI** para velocidad

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a3e2e -->

# 📤 Text-to-Speech (TTS)

## Convertir Texto en Voz

---

# 🔊 Text-to-Speech - Conceptos

**¿Qué es?**
Tecnología que convierte texto escrito en audio hablado.

**Evolución:**
1. 🤖 **Concatenativo** - Unir fragmentos pregrabados (robótico)
2. 📊 **Paramétrico** - Sintetizar con reglas (mejor pero artificial)
3. 🧠 **Neural** - Modelos de IA (natural, casi humano)

**Estado actual:**
Las voces neurales son prácticamente **indistinguibles de humanos** 🎭

---

# 🏠 TTS Local: pyttsx3

**¿Qué es?**
Wrapper para motores TTS del sistema operativo

**Ventajas:**
✅ Muy rápido (instantáneo)
✅ Sin dependencias pesadas
✅ 100% offline

**Desventajas:**
❌ Voces robóticas
❌ Limitado a voces del SO

```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Hola, soy una voz del sistema")
engine.runAndWait()
```

---

# 🏠 TTS Local: Coqui TTS

**¿Qué es?**
Modelos de IA open source de alta calidad

**Ventajas:**
✅ Voces naturales (calidad IA)
✅ Multilingüe (16+ idiomas)
✅ Clonación de voz
✅ 100% local y gratis

**Desventajas:**
⚠️ Más lento que pyttsx3
⚠️ Requiere ~1-3GB RAM

```python
from TTS.api import TTS
tts = TTS("tts_models/es/css10/vits")
tts.tts_to_file(text="Hola mundo", file_path="audio.wav")
```

---

# 🏠 TTS Local: Scripts

**pyttsx3 (voces del sistema):**
- `03a` - Síntesis básica
- `03b` - Listar voces disponibles
- `03c` - Configurar velocidad/volumen
- `03d` - Guardar en archivo

**Coqui TTS (modelos IA):**
- `03e` - Modelo español básico
- `03f` - Multilingüe (XTTS v2)
- `03g` - Convertir archivo de texto
- `03h` - Listar modelos disponibles
- `03i` - Comparación calidad

---

# ☁️ TTS Cloud: OpenAI TTS

**¿Qué es?**
API de OpenAI con voces ultra-realistas

**Características:**
- 🎤 **6 voces** con diferentes estilos
- 🎚️ **2 modelos**: TTS-1 (rápido) y TTS-1-HD (calidad)
- ⚡ **Velocidad ajustable**: 0.25x a 4.0x
- 🎵 **Formatos**: MP3, Opus, AAC, FLAC

**Costo:**
- 💰 TTS-1: **$15 / 1M caracteres**
- 💰 TTS-1-HD: **$30 / 1M caracteres**

---

# ☁️ OpenAI TTS: Las 6 Voces

| Voz | Estilo | Mejor para |
|-----|--------|------------|
| **alloy** | Neutral, profesional | Tutoriales, documentación |
| **echo** | Masculina, cálida | Audiolibros, narración |
| **fable** | Neutral, expresiva | Podcasts, storytelling |
| **onyx** | Masculina, profunda | Documentales, anuncios |
| **nova** | Femenina, energética | Marketing, presentaciones |
| **shimmer** | Femenina, suave | Meditación, e-learning |

---

# ☁️ OpenAI TTS: Ejemplo

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1-hd",    # Alta calidad
    voice="nova",        # Voz energética
    input="¡Hola! Bienvenidos a este tutorial.",
    speed=1.0           # Velocidad normal
)

response.stream_to_file("output.mp3")
```

**Scripts:** `04a-04i` (básico, voces, modelos, formatos, velocidad, audiolibro, streaming, costos, YouTube)

---

# 📊 Comparación TTS

| Característica | pyttsx3 | Coqui TTS | OpenAI TTS |
|----------------|---------|-----------|------------|
| **Costo** | ✅ Gratis | ✅ Gratis | 💰 $15/1M chars |
| **Calidad** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Naturalidad** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Velocidad** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡⚡ |
| **Setup** | Muy fácil | Complejo | Fácil |
| **Voces** | Sistema | Muchas IA | 6 premium |
| **Internet** | ❌ No | ❌ No | ✅ Sí |

---

<!-- _class: lead -->
<!-- _backgroundColor: #3e1a2e -->

# 🔊 Audio en Tiempo Real

## Conversaciones Bidireccionales con IA

---

# ⚡ Realtime Audio - Conceptos

**¿Qué es?**
Comunicación de voz bidireccional con latencia ultra-baja

**Tradicional vs Realtime:**

| Tradicional | Realtime |
|-------------|----------|
| STT → LLM → TTS | Modelo unificado |
| ~3-5 segundos latencia | ~300ms latencia |
| No interrumpible | Interrupciones naturales |
| Turnos estrictos | Conversación fluida |

**Modelos disponibles:**
- 🟢 OpenAI: `gpt-4o-realtime-preview`
- 🔵 Google: `gemini-2.0-flash` (Live API)

---

# 🟢 OpenAI Realtime API

**Características:**
- ⚡ Latencia: ~320ms
- 🎤 6 voces (mismas que TTS)
- 🔄 WebSocket bidireccional
- ⚠️ Interrupciones naturales
- 🛠️ Soporte para funciones

**Costo:**
💰 **~$0.30 por minuto** de conversación
(Input: $0.10/1K tokens, Output: $0.20/1K tokens)

```javascript
// WebSocket connection
ws = new WebSocket("wss://api.openai.com/v1/realtime");
ws.send(JSON.stringify({type: "input_audio_buffer.append", audio: base64}));
```

---

# 🔵 Gemini Live API

**Características:**
- ⚡ Latencia: ~400ms
- 🎥 **Multimodal**: Audio + Video + Texto
- 🔄 WebSocket bidireccional
- ✅ Gratis durante preview
- 🛠️ Soporte para funciones

**Ventaja única:**
Puede ver tu cámara mientras conversa 📹🎤

```python
from google import genai
client = genai.Client()
async with client.aio.live.connect(model="gemini-2.0-flash") as session:
    await session.send(input="Hola, ¿cómo estás?")
```

---

# 📊 Comparación Realtime

| Característica | OpenAI | Gemini |
|----------------|--------|--------|
| **Latencia** | ~320ms ⚡⚡⚡⚡⚡ | ~400ms ⚡⚡⚡⚡ |
| **Costo** | 💰 ~$0.30/min | ✅ Gratis (preview) |
| **Interrupciones** | ✅ Natural | ✅ Natural |
| **Multimodal** | ❌ Solo audio | ✅ Audio + Video |
| **Voces** | 6 predefinidas | 5 configurables |
| **Calidad voz** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Funciones** | ✅ Sí | ✅ Sí |

---

# 🌐 Realtime: Frontend Web

Ambas APIs incluyen **frontends web completos**:

**OpenAI Realtime:**
```bash
python 05_realtime_openai_server.py
# Abrir: http://localhost:8000
```

**Gemini Live:**
```bash
python 06_realtime_gemini_server.py
# Abrir: http://localhost:8001
```

**Características:**
- 🎤 Acceso al micrófono del navegador
- 🔊 Reproducción de audio en tiempo real
- 📝 Transcripción en vivo
- ⏹️ Interrumpir al asistente

---

<!-- _class: lead -->
<!-- _backgroundColor: #2e3e1a -->

# 🖥️ Demos

## Frontends Interactivos

---

# 🎙️ Demo: STT Frontend

**Ejecutar:**
```bash
cd sesion08
python frontend_stt_server.py
# Abrir: http://localhost:8080
```

**Características:**
- 🎤 Grabar desde micrófono
- 📁 Subir archivo de audio
- 🏠 Backend local o ☁️ cloud
- 🌍 Selección de idioma
- ⏱️ Timestamps por segmento
- 📊 Métricas de rendimiento

---

# 🔊 Demo: TTS Frontend

**Ejecutar:**
```bash
cd sesion08
python frontend_tts_server.py
# Abrir: http://localhost:8081
```

**Características:**
- 📝 Escribir o pegar texto
- 🎵 Ejemplos rápidos (Saludo, Noticia, Tutorial, Cuento)
- 🎛️ Seleccionar backend (pyttsx3, Coqui, OpenAI)
- 🎤 Elegir entre 6 voces (OpenAI)
- ⚡ Ajustar velocidad (0.5x - 2.0x)
- 🎧 Reproducir resultado
- 💰 Ver costo estimado

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a2e3e -->

# 🎯 Casos de Uso

## Aplicaciones del Mundo Real

---

# 📥 Casos de Uso: STT

| Industria | Aplicación |
|-----------|------------|
| 📝 **Productividad** | Transcripción de reuniones |
| 🎬 **Media** | Subtitulado automático (YouTube) |
| 📞 **Call Centers** | Análisis de llamadas |
| 🎙️ **Podcasts** | Conversión a texto para SEO |
| ⚖️ **Legal** | Transcripciones de audiencias |
| 🏥 **Medicina** | Dictado médico |
| 🔍 **Búsqueda** | Indexación de contenido de audio |

---

# 📤 Casos de Uso: TTS

| Industria | Aplicación |
|-----------|------------|
| 📚 **Editorial** | Audiolibros automáticos |
| 🎓 **Educación** | Narración de cursos online |
| 🎬 **Video** | Voiceovers para YouTube/TikTok |
| 🤖 **Bots** | Chatbots con voz |
| 📻 **Noticias** | Podcasts automatizados |
| ♿ **Accesibilidad** | Lectores de pantalla |
| 🎮 **Gaming** | NPCs con diálogos dinámicos |

---

# ⚡ Casos de Uso: Realtime

| Industria | Aplicación |
|-----------|------------|
| 🤖 **Asistentes** | Siri/Alexa-like apps |
| 📞 **Soporte** | Call center con IA |
| 🎓 **Idiomas** | Tutor de conversación |
| 👴 **Cuidado** | Compañía para mayores |
| 🏥 **Salud** | Triage inicial |
| 🚗 **Auto** | Asistente manos libres |
| 🎮 **Gaming** | NPCs realistas |

---

<!-- _class: lead -->
<!-- _backgroundColor: #3e2e1a -->

# 💰 Costos

## Comparativa de Precios

---

# 💰 Tabla de Costos

| Servicio | Modelo | Costo | Ejemplo |
|----------|--------|-------|---------|
| **STT Local** | Faster-Whisper | ✅ Gratis | Ilimitado |
| **STT Cloud** | OpenAI Whisper | $0.006/min | 1h = $0.36 |
| **TTS Local** | pyttsx3/Coqui | ✅ Gratis | Ilimitado |
| **TTS Cloud** | OpenAI TTS-1 | $15/1M chars | 1000 palabras ≈ $0.08 |
| **TTS Cloud** | OpenAI TTS-1-HD | $30/1M chars | 1000 palabras ≈ $0.15 |
| **Realtime** | OpenAI | ~$0.30/min | 10 min = $3.00 |
| **Realtime** | Gemini | ✅ Gratis* | Ilimitado* |

*Durante el período de preview

---

# 💡 Optimización de Costos

**Para STT:**
- 🏠 Usa **local** para datos sensibles o alto volumen
- ☁️ Usa **cloud** cuando necesites máxima precisión
- ✂️ Divide archivos grandes en chunks

**Para TTS:**
- 🏠 Usa **pyttsx3** para prototipos rápidos
- 🎙️ Usa **Coqui** para calidad sin costo
- ☁️ Usa **OpenAI** para producción profesional
- 💾 **Cachea** audios generados

**Para Realtime:**
- 🔵 Usa **Gemini** (gratis en preview)
- 🟢 Usa **OpenAI** para mejor latencia

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a1a2e -->

# 🛠️ Instalación

## Quick Start

---

# 🚀 Instalación Rápida

```bash
# Clonar/navegar al proyecto
cd sesion08

# Instalar todas las dependencias
pip install -r requirements.txt

# Configurar API keys (crear archivo .env)
echo "OPENAI_API_KEY=sk-tu-key-aqui" > .env
echo "GOOGLE_API_KEY=tu-google-key" >> .env
```

**Dependencias principales:**
- `faster-whisper` - STT local
- `pyttsx3`, `TTS` - TTS local
- `openai` - APIs de OpenAI
- `google-generativeai` - Gemini
- `fastapi`, `uvicorn` - Frontends web

---

# 📁 Estructura de Archivos

```
sesion08/
├── 01a-f_stt_faster_whisper_*.py   # 6 ejemplos STT local
├── 02a-h_stt_openai_*.py           # 8 ejemplos STT cloud
├── 03a-i_tts_*.py                  # 9 ejemplos TTS local
├── 04a-i_tts_openai_*.py           # 9 ejemplos TTS cloud
├── 05_realtime_openai*             # OpenAI Realtime
├── 06_realtime_gemini*             # Gemini Live
├── frontend_stt_*                  # Demo STT web
├── frontend_tts_*                  # Demo TTS web
├── requirements.txt                # Dependencias
└── README.md                       # Documentación
```

**Total: 36 scripts + 4 frontends HTML**

---

# 📖 Recursos Adicionales

**Documentación Oficial:**
- 🔗 [Faster-Whisper](https://github.com/guillaumekln/faster-whisper)
- 🔗 [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- 🔗 [pyttsx3](https://pyttsx3.readthedocs.io/)
- 🔗 [Coqui TTS](https://github.com/coqui-ai/TTS)
- 🔗 [OpenAI TTS API](https://platform.openai.com/docs/guides/text-to-speech)
- 🔗 [OpenAI Realtime](https://platform.openai.com/docs/guides/realtime)
- 🔗 [Gemini Live](https://ai.google.dev/api/multimodal-live)

**Herramientas útiles:**
- 🎵 [FFmpeg](https://ffmpeg.org/) - Conversión de audio
- 🎧 [Audacity](https://www.audacityteam.org/) - Editor de audio

---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# ✅ Resumen

---

# 🎓 Lo que Aprendimos

### Speech-to-Text (STT)
✅ **Faster-Whisper**: Local, gratis, privado
✅ **OpenAI Whisper**: Cloud, máxima precisión

### Text-to-Speech (TTS)
✅ **pyttsx3**: Rápido, simple, voces del sistema
✅ **Coqui TTS**: IA local, alta calidad
✅ **OpenAI TTS**: Cloud, voces ultra-realistas

### Audio en Tiempo Real
✅ **OpenAI Realtime**: Baja latencia, 6 voces
✅ **Gemini Live**: Multimodal, gratis (preview)

---

# 🚀 Próximos Pasos

Después de esta sesión, puedes explorar:

- 🎼 **Generación de Música**: MusicGen, AudioCraft
- 🔊 **Separación de Audio**: Demucs (voces/instrumentos)
- 🎭 **Clonación de Voz**: XTTS v2, RVC
- 🎚️ **Mejora de Audio**: Reducción de ruido
- 🔄 **Pipelines Completos**: STT → LLM → TTS

**¡El audio generativo es una de las áreas más emocionantes de la IA!** 🎙️✨

---

<!-- _class: lead -->
<!-- _backgroundColor: #1a1a2e -->

# ❓ Preguntas

## ¿Dudas? ¿Comentarios?

---

# 🙏 ¡Gracias!

**Sesión 08 - Audio Generativo**

📁 Todos los ejemplos en: `sesion08/`

🌐 Demos:
- STT: `http://localhost:8080`
- TTS: `http://localhost:8081`

📧 ¿Preguntas después de la sesión?
Revisa el `README.md` para más detalles

---

<!-- _class: lead -->
<!-- _backgroundColor: #0f0f23 -->

# 🎙️ ¡A practicar!

## Ejecuta los ejemplos y experimenta

```bash
cd sesion08
python frontend_stt_server.py  # Puerto 8080
python frontend_tts_server.py  # Puerto 8081
```

