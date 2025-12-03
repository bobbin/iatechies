# Audio Generativo con IA
## Text-to-Speech, Voice Conversion y Voice Effects

---

# 📚 Contenido de esta sesión

1. **Text-to-Speech (TTS)** - Convertir texto en voz
2. **Speech-to-Text (STT)** - Convertir voz en texto  
3. **Voice Conversion** - Cambiar identidad vocal
4. **Voice Effects** - Efectos de audio
5. **Comparativa de tecnologías**

---

# PARTE 1
## Text-to-Speech (TTS)
### Convertir texto en voz hablada

---

# ¿Qué es Text-to-Speech?

```
┌─────────────┐         ┌─────────────┐
│   TEXTO     │  ────►  │   AUDIO     │
│  "Hola"     │   TTS   │   🔊        │
└─────────────┘         └─────────────┘
```

**TTS** convierte texto escrito en voz sintetizada.

### Usos comunes:
- 📱 Asistentes virtuales (Siri, Alexa)
- 📖 Audiolibros
- ♿ Accesibilidad
- 🎮 Videojuegos
- 📺 Contenido de video

---

# Evolución del TTS

| Generación | Tecnología | Calidad |
|------------|------------|---------|
| **1ª Gen** | Concatenativo | Robótico ⭐ |
| **2ª Gen** | Paramétrico | Mejor ⭐⭐ |
| **3ª Gen** | Neural (Tacotron) | Natural ⭐⭐⭐ |
| **4ª Gen** | Transformer (XTTS) | Humano ⭐⭐⭐⭐ |

---

# Soluciones TTS disponibles

## Gratuitas (sin API key)
- 🔷 **Edge TTS** - Microsoft Edge (neural)
- 🐸 **Coqui TTS** - Open source, local
- 🔊 **pyttsx3** - Voces del sistema

## De pago (con API key)
- 🟢 **OpenAI TTS** - $15/1M caracteres
- 🔵 **Azure TTS** - Freemium
- ⚡ **ElevenLabs** - Ultra realista

---

# Edge TTS - ¿Cómo funciona?

```
┌──────────────────────────────────────────────────────────┐
│                    MICROSOFT EDGE                        │
│  ┌─────────────┐                                         │
│  │ Función     │                                         │
│  │ "Leer en    │ ──────────────────────────────┐        │
│  │  voz alta"  │                               │        │
│  └─────────────┘                               ▼        │
│                                    ┌───────────────────┐ │
│                                    │   AZURE SPEECH    │ │
│  ┌─────────────┐                   │   SERVICES        │ │
│  │ edge-tts    │ ──────────────────►  (backend)       │ │
│  │ (Python)    │    misma API      │                   │ │
│  └─────────────┘                   │   Voces neurales  │ │
│                                    └───────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Edge TTS** usa la misma API que Microsoft Edge para acceder a Azure Speech Services **gratis**.

---

# Edge TTS - Código básico

```python
import asyncio
import edge_tts

VOICE = "es-ES-XimenaNeural"
TEXT = "Hola, esto es una prueba de síntesis de voz."

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save("output.mp3")

asyncio.run(main())
```

✅ Sin API key
✅ 5 líneas de código
✅ Calidad neural

---

# Edge TTS - Voces disponibles

## 77 voces en español de diferentes países:

| País | Voces | Ejemplo |
|------|-------|---------|
| 🇪🇸 España | 20 | es-ES-XimenaNeural |
| 🇲🇽 México | 18 | es-MX-DaliaNeural |
| 🇦🇷 Argentina | 2 | es-AR-ElenaNeural |
| 🇨🇴 Colombia | 2 | es-CO-SalomeNeural |
| ... | ... | ... |

```python
# Listar voces
voices = await VoicesManager.create()
spanish = voices.find(Language="es")
```

---

# Edge TTS - Parámetros de control

```python
communicate = edge_tts.Communicate(
    text="Texto a sintetizar",
    voice="es-ES-AlvaroNeural",
    rate="+20%",      # Velocidad: -50% a +100%
    volume="+10%",    # Volumen: -50% a +50%
    pitch="+5Hz"      # Tono: -20Hz a +20Hz
)
```

### Ejemplos de estilos:

| Estilo | Rate | Pitch | Volume |
|--------|------|-------|--------|
| 📰 Noticias | -10% | -5Hz | +0% |
| ⚽ Deportes | +20% | +0Hz | +10% |
| 🧘 Meditación | -30% | +0Hz | +0% |

---

# Edge TTS - Subtítulos SRT

```python
communicate = edge_tts.Communicate(TEXT, VOICE)
submaker = edge_tts.SubMaker()

with open("audio.mp3", "wb") as audio:
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.write(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            submaker.feed(chunk)

# Guardar subtítulos sincronizados
with open("subtitulos.srt", "w") as srt:
    srt.write(submaker.get_srt())
```

Genera subtítulos **sincronizados por palabra** automáticamente.

---

# Edge TTS - Limitaciones

| Limitación | Detalle |
|------------|---------|
| ❌ Sin SSML avanzado | Microsoft bloqueó SSML personalizado |
| ❌ Sin emociones | No tiene estilos como "cheerful", "sad" |
| ❌ Sin clonación | Solo voces predefinidas |
| ⚠️ Uso no comercial | Zona gris legal |
| ⚠️ Rate limiting | Sin límites documentados |
| ❌ Requiere internet | No funciona offline |

**Para producción comercial**: usar Azure Speech Services (oficial, de pago).

---

# PARTE 2
## Speech-to-Text (STT)
### Convertir voz en texto

---

# ¿Qué es Speech-to-Text?

```
┌─────────────┐         ┌─────────────┐
│   AUDIO     │  ────►  │   TEXTO     │
│   🎤        │   STT   │  "Hola..."  │
└─────────────┘         └─────────────┘
```

**STT** (también llamado ASR - Automatic Speech Recognition) convierte audio hablado en texto.

### Usos comunes:
- 🎤 Dictado de voz
- 📝 Transcripción de reuniones
- 🎬 Subtítulos automáticos
- 🤖 Comandos de voz

---

# Faster-Whisper - STT Local

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu")
segments, info = model.transcribe("audio.mp3", language="es")

for segment in segments:
    print(f"[{segment.start:.1f}s] {segment.text}")
```

### Modelos disponibles:

| Modelo | Tamaño | Velocidad | Precisión |
|--------|--------|-----------|-----------|
| tiny | 75 MB | ⚡⚡⚡ | ⭐ |
| base | 150 MB | ⚡⚡ | ⭐⭐ |
| small | 500 MB | ⚡ | ⭐⭐⭐ |
| medium | 1.5 GB | 🐢 | ⭐⭐⭐⭐ |
| large | 3 GB | 🐢🐢 | ⭐⭐⭐⭐⭐ |

---

# PARTE 3
## Voice Conversion
### Cambiar la identidad vocal

---

# ¿Qué es Voice Conversion?

```
┌─────────────┐         ┌─────────────┐
│  Audio de   │  ────►  │  Audio de   │
│  Persona A  │   VC    │  Persona B  │
└─────────────┘         └─────────────┘
```

**Voice Conversion** transforma la voz de una persona para que suene como otra, manteniendo el contenido y la prosodia.

### ⚠️ NO confundir con:
- **TTS**: Texto → Audio (genera desde cero)
- **Voice Cloning**: Texto + Referencia → Audio con voz clonada

---

# Método 1: STT → TTS (Pseudo Voice Conversion)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Audio      │───►│   TEXTO     │───►│  Audio      │
│  Sara       │STT │"Hola..."    │TTS │  Juan       │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Proceso:
1. **Transcribir** el audio original (STT)
2. **Regenerar** con otra voz (TTS)

### ❌ Problema:
- **Pierde la prosodia** (ritmo, pausas, entonación)
- El audio resultante tiene la "personalidad" del TTS, no del original

---

# Método 1: Código

```python
from faster_whisper import WhisperModel
import edge_tts

# Paso 1: Transcribir
model = WhisperModel("small")
segments, _ = model.transcribe("sara.mp3", language="es")
texto = " ".join([s.text for s in segments])

# Paso 2: Regenerar con otra voz
async def convertir():
    tts = edge_tts.Communicate(texto, "es-ES-AlvaroNeural")
    await tts.save("sara_como_alvaro.mp3")
```

**Útil para**: Crear versiones en diferentes acentos/idiomas
**No útil para**: Preservar la expresividad del original

---

# Método 2: Voice Conversion REAL con IA

```
┌─────────────┐    ┌─────────────────────┐    ┌─────────────┐
│  Audio      │───►│  MODELO DE IA       │───►│  Audio      │
│  Sara       │    │  • HuBERT           │    │  Con voz    │
│             │    │  • WavLM            │    │  de Juan    │
└─────────────┘    │  • Decoder          │    └─────────────┘
                   └─────────────────────┘
                              ▲
                              │
                   ┌─────────────────────┐
                   │  Voz de referencia  │
                   │  (Juan, 5-10 seg)   │
                   └─────────────────────┘
```

### ✅ Ventajas:
- **Preserva la prosodia** (ritmo, pausas, entonación)
- Solo cambia la **identidad vocal** (timbre)

---

# Voice Conversion Real: Arquitectura

```
╔══════════════════════════════════════════════════════════════════╗
║  AUDIO ORIGINAL (Sara)                                           ║
║  │                                                               ║
║  ▼                                                               ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │  HuBERT (Red Neuronal de Meta/Facebook)                    │ ║
║  │                                                            │ ║
║  │  • Extrae CONTENIDO LINGÜÍSTICO (fonemas, palabras)        │ ║
║  │  • Extrae PROSODIA (ritmo, pausas, entonación)             │ ║
║  │  • IGNORA el timbre/identidad vocal                        │ ║
║  │                                                            │ ║
║  │  Salida: Vector de características (embeddings)            │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

**HuBERT** fue entrenado con miles de horas de audio para "entender" el habla.

---

# Voice Conversion Real: Arquitectura (cont.)

```
╔══════════════════════════════════════════════════════════════════╗
║  VOZ DE REFERENCIA (Juan)                                        ║
║  │                                                               ║
║  ▼                                                               ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │  WavLM (Red Neuronal de Microsoft)                         │ ║
║  │                                                            │ ║
║  │  • Extrae EMBEDDING DE IDENTIDAD VOCAL                     │ ║
║  │  • Captura: timbre, formantes, características únicas      │ ║
║  │  • Solo necesita 5-10 segundos de audio                    │ ║
║  │                                                            │ ║
║  │  Salida: Vector de identidad vocal (speaker embedding)     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

**WavLM** aprendió qué hace ÚNICA a cada voz.

---

# Voice Conversion Real: Arquitectura (cont.)

```
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  Contenido + Prosodia (de HuBERT) ────┐                         ║
║                                        │                         ║
║                                        ▼                         ║
║                            ┌────────────────────┐                ║
║                            │     DECODER        │                ║
║                            │  (Red Neuronal)    │                ║
║                            │                    │                ║
║                            │  Combina:          │                ║
║                            │  • Contenido       │                ║
║                            │  • Prosodia        │                ║
║                            │  • Nueva identidad │                ║
║                            └────────────────────┘                ║
║                                        │                         ║
║  Identidad vocal (de WavLM) ──────────┘                         ║
║                                        │                         ║
║                                        ▼                         ║
║                            ┌────────────────────┐                ║
║                            │  AUDIO CONVERTIDO  │                ║
║                            │  (Sara con voz     │                ║
║                            │   de Juan)         │                ║
║                            └────────────────────┘                ║
╚══════════════════════════════════════════════════════════════════╝
```

---

# Voice Conversion Real: Código

```python
from TTS.api import TTS

# Cargar modelo FreeVC
model = TTS("voice_conversion_models/multilingual/vctk/freevc24")

# Voice Conversion
model.voice_conversion_to_file(
    source_wav="sara.wav",        # Audio original
    target_wav="juan.wav",        # Voz de referencia
    file_path="sara_como_juan.wav"  # Resultado
)
```

### Modelos disponibles:

| Modelo | ID |
|--------|-----|
| **FreeVC** | `voice_conversion_models/multilingual/vctk/freevc24` |
| **OpenVoice v1** | `voice_conversion_models/multilingual/multi-dataset/openvoice_v1` |
| **OpenVoice v2** | `voice_conversion_models/multilingual/multi-dataset/openvoice_v2` |

---

# Comparativa: STT→TTS vs VC Real

```
╔═══════════════════════════════════════════════════════════════════╗
║  MÉTODO STT → TTS                                                 ║
║  ─────────────────                                                ║
║  Audio Sara → Whisper → Texto → Edge TTS → Nuevo Audio            ║
║                                                                   ║
║  ❌ PIERDE: pausas, ritmo, entonación, emoción                    ║
║  ✅ CONSERVA: solo el contenido (palabras)                        ║
╠═══════════════════════════════════════════════════════════════════╣
║  VOICE CONVERSION REAL (FreeVC/OpenVoice)                         ║
║  ────────────────────────────────────────                         ║
║  Audio Sara → HuBERT → Contenido + Prosodia                       ║
║                         ↓                                         ║
║              WavLM ← Voz referencia (timbre)                      ║
║                         ↓                                         ║
║                    Nuevo Audio                                    ║
║                                                                   ║
║  ✅ PRESERVA: pausas, ritmo, entonación, emoción                  ║
║  ✅ CAMBIA: solo la identidad vocal (timbre)                      ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

# PARTE 4
## Voice Effects vs Voice Conversion con IA
### La diferencia fundamental

---

# Voice Effects (DSP) - ¿Qué es?

**DSP** = Digital Signal Processing (Procesamiento Digital de Señales)

```
┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│   Audio     │───►│  ALGORITMOS     │───►│   Audio     │
│   Original  │    │  MATEMÁTICOS    │    │   Modificado│
└─────────────┘    └─────────────────┘    └─────────────┘
```

### Operaciones típicas:
- **Pitch shift**: Cambiar frecuencia fundamental
- **Filtros**: Paso alto, paso bajo, paso banda
- **Reverb/Echo**: Añadir reflexiones
- **Distorsión**: Modificar forma de onda

---

# Voice Effects (DSP) - Ejemplos

## 🤖 Efecto Robot (DSP)
```python
# Downsampling (efecto digital)
robot = audio.set_frame_rate(8000).set_frame_rate(22050)

# Filtro paso bajo (más metálico)
robot = low_pass_filter(robot, 2000)

# Eco corto (efecto robótico)
eco = robot - 10
robot = robot.overlay(eco, position=50)
```

### Lo que hace matemáticamente:
1. Reduce resolución temporal → suena "digital"
2. Elimina frecuencias altas → suena "apagado"
3. Añade copia retrasada → suena "metálico"

---

# Voice Effects (DSP) - Ejemplos (cont.)

## 🎌 Efecto Anime (DSP)
```python
# Subir pitch (más agudo)
anime = audio._spawn(audio.raw_data, overrides={
    "frame_rate": int(audio.frame_rate * 1.4)
}).set_frame_rate(original_rate)

# Filtro paso alto (más brillo)
anime = high_pass_filter(anime, 200)
```

### Lo que hace matemáticamente:
1. Comprime en tiempo → frecuencias suben 40%
2. Elimina frecuencias graves → suena más "brillante"

**Problema**: Suena artificial, no como una persona real.

---

# Voice Conversion con IA - La diferencia

```
╔═══════════════════════════════════════════════════════════════════╗
║  VOICE EFFECTS (DSP)                                              ║
║  ───────────────────                                              ║
║  • Manipula FRECUENCIAS matemáticamente                           ║
║  • No "entiende" qué es una voz                                   ║
║  • Resultado: artificial, mecánico                                ║
║  • Ejemplo: pitch shift de +40% = todo sube igual                 ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║  VOICE CONVERSION CON IA                                          ║
║  ────────────────────────                                         ║
║  • Usa REDES NEURONALES entrenadas con miles de voces             ║
║  • "Entiende" qué hace única a cada voz                           ║
║  • Resultado: natural, preserva expresividad                      ║
║  • Ejemplo: transfiere SOLO el timbre, mantiene TODO lo demás     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

# Voice Conversion IA: Robot y Anime

Para crear estilos como "robot" o "anime" con IA necesitamos:

### Paso 1: Crear voz de REFERENCIA con el estilo deseado
```python
# Voz grave para "robot"
communicate = edge_tts.Communicate(
    text=texto_muestra,
    voice="es-ES-AlvaroNeural",
    pitch="-10Hz",  # Más grave
    rate="-20%"     # Más lento
)
await communicate.save("ref_robot.mp3")
```

### Paso 2: Usar FreeVC para transferir el estilo
```python
model.voice_conversion_to_file(
    source_wav="sara.wav",
    target_wav="ref_robot.wav",
    file_path="sara_robot_ia.wav"
)
```

---

# ¿Por qué la IA suena más natural?

## DSP (Pitch Shift):
```
Frecuencia original: 200 Hz → 280 Hz (+40%)
Formante F1: 500 Hz → 700 Hz (+40%)
Formante F2: 1500 Hz → 2100 Hz (+40%)

❌ TODO sube igual → suena como "ardilla"
```

## IA (Voice Conversion):
```
La red neuronal aprendió que:
- Las voces femeninas tienen F1 ≈ 850 Hz, F2 ≈ 2600 Hz
- Las voces masculinas tienen F1 ≈ 730 Hz, F2 ≈ 2200 Hz
- El timbre depende de la forma del tracto vocal

✅ Ajusta SELECTIVAMENTE las características vocales
✅ Preserva las proporciones naturales
```

---

# Arquitectura completa de VC con IA

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  AUDIO ORIGINAL ──► HuBERT ──► [Contenido + Prosodia] ──┐          │
│  (Sara hablando)                                         │          │
│                                                          ▼          │
│                                                    ┌──────────┐     │
│                                                    │ DECODER  │     │
│                                                    │(Neuronal)│     │
│                                                    └──────────┘     │
│                                                          ▲          │
│  VOZ REFERENCIA ──► WavLM ──► [Speaker Embedding] ──────┘          │
│  (estilo robot/                                                     │
│   anime/etc)                           │                            │
│                                        ▼                            │
│                               AUDIO CONVERTIDO                      │
│                               (Sara con estilo)                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

# PARTE 5
## Resumen y comparativa final

---

# Tecnologías cubiertas

| Tecnología | Función | Modelo/Herramienta |
|------------|---------|-------------------|
| **TTS** | Texto → Audio | Edge TTS, Coqui TTS |
| **STT** | Audio → Texto | Faster-Whisper |
| **VC (fake)** | Audio → Audio | STT + TTS |
| **VC (real)** | Audio → Audio | FreeVC, OpenVoice |
| **Effects** | Audio → Audio | pydub (DSP) |
| **VC + IA** | Audio → Audio estilizado | FreeVC + referencias |

---

# Cuándo usar cada tecnología

| Caso de uso | Tecnología recomendada |
|-------------|------------------------|
| Crear audiolibros | TTS (Edge TTS, OpenAI) |
| Transcribir reuniones | STT (Faster-Whisper) |
| Doblar video a otro idioma | STT → TTS |
| Cambiar voz preservando emoción | Voice Conversion (FreeVC) |
| Efectos especiales (robot, eco) | DSP (pydub) |
| Voz de personaje (anime, villano) | VC + IA (FreeVC + ref) |
| Clonar tu voz para TTS | XTTS, Coqui Voice Cloning |

---

# Modelos de IA involucrados

| Modelo | Desarrollador | Función |
|--------|---------------|---------|
| **HuBERT** | Meta/Facebook | Extraer contenido lingüístico |
| **WavLM** | Microsoft | Extraer embedding de voz |
| **Whisper** | OpenAI | Speech-to-Text |
| **FreeVC** | Open source | Voice Conversion |
| **OpenVoice** | MyShell | Voice Conversion |
| **XTTS** | Coqui | TTS con clonación |

---

# Diagrama completo del ecosistema

```
                    ┌─────────────────────────────────────┐
                    │           ENTRADA                   │
                    │   ┌─────────┐    ┌─────────┐       │
                    │   │  TEXTO  │    │  AUDIO  │       │
                    │   └────┬────┘    └────┬────┘       │
                    │        │              │             │
                    └────────┼──────────────┼─────────────┘
                             │              │
              ┌──────────────┼──────────────┼──────────────┐
              │              ▼              ▼              │
              │         ┌────────┐    ┌────────┐          │
              │         │  TTS   │    │  STT   │          │
              │         └────┬───┘    └────┬───┘          │
              │              │              │              │
              │              ▼              ▼              │
              │         ┌────────────────────┐            │
              │         │       AUDIO        │            │
              │         └─────────┬──────────┘            │
              │                   │                       │
              │     ┌─────────────┼─────────────┐        │
              │     ▼             ▼             ▼        │
              │ ┌────────┐  ┌──────────┐  ┌────────┐    │
              │ │ EFFECTS│  │  VOICE   │  │ VOICE  │    │
              │ │  (DSP) │  │CONVERSION│  │CLONING │    │
              │ └────────┘  └──────────┘  └────────┘    │
              │                                          │
              └──────────────────────────────────────────┘
```

---

# Ejercicios creados en esta sesión

| Archivo | Descripción |
|---------|-------------|
| `03j_tts_edge_microsoft.py` | TTS básico con Edge |
| `03k_tts_edge_avanzado.py` | TTS con velocidad, tono, subtítulos |
| `03l_voice_conversion.py` | VC con STT→TTS |
| `03m_voice_conversion_real.py` | VC real con FreeVC |
| `03n_voice_effects.py` | Efectos DSP (robot, anime...) |
| `03o_voice_conversion_estilos_ia.py` | VC con IA para estilos |

---

# Archivos de audio generados

## Voice Conversion STT→TTS:
- `voice_converted_hombre_espanol.mp3`
- `voice_converted_hombre_argentino.mp3`
- `voice_converted_mujer_mexicana.mp3`
- ... (9 variantes)

## Voice Effects (DSP):
- `voice_effect_robot.mp3`
- `voice_effect_anime.mp3`
- `voice_effect_fantasma.mp3`
- ... (7 efectos)

---

# Archivos de audio generados (cont.)

## Voice Conversion Real (FreeVC):
- `vc_real_hombre_es_freevc.wav`
- `vc_real_hombre_ar_freevc.wav`

## Voice Conversion IA (estilos):
- `vc_ia_robot_grave.wav`
- `vc_ia_anime_femenino.wav`
- `vc_ia_anime_kawaii.wav`
- `vc_ia_villano.wav`
- `vc_ia_robot_ia.wav`

---

# Conclusiones

## Lo que aprendimos:

1. **TTS** ha evolucionado de robótico a indistinguible de humanos
2. **Voice Conversion** puede ser "fake" (STT→TTS) o "real" (IA)
3. **Effects DSP** son rápidos pero artificiales
4. **Voice Conversion con IA** preserva la expresividad natural
5. Las **redes neuronales** (HuBERT, WavLM) "entienden" la voz

## Próximos pasos:
- Explorar **RVC** para entrenamiento de voces personalizadas
- Probar **ElevenLabs** para calidad premium
- Implementar **streaming** para tiempo real

---

# ¿Preguntas?

## Recursos adicionales:

- 📚 [Edge TTS GitHub](https://github.com/rany2/edge-tts)
- 📚 [Coqui TTS Docs](https://tts.readthedocs.io/)
- 📚 [FreeVC Paper](https://arxiv.org/abs/2210.15418)
- 📚 [HuBERT Paper](https://arxiv.org/abs/2106.07447)
- 📚 [WavLM Paper](https://arxiv.org/abs/2110.13900)

---

# ¡Gracias!

## Código disponible en:
`sesion08/03j_*.py` - `sesion08/03o_*.py`

## Audios de ejemplo en:
`sesion08/voice_*.mp3` y `sesion08/vc_*.wav`

