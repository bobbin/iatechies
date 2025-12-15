"""
TTS OpenAI - Comparar TTS-1 vs TTS-1-HD
=======================================
TTS-1: Baja latencia, más económico
TTS-1-HD: Máxima calidad, más caro
"""

from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🎯 Comparar TTS-1 vs TTS-1-HD")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    texto = "La calidad del audio puede variar significativamente entre el modelo estándar y el de alta definición."
    
    modelos = {
        "tts-1": {
            "descripcion": "Estándar (baja latencia)",
            "costo_1k": 0.015
        },
        "tts-1-hd": {
            "descripcion": "Alta Definición (máxima calidad)",
            "costo_1k": 0.030
        },
        "gpt-4o-mini-tts": {
            "descripcion": "GPT-4o Mini (alta calidad)",
            "costo_1k": 0.030
        }
    }
    
    print(f"\n📝 Texto: {texto}\n")
    
    for modelo, info in modelos.items():
        print(f"🎯 {modelo}: {info['descripcion']}")
        
        inicio = time.time()
        
        response = client.audio.speech.create(
            model=modelo,
            voice="nova",
            input=texto
        )
        
        tiempo = time.time() - inicio
        
        output_file = f"output_{modelo.replace('-', '_')}.mp3"
        response.stream_to_file(output_file)
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file) / 1024
            costo = (len(texto) / 1000) * info['costo_1k']
            
            print(f"   ⏱️  Tiempo: {tiempo:.2f}s")
            print(f"   📁 Archivo: {output_file} ({size:.1f} KB)")
            print(f"   💰 Costo: ${costo:.4f}\n")
    
    print("💡 Comparación:")
    print("   • TTS-1: Más rápido, $15/1M chars, ideal para tiempo real")
    print("   • TTS-1-HD: Mejor calidad, $30/1M chars, ideal para producción")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

