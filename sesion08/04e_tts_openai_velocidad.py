"""
TTS OpenAI - Control de Velocidad
=================================
Ajustar la velocidad de habla entre 0.25x y 4.0x.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("⚡ Control de Velocidad")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    texto = "La velocidad de habla se puede ajustar para diferentes necesidades."
    
    velocidades = {
        0.5: "Muy lenta (0.5x) - Aprendizaje idiomas",
        0.75: "Lenta (0.75x) - Accesibilidad",
        1.0: "Normal (1.0x) - Estándar",
        1.25: "Rápida (1.25x) - Podcasts",
        1.5: "Muy rápida (1.5x) - Resúmenes",
        2.0: "Ultra rápida (2.0x) - Revisión"
    }
    
    print(f"\n📝 Texto: {texto}\n")
    
    for velocidad, descripcion in velocidades.items():
        print(f"⚡ {descripcion}")
        
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=texto,
                speed=velocidad
            )
            
            output_file = f"output_velocidad_{str(velocidad).replace('.', '_')}x.mp3"
            response.stream_to_file(output_file)
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"   ✅ {output_file} ({size:.1f} KB)\n")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}\n")
    
    print("💡 Rango de velocidad: 0.25x a 4.0x")
    print("   • <1.0: Más lento que normal")
    print("   • 1.0: Velocidad normal")
    print("   • >1.0: Más rápido que normal")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

