"""
TTS OpenAI - Síntesis Básica
============================
Ejemplo básico de síntesis de voz con OpenAI TTS.

Instalación:
pip install openai python-dotenv

Configuración:
Crear archivo .env con: OPENAI_API_KEY=sk-tu-key

Costo: $0.015 / 1000 caracteres (TTS-1)
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🔊 Síntesis Básica con OpenAI TTS")
    print("=" * 50)
    
    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ OPENAI_API_KEY no encontrada")
        print("   1. Obtén una en: https://platform.openai.com/api-keys")
        print("   2. Crea archivo .env con: OPENAI_API_KEY=sk-tu-key")
        return
    
    client = OpenAI(api_key=api_key)
    
    texto = "Hola, soy una voz generada por la API de OpenAI. Mi calidad es profesional y prácticamente indistinguible de una voz humana real."
    
    print(f"\n📝 Texto: {texto}")
    print(f"\n🎙️  Modelo: tts-1")
    print(f"🔊 Voz: alloy")
    print(f"⏳ Generando audio...")
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=texto
    )
    
    output_file = "output_openai_basic.mp3"
    response.stream_to_file(output_file)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        num_chars = len(texto)
        costo = (num_chars / 1000) * 0.015
        
        print(f"\n✅ Audio generado:")
        print(f"   📁 {output_file} ({size:.1f} KB)")
        print(f"\n💰 Costo:")
        print(f"   Caracteres: {num_chars}")
        print(f"   Costo: ${costo:.4f} USD")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

