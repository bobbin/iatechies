"""
TTS OpenAI - Voiceover para YouTube
===================================
Caso práctico: Generar narración para un video tutorial.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🎬 Voiceover para YouTube")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Script del tutorial
    script = """
    ¡Hola a todos! Bienvenidos a este tutorial sobre inteligencia artificial.
    
    Hoy vamos a aprender cómo generar audio a partir de texto usando la API de OpenAI.
    
    Primero, necesitas crear una cuenta en OpenAI y obtener tu clave API.
    
    Luego, instala la librería de Python con pip install openai.
    
    El código es muy simple: solo necesitas llamar a la función speech create
    pasando el modelo, la voz y el texto que quieres convertir.
    
    ¡Y eso es todo! Espero que te haya gustado este tutorial.
    No olvides darle like y suscribirte para más contenido.
    ¡Hasta la próxima!
    """
    
    print(f"\n📝 Script del video:")
    print("-" * 40)
    print(script)
    print("-" * 40)
    print(f"\n📊 Estadísticas:")
    print(f"   Palabras: {len(script.split())}")
    print(f"   Caracteres: {len(script)}")
    
    print(f"\n🎬 Generando voiceover...")
    
    # Configuración para YouTube
    response = client.audio.speech.create(
        model="tts-1-hd",    # Alta calidad para video
        voice="nova",        # Voz energética
        input=script,
        speed=1.1           # Ligeramente más rápido
    )
    
    output_file = "tutorial_youtube_voiceover.mp3"
    response.stream_to_file(output_file)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        costo = (len(script) / 1000) * 0.030
        
        print(f"\n✅ Voiceover generado:")
        print(f"   📁 {output_file}")
        print(f"   📊 Tamaño: {size:.1f} KB")
        print(f"   💰 Costo: ${costo:.4f}")
    
    print(f"\n🎯 Siguientes pasos:")
    print(f"   1. Importar {output_file} a tu editor")
    print(f"   2. Sincronizar con las imágenes/pantallas")
    print(f"   3. Añadir música de fondo")
    print(f"   4. Exportar y publicar")
    
    print(f"\n💡 Tips para YouTube:")
    print(f"   • Voz 'nova' para tutoriales")
    print(f"   • Velocidad 1.1-1.2x mantiene atención")
    print(f"   • Usar TTS-1-HD para calidad profesional")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

