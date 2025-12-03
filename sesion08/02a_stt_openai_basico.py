"""
STT OpenAI - Transcripción Básica
=================================
Ejemplo básico de transcripción con OpenAI Whisper API.

Instalación:
pip install openai python-dotenv gtts

Configuración:
Crear archivo .env con: OPENAI_API_KEY=sk-tu-api-key

Costo: $0.006 por minuto de audio
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def crear_audio_ejemplo():
    """Crear archivo de audio de ejemplo si no existe"""
    try:
        from gtts import gTTS
        texto = "Hola, este es un ejemplo de audio para probar OpenAI Whisper."
        print("🔊 Generando audio de ejemplo...")
        tts = gTTS(text=texto, lang='es')
        tts.save("ejemplo_audio.wav")
        print(f"✅ Audio creado: ejemplo_audio.wav")
    except ImportError:
        print("⚠️  Instala gTTS: pip install gtts")


def main():
    print("🎙️  Transcripción Básica con OpenAI Whisper")
    print("=" * 50)
    
    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ OPENAI_API_KEY no encontrada")
        print("   1. Obtén una en: https://platform.openai.com/api-keys")
        print("   2. Crea archivo .env con: OPENAI_API_KEY=sk-tu-key")
        return
    
    audio_file = "ejemplo_audio.wav"
    
    # Crear audio de ejemplo si no existe
    if not os.path.exists(audio_file):
        crear_audio_ejemplo()
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        return
    
    # Crear cliente
    client = OpenAI(api_key=api_key)
    
    # Transcribir
    print(f"\n🎤 Transcribiendo: {audio_file}")
    print("⏳ Enviando a OpenAI...")
    
    with open(audio_file, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            language="es"  # Opcional pero mejora precisión
        )
    
    # Mostrar resultado
    print(f"\n📝 Transcripción:")
    print(f"   {transcript.text}")
    
    # Info de costo
    size_mb = os.path.getsize(audio_file) / (1024 * 1024)
    print(f"\n💰 Info:")
    print(f"   Tamaño: {size_mb:.2f} MB")
    print(f"   Costo: ~$0.006/minuto")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

