"""
STT OpenAI - Traducción Automática a Inglés
===========================================
Transcribir audio en cualquier idioma y traducirlo automáticamente al inglés.

Este ejemplo demuestra:
- Usar endpoint translations en lugar de transcriptions
- Traducir audio español a texto en inglés
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🌍 Traducción Automática a Inglés")
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
    
    # Primero transcribir en español
    print(f"\n📝 Paso 1: Transcripción original...")
    with open(audio_file, "rb") as audio:
        transcripcion = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            language="es"
        )
    
    print(f"   Español: {transcripcion.text}")
    
    # Ahora traducir a inglés
    print(f"\n🌍 Paso 2: Traducción a inglés...")
    with open(audio_file, "rb") as audio:
        # Usar endpoint de translations
        traduccion = client.audio.translations.create(
            model="whisper-1",
            file=audio
            # No se especifica idioma - siempre traduce a inglés
        )
    
    print(f"   Inglés: {traduccion.text}")
    
    print("\n💡 Nota:")
    print("   translations siempre traduce a inglés")
    print("   Soporta 99+ idiomas de entrada")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

