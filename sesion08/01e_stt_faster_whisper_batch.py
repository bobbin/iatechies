"""
STT Local - Transcripción en Batch
==================================
Transcribir múltiples archivos de audio automáticamente.

Este ejemplo demuestra:
- Buscar archivos de audio en directorio
- Transcribir en batch
- Guardar resultados en archivo
"""

from faster_whisper import WhisperModel
from pathlib import Path
import os


def main():
    print("📂 Transcripción en Batch")
    print("=" * 50)
    
    # Buscar archivos de audio
    audio_extensions = [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(Path(".").glob(f"*{ext}"))
    
    if not audio_files:
        print(f"\n⚠️  No se encontraron archivos de audio")
        print(f"📁 Extensiones soportadas: {', '.join(audio_extensions)}")
        print(f"\n💡 Ejecuta primero: python 01a_stt_faster_whisper_basico.py")
        return
    
    print(f"\n📂 Encontrados {len(audio_files)} archivos:")
    for f in audio_files:
        print(f"   - {f.name}")
    
    # Cargar modelo (una vez para todos)
    print("\n⏳ Cargando modelo...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    # Procesar cada archivo
    resultados = []
    
    for audio_file in audio_files:
        print(f"\n🎤 Procesando: {audio_file.name}")
        
        try:
            segments, info = model.transcribe(str(audio_file), language="es")
            
            texto = " ".join([segment.text for segment in segments])
            
            resultados.append({
                "archivo": audio_file.name,
                "idioma": info.language,
                "duracion": info.duration,
                "transcripcion": texto
            })
            
            print(f"   ✅ Completado ({info.duration:.1f}s)")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # Guardar resultados
    output_file = "transcripciones_batch.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("TRANSCRIPCIONES EN BATCH\n")
        f.write("=" * 60 + "\n\n")
        
        for r in resultados:
            f.write(f"Archivo: {r['archivo']}\n")
            f.write(f"Idioma: {r['idioma']}\n")
            f.write(f"Duración: {r['duracion']:.2f}s\n")
            f.write(f"Transcripción:\n{r['transcripcion']}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"\n✅ Resultados guardados: {output_file}")
    print(f"   Total procesados: {len(resultados)} archivos")


if __name__ == "__main__":
    main()

