"""
TTS Local - Coqui TTS Básico
============================
Síntesis de voz de alta calidad con modelos de IA.

Instalación:
pip install TTS

Nota: La primera ejecución descarga el modelo (~500MB)
"""

import os


def main():
    print("🎙️ Coqui TTS - Alta Calidad")
    print("=" * 50)
    
    try:
        from TTS.api import TTS
    except ImportError:
        print("\n❌ Error: TTS (Coqui) no está instalado")
        print("   pip install TTS")
        return
    
    print("\n⏳ Inicializando Coqui TTS...")
    print("   (La primera vez descargará el modelo)")
    
    # Usar modelo español
    tts = TTS(model_name="tts_models/es/css10/vits")
    
    texto = "Hola, soy una voz generada con Coqui TTS. La calidad es mucho mejor que las voces tradicionales del sistema."
    output_file = "output_coqui_es.wav"
    
    print(f"\n📝 Texto: {texto}")
    print(f"🎙️  Modelo: tts_models/es/css10/vits")
    print(f"💾 Generando audio...")
    
    # Generar audio
    tts.tts_to_file(text=texto, file_path=output_file)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        print(f"\n✅ Audio generado:")
        print(f"   📁 Archivo: {output_file}")
        print(f"   📊 Tamaño: {size:.1f} KB")
    
    print(f"\n💡 Modelos recomendados:")
    print(f"   - tts_models/es/css10/vits (español)")
    print(f"   - tts_models/en/ljspeech/tacotron2-DDC (inglés)")
    print(f"   - tts_models/multilingual/multi-dataset/xtts_v2 (multilingüe)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Si falla, prueba:")
        print("   pip install TTS --upgrade")

