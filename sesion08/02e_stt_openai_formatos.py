"""
STT OpenAI - Múltiples Formatos de Audio
========================================
Transcribir diferentes formatos de audio.

Este ejemplo demuestra:
- Formatos soportados: mp3, mp4, m4a, wav, webm, etc.
- Límite de tamaño: 25 MB
- Procesamiento de múltiples archivos
"""

from openai import OpenAI
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("📂 Múltiples Formatos de Audio")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY no encontrada")
        return
    
    # Formatos soportados por OpenAI Whisper
    formatos = [".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"]
    
    print(f"\n📋 Formatos soportados:")
    print(f"   {', '.join(formatos)}")
    print(f"   Límite: 25 MB por archivo")
    
    # Buscar archivos
    archivos = []
    for fmt in formatos:
        archivos.extend(Path(".").glob(f"*{fmt}"))
    
    if not archivos:
        print(f"\n⚠️  No se encontraron archivos de audio")
        print("   Ejecuta primero: python 02a_stt_openai_basico.py")
        return
    
    print(f"\n📂 Encontrados {len(archivos)} archivos:")
    for f in archivos:
        size_mb = f.stat().st_size / (1024 * 1024)
        status = "✅" if size_mb <= 25 else "❌ >25MB"
        print(f"   {status} {f.name} ({size_mb:.2f} MB)")
    
    client = OpenAI(api_key=api_key)
    
    # Procesar archivos válidos (hasta 3)
    print(f"\n🎤 Transcribiendo...\n")
    
    for archivo in archivos[:3]:
        size_mb = archivo.stat().st_size / (1024 * 1024)
        
        if size_mb > 25:
            print(f"⚠️  {archivo.name}: Muy grande ({size_mb:.1f} MB)")
            continue
        
        print(f"📄 {archivo.name}")
        
        try:
            with open(archivo, "rb") as audio:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio,
                    language="es"
                )
            
            print(f"   ✅ {transcript.text[:80]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\n✅ Completado")


if __name__ == "__main__":
    main()

