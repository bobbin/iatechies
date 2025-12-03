"""
Voice Conversion: Cambiar la voz de un audio por otra completamente distinta

Proceso:
1. Transcribir el audio original (STT con Faster-Whisper)
2. Regenerar con diferentes voces (TTS con Edge TTS)

Entrada: sara-locutora-spanish-voiceover.mp3
Salida: Mismo contenido con voces de hombre, locutor, mexicana, etc.
"""

import asyncio
import edge_tts
from faster_whisper import WhisperModel

# Configuración
AUDIO_ORIGINAL = "sara-locutora-spanish-voiceover.mp3"

# Voces para la conversión (Edge TTS - Azure Neural Voices)
VOCES_DESTINO = [
    # España
    ("es-ES-AlvaroNeural", "hombre_espanol", "♂️ Álvaro - Hombre español"),
    ("es-ES-ElviraNeural", "mujer_espanola", "♀️ Elvira - Mujer española"),
    
    # México (acento diferente)
    ("es-MX-JorgeNeural", "hombre_mexicano", "♂️ Jorge - Hombre mexicano"),
    ("es-MX-DaliaNeural", "mujer_mexicana", "♀️ Dalia - Mujer mexicana"),
    
    # Argentina (acento rioplatense)
    ("es-AR-TomasNeural", "hombre_argentino", "♂️ Tomás - Hombre argentino"),
    ("es-AR-ElenaNeural", "mujer_argentina", "♀️ Elena - Mujer argentina"),
    
    # Colombia
    ("es-CO-GonzaloNeural", "hombre_colombiano", "♂️ Gonzalo - Hombre colombiano"),
    
    # Voces multilingües (más expresivas)
    ("es-ES-TristanMultilingualNeural", "locutor_premium", "♂️ Tristán - Locutor premium"),
    ("es-ES-XimenaMultilingualNeural", "locutora_premium", "♀️ Ximena - Locutora premium"),
]


def transcribir_audio(audio_path: str) -> str:
    """Paso 1: Transcribir el audio original usando Faster-Whisper"""
    print(f"\n🎤 Transcribiendo: {audio_path}")
    print("-" * 50)
    
    # Cargar modelo (small es un buen balance)
    model = WhisperModel("small", device="cpu", compute_type="int8")
    
    # Transcribir
    segments, info = model.transcribe(audio_path, language="es")
    
    # Unir todos los segmentos
    texto_completo = ""
    for segment in segments:
        texto_completo += segment.text + " "
        print(f"  [{segment.start:.1f}s - {segment.end:.1f}s] {segment.text}")
    
    texto_completo = texto_completo.strip()
    print("-" * 50)
    print(f"📝 Texto completo ({len(texto_completo)} caracteres):")
    print(f"   \"{texto_completo[:100]}...\"" if len(texto_completo) > 100 else f"   \"{texto_completo}\"")
    
    return texto_completo


async def generar_con_voz(texto: str, voz: str, nombre_archivo: str, descripcion: str):
    """Genera audio con una voz específica"""
    output_file = f"voice_converted_{nombre_archivo}.mp3"
    
    communicate = edge_tts.Communicate(
        text=texto,
        voice=voz,
        rate="+0%",  # Velocidad normal
    )
    
    await communicate.save(output_file)
    print(f"  ✅ {descripcion}: {output_file}")
    return output_file


async def convertir_voz(texto: str):
    """Paso 2: Regenerar el texto con múltiples voces"""
    print(f"\n🔄 CONVIRTIENDO A {len(VOCES_DESTINO)} VOCES DIFERENTES:")
    print("-" * 50)
    
    archivos_generados = []
    
    for voz, nombre, descripcion in VOCES_DESTINO:
        archivo = await generar_con_voz(texto, voz, nombre, descripcion)
        archivos_generados.append(archivo)
    
    return archivos_generados


async def demo_estilos_locutor(texto: str):
    """Bonus: Generar con diferentes estilos de locución"""
    print(f"\n🎙️ ESTILOS DE LOCUCIÓN (misma voz, diferentes parámetros):")
    print("-" * 50)
    
    estilos = [
        # (rate, pitch, volume, nombre, descripcion)
        ("-10%", "-5Hz", "+0%", "locutor_serio", "📰 Locutor de noticias (pausado, grave)"),
        ("+20%", "+0Hz", "+10%", "locutor_deportes", "⚽ Locutor deportivo (rápido, enérgico)"),
        ("-20%", "-10Hz", "-10%", "narrador_documental", "🎬 Narrador documental (lento, profundo)"),
        ("+10%", "+10Hz", "+20%", "anuncio_radio", "📻 Anuncio de radio (alegre, alto)"),
        ("-30%", "+0Hz", "+0%", "meditacion", "🧘 Guía de meditación (muy lento)"),
    ]
    
    voz_base = "es-ES-AlvaroNeural"  # Voz masculina española
    
    for rate, pitch, volume, nombre, descripcion in estilos:
        output_file = f"voice_style_{nombre}.mp3"
        
        communicate = edge_tts.Communicate(
            text=texto[:200],  # Solo primeros 200 chars para el demo
            voice=voz_base,
            rate=rate,
            pitch=pitch,
            volume=volume,
        )
        
        await communicate.save(output_file)
        print(f"  ✅ {descripcion}: {output_file}")


async def main():
    print("=" * 60)
    print("🎭 VOICE CONVERSION - Cambiar voz de un audio")
    print("=" * 60)
    
    # Paso 1: Transcribir audio original
    texto = transcribir_audio(AUDIO_ORIGINAL)
    
    if not texto:
        print("❌ Error: No se pudo transcribir el audio")
        return
    
    # Paso 2: Regenerar con diferentes voces
    archivos = await convertir_voz(texto)
    
    # Bonus: Estilos de locución
    await demo_estilos_locutor(texto)
    
    print("\n" + "=" * 60)
    print("✅ VOICE CONVERSION COMPLETADO!")
    print("=" * 60)
    print(f"\n📁 Archivos generados:")
    print(f"   - {len(archivos)} conversiones de voz")
    print(f"   - 5 estilos de locución")
    print(f"\n💡 Compara el audio original con las conversiones!")


if __name__ == "__main__":
    asyncio.run(main())

