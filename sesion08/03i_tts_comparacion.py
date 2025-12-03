"""
TTS Local - Comparación de Calidad
==================================
Comparar pyttsx3 (voces sistema) vs Coqui TTS (IA).
"""

import os


def main():
    print("📊 Comparación de Calidad: pyttsx3 vs Coqui TTS")
    print("=" * 50)
    
    texto = "La inteligencia artificial permite crear voces sintéticas muy realistas."
    
    print(f"\n📝 Texto de prueba:")
    print(f"   {texto}\n")
    
    # Test pyttsx3
    print("=" * 50)
    print("1️⃣  pyttsx3 (Voces del Sistema)")
    print("=" * 50)
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        output1 = "comparacion_pyttsx3.wav"
        engine.save_to_file(texto, output1)
        engine.runAndWait()
        
        if os.path.exists(output1):
            size = os.path.getsize(output1) / 1024
            print(f"   ✅ Generado: {output1} ({size:.1f} KB)")
            print(f"\n   Características:")
            print(f"   • Velocidad: ⭐⭐⭐⭐⭐ (instantáneo)")
            print(f"   • Calidad: ⭐⭐⭐ (robótica)")
            print(f"   • Dependencias: Ninguna (usa sistema)")
            print(f"   • RAM: ~50 MB")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test Coqui TTS
    print("\n" + "=" * 50)
    print("2️⃣  Coqui TTS (Modelo IA)")
    print("=" * 50)
    
    try:
        from TTS.api import TTS
        
        print("   ⏳ Cargando modelo...")
        tts = TTS(model_name="tts_models/es/css10/vits")
        
        output2 = "comparacion_coqui.wav"
        tts.tts_to_file(text=texto, file_path=output2)
        
        if os.path.exists(output2):
            size = os.path.getsize(output2) / 1024
            print(f"   ✅ Generado: {output2} ({size:.1f} KB)")
            print(f"\n   Características:")
            print(f"   • Velocidad: ⭐⭐⭐ (segundos)")
            print(f"   • Calidad: ⭐⭐⭐⭐⭐ (natural)")
            print(f"   • Dependencias: PyTorch, modelo ~500MB")
            print(f"   • RAM: ~1-2 GB")
    except ImportError:
        print("   ⚠️  Coqui TTS no instalado")
        print("   pip install TTS")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN")
    print("=" * 50)
    print("""
| Característica | pyttsx3    | Coqui TTS  |
|----------------|------------|------------|
| Velocidad      | ⭐⭐⭐⭐⭐    | ⭐⭐⭐       |
| Calidad        | ⭐⭐⭐       | ⭐⭐⭐⭐⭐    |
| Setup          | Muy fácil  | Medio      |
| Tamaño         | ~0 MB      | ~500MB+    |
| GPU            | No         | Opcional   |
| Voces          | Sistema    | Muchas IA  |
""")
    
    print("💡 Recomendaciones:")
    print("   • pyttsx3: Prototipado, demos, bajo recursos")
    print("   • Coqui TTS: Producción, audiolibros, calidad")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

