"""
STT OpenAI - Calculadora de Costos
==================================
Calcular costos de transcripción con OpenAI Whisper.

Este ejemplo demuestra:
- Tarifa actual: $0.006 por minuto
- Ejemplos de costos para diferentes duraciones
- Comparación con alternativas
"""


def main():
    print("💰 Calculadora de Costos - OpenAI Whisper")
    print("=" * 50)
    
    # Tarifa actual (2024)
    COSTO_POR_MINUTO = 0.006
    
    print(f"\n📋 Tarifa actual:")
    print(f"   ${COSTO_POR_MINUTO} USD por minuto de audio")
    print(f"   ${COSTO_POR_MINUTO * 60:.2f} USD por hora")
    
    # Ejemplos
    print(f"\n📊 Ejemplos de costos:")
    print("-" * 50)
    
    ejemplos = [
        ("Nota de voz (1 min)", 1),
        ("Entrevista corta (15 min)", 15),
        ("Entrevista larga (30 min)", 30),
        ("Reunión de trabajo (1 hora)", 60),
        ("Podcast episodio (1.5 horas)", 90),
        ("Clase/conferencia (2 horas)", 120),
        ("Curso completo (10 horas)", 600),
        ("Audiolibro (15 horas)", 900),
    ]
    
    for descripcion, minutos in ejemplos:
        costo = minutos * COSTO_POR_MINUTO
        horas = minutos / 60
        
        if horas >= 1:
            duracion = f"{horas:.1f} horas"
        else:
            duracion = f"{minutos} min"
        
        print(f"\n   {descripcion}")
        print(f"      Duración: {duracion}")
        print(f"      Costo: ${costo:.2f} USD")
    
    # Comparación
    print(f"\n\n📊 Comparación con alternativas:")
    print("-" * 50)
    print(f"""
   | Servicio          | Costo/hora | Precisión | Setup    |
   |-------------------|------------|-----------|----------|
   | OpenAI Whisper    | $0.36      | ⭐⭐⭐⭐⭐   | Fácil    |
   | Google Cloud STT  | $1.44+     | ⭐⭐⭐⭐    | Medio    |
   | AWS Transcribe    | $1.44+     | ⭐⭐⭐⭐    | Medio    |
   | Azure Speech      | $1.00+     | ⭐⭐⭐⭐    | Medio    |
   | Faster-Whisper    | GRATIS     | ⭐⭐⭐⭐    | Fácil    |
   | Assembly AI       | $0.65+     | ⭐⭐⭐⭐⭐   | Fácil    |
    """)
    
    # Calculadora interactiva
    print(f"\n🧮 Calculadora rápida:")
    print("-" * 50)
    
    try:
        minutos_input = input("   Ingresa minutos de audio (Enter para saltar): ")
        
        if minutos_input.strip():
            minutos = float(minutos_input)
            costo = minutos * COSTO_POR_MINUTO
            print(f"\n   💵 Costo estimado: ${costo:.2f} USD")
            print(f"   📊 ({minutos:.0f} min × ${COSTO_POR_MINUTO})")
    except ValueError:
        pass
    except KeyboardInterrupt:
        pass
    
    print(f"\n✅ Completado")


if __name__ == "__main__":
    main()

