"""
Frontend STT - Servidor FastAPI
===============================
Servidor web para demostrar Speech-to-Text.
Soporta Faster-Whisper (local) y OpenAI Whisper (cloud).

Instalación:
pip install fastapi uvicorn python-multipart faster-whisper openai python-dotenv

Ejecución:
python frontend_stt_server.py

Abrir: http://localhost:8080
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Demo STT - Speech to Text")

# CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales para modelos
whisper_model = None
openai_client = None


def get_whisper_model():
    """Cargar modelo Faster-Whisper (lazy loading)"""
    global whisper_model
    if whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            print("Cargando modelo Faster-Whisper...")
            whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
            print("Modelo cargado OK")
        except ImportError:
            print("Faster-Whisper no instalado")
            return None
    return whisper_model


def get_openai_client():
    """Obtener cliente OpenAI"""
    global openai_client
    if openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            from openai import OpenAI
            openai_client = OpenAI(api_key=api_key)
    return openai_client


@app.get("/", response_class=HTMLResponse)
async def home():
    """Página principal"""
    html_path = Path(__file__).parent / "frontend_stt.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Error: frontend_stt.html no encontrado</h1>"


@app.get("/api/status")
async def status():
    """Estado de los servicios"""
    return {
        "faster_whisper": get_whisper_model() is not None,
        "openai": os.getenv("OPENAI_API_KEY") is not None
    }


@app.post("/api/transcribe/local")
async def transcribe_local(
    audio: UploadFile = File(...),
    language: str = Form("es")
):
    """Transcribir con Faster-Whisper (local)"""
    try:
        model = get_whisper_model()
        if model is None:
            raise HTTPException(
                status_code=500,
                detail="Faster-Whisper no disponible. Instala con: pip install faster-whisper"
            )
        
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await audio.read()
            if not content:
                raise HTTPException(status_code=400, detail="Archivo de audio vacío")
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            inicio = time.time()
            
            # Transcribir
            segments, info = model.transcribe(
                tmp_path,
                language=language if language != "auto" else None,
                word_timestamps=True
            )
            
            # Procesar segmentos
            segments_list = []
            texto_completo = ""
            
            for seg in segments:
                segments_list.append({
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip()
                })
                texto_completo += seg.text
            
            tiempo = time.time() - inicio
            
            return {
                "success": True,
                "backend": "Faster-Whisper (Local)",
                "text": texto_completo.strip(),
                "language": info.language,
                "language_probability": round(info.language_probability * 100, 1),
                "duration": round(info.duration, 2),
                "processing_time": round(tiempo, 2),
                "segments": segments_list
            }
            
        except Exception as e:
            print(f"❌ Error transcribiendo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al transcribir: {str(e)}"
            )
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass
                
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en transcribe_local: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error del servidor: {str(e)}"
        )


@app.post("/api/transcribe/openai")
async def transcribe_openai(
    audio: UploadFile = File(...),
    language: str = Form("es")
):
    """Transcribir con OpenAI Whisper API"""
    try:
        client = get_openai_client()
        if client is None:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key no configurada. Agrega OPENAI_API_KEY en .env"
            )
        
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await audio.read()
            if not content:
                raise HTTPException(status_code=400, detail="Archivo de audio vacío")
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            inicio = time.time()
            
            with open(tmp_path, "rb") as audio_file:
                # Transcribir con formato detallado
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    language=language if language != "auto" else None
                )
            
            tiempo = time.time() - inicio
            
            # Procesar segmentos si existen
            segments_list = []
            if hasattr(transcript, 'segments') and transcript.segments:
                for seg in transcript.segments:
                    segments_list.append({
                        "start": round(seg['start'], 2),
                        "end": round(seg['end'], 2),
                        "text": seg['text'].strip()
                    })
            
            return {
                "success": True,
                "backend": "OpenAI Whisper API",
                "text": transcript.text,
                "language": transcript.language,
                "language_probability": 100,  # OpenAI no devuelve probabilidad
                "duration": round(transcript.duration, 2),
                "processing_time": round(tiempo, 2),
                "segments": segments_list
            }
            
        except Exception as e:
            print(f"❌ Error transcribiendo con OpenAI: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al transcribir con OpenAI: {str(e)}"
            )
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass
                
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en transcribe_openai: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error del servidor: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  Demo Speech-to-Text")
    print("=" * 50)
    print(f"\n  Abriendo: http://localhost:8080")
    print(f"\n  Presiona Ctrl+C para detener\n")
    uvicorn.run(app, host="0.0.0.0", port=8080)

