"""
VOICE CONVERSION CON IA - Estilos Robot, Anime, etc.

Este script usa Voice Conversion REAL con IA (FreeVC) para transformar voces.

El proceso:
1. Crear voces de REFERENCIA con características específicas
2. Usar FreeVC para transferir esas características al audio original
3. El modelo de IA extrae el "embedding" de la voz de referencia
4. Aplica ese embedding al contenido lingüístico del audio original

Esto es diferente a efectos DSP porque:
- Usa redes neuronales (HuBERT, WavLM) para extraer características
- El "timbre" se transfiere de forma inteligente, no mecánica
- Preserva la prosodia original de forma más natural
"""

import os
import asyncio

os.environ["COQUI_TOS_AGREED"] = "1"

# Configuración
AUDIO_ORIGINAL = "sara-locutora-spanish-voiceover.mp3"


async def crear_voces_referencia():
    """
    Crea voces de referencia con características distintivas.
    Usamos Edge TTS con parámetros extremos para crear "personajes".
    """
    import edge_tts
    
    print("\n📥 PASO 1: Creando voces de referencia con características únicas...")
    print("-" * 60)
    
    # Texto largo para capturar bien las características de la voz
    texto_ref = """
    Hola, soy una voz con características muy particulares.
    Mi forma de hablar es única y distintiva.
    Escucha cómo pronuncio cada palabra con mi timbre especial.
    Esta es una muestra de mi voz para que puedas conocerme mejor.
    """
    
    # Voces de referencia con características distintivas
    voces_referencia = [
        # Voz muy grave (masculina profunda) - para "robot grave"
        {
            "voice": "es-ES-AlvaroNeural",
            "rate": "-20%",
            "pitch": "-10Hz",
            "volume": "+0%",
            "output": "ref_voz_grave.mp3",
            "descripcion": "🔊 Voz muy grave (base para robot)"
        },
        # Voz muy aguda (femenina brillante) - para "anime"
        {
            "voice": "es-MX-DaliaNeural", 
            "rate": "+15%",
            "pitch": "+10Hz",
            "volume": "+10%",
            "output": "ref_voz_aguda.mp3",
            "descripcion": "🎀 Voz aguda y brillante (base para anime)"
        },
        # Voz infantil/juvenil - más "anime kawaii"
        {
            "voice": "es-ES-IreneNeural",
            "rate": "+25%",
            "pitch": "+15Hz",
            "volume": "+5%",
            "output": "ref_voz_juvenil.mp3",
            "descripcion": "✨ Voz juvenil energética (anime kawaii)"
        },
        # Voz profunda dramática - para "villano/demonio"
        {
            "voice": "es-ES-TristanMultilingualNeural",
            "rate": "-15%",
            "pitch": "-15Hz",
            "volume": "+5%",
            "output": "ref_voz_dramatica.mp3",
            "descripcion": "🎭 Voz dramática profunda (villano)"
        },
        # Voz robótica (lo más "plana" posible)
        {
            "voice": "es-ES-AlvaroNeural",
            "rate": "-5%",
            "pitch": "-5Hz",
            "volume": "+0%",
            "output": "ref_voz_monotona.mp3",
            "descripcion": "🤖 Voz monótona (base para robot IA)"
        },
    ]
    
    for config in voces_referencia:
        communicate = edge_tts.Communicate(
            text=texto_ref,
            voice=config["voice"],
            rate=config["rate"],
            pitch=config["pitch"],
            volume=config["volume"]
        )
        await communicate.save(config["output"])
        print(f"  ✅ {config['descripcion']}: {config['output']}")
    
    return voces_referencia


def convertir_a_wav(mp3_path: str) -> str:
    """Convierte MP3 a WAV (formato requerido por FreeVC)"""
    from pydub import AudioSegment
    
    wav_path = mp3_path.replace(".mp3", ".wav")
    if not os.path.exists(wav_path) or os.path.getmtime(mp3_path) > os.path.getmtime(wav_path):
        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(22050).set_channels(1)
        audio.export(wav_path, format="wav")
    return wav_path


def voice_conversion_ia(voces_referencia: list):
    """
    Voice Conversion REAL usando FreeVC (modelo de IA)
    
    FreeVC usa:
    - HuBERT: Para extraer contenido lingüístico del audio original
    - WavLM: Para extraer el embedding de la voz de referencia
    - Decoder: Para generar el nuevo audio
    """
    print("\n🧠 PASO 2: Voice Conversion con IA (FreeVC)")
    print("-" * 60)
    
    from TTS.api import TTS
    
    # Cargar modelo FreeVC
    print("📥 Cargando modelo FreeVC...")
    model = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24")
    
    # Convertir audio original a WAV
    audio_original_wav = convertir_a_wav(AUDIO_ORIGINAL)
    
    resultados = []
    
    # Mapeo de voces de referencia a estilos
    estilos = [
        ("ref_voz_grave.mp3", "vc_ia_robot_grave", "🤖 Robot (voz grave IA)"),
        ("ref_voz_aguda.mp3", "vc_ia_anime_femenino", "🎌 Anime femenino (IA)"),
        ("ref_voz_juvenil.mp3", "vc_ia_anime_kawaii", "✨ Anime kawaii (IA)"),
        ("ref_voz_dramatica.mp3", "vc_ia_villano", "🎭 Villano dramático (IA)"),
        ("ref_voz_monotona.mp3", "vc_ia_robot_ia", "🤖 Robot IA monótono"),
    ]
    
    for ref_file, output_base, descripcion in estilos:
        if not os.path.exists(ref_file):
            print(f"  ⚠️ Saltando {ref_file} - no existe")
            continue
        
        ref_wav = convertir_a_wav(ref_file)
        output_path = f"{output_base}.wav"
        
        print(f"\n🎭 Procesando: {descripcion}")
        print(f"   Audio original: {AUDIO_ORIGINAL}")
        print(f"   Voz referencia: {ref_file}")
        
        # Voice Conversion con IA
        model.voice_conversion_to_file(
            source_wav=audio_original_wav,
            target_wav=ref_wav,
            file_path=output_path
        )
        
        print(f"   ✅ Resultado: {output_path}")
        resultados.append((output_path, descripcion))
    
    return resultados


def explicar_proceso():
    """Explica cómo funciona el Voice Conversion con IA"""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    VOICE CONVERSION CON IA - Cómo funciona               ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  1. AUDIO ORIGINAL (Sara)                                                ║
║     │                                                                    ║
║     ▼                                                                    ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │  HuBERT (Red Neuronal)                                           │   ║
║  │  • Extrae contenido lingüístico (fonemas, palabras)              │   ║
║  │  • Extrae prosodia (ritmo, pausas, entonación)                   │   ║
║  │  • IGNORA el timbre/identidad vocal                              │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
║     │                                                                    ║
║     │  contenido + prosodia                                              ║
║     │                                                                    ║
║     ▼                                                                    ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │  DECODER (Red Neuronal)  ◄─── Embedding de voz referencia        │   ║
║  │  • Combina contenido original con timbre nuevo                   │   ║
║  │  • Genera forma de onda del nuevo audio                          │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
║     │                                           ▲                        ║
║     │                                           │                        ║
║     ▼                                           │                        ║
║  AUDIO CONVERTIDO                    ┌──────────────────────┐           ║
║  (Sara con voz de robot/anime)       │  WavLM (Red Neuronal)│           ║
║                                      │  • Extrae "embedding"│           ║
║                                      │    de la voz objetivo│           ║
║                                      └──────────────────────┘           ║
║                                                 ▲                        ║
║                                                 │                        ║
║                                      VOZ DE REFERENCIA                   ║
║                                      (robot, anime, etc.)                ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

💡 La IA "entiende" qué hace única a cada voz (timbre, formantes, etc.)
   y transfiere solo esas características, preservando TODO lo demás.
""")


async def main():
    print("=" * 70)
    print("🧠 VOICE CONVERSION CON IA - Robot, Anime, Villano")
    print("   (Usando redes neuronales, no efectos DSP)")
    print("=" * 70)
    
    # Explicar el proceso
    explicar_proceso()
    
    if not os.path.exists(AUDIO_ORIGINAL):
        print(f"❌ No se encuentra: {AUDIO_ORIGINAL}")
        return
    
    # Paso 1: Crear voces de referencia
    voces_ref = await crear_voces_referencia()
    
    # Paso 2: Voice Conversion con IA
    resultados = voice_conversion_ia(voces_ref)
    
    print("\n" + "=" * 70)
    print("✅ VOICE CONVERSION CON IA COMPLETADO!")
    print("=" * 70)
    print("""
📁 Archivos generados (con IA real):

   🤖 vc_ia_robot_grave.wav     - Sara → Voz robótica grave (IA)
   🎌 vc_ia_anime_femenino.wav  - Sara → Voz anime femenina (IA)
   ✨ vc_ia_anime_kawaii.wav    - Sara → Voz anime kawaii (IA)
   🎭 vc_ia_villano.wav         - Sara → Voz de villano (IA)
   🤖 vc_ia_robot_ia.wav        - Sara → Voz robot monótona (IA)

🔬 DIFERENCIA vs efectos DSP:
   • DSP: Modifica frecuencias matemáticamente (pitch shift, filtros)
   • IA:  "Entiende" las características vocales y las transfiere

   Los resultados de IA suenan más naturales porque la red neuronal
   aprendió qué hace única a cada voz analizando miles de ejemplos.
""")


if __name__ == "__main__":
    asyncio.run(main())

