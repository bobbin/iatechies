"""
TTS Local - Coqui TTS Multilingüe (XTTS v2)
===========================================
Modelo multilingüe de alta calidad que soporta 16+ idiomas.

Nota: XTTS v2 es un modelo grande (~2GB), tarda en descargar.
"""

import os


def main():
    print("🌍 Coqui TTS - Multilingüe (XTTS v2)")
    print("=" * 50)
    
    try:
        from TTS.api import TTS
    except ImportError:
        print("\n❌ Error: TTS (Coqui) no está instalado")
        print("   pip install TTS")
        return
    
    print("\n⏳ Inicializando XTTS v2...")
    print("   ⚠️  Modelo grande (~2GB), primera vez tarda más")
    
    # Modelo multilingüe
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    
    textos = {
        "es": "Este es un ejemplo en español con calidad profesional.",
        "en": "This is an example in English with professional quality.",
        "fr": "Ceci est un exemple en français avec une qualité professionnelle.",
        "de": "Dies ist ein Beispiel auf Deutsch mit professioneller Qualität.",
        "pt": "Este é um exemplo em português com qualidade profissional."
    }
    
    print(f"\n🌍 Generando audio en múltiples idiomas:\n")
    
    for idioma, texto in textos.items():
        output_file = f"output_xtts_{idioma}.wav"
        
        print(f"🔊 {idioma.upper()}: {texto[:40]}...")
        
        try:
            tts.tts_to_file(
                text=texto,
                file_path=output_file,
                language=idioma
            )
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"   ✅ {output_file} ({size:.1f} KB)")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n📋 Idiomas soportados por XTTS v2:")
    print("   es, en, fr, de, pt, it, pl, tr, ru, nl, cs, ar, zh, ja, hu, ko")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

