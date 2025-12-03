"""
TTS OpenAI - Streaming de Audio
===============================
Recibir audio en chunks para reproducción en tiempo real.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🌊 Streaming de Audio")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    texto = "Este es un ejemplo de streaming de audio en tiempo real para aplicaciones interactivas."
    
    print(f"\n📝 Texto: {texto}")
    print(f"\n🌊 Generando audio con streaming...")
    
    # TTS-1 tiene menor latencia, ideal para streaming
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=texto
    )
    
    output_file = "output_streaming.mp3"
    
    # Stream chunks a archivo
    print("\n⏳ Recibiendo chunks: ", end="", flush=True)
    
    chunks_count = 0
    with open(output_file, "wb") as f:
        for chunk in response.iter_bytes(chunk_size=1024):
            f.write(chunk)
            print("█", end="", flush=True)
            chunks_count += 1
    
    print(f"\n\n✅ Streaming completado:")
    print(f"   📁 {output_file}")
    print(f"   📦 Chunks recibidos: {chunks_count}")
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        print(f"   📊 Tamaño: {size:.1f} KB")
    
    print(f"\n💡 Uso de streaming:")
    print(f"   • Chatbots: Reproducir mientras genera")
    print(f"   • Asistentes: Menor latencia percibida")
    print(f"   • Apps móviles: Ahorro de memoria")
    print(f"\n📝 Código para producción:")
    print(f"   En lugar de escribir a archivo,")
    print(f"   enviar chunks directamente al cliente/altavoz")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

