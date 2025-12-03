"""
TTS OpenAI - Comparar las 6 Voces
=================================
OpenAI TTS ofrece 6 voces con diferentes estilos.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🎤 Comparar las 6 Voces de OpenAI TTS")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    voces = {
        "alloy": "Neutral, profesional",
        "echo": "Masculina, cálida",
        "fable": "Neutral, expresiva",
        "onyx": "Masculina, profunda",
        "nova": "Femenina, energética",
        "shimmer": "Femenina, suave"
    }
    
    texto = "Esta es una demostración de las diferentes voces disponibles en OpenAI TTS."
    
    print(f"\n📝 Texto: {texto}")
    print(f"\n🎤 Generando audio con las 6 voces:\n")
    
    for voz, descripcion in voces.items():
        print(f"🔊 {voz}: {descripcion}")
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voz,
                input=texto
            )
            
            output_file = f"output_voz_{voz}.mp3"
            response.stream_to_file(output_file)
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"   ✅ {output_file} ({size:.1f} KB)\n")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")
    
    print("💡 Recomendaciones de uso:")
    print("   • alloy: Tutoriales, documentación")
    print("   • echo: Audiolibros, narraciones")
    print("   • nova: Marketing, presentaciones")
    print("   • shimmer: Meditación, e-learning")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

