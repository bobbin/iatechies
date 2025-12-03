"""
TTS Local - Guardar Audio en Archivo
====================================
Guardar la síntesis de voz en un archivo de audio.
"""

import pyttsx3
import os


def main():
    print("💾 Guardar Audio en Archivo")
    print("=" * 50)
    
    engine = pyttsx3.init()
    
    texto = "Este audio ha sido generado y guardado en un archivo usando pyttsx3."
    output_file = "output_pyttsx3.wav"
    
    print(f"\n📝 Texto: {texto}")
    print(f"💾 Archivo destino: {output_file}")
    
    # Configurar para mejor calidad
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    print(f"\n⏳ Generando audio...")
    
    # Guardar a archivo
    engine.save_to_file(texto, output_file)
    engine.runAndWait()
    
    # Verificar resultado
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        print(f"\n✅ Audio guardado correctamente")
        print(f"   📁 Archivo: {output_file}")
        print(f"   📊 Tamaño: {size:.1f} KB")
    else:
        print(f"\n⚠️  No se pudo guardar el archivo")
        print(f"   Algunos sistemas no soportan save_to_file")
    
    print(f"\n💡 Formatos:")
    print(f"   - .wav es el formato más compatible")
    print(f"   - Algunos drivers también soportan .mp3")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: pyttsx3 no está instalado")
        print("   pip install pyttsx3")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

