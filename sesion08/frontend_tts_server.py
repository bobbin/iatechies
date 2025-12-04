"""
Frontend TTS - Servidor FastAPI (Avanzado)
==========================================
Servidor web para demostrar Text-to-Speech con funcionalidades avanzadas.

Backends soportados:
- pyttsx3: Voces del sistema (local, gratis)
- Coqui VITS: Modelo IA español (local, gratis)
- Coqui XTTS: Multilingüe con clonación de voz (local, gratis)
- Kokoro TTS: Modelo ligero multilingüe vía HuggingFace (cloud, gratis)
- OpenAI TTS: Voces premium (cloud, de pago)

Ejecución:
python frontend_tts_server.py

Abrir: http://localhost:8081
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import tempfile
import time
import shutil
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Demo TTS - Text to Speech (Avanzado)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales - modelos cargados
pyttsx3_engine = None
coqui_vits_es = None
coqui_xtts = None
openai_client = None
temp_files = []

# Directorio para audios de referencia
REFERENCE_DIR = Path(tempfile.gettempdir()) / "tts_references"
REFERENCE_DIR.mkdir(exist_ok=True)


class TTSRequest(BaseModel):
    text: str
    backend: str = "coqui_vits"
    voice: str = "default"
    speed: float = 1.0
    language: str = "es"
    speaker: str = "default"
    reference_audio: Optional[str] = None


def get_pyttsx3():
    """Motor pyttsx3"""
    global pyttsx3_engine
    if pyttsx3_engine is None:
        try:
            import pyttsx3
            pyttsx3_engine = pyttsx3.init()
        except:
            return None
    return pyttsx3_engine


def get_coqui_vits():
    """Coqui TTS - Modelo español VITS"""
    global coqui_vits_es
    if coqui_vits_es is None:
        try:
            from TTS.api import TTS
            print("Cargando Coqui VITS (espanol)...")
            coqui_vits_es = TTS(model_name="tts_models/es/css10/vits")
            print("Coqui VITS cargado OK")
        except Exception as e:
            print(f"Error cargando Coqui VITS: {e}")
            return None
    return coqui_vits_es


def get_coqui_xtts():
    """Coqui TTS - XTTS v2 Multilingüe"""
    global coqui_xtts
    if coqui_xtts is None:
        try:
            from TTS.api import TTS
            print("Cargando XTTS v2 (multilingue)...")
            # Aceptar términos automáticamente
            os.environ["COQUI_TOS_AGREED"] = "1"
            coqui_xtts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            print("XTTS v2 cargado OK")
            if hasattr(coqui_xtts, 'speakers'):
                print(f"  Speakers: {len(coqui_xtts.speakers) if coqui_xtts.speakers else 0}")
            if hasattr(coqui_xtts, 'languages'):
                print(f"  Idiomas: {coqui_xtts.languages}")
        except Exception as e:
            print(f"Error cargando XTTS: {e}")
            return None
    return coqui_xtts


def get_openai():
    """Cliente OpenAI"""
    global openai_client
    if openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            from openai import OpenAI
            openai_client = OpenAI(api_key=api_key)
    return openai_client


def get_kokoro_token():
    """Token para Kokoro TTS via HuggingFace Router"""
    return os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")


def kokoro_tts(text: str, voice: str = "af_heart") -> bytes:
    """
    Genera audio con Kokoro TTS via HuggingFace Router + fal-ai
    
    Endpoints disponibles:
    - american-english: voces af_* y am_*
    - british-english: voces bf_* y bm_*  
    - spanish: voces ef_* y em_*
    - Y otros idiomas...
    """
    hf_token = get_kokoro_token()
    if not hf_token:
        raise Exception("HF_TOKEN no configurado")
    
    # Determinar el endpoint según el prefijo de la voz
    # Si hay mezcla (formato: "voice1[weight1]+voice2[weight2]"), extraer la primera voz
    if "+" in voice:
        # Es una mezcla, extraer la primera voz
        first_voice = voice.split("+")[0].split("[")[0]  # Ej: "ef_dora[0.7]" -> "ef_dora"
        voice_prefix = first_voice[:2] if len(first_voice) >= 2 else "af"
        print(f"🎨 Mezcla detectada. Primera voz: {first_voice}, prefijo: {voice_prefix}")
    else:
        voice_prefix = voice[:2] if len(voice) >= 2 else "af"
    
    # Mapeo de prefijos a endpoints
    endpoint_map = {
        "af": "american-english",  # American Female
        "am": "american-english",  # American Male
        "bf": "british-english",   # British Female
        "bm": "british-english",   # British Male
        "ef": "spanish",           # Español Female
        "em": "spanish",           # Español Male
        "ff": "french",            # French Female
        "fm": "french",            # French Male
        "hf": "hindi",             # Hindi Female
        "hm": "hindi",             # Hindi Male
        "if": "italian",           # Italian Female
        "im": "italian",           # Italian Male
        "jf": "japanese",          # Japanese Female
        "jm": "japanese",          # Japanese Male
        "pf": "brazilian-portuguese",  # Portuguese Female
        "pm": "brazilian-portuguese",  # Portuguese Male
        "zf": "mandarin-chinese",  # Chinese Female
        "zm": "mandarin-chinese",  # Chinese Male
    }
    
    lang_endpoint = endpoint_map.get(voice_prefix, "american-english")
    
    API_URL = f"https://router.huggingface.co/fal-ai/fal-ai/kokoro/{lang_endpoint}"
    
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    
    # El payload debe usar "prompt" según la documentación de fal.ai
    payload = {
        "prompt": text,
        "voice": voice
    }
    
    print(f"🌐 Llamando a: {API_URL}")
    print(f"   Payload: {payload}")
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
    # La respuesta puede ser JSON con audio y sampling_rate, o directamente bytes
    content_type = response.headers.get("content-type", "").lower()
    
    # Intentar parsear como JSON primero
    try:
        data = response.json()
        print(f"📦 Respuesta JSON recibida. Keys: {list(data.keys())}")
        
        # Si es JSON, el audio puede estar en base64 o como lista de floats
        if "audio" in data:
            audio_data = data["audio"]
            sampling_rate = data.get("sampling_rate", 24000)
            
            print(f"🎵 Tipo de audio_data: {type(audio_data)}")
            
            # Si es lista de floats, convertir a WAV
            if isinstance(audio_data, list):
                import numpy as np
                import struct
                import io
                
                print(f"📊 Audio es lista de {len(audio_data)} elementos")
                
                # Convertir floats a int16
                audio_array = np.array(audio_data, dtype=np.float32)
                audio_int16 = (audio_array * 32767).astype(np.int16)
                
                # Crear WAV en memoria
                wav_buffer = io.BytesIO()
                # Header WAV
                wav_buffer.write(b'RIFF')
                wav_buffer.write(struct.pack('<I', 36 + len(audio_int16) * 2))
                wav_buffer.write(b'WAVE')
                wav_buffer.write(b'fmt ')
                wav_buffer.write(struct.pack('<I', 16))  # Subchunk1Size
                wav_buffer.write(struct.pack('<H', 1))   # AudioFormat (PCM)
                wav_buffer.write(struct.pack('<H', 1))   # NumChannels
                wav_buffer.write(struct.pack('<I', sampling_rate))  # SampleRate
                wav_buffer.write(struct.pack('<I', sampling_rate * 2))  # ByteRate
                wav_buffer.write(struct.pack('<H', 2))   # BlockAlign
                wav_buffer.write(struct.pack('<H', 16))  # BitsPerSample
                wav_buffer.write(b'data')
                wav_buffer.write(struct.pack('<I', len(audio_int16) * 2))
                wav_buffer.write(audio_int16.tobytes())
                
                return wav_buffer.getvalue()
            elif isinstance(audio_data, str):
                # Base64 encoded
                print("🔐 Audio es string (base64)")
                import base64
                return base64.b64decode(audio_data)
            elif isinstance(audio_data, dict):
                # Si audio es un dict, puede tener 'url' o 'data'
                print(f"📦 Audio es dict. Keys: {list(audio_data.keys())}")
                if "url" in audio_data:
                    # Descargar desde URL
                    audio_url = audio_data["url"]
                    print(f"🌐 Descargando audio desde: {audio_url}")
                    audio_response = requests.get(audio_url, timeout=30)
                    audio_response.raise_for_status()
                    return audio_response.content
                elif "data" in audio_data:
                    # Datos directos
                    return audio_data["data"]
                else:
                    raise Exception(f"Dict audio sin 'url' ni 'data': {list(audio_data.keys())}")
            else:
                raise Exception(f"Formato de audio_data no soportado: {type(audio_data)}. Valor: {str(audio_data)[:100]}")
        else:
            raise Exception(f"Respuesta JSON sin clave 'audio'. Keys disponibles: {list(data.keys())}")
    except ValueError:
        # No es JSON, es bytes directo
        print("📦 Respuesta es bytes directos")
        return response.content


# Voces disponibles en Kokoro TTS (hexgrad/Kokoro-82M)
KOKORO_VOICES = {
    # Voces en español
    "ef_dora": "🇪🇸 Dora (ES Femenina)",
    "em_alex": "🇪🇸 Alex (ES Masculina)",
    "ef_bella": "🇪🇸 Bella (ES Femenina)",
    "em_santa": "🇪🇸 Santa (ES Masculina)",
    # Voces en inglés americano
    "af_heart": "🇺🇸 Heart (EN-US Femenina)",
    "af_alloy": "🇺🇸 Alloy (EN-US Femenina)",
    "af_aoede": "🇺🇸 Aoede (EN-US Femenina)",
    "af_bella": "🇺🇸 Bella (EN-US Femenina)",
    "af_jessica": "🇺🇸 Jessica (EN-US Femenina)",
    "af_kore": "🇺🇸 Kore (EN-US Femenina)",
    "af_nicole": "🇺🇸 Nicole (EN-US Femenina)",
    "af_nova": "🇺🇸 Nova (EN-US Femenina)",
    "af_river": "🇺🇸 River (EN-US Femenina)",
    "af_sarah": "🇺🇸 Sarah (EN-US Femenina)",
    "af_sky": "🇺🇸 Sky (EN-US Femenina)",
    "am_adam": "🇺🇸 Adam (EN-US Masculina)",
    "am_echo": "🇺🇸 Echo (EN-US Masculina)",
    "am_eric": "🇺🇸 Eric (EN-US Masculina)",
    "am_fenrir": "🇺🇸 Fenrir (EN-US Masculina)",
    "am_liam": "🇺🇸 Liam (EN-US Masculina)",
    "am_michael": "🇺🇸 Michael (EN-US Masculina)",
    "am_onyx": "🇺🇸 Onyx (EN-US Masculina)",
    # Voces en inglés británico
    "bf_emma": "🇬🇧 Emma (EN-GB Femenina)",
    "bf_isabella": "🇬🇧 Isabella (EN-GB Femenina)",
    "bm_george": "🇬🇧 George (EN-GB Masculina)",
    "bm_lewis": "🇬🇧 Lewis (EN-GB Masculina)",
    # Otras voces
    "ff_siwis": "🇫🇷 Siwis (FR Femenina)",
    "hf_alpha": "🇮🇳 Alpha (HI Femenina)",
    "hm_omega": "🇮🇳 Omega (HI Masculina)",
    "if_sara": "🇮🇹 Sara (IT Femenina)",
    "im_nicola": "🇮🇹 Nicola (IT Masculina)",
    "jf_alpha": "🇯🇵 Alpha (JA Femenina)",
    "jf_gongitsune": "🇯🇵 Gongitsune (JA Femenina)",
    "jm_kumo": "🇯🇵 Kumo (JA Masculina)",
    "pf_dora": "🇧🇷 Dora (PT-BR Femenina)",
    "pm_alex": "🇧🇷 Alex (PT-BR Masculina)",
    "zf_xiaobei": "🇨🇳 Xiaobei (ZH Femenina)",
    "zf_xiaoni": "🇨🇳 Xiaoni (ZH Femenina)",
    "zm_yunjian": "🇨🇳 Yunjian (ZH Masculina)",
}


@app.get("/", response_class=HTMLResponse)
async def home():
    """Página principal"""
    html_path = Path(__file__).parent / "frontend_tts.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Error: frontend_tts.html no encontrado</h1>"


@app.get("/api/status")
async def status():
    """Estado de los servicios"""
    pyttsx3_ok = False
    coqui_ok = False
    xtts_ok = False
    kokoro_ok = False
    
    try:
        import pyttsx3
        pyttsx3_ok = True
    except:
        pass
    
    try:
        from TTS.api import TTS
        coqui_ok = True
        xtts_ok = True  # Si TTS está instalado, XTTS también
    except:
        pass
    
    # Kokoro via HuggingFace
    kokoro_ok = (os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")) is not None
    
    return {
        "pyttsx3": pyttsx3_ok,
        "coqui_vits": coqui_ok,
        "coqui_xtts": xtts_ok,
        "kokoro": kokoro_ok,
        "openai": os.getenv("OPENAI_API_KEY") is not None
    }


@app.get("/api/models")
async def get_models():
    """Información de modelos disponibles"""
    return {
        "coqui_vits": {
            "name": "Coqui VITS (Español)",
            "description": "Modelo IA de alta calidad para español",
            "languages": ["es"],
            "speakers": [],
            "supports_cloning": False
        },
        "coqui_xtts": {
            "name": "Coqui XTTS v2 (Multilingüe)",
            "description": "Modelo avanzado con 17 idiomas y clonación de voz",
            "languages": ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko", "hi"],
            "speakers": get_xtts_speakers(),
            "supports_cloning": True
        },
        "kokoro": {
            "name": "Kokoro TTS (HuggingFace)",
            "description": "Modelo ligero 82M vía HuggingFace - Español, Inglés, +6 idiomas",
            "languages": ["es", "en-us", "en-gb", "fr", "it", "pt-br", "ja", "zh", "hi"],
            "speakers": list(KOKORO_VOICES.keys()),
            "speaker_names": KOKORO_VOICES,
            "supports_cloning": False
        },
        "pyttsx3": {
            "name": "pyttsx3 (Sistema)",
            "description": "Voces del sistema operativo",
            "languages": ["sistema"],
            "speakers": get_pyttsx3_voices(),
            "supports_cloning": False
        },
        "openai": {
            "name": "OpenAI TTS",
            "description": "Voces premium de OpenAI",
            "languages": ["auto"],
            "speakers": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "supports_cloning": False
        }
    }


def get_xtts_speakers():
    """Obtener speakers de XTTS sin cargar el modelo completo"""
    # Speakers predefinidos de XTTS v2
    return [
        "Claribel Dervla", "Daisy Studious", "Gracie Wise", "Tammie Ema",
        "Alison Dietlinde", "Ana Florence", "Annmarie Nele", "Asya Anara",
        "Brenda Stern", "Gitta Nikolina", "Henriette Usha", "Sofia Hellen",
        "Tammy Grit", "Tanja Adelina", "Vjollca Johnnie", "Andrew Chipper",
        "Badr Odhiambo", "Dionisio Schuyler", "Royston Min", "Viktor Eka",
        "Abrahan Mack", "Adde Michal", "Baldur Sansen", "Craig Gutsy",
        "Damien Black", "Gilberto Mathias", "Ilkin Urbansen", "Kazuhiko Atallah",
        "Ludvig Milivoj", "Suad Qasim", "Torcull Diarmuid", "Viktor Menelaos",
        "Zacharie Aimilios", "Nova", "Adam", "Antoni"
    ]


def get_pyttsx3_voices():
    """Obtener voces de pyttsx3"""
    voices = []
    engine = get_pyttsx3()
    if engine:
        for v in engine.getProperty('voices'):
            name = v.name if hasattr(v, 'name') else str(v.id)[-30:]
            voices.append(name)
    return voices


@app.post("/api/upload_reference")
async def upload_reference(audio: UploadFile = File(...)):
    """Subir audio de referencia para clonación de voz"""
    if not audio.filename:
        raise HTTPException(400, "No se proporcionó archivo")
    
    # Validar extensión
    allowed = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
    ext = Path(audio.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, f"Formato no soportado. Usar: {', '.join(allowed)}")
    
    # Guardar archivo
    filename = f"ref_{int(time.time())}{ext}"
    filepath = REFERENCE_DIR / filename
    
    with open(filepath, "wb") as f:
        shutil.copyfileobj(audio.file, f)
    
    return {
        "success": True,
        "reference_id": filename,
        "message": "Audio de referencia subido correctamente"
    }


@app.post("/api/synthesize")
async def synthesize(request: TTSRequest):
    """Generar audio desde texto"""
    if not request.text.strip():
        raise HTTPException(400, "Texto vacío")
    
    # Crear archivo temporal
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.close()
    output_path = tmp.name
    temp_files.append(output_path)
    
    inicio = time.time()
    
    try:
        if request.backend == "pyttsx3":
            engine = get_pyttsx3()
            if not engine:
                raise HTTPException(500, "pyttsx3 no disponible")
            
            engine.setProperty('rate', int(150 * request.speed))
            if request.voice != "default":
                # Buscar voz por nombre
                voices = engine.getProperty('voices')
                for v in voices:
                    if request.voice in v.name or request.voice in v.id:
                        engine.setProperty('voice', v.id)
                        break
            
            engine.save_to_file(request.text, output_path)
            engine.runAndWait()
            
        elif request.backend == "coqui_vits":
            tts = get_coqui_vits()
            if not tts:
                raise HTTPException(500, "Coqui VITS no disponible")
            
            tts.tts_to_file(text=request.text, file_path=output_path)
            
        elif request.backend == "coqui_xtts":
            tts = get_coqui_xtts()
            if not tts:
                raise HTTPException(500, "XTTS no disponible. Requiere aceptar licencia CPML.")
            
            # Preparar parámetros
            kwargs = {
                "text": request.text,
                "file_path": output_path,
                "language": request.language if request.language else "es"
            }
            
            # XTTS v2 requiere speaker_wav o speaker_id
            speaker_wav_provided = False
            
            # Si hay audio de referencia, usar clonación
            if request.reference_audio and request.reference_audio != "none":
                ref_path = REFERENCE_DIR / request.reference_audio
                if ref_path.exists():
                    kwargs["speaker_wav"] = str(ref_path)
                    speaker_wav_provided = True
                else:
                    raise HTTPException(400, "Audio de referencia no encontrado")
            
            # Si no hay referencia, generar una automáticamente con pyttsx3
            if not speaker_wav_provided:
                try:
                    import pyttsx3
                    # Generar audio de referencia temporal
                    ref_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                    ref_temp.close()
                    
                    engine = pyttsx3.init()
                    texto_ref = "Hola, esta es una voz de referencia para el modelo multilingüe."
                    engine.save_to_file(texto_ref, ref_temp.name)
                    engine.runAndWait()
                    
                    if os.path.exists(ref_temp.name):
                        kwargs["speaker_wav"] = ref_temp.name
                        print(f"✅ Audio de referencia generado automáticamente: {ref_temp.name}")
                    else:
                        raise HTTPException(500, "No se pudo generar audio de referencia")
                except Exception as e:
                    print(f"⚠️  Error generando referencia automática: {e}")
                    raise HTTPException(
                        500, 
                        f"XTTS requiere un audio de referencia. Sube uno en la sección 'Clonación de Voz' o instala pyttsx3 para generación automática. Error: {str(e)}"
                    )
            
            tts.tts_to_file(**kwargs)
            
            # Limpiar archivo temporal de referencia si se generó automáticamente
            if not speaker_wav_provided and "speaker_wav" in kwargs:
                try:
                    if os.path.exists(kwargs["speaker_wav"]) and kwargs["speaker_wav"].startswith(tempfile.gettempdir()):
                        os.unlink(kwargs["speaker_wav"])
                except:
                    pass
            
        elif request.backend == "kokoro":
            # Kokoro TTS via HuggingFace Router + fal-ai
            if not get_kokoro_token():
                raise HTTPException(500, "HF_TOKEN no configurado para Kokoro TTS. Añade HF_TOKEN en .env")
            
            # Verificar si hay mezcla de voces en request.voice
            voice = None
            using_blend = False
            blend_warning = None
            
            if request.voice and request.voice != "default" and "+" in request.voice:
                # Hay una mezcla, pero la API de fal.ai NO soporta mezclas
                # Extraer la primera voz de la mezcla
                first_voice = request.voice.split("+")[0].split("[")[0].strip()
                voice = first_voice if first_voice in KOKORO_VOICES else "ef_dora"
                using_blend = True
                blend_warning = f"⚠️ La API de fal.ai no soporta mezclas de voces. Usando solo la primera voz: {voice}"
                print(f"🎨 Mezcla detectada: {request.voice}")
                print(f"   {blend_warning}")
            else:
                # Usar voz individual del selector
                voice = request.speaker if request.speaker in KOKORO_VOICES else "ef_dora"
                print(f"🎤 Usando voz individual: {voice} ({KOKORO_VOICES.get(voice, 'desconocida')})")
            
            print(f"🎤 Kokoro TTS via HuggingFace Router")
            print(f"   Voz final: {voice}")
            print(f"   Texto: {request.text[:80]}...")
            
            try:
                # Llamar a la API usando requests directo
                # La API de fal.ai solo acepta voces individuales del enum
                audio_bytes = kokoro_tts(request.text, voice)
                
                print(f"✅ Audio generado: {len(audio_bytes)} bytes con voz {voice}")
                
                # Guardar el audio
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
                    
            except Exception as e:
                print(f"❌ Error en Kokoro: {str(e)}")
                raise HTTPException(500, f"Error en Kokoro TTS: {str(e)}")
            
        elif request.backend == "openai":
            client = get_openai()
            if not client:
                raise HTTPException(500, "OpenAI API key no configurada")
            
            voice = request.voice if request.voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"] else "nova"
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=request.text,
                speed=request.speed
            )
            
            mp3_path = output_path.replace('.wav', '.mp3')
            response.stream_to_file(mp3_path)
            output_path = mp3_path
            temp_files.append(output_path)
        
        else:
            raise HTTPException(400, f"Backend no válido: {request.backend}")
        
        tiempo = time.time() - inicio
        
        # Obtener tamaño
        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / 1024
        else:
            raise HTTPException(500, "Error al generar audio")
        
        # Calcular costo para OpenAI
        costo = None
        if request.backend == "openai":
            costo = (len(request.text) / 1000) * 0.015
        
        # Preparar respuesta
        response_data = {
            "success": True,
            "audio_url": f"/api/audio/{Path(output_path).name}",
            "processing_time": round(tiempo, 2),
            "file_size": round(size, 1),
            "characters": len(request.text),
            "cost": round(costo, 4) if costo else None,
            "backend": request.backend,
            "language": request.language
        }
        
        # Añadir warning si se usó mezcla en Kokoro
        if request.backend == "kokoro" and request.voice and request.voice != "default" and "+" in request.voice:
            response_data["warning"] = "La API de fal.ai no soporta mezclas de voces. Se usó solo la primera voz de la mezcla."
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """Servir archivo de audio"""
    for path in temp_files:
        if Path(path).name == filename:
            if os.path.exists(path):
                media_type = "audio/mpeg" if filename.endswith('.mp3') else "audio/wav"
                return FileResponse(path, media_type=media_type)
    
    raise HTTPException(404, "Archivo no encontrado")


@app.get("/api/references")
async def list_references():
    """Listar audios de referencia disponibles"""
    refs = []
    if REFERENCE_DIR.exists():
        for f in REFERENCE_DIR.iterdir():
            if f.is_file():
                refs.append({
                    "id": f.name,
                    "size": round(f.stat().st_size / 1024, 1)
                })
    return {"references": refs}


@app.delete("/api/references/{ref_id}")
async def delete_reference(ref_id: str):
    """Eliminar audio de referencia"""
    ref_path = REFERENCE_DIR / ref_id
    if ref_path.exists():
        ref_path.unlink()
        return {"success": True}
    raise HTTPException(404, "Referencia no encontrada")


@app.on_event("shutdown")
async def cleanup():
    """Limpiar archivos temporales"""
    for path in temp_files:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  Demo Text-to-Speech (Avanzado)")
    print("=" * 50)
    print("\n  Backends disponibles:")
    print("    - pyttsx3: Voces del sistema")
    print("    - Coqui VITS: Modelo espanol IA")
    print("    - Coqui XTTS: Multilingue + clonacion")
    print("    - OpenAI TTS: Voces premium")
    print(f"\n  Abriendo: http://localhost:8081")
    print(f"\n  Presiona Ctrl+C para detener\n")
    uvicorn.run(app, host="0.0.0.0", port=8081)
