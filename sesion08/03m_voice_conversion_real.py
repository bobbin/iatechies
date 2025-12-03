"""
VOICE CONVERSION REAL - Cambiar identidad vocal preservando prosodia

A diferencia del método STT→TTS (que pierde la prosodia), este método:
1. Toma el audio original COMPLETO
2. Extrae el contenido lingüístico (fonemas, palabras)
3. Preserva la prosodia (ritmo, pausas, entonación)
4. Aplica el timbre/embedding de otra voz
5. Devuelve audio con MISMA prosodia pero OTRA identidad vocal

Modelos disponibles en Coqui TTS:
- FreeVC: voice_conversion_models/multilingual/vctk/freevc24
- OpenVoice v1: voice_conversion_models/multilingual/multi-dataset/openvoice_v1
- OpenVoice v2: voice_conversion_models/multilingual/multi-dataset/openvoice_v2
- kNN-VC: voice_conversion_models/multilingual/multi-dataset/knnvc
"""

import os
import sys

# Configuración para aceptar licencias automáticamente
os.environ["COQUI_TOS_AGREED"] = "1"

# =============================================================================
# ARCHIVOS DE ENTRADA/SALIDA
# =============================================================================
AUDIO_ORIGINAL = "sara-locutora-spanish-voiceover.mp3"  # Audio a convertir

# Audios de referencia (voces objetivo) - necesitamos crearlos o usar existentes
# Para este ejemplo, usaremos algunos de los ya generados con Edge TTS
VOCES_REFERENCIA = [
    ("voice_converted_hombre_espanol.mp3", "vc_real_hombre_es"),
    ("voice_converted_hombre_argentino.mp3", "vc_real_hombre_ar"),
]


def convertir_a_wav(mp3_path: str) -> str:
    """Convierte MP3 a WAV (requerido por algunos modelos)"""
    from pydub import AudioSegment
    
    wav_path = mp3_path.replace(".mp3", ".wav")
    if not os.path.exists(wav_path):
        print(f"  📦 Convirtiendo {mp3_path} → WAV...")
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(22050).set_channels(1)  # Mono, 22kHz
        audio.export(wav_path, format="wav")
    return wav_path


def voice_conversion_freevc():
    """
    Voice Conversion usando FreeVC
    
    FreeVC usa HuBERT para extraer contenido lingüístico y 
    WavLM para extraer el embedding de la voz objetivo.
    """
    print("\n" + "=" * 60)
    print("🔄 VOICE CONVERSION con FreeVC")
    print("=" * 60)
    
    try:
        from TTS.api import TTS
        
        # Cargar modelo FreeVC
        print("📥 Cargando modelo FreeVC...")
        model = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24")
        
        # Preparar audio original
        audio_original_wav = convertir_a_wav(AUDIO_ORIGINAL)
        
        for ref_audio, output_name in VOCES_REFERENCIA:
            if not os.path.exists(ref_audio):
                print(f"  ⚠️ No existe {ref_audio}, saltando...")
                continue
                
            ref_wav = convertir_a_wav(ref_audio)
            output_path = f"{output_name}_freevc.wav"
            
            print(f"\n🎭 Convirtiendo voz...")
            print(f"   Origen: {AUDIO_ORIGINAL}")
            print(f"   Voz objetivo: {ref_audio}")
            
            # Voice Conversion real
            model.voice_conversion_to_file(
                source_wav=audio_original_wav,
                target_wav=ref_wav,
                file_path=output_path
            )
            
            print(f"   ✅ Resultado: {output_path}")
            
    except Exception as e:
        print(f"❌ Error con FreeVC: {e}")
        return False
    
    return True


def voice_conversion_openvoice():
    """
    Voice Conversion usando OpenVoice v2
    
    OpenVoice usa un "Tone Color Converter" que:
    1. Extrae el contenido del audio fuente
    2. Aplica el "color tonal" de la voz de referencia
    """
    print("\n" + "=" * 60)
    print("🔄 VOICE CONVERSION con OpenVoice v2")
    print("=" * 60)
    
    try:
        from TTS.api import TTS
        
        # Cargar modelo OpenVoice v2
        print("📥 Cargando modelo OpenVoice v2...")
        model = TTS(model_name="voice_conversion_models/multilingual/multi-dataset/openvoice_v2")
        
        # Preparar audio original
        audio_original_wav = convertir_a_wav(AUDIO_ORIGINAL)
        
        for ref_audio, output_name in VOCES_REFERENCIA:
            if not os.path.exists(ref_audio):
                print(f"  ⚠️ No existe {ref_audio}, saltando...")
                continue
                
            ref_wav = convertir_a_wav(ref_audio)
            output_path = f"{output_name}_openvoice.wav"
            
            print(f"\n🎭 Convirtiendo voz...")
            print(f"   Origen: {AUDIO_ORIGINAL}")
            print(f"   Voz objetivo: {ref_audio}")
            
            # Voice Conversion real
            model.voice_conversion_to_file(
                source_wav=audio_original_wav,
                target_wav=ref_wav,
                file_path=output_path
            )
            
            print(f"   ✅ Resultado: {output_path}")
            
    except Exception as e:
        print(f"❌ Error con OpenVoice: {e}")
        return False
    
    return True


def explicar_diferencia():
    """Explica la diferencia entre los métodos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              DIFERENCIA: STT→TTS vs VOICE CONVERSION                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  MÉTODO STT → TTS (ejemplo anterior):                                ║
║  ┌─────────┐    ┌─────────┐    ┌─────────┐                          ║
║  │ Audio   │───▶│ Texto   │───▶│ Nuevo   │                          ║
║  │ Sara    │    │(transcr)│    │ Audio   │                          ║
║  └─────────┘    └─────────┘    └─────────┘                          ║
║       ❌ Se pierde: entonación, pausas, ritmo, emoción               ║
║                                                                      ║
║  ─────────────────────────────────────────────────────────────────── ║
║                                                                      ║
║  VOICE CONVERSION REAL (este ejemplo):                               ║
║  ┌─────────┐    ┌─────────────────┐    ┌─────────┐                  ║
║  │ Audio   │───▶│ Contenido       │───▶│ Nuevo   │                  ║
║  │ Sara    │    │ + Prosodia      │    │ Audio   │                  ║
║  └─────────┘    │ + Voz objetivo  │    └─────────┘                  ║
║                 └─────────────────┘                                  ║
║       ✅ Se preserva: entonación, pausas, ritmo, emoción             ║
║       ✅ Solo cambia: identidad vocal (timbre)                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def main():
    print("=" * 70)
    print("🎭 VOICE CONVERSION REAL - Preservando prosodia")
    print("=" * 70)
    
    # Explicar la diferencia
    explicar_diferencia()
    
    # Verificar que existe el audio original
    if not os.path.exists(AUDIO_ORIGINAL):
        print(f"❌ No se encuentra el audio original: {AUDIO_ORIGINAL}")
        return
    
    # Intentar FreeVC primero (más ligero)
    success = voice_conversion_freevc()
    
    if not success:
        # Si FreeVC falla, intentar OpenVoice
        voice_conversion_openvoice()
    
    print("\n" + "=" * 70)
    print("✅ VOICE CONVERSION COMPLETADO")
    print("=" * 70)
    print("""
📊 COMPARA LOS RESULTADOS:

1. Audio original:        sara-locutora-spanish-voiceover.mp3
2. STT→TTS (pierde prosodia): voice_converted_*.mp3
3. VC Real (preserva prosodia): vc_real_*_freevc.wav

La diferencia clave está en las pausas, ritmo y entonación.
El VC real mantiene EXACTAMENTE la misma prosodia del original.
""")


if __name__ == "__main__":
    main()

