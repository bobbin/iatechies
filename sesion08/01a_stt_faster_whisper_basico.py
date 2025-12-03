"""
STT Local - Transcripción Básica con Faster-Whisper
===================================================
Ejemplo básico de transcripción de audio a texto usando Faster-Whisper.

Instalación:
pip install faster-whisper gtts

Este ejemplo demuestra:
- Cargar un modelo de Whisper
- Transcribir un archivo de audio
- Obtener información del audio (idioma, duración)
"""

from faster_whisper import WhisperModel
import os


def crear_audio_ejemplo():
    """Crear archivo de audio de ejemplo si no existe"""
    try:
        from gtts import gTTS
        texto = "Hola, este es un ejemplo de audio para probar Faster Whisper."
        print("🔊 Generando audio de ejemplo...")
        tts = gTTS(text=texto, lang='es')
        tts.save("ejemplo_audio.wav")
        print(f"✅ Audio creado: ejemplo_audio.wav")
    except ImportError:
        print("⚠️  Instala gTTS: pip install gtts")
        print("   O usa cualquier archivo de audio .wav, .mp3, .m4a")


def main():
    print("🎙️  Transcripción Básica con Faster-Whisper")
    print("=" * 50)
    
    audio_file = "ejemplo_audio.wav"
    
    # Crear audio de ejemplo si no existe
    if not os.path.exists(audio_file):
        crear_audio_ejemplo()
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        return
    
    # Cargar modelo (opciones: tiny, base, small, medium, large-v3)
    print("\n⏳ Cargando modelo Whisper (tiny)...")
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    
    # Transcribir
    print(f"🎤 Transcribiendo: {audio_file}")
    segments, info = model.transcribe(audio_file, language="es")
    
    # Mostrar información
    print(f"\n📊 Información del audio:")
    print(f"   Idioma: {info.language} ({info.language_probability:.1%})")
    print(f"   Duración: {info.duration:.2f} segundos")
    
    # Mostrar transcripción
    print(f"\n📝 Transcripción:")
    for segment in segments:
        print(f"   {segment.text}")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

