"""
STT OpenAI - Archivos Grandes (>25 MB)
======================================
Estrategias para transcribir archivos mayores a 25 MB.

Este ejemplo demuestra:
- Dividir audio en chunks con pydub
- Procesar cada chunk por separado
- Unir transcripciones
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def dividir_audio_ejemplo():
    """Ejemplo de cómo dividir audio con pydub"""
    codigo = '''
from pydub import AudioSegment

def dividir_audio(archivo_entrada, chunk_duracion_ms=600000):
    """
    Dividir audio en chunks de 10 minutos (600,000 ms)
    
    Args:
        archivo_entrada: Ruta al archivo de audio
        chunk_duracion_ms: Duración de cada chunk en ms
    
    Returns:
        Lista de nombres de archivos chunk
    """
    audio = AudioSegment.from_file(archivo_entrada)
    
    chunks = []
    for i in range(0, len(audio), chunk_duracion_ms):
        chunk = audio[i:i + chunk_duracion_ms]
        chunk_filename = f"chunk_{i // chunk_duracion_ms}.mp3"
        chunk.export(chunk_filename, format="mp3")
        chunks.append(chunk_filename)
        print(f"Creado: {chunk_filename}")
    
    return chunks

# Uso
chunks = dividir_audio("audio_grande.mp3")
'''
    return codigo


def transcribir_chunks_ejemplo():
    """Ejemplo de cómo transcribir chunks"""
    codigo = '''
from openai import OpenAI

def transcribir_chunks(client, chunks):
    """
    Transcribir lista de chunks y unir resultados
    """
    transcripciones = []
    
    for i, chunk in enumerate(chunks):
        print(f"Procesando chunk {i+1}/{len(chunks)}...")
        
        with open(chunk, "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
                language="es"
            )
        
        transcripciones.append(transcript.text)
    
    # Unir todas las transcripciones
    texto_completo = " ".join(transcripciones)
    return texto_completo

# Uso
client = OpenAI()
chunks = ["chunk_0.mp3", "chunk_1.mp3", "chunk_2.mp3"]
texto = transcribir_chunks(client, chunks)
'''
    return codigo


def main():
    print("📦 Archivos Grandes (>25 MB)")
    print("=" * 50)
    
    print(f"\n⚠️  Límite de OpenAI Whisper: 25 MB por archivo")
    
    print(f"\n💡 Estrategias para archivos grandes:")
    print(f"   1. Dividir en chunks de ~10 minutos")
    print(f"   2. Comprimir audio (ej: WAV → MP3)")
    print(f"   3. Reducir calidad (bitrate más bajo)")
    print(f"   4. Usar Faster-Whisper local (sin límite)")
    
    print(f"\n📝 Código para dividir audio:")
    print("-" * 50)
    print(dividir_audio_ejemplo())
    
    print(f"\n📝 Código para transcribir chunks:")
    print("-" * 50)
    print(transcribir_chunks_ejemplo())
    
    print(f"\n📦 Instalación de pydub:")
    print(f"   pip install pydub")
    print(f"   + ffmpeg instalado en el sistema")
    
    print(f"\n💰 Costo estimado:")
    print(f"   Audio de 1 hora: $0.36 (~$0.006 × 60 min)")
    print(f"   Audio de 4 horas: $1.44")


if __name__ == "__main__":
    main()

