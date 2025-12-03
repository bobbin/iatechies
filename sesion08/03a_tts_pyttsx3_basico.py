"""
TTS Local - Síntesis Básica con pyttsx3
=======================================
Ejemplo básico de síntesis de voz usando voces del sistema.

Instalación:
pip install pyttsx3

100% local, gratuito y sin límites.
"""

import pyttsx3


def main():
    print("🔊 Síntesis Básica con pyttsx3")
    print("=" * 50)
    
    # Inicializar motor TTS
    print("\n⏳ Inicializando motor...")
    engine = pyttsx3.init()
    
    texto = "Hola, soy un ejemplo de síntesis de voz usando pyttsx3. Esta es una solución completamente local y gratuita."
    
    print(f"\n📝 Texto a sintetizar:")
    print(f"   {texto}")
    
    print(f"\n🔊 Reproduciendo audio...")
    
    # Hablar
    engine.say(texto)
    engine.runAndWait()
    
    print(f"✅ Audio reproducido correctamente")
    
    print(f"\n💡 Info:")
    try:
        voices = engine.getProperty('voices')
        current_voice = engine.getProperty('voice')
        voice_name = "Sistema"
        if voices and current_voice:
            for voice in voices:
                if voice.id == current_voice:
                    voice_name = voice.name
                    break
        print(f"   - Voz: {voice_name}")
    except:
        print(f"   - Motor: pyttsx3 (Sistema)")
    
    try:
        rate = engine.getProperty('rate')
        print(f"   - Velocidad: {rate} palabras/min")
    except:
        print(f"   - Velocidad: No disponible")
    
    try:
        volume = engine.getProperty('volume')
        print(f"   - Volumen: {volume:.2f}")
    except:
        print(f"   - Volumen: No disponible")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: pyttsx3 no está instalado")
        print("   pip install pyttsx3")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

