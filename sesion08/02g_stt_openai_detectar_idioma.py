"""
STT OpenAI - Detección Automática de Idioma
===========================================
Transcribir sin especificar idioma para que Whisper lo detecte.

Este ejemplo demuestra:
- Omitir parámetro language
- Obtener idioma detectado con verbose_json
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🌍 Detección Automática de Idioma (OpenAI)")
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
    
    print(f"\n🎤 Transcribiendo (sin especificar idioma)...")
    
    with open(audio_file, "rb") as audio:
        # NO especificar language para detección automática
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="verbose_json"
            # language omitido intencionalmente
        )
    
    print(f"\n📊 Resultados:")
    print(f"   Idioma detectado: {transcript.language}")
    print(f"   Duración: {transcript.duration:.2f}s")
    
    print(f"\n📝 Transcripción:")
    print(f"   {transcript.text}")
    
    print(f"\n💡 Tips:")
    print(f"   - Especificar idioma mejora precisión")
    print(f"   - Detección automática útil para idioma desconocido")
    print(f"   - Whisper soporta 99+ idiomas")
    
    print(f"\n🌐 Idiomas más comunes:")
    idiomas = ["es (español)", "en (inglés)", "fr (francés)", 
               "de (alemán)", "pt (portugués)", "it (italiano)",
               "zh (chino)", "ja (japonés)", "ko (coreano)"]
    for idioma in idiomas:
        print(f"   - {idioma}")


if __name__ == "__main__":
    main()

