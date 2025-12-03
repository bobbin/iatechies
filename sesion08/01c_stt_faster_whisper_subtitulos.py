"""
STT Local - Generar Subtítulos SRT
==================================
Generar archivo de subtítulos en formato SRT.

Este ejemplo demuestra:
- Transcribir audio y generar subtítulos
- Formatear timestamps en formato SRT
- Guardar archivo .srt compatible con reproductores
"""

from faster_whisper import WhisperModel
from datetime import timedelta
import os


def format_timestamp_srt(seconds):
    """Convertir segundos a formato SRT (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60
    millis = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main():
    print("🎬 Generar Subtítulos SRT")
    print("=" * 50)
    
    audio_file = "ejemplo_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        print("   Ejecuta primero: python 01a_stt_faster_whisper_basico.py")
        return
    
    # Cargar modelo
    print("\n⏳ Cargando modelo...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # Transcribir
    print(f"🎤 Transcribiendo...")
    segments, info = model.transcribe(audio_file, language="es")
    
    # Generar archivo SRT
    srt_file = "subtitulos.srt"
    
    print(f"📝 Generando subtítulos...")
    
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            # Formato SRT:
            # 1
            # 00:00:00,000 --> 00:00:02,000
            # Texto del subtítulo
            
            start = format_timestamp_srt(segment.start)
            end = format_timestamp_srt(segment.end)
            
            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{segment.text.strip()}\n\n")
    
    print(f"\n✅ Subtítulos guardados: {srt_file}")
    
    # Mostrar contenido
    print(f"\n📄 Vista previa:")
    print("-" * 40)
    with open(srt_file, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()

