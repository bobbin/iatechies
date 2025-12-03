"""
TTS Local - Modelos Disponibles en Coqui TTS
============================================
Listar todos los modelos de voz disponibles.
"""


def main():
    print("📚 Modelos Disponibles en Coqui TTS")
    print("=" * 50)
    
    try:
        from TTS.api import TTS
    except ImportError:
        print("\n❌ Error: TTS (Coqui) no está instalado")
        print("   pip install TTS")
        return
    
    # Listar todos los modelos
    models = TTS.list_models()
    
    print(f"\n📊 Total de modelos: {len(models)}")
    
    # Modelos en español
    print(f"\n🇪🇸 Modelos en Español:")
    print("-" * 40)
    spanish = [m for m in models if '/es/' in m]
    for model in spanish:
        print(f"   • {model}")
    
    # Modelos multilingües
    print(f"\n🌍 Modelos Multilingües:")
    print("-" * 40)
    multilingual = [m for m in models if 'multilingual' in m]
    for model in multilingual:
        print(f"   • {model}")
    
    # Modelos en inglés (primeros 5)
    print(f"\n🇬🇧 Modelos en Inglés (top 5):")
    print("-" * 40)
    english = [m for m in models if '/en/' in m][:5]
    for model in english:
        print(f"   • {model}")
    
    # Recomendaciones
    print(f"\n💡 Modelos recomendados:")
    print("-" * 40)
    print(f"   📌 Español rápido:")
    print(f"      tts_models/es/css10/vits")
    print(f"\n   📌 Inglés alta calidad:")
    print(f"      tts_models/en/ljspeech/tacotron2-DDC")
    print(f"\n   📌 Multilingüe (mejor calidad):")
    print(f"      tts_models/multilingual/multi-dataset/xtts_v2")
    print(f"\n   📌 Con clonación de voz:")
    print(f"      tts_models/multilingual/multi-dataset/your_tts")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

