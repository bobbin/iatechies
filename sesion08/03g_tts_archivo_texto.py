"""
TTS Local - Convertir Archivo de Texto a Audio
===============================================
Leer un archivo de texto completo y convertirlo a audio.
"""

import pyttsx3
import os


def main():
    print("📄 Convertir Archivo de Texto a Audio")
    print("=" * 50)
    
    # Crear archivo de texto de ejemplo
    texto_largo = """
La inteligencia artificial está transformando el mundo.
El procesamiento de lenguaje natural permite que las máquinas comprendan y generen texto humano.
La síntesis de voz es una de las aplicaciones más impresionantes de esta tecnología.
Ahora podemos convertir cualquier texto en audio con voces naturales y expresivas.
    """.strip()
    
    input_file = "texto_ejemplo.txt"
    output_file = "output_texto_completo.wav"
    
    # Crear archivo de ejemplo
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(texto_largo)
    
    print(f"\n📄 Archivo creado: {input_file}")
    print(f"\n📝 Contenido:")
    print("-" * 40)
    print(texto_largo)
    print("-" * 40)
    
    # Leer archivo
    with open(input_file, "r", encoding="utf-8") as f:
        texto = f.read()
    
    print(f"\n📊 Estadísticas:")
    print(f"   Caracteres: {len(texto)}")
    print(f"   Palabras: {len(texto.split())}")
    print(f"   Líneas: {len(texto.splitlines())}")
    
    # Convertir a audio
    print(f"\n⏳ Generando audio...")
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.save_to_file(texto, output_file)
    engine.runAndWait()
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / 1024
        print(f"\n✅ Audio generado:")
        print(f"   📁 {output_file} ({size:.1f} KB)")
    else:
        print(f"\n⚠️  No se pudo guardar el archivo")
    
    print(f"\n💡 Casos de uso:")
    print(f"   - Convertir documentos a audiolibros")
    print(f"   - Leer emails o noticias")
    print(f"   - Accesibilidad para personas con discapacidad visual")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: pyttsx3 no está instalado")
        print("   pip install pyttsx3")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

