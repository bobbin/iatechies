"""
TTS OpenAI - Diferentes Formatos de Audio
=========================================
Generar audio en MP3, Opus, AAC o FLAC.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🎵 Diferentes Formatos de Audio")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    texto = "Este audio está disponible en múltiples formatos."
    
    formatos = {
        "mp3": "Universal, buen balance tamaño/calidad",
        "opus": "Mejor compresión, ideal para web/streaming",
        "aac": "Excelente para iOS/Apple",
        "flac": "Sin pérdida, producción profesional"
    }
    
    print(f"\n📝 Texto: {texto}")
    print(f"\n🎵 Generando en diferentes formatos:\n")
    
    for formato, descripcion in formatos.items():
        print(f"📦 {formato.upper()}: {descripcion}")
        
        try:
            response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",
                input=texto,
                response_format=formato
            )
            
            output_file = f"output_formato.{formato}"
            response.stream_to_file(output_file)
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"   ✅ {output_file} ({size:.1f} KB)\n")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")
    
    print("💡 Cuándo usar cada formato:")
    print("   • mp3: Web general, podcasts")
    print("   • opus: Apps, streaming, menor tamaño")
    print("   • aac: Apps iOS, iTunes")
    print("   • flac: Edición de audio, archivos master")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

