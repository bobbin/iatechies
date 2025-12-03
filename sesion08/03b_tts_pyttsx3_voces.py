"""
TTS Local - Listar Voces Disponibles
====================================
Ver todas las voces instaladas en el sistema.

Las voces varían según el sistema operativo:
- Windows: SAPI5 voices
- macOS: NSSpeechSynthesizer
- Linux: espeak, festival
"""

import pyttsx3


def main():
    print("🎤 Voces Disponibles en el Sistema")
    print("=" * 50)
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n📋 Encontradas {len(voices)} voces:\n")
    print("-" * 50)
    
    for i, voice in enumerate(voices):
        print(f"\nVoz {i}:")
        print(f"   ID: {voice.id[:50]}..." if len(voice.id) > 50 else f"   ID: {voice.id}")
        print(f"   Nombre: {voice.name}")
        
        # Idiomas (puede estar vacío en algunos sistemas)
        if voice.languages:
            print(f"   Idiomas: {voice.languages}")
        
        # Género (puede no estar disponible)
        genero = getattr(voice, 'gender', None)
        if genero:
            print(f"   Género: {genero}")
    
    # Probar cada voz
    print("\n" + "=" * 50)
    print("🔊 Probando voces disponibles:")
    print("=" * 50)
    
    for i, voice in enumerate(voices[:3]):  # Solo las primeras 3
        print(f"\n{i+1}. Probando: {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 150)
        engine.say(f"Hola, esta es la voz número {i+1}")
        engine.runAndWait()
    
    print("\n✅ Completado")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: pyttsx3 no está instalado")
        print("   pip install pyttsx3")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

