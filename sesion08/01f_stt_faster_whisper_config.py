"""
STT Local - Configuración Avanzada
==================================
Comparar diferentes configuraciones de modelo y parámetros.

Este ejemplo demuestra:
- Diferentes tamaños de modelo (tiny, base, small)
- Configuración de compute_type (int8, float32)
- Ajustar beam_size para velocidad vs precisión
"""

from faster_whisper import WhisperModel
import os
import time


def main():
    print("⚙️  Configuración Avanzada")
    print("=" * 50)
    
    audio_file = "ejemplo_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"❌ Archivo '{audio_file}' no encontrado")
        print("   Ejecuta primero: python 01a_stt_faster_whisper_basico.py")
        return
    
    # Configuraciones a probar
    configs = [
        {
            "nombre": "🚀 Máxima Velocidad",
            "modelo": "tiny",
            "compute_type": "int8",
            "beam_size": 1
        },
        {
            "nombre": "⚖️  Equilibrado",
            "modelo": "base",
            "compute_type": "int8",
            "beam_size": 5
        },
        {
            "nombre": "🎯 Máxima Precisión",
            "modelo": "small",
            "compute_type": "float32",
            "beam_size": 5
        }
    ]
    
    print("\n📊 Comparando configuraciones:\n")
    print("-" * 60)
    
    resultados = []
    
    for config in configs:
        print(f"\n{config['nombre']}")
        print(f"   Modelo: {config['modelo']}")
        print(f"   Compute: {config['compute_type']}")
        print(f"   Beam size: {config['beam_size']}")
        
        # Cargar modelo
        print(f"   Cargando modelo...")
        model = WhisperModel(
            config['modelo'],
            device="cpu",
            compute_type=config['compute_type']
        )
        
        # Medir tiempo
        inicio = time.time()
        
        segments, info = model.transcribe(
            audio_file,
            language="es",
            beam_size=config['beam_size']
        )
        
        tiempo = time.time() - inicio
        texto = " ".join([s.text for s in segments])
        
        print(f"   ⏱️  Tiempo: {tiempo:.2f}s")
        print(f"   📝 Transcripción: {texto[:80]}...")
        
        resultados.append({
            "config": config['nombre'],
            "tiempo": tiempo,
            "texto": texto
        })
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    for r in resultados:
        print(f"\n{r['config']}: {r['tiempo']:.2f}s")
    
    print("\n💡 Recomendaciones:")
    print("   - Prototipado rápido → tiny + int8 + beam=1")
    print("   - Producción balanceada → base + int8 + beam=5")
    print("   - Máxima calidad → large-v3 + float16 + GPU")


if __name__ == "__main__":
    main()

