"""
TTS OpenAI - Calculadora de Costos
==================================
Estimar costos para diferentes proyectos.
"""


def main():
    print("💰 Calculadora de Costos - OpenAI TTS")
    print("=" * 50)
    
    # Tarifas actuales (2024)
    COSTO_TTS1_1K = 0.015      # $15 por millón = $0.015 por 1000
    COSTO_TTS1HD_1K = 0.030    # $30 por millón = $0.030 por 1000
    
    print(f"\n📋 Tarifas actuales:")
    print(f"   TTS-1:    ${COSTO_TTS1_1K:.3f} / 1000 caracteres ($15/1M)")
    print(f"   TTS-1-HD: ${COSTO_TTS1HD_1K:.3f} / 1000 caracteres ($30/1M)")
    
    # Proyectos de ejemplo
    proyectos = [
        ("Notificación app (50 chars)", 50, "tts-1"),
        ("Artículo blog (2,500 chars)", 2500, "tts-1"),
        ("Video YouTube (10,000 chars)", 10000, "tts-1-hd"),
        ("Curso e-learning (100,000 chars)", 100000, "tts-1-hd"),
        ("Audiolibro (400,000 chars)", 400000, "tts-1-hd"),
        ("Podcast anual (520,000 chars)", 520000, "tts-1"),
    ]
    
    print(f"\n📊 Ejemplos de costos:")
    print("-" * 50)
    
    for nombre, caracteres, modelo in proyectos:
        costo_1k = COSTO_TTS1_1K if modelo == "tts-1" else COSTO_TTS1HD_1K
        costo = (caracteres / 1000) * costo_1k
        
        print(f"\n{nombre}")
        print(f"   Caracteres: {caracteres:,}")
        print(f"   Modelo: {modelo}")
        print(f"   Costo: ${costo:.2f} USD")
    
    # Calculadora interactiva
    print(f"\n" + "=" * 50)
    print("🧮 Calculadora Rápida")
    print("=" * 50)
    
    try:
        chars = input("\nCaracteres (Enter para saltar): ").strip()
        if chars:
            chars = int(chars)
            costo_tts1 = (chars / 1000) * COSTO_TTS1_1K
            costo_hd = (chars / 1000) * COSTO_TTS1HD_1K
            
            print(f"\n💵 Para {chars:,} caracteres:")
            print(f"   TTS-1:    ${costo_tts1:.4f}")
            print(f"   TTS-1-HD: ${costo_hd:.4f}")
    except:
        pass
    
    print(f"\n💡 Tips para reducir costos:")
    print(f"   • Usar TTS-1 para prototipado")
    print(f"   • Cachear audio generado")
    print(f"   • TTS local (gratis) para testing")


if __name__ == "__main__":
    main()

