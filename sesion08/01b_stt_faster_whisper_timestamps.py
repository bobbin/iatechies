"""
STT Local - Transcripción con Timestamps
========================================
Transcripción con marcas de tiempo a nivel de segmento y palabra.

Este ejemplo demuestra:
- Obtener timestamps por segmento
- Obtener timestamps por palabra (word_timestamps)
- Formatear tiempos para subtítulos
"""

from faster_whisper import WhisperModel
from datetime import timedelta
import os


def main():
    print("⏱️  Transcripción con Timestamps")
    print("=" * 50)
    
    audio_file = "ejemplo_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        print("   Ejecuta primero: python 01a_stt_faster_whisper_basico.py")
        return
    
    # Cargar modelo
    print("\n⏳ Cargando modelo...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # Transcribir con timestamps de palabras
    print(f"🎤 Transcribiendo con timestamps...")
    segments, info = model.transcribe(
        audio_file,
        language="es",
        word_timestamps=True  # Obtener timestamps a nivel de palabra
    )
    
    print(f"\n📊 Duración: {info.duration:.2f} segundos")
    
    # Mostrar segmentos con tiempo
    print(f"\n⏱️  Segmentos con timestamps:")
    print("-" * 50)
    
    for segment in segments:
        start = str(timedelta(seconds=segment.start))
        end = str(timedelta(seconds=segment.end))
        
        print(f"\n[{start} --> {end}]")
        print(f"Texto: {segment.text}")
        
        # Mostrar palabras individuales (si hay)
        if segment.words:
            print("Palabras:")
            for word in segment.words[:5]:  # Primeras 5 palabras
                w_start = f"{word.start:.2f}s"
                w_end = f"{word.end:.2f}s"
                print(f"   {w_start}-{w_end}: {word.word}")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

