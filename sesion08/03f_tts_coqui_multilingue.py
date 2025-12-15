"""
TTS Local - Coqui TTS Multilingüe (XTTS v2)
===========================================
Modelo multilingüe de alta calidad que soporta 16+ idiomas.

Nota: XTTS v2 es un modelo grande (~2GB), tarda en descargar.
Requiere un archivo de audio de referencia (speaker_wav) para clonar la voz.
"""

import os
import tempfile


def generar_audio_referencia():
    """Genera un audio de referencia usando pyttsx3 para XTTS v2"""
    try:
        import pyttsx3
        
        print("   📝 Generando audio de referencia...")
        engine = pyttsx3.init()
        
        # Texto corto para referencia
        texto_ref = "Hola, esta es una voz de referencia para el modelo multilingüe."
        
        # Crear archivo temporal
        ref_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        ref_file.close()
        
        engine.save_to_file(texto_ref, ref_file.name)
        engine.runAndWait()
        
        if os.path.exists(ref_file.name):
            return ref_file.name
    except Exception as e:
        print(f"   ⚠️  No se pudo generar referencia con pyttsx3: {e}")
    
    return None


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
    
    # Aceptar términos automáticamente
    os.environ["COQUI_TOS_AGREED"] = "1"
    
    # Modelo multilingüe
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    
    # Generar audio de referencia
    speaker_wav = generar_audio_referencia()
    
    if not speaker_wav or not os.path.exists(speaker_wav):
        print("\n❌ Error: No se pudo generar archivo de referencia")
        print("   XTTS v2 requiere un archivo de audio de referencia (speaker_wav)")
        print("   Alternativa: Usa un archivo .wav existente como referencia")
        return
    
    print(f"   ✅ Audio de referencia: {os.path.basename(speaker_wav)}")
    
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
                language=idioma,
                speaker_wav=speaker_wav  # Archivo de referencia requerido
            )
            
            if os.path.exists(output_file):
                size = os.path.getsize(output_file) / 1024
                print(f"   ✅ {output_file} ({size:.1f} KB)")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Limpiar archivo temporal
    try:
        if os.path.exists(speaker_wav):
            os.unlink(speaker_wav)
    except:
        pass
    
    print(f"\n📋 Idiomas soportados por XTTS v2:")
    print("   es, en, fr, de, pt, it, pl, tr, ru, nl, cs, ar, zh, ja, hu, ko")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")

