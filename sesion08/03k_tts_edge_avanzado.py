"""
Ejemplo avanzado de Microsoft Edge TTS
Muestra todas las características disponibles:
- Cambio de velocidad (rate)
- Cambio de volumen  
- Cambio de tono (pitch)
- Generación de subtítulos SRT
- Listado de voces
- Streaming de audio

Librería: https://github.com/rany2/edge-tts
"""

import asyncio
import edge_tts
from edge_tts import VoicesManager

TEXT = """Todo quedó abierto tras el 0-0 de Kaiserslautern, un partido de doble lectura. 
En la primera parte, Alemania impuso músculo, ritmo y una presión que obligó a España a resistir."""


# =============================================================================
# 1. LISTAR VOCES DISPONIBLES
# =============================================================================
async def listar_voces_espanol():
    """Lista todas las voces en español disponibles"""
    voices = await VoicesManager.create()
    spanish_voices = voices.find(Language="es")
    
    print("🎤 VOCES EN ESPAÑOL DISPONIBLES:")
    print("-" * 60)
    for voice in spanish_voices:
        gender = "♀️" if voice["Gender"] == "Female" else "♂️"
        print(f"  {gender} {voice['ShortName']:30} - {voice['Locale']}")
    print("-" * 60)
    print(f"Total: {len(spanish_voices)} voces\n")
    return spanish_voices


# =============================================================================
# 2. CAMBIAR VELOCIDAD (RATE)
# =============================================================================
async def ejemplo_velocidad():
    """Genera audio con diferentes velocidades"""
    print("⚡ EJEMPLO: Cambio de velocidad")
    
    velocidades = [
        ("-50%", "lento"),
        ("+0%", "normal"),
        ("+50%", "rapido"),
        ("+100%", "muy_rapido"),
    ]
    
    for rate, nombre in velocidades:
        communicate = edge_tts.Communicate(
            text="Hola, esta es una prueba de velocidad.",
            voice="es-ES-ElviraNeural",
            rate=rate
        )
        output = f"output_edge_{nombre}.mp3"
        await communicate.save(output)
        print(f"  ✅ {nombre}: {output}")


# =============================================================================
# 3. CAMBIAR VOLUMEN
# =============================================================================
async def ejemplo_volumen():
    """Genera audio con diferentes volúmenes"""
    print("\n🔊 EJEMPLO: Cambio de volumen")
    
    volumenes = [
        ("-50%", "bajo"),
        ("+0%", "normal"),
        ("+50%", "alto"),
    ]
    
    for volume, nombre in volumenes:
        communicate = edge_tts.Communicate(
            text="Probando diferentes niveles de volumen.",
            voice="es-ES-AlvaroNeural",
            volume=volume
        )
        output = f"output_edge_vol_{nombre}.mp3"
        await communicate.save(output)
        print(f"  ✅ Volumen {nombre}: {output}")


# =============================================================================
# 4. CAMBIAR TONO (PITCH)
# =============================================================================
async def ejemplo_tono():
    """Genera audio con diferentes tonos"""
    print("\n🎵 EJEMPLO: Cambio de tono (pitch)")
    
    tonos = [
        ("-20Hz", "grave"),
        ("+0Hz", "normal"),
        ("+20Hz", "agudo"),
    ]
    
    for pitch, nombre in tonos:
        communicate = edge_tts.Communicate(
            text="El tono de mi voz puede variar.",
            voice="es-ES-ElviraNeural",
            pitch=pitch
        )
        output = f"output_edge_tono_{nombre}.mp3"
        await communicate.save(output)
        print(f"  ✅ Tono {nombre}: {output}")


# =============================================================================
# 5. GENERAR SUBTÍTULOS (SRT)
# =============================================================================
async def ejemplo_subtitulos():
    """Genera audio CON subtítulos sincronizados"""
    print("\n📝 EJEMPLO: Audio + Subtítulos SRT")
    
    communicate = edge_tts.Communicate(TEXT, "es-ES-XimenaNeural")
    
    submaker = edge_tts.SubMaker()
    
    with open("output_edge_subtitulos.mp3", "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    
    # Guardar subtítulos
    with open("output_edge_subtitulos.srt", "w", encoding="utf-8") as srt_file:
        srt_file.write(submaker.get_srt())
    
    print("  ✅ Audio: output_edge_subtitulos.mp3")
    print("  ✅ Subtítulos: output_edge_subtitulos.srt")


# =============================================================================
# 6. STREAMING (para apps en tiempo real)
# =============================================================================
async def ejemplo_streaming():
    """Muestra cómo hacer streaming del audio"""
    print("\n🌊 EJEMPLO: Streaming de audio")
    
    communicate = edge_tts.Communicate(
        "Esto es streaming, el audio se genera por partes.",
        "es-MX-DaliaNeural"
    )
    
    total_bytes = 0
    chunks = 0
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            total_bytes += len(chunk["data"])
            chunks += 1
    
    print(f"  📊 Chunks recibidos: {chunks}")
    print(f"  📊 Bytes totales: {total_bytes:,}")


# =============================================================================
# 7. EJEMPLO COMPLETO CON TODAS LAS OPCIONES
# =============================================================================
async def ejemplo_completo():
    """Combina todas las opciones en un ejemplo"""
    print("\n🎯 EJEMPLO COMPLETO:")
    
    communicate = edge_tts.Communicate(
        text=TEXT,
        voice="es-ES-XimenaNeural",
        rate="+10%",      # Ligeramente más rápido
        volume="+20%",    # Ligeramente más alto
        pitch="+5Hz"      # Tono ligeramente más agudo
    )
    
    submaker = edge_tts.SubMaker()
    
    with open("output_edge_completo.mp3", "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    
    with open("output_edge_completo.srt", "w", encoding="utf-8") as srt_file:
        srt_file.write(submaker.get_srt())
    
    print("  ✅ Audio: output_edge_completo.mp3")
    print("  ✅ Subtítulos: output_edge_completo.srt")


# =============================================================================
# MAIN
# =============================================================================
async def main():
    print("=" * 60)
    print("🔷 MICROSOFT EDGE TTS - EJEMPLO AVANZADO")
    print("=" * 60)
    
    # 1. Listar voces
    await listar_voces_espanol()
    
    # 2-6. Ejecutar ejemplos
    await ejemplo_velocidad()
    await ejemplo_volumen()
    await ejemplo_tono()
    await ejemplo_subtitulos()
    await ejemplo_streaming()
    await ejemplo_completo()
    
    print("\n" + "=" * 60)
    print("✅ Todos los ejemplos completados!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

