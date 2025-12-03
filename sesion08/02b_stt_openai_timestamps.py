"""
STT OpenAI - Transcripción con Timestamps
=========================================
Obtener transcripción con información detallada y timestamps.

Este ejemplo demuestra:
- Usar response_format="verbose_json"
- Obtener idioma, duración y segmentos
- Acceder a timestamps de cada segmento
"""

from openai import OpenAI
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("⏱️  Transcripción con Timestamps (OpenAI)")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    audio_file = "ejemplo_audio.wav"
    if not os.path.exists(audio_file):
        print(f"❌ Archivo no encontrado: {audio_file}")
        print("   Ejecuta primero: python 02a_stt_openai_basico.py")
        return
    
    client = OpenAI(api_key=api_key)
    
    print(f"\n🎤 Transcribiendo con formato detallado...")
    
    with open(audio_file, "rb") as audio:
        # verbose_json devuelve info completa
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="verbose_json",
            language="es"
        )
    
    # Información general
    print(f"\n📊 Información:")
    print(f"   Idioma: {transcript.language}")
    print(f"   Duración: {transcript.duration:.2f}s")
    
    print(f"\n📝 Texto completo:")
    print(f"   {transcript.text}")
    
    # Segmentos con timestamps
    if hasattr(transcript, 'segments') and transcript.segments:
        print(f"\n⏱️  Segmentos ({len(transcript.segments)}):")
        print("-" * 50)
        
        for i, seg in enumerate(transcript.segments[:5], 1):
            start = timedelta(seconds=seg['start'])
            end = timedelta(seconds=seg['end'])
            print(f"\nSegmento {i}:")
            print(f"   Tiempo: {start} --> {end}")
            print(f"   Texto: {seg['text']}")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

