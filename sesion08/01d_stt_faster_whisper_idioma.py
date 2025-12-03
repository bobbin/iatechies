"""
STT Local - Detección Automática de Idioma
==========================================
Detectar automáticamente el idioma del audio sin especificarlo.

Este ejemplo demuestra:
- Transcribir sin especificar idioma
- Obtener idioma detectado y probabilidad
- Comparar con idioma especificado
"""

from faster_whisper import WhisperModel
import os


def main():
    print("🌍 Detección Automática de Idioma")
    print("=" * 50)
    
    audio_file = "ejemplo_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        print("   Ejecuta primero: python 01a_stt_faster_whisper_basico.py")
        return
    
    # Cargar modelo
    print("\n⏳ Cargando modelo...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # Transcribir SIN especificar idioma
    print(f"🎤 Transcribiendo (detección automática)...")
    segments, info = model.transcribe(audio_file)  # Sin language="es"
    
    # Mostrar resultados
    print(f"\n📊 Resultados de detección:")
    print(f"   Idioma detectado: {info.language}")
    print(f"   Confianza: {info.language_probability:.1%}")
    print(f"   Duración: {info.duration:.2f}s")
    
    # Mostrar transcripción
    print(f"\n📝 Transcripción:")
    texto = " ".join([segment.text for segment in segments])
    print(f"   {texto}")
    
    # Comparación: Con vs Sin especificar idioma
    print(f"\n💡 Tip:")
    print(f"   Especificar idioma mejora precisión y velocidad")
    print(f"   Usar detección automática cuando idioma es desconocido")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

