"""
TTS Local - Configuración de Voz
================================
Ajustar velocidad, volumen y cambiar de voz.
"""

import pyttsx3


def main():
    print("⚙️  Configuración de Voz")
    print("=" * 50)
    
    engine = pyttsx3.init()
    
    # Configuración actual
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    voices = engine.getProperty('voices')
    
    print(f"\n📋 Configuración actual:")
    print(f"   Velocidad: {rate} palabras/min")
    print(f"   Volumen: {volume}")
    print(f"   Voces disponibles: {len(voices)}")
    
    # Probar diferentes velocidades
    print(f"\n🔧 Probando velocidades:\n")
    
    # Velocidad normal
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    print("1️⃣  Velocidad normal (150 wpm)")
    engine.say("Esta es la velocidad normal de habla")
    engine.runAndWait()
    
    # Velocidad rápida
    engine.setProperty('rate', 250)
    print("\n2️⃣  Velocidad rápida (250 wpm)")
    engine.say("Esta es una velocidad rápida de habla")
    engine.runAndWait()
    
    # Velocidad lenta
    engine.setProperty('rate', 100)
    print("\n3️⃣  Velocidad lenta (100 wpm)")
    engine.say("Esta es una velocidad lenta de habla")
    engine.runAndWait()
    
    # Cambiar volumen
    print("\n4️⃣  Volumen bajo (50%)")
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.5)
    engine.say("Este es el volumen al cincuenta por ciento")
    engine.runAndWait()
    
    # Restaurar volumen
    engine.setProperty('volume', 1.0)
    
    # Cambiar voz si hay más de una
    if len(voices) > 1:
        print("\n5️⃣  Cambiando de voz")
        engine.setProperty('voice', voices[1].id)
        engine.say("Esta es una voz diferente")
        engine.runAndWait()
    
    print("\n✅ Configuraciones probadas correctamente")
    
    print("\n💡 Rangos recomendados:")
    print("   - Velocidad: 100-200 wpm (normal ~150)")
    print("   - Volumen: 0.0 a 1.0")


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("❌ Error: pyttsx3 no está instalado")
        print("   pip install pyttsx3")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

