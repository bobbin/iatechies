"""
STT OpenAI - Generar Subtítulos SRT
===================================
Generar archivo de subtítulos directamente desde la API.

Este ejemplo demuestra:
- Usar response_format="srt" para obtener subtítulos
- También disponible: vtt (WebVTT)
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("🎬 Generar Subtítulos SRT (OpenAI)")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    audio_file = "ejemplo_audio.wav"
    if not os.path.exists(audio_file):
        print(f"❌ Archivo no encontrado: {audio_file}")
        print("   Ejecuta primero: python 02a_stt_openai_basico.py")
        return
    
    client = OpenAI(api_key=api_key)
    
    print(f"\n🎤 Generando subtítulos SRT...")
    
    with open(audio_file, "rb") as audio:
        # response_format="srt" genera subtítulos directamente
        subtitulos = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="srt",  # o "vtt" para WebVTT
            language="es"
        )
    
    # Guardar archivo SRT
    srt_file = "subtitulos_openai.srt"
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(subtitulos)
    
    print(f"✅ Guardado: {srt_file}")
    
    # Mostrar contenido
    print(f"\n📄 Contenido:")
    print("-" * 40)
    print(subtitulos)
    
    print("\n💡 Formatos disponibles:")
    print("   - json (texto simple)")
    print("   - verbose_json (con metadata)")
    print("   - srt (subtítulos SubRip)")
    print("   - vtt (WebVTT para web)")
    print("   - text (solo texto)")


if __name__ == "__main__":
    main()

