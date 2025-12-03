"""
TTS OpenAI - Generar Audiolibro
===============================
Convertir texto largo a audio de alta calidad.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("📚 Generar Audiolibro")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAI(api_key=api_key)
    
    # Texto de ejemplo (capítulo de libro)
    texto_largo = """
    Capítulo 1: El Inicio de la Aventura.
    
    Había una vez, en un reino muy lejano, un joven programador llamado Alex
    que soñaba con dominar las artes de la inteligencia artificial.
    
    Cada día, Alex estudiaba con dedicación, aprendiendo sobre modelos de lenguaje,
    redes neuronales y algoritmos de aprendizaje profundo.
    
    Un día, descubrió una tecnología maravillosa: la síntesis de voz con IA.
    Esta tecnología permitía convertir cualquier texto en audio con voces naturales.
    
    Alex se dio cuenta del potencial: podría crear audiolibros, asistentes virtuales,
    y dar voz a sus aplicaciones. El futuro estaba lleno de posibilidades.
    """
    
    print(f"\n📚 Generando audiolibro...")
    print(f"📝 Caracteres: {len(texto_largo)}")
    print(f"📝 Palabras: ~{len(texto_largo.split())}")
    
    # Usar modelo HD y voz cálida para narración
    response = client.audio.speech.create(
        model="tts-1-hd",          # Máxima calidad
        voice="echo",              # Voz cálida para narración
        input=texto_largo
    )
    
    output_file = "audiolibro_capitulo1.mp3"
    response.stream_to_file(output_file)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        costo = (len(texto_largo) / 1000) * 0.030
        
        print(f"\n✅ Audiolibro generado:")
        print(f"   📁 {output_file}")
        print(f"   📊 Tamaño: {size:.1f} KB")
        print(f"   💰 Costo: ${costo:.4f}")
    
    print(f"\n💡 Tips para audiolibros:")
    print(f"   • Usar tts-1-hd para máxima calidad")
    print(f"   • Voz 'echo' ideal para narración")
    print(f"   • Dividir en capítulos/secciones")
    print(f"   • Límite: 4096 caracteres por request")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

