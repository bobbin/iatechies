"""
VOICE EFFECTS - Transformar voz a Robot, Anime, y más

Este script aplica efectos de audio para crear voces estilizadas:
- 🤖 Robot: Vocoder, distorsión metálica, pitch bajo
- 🎌 Anime: Pitch alto, velocidad aumentada, eco suave
- 👻 Fantasma: Reverb, susurro, pitch bajo
- 📻 Radio antigua: Filtro paso banda, ruido, distorsión
- 🎭 Demonio: Pitch muy bajo, reverb, distorsión
"""

import os
import numpy as np
from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter
import wave
import struct


# Archivo de entrada
AUDIO_ORIGINAL = "sara-locutora-spanish-voiceover.mp3"


def cargar_audio(path: str) -> AudioSegment:
    """Carga un archivo de audio"""
    if path.endswith('.mp3'):
        return AudioSegment.from_mp3(path)
    elif path.endswith('.wav'):
        return AudioSegment.from_wav(path)
    else:
        return AudioSegment.from_file(path)


def efecto_robot(audio: AudioSegment) -> AudioSegment:
    """
    🤖 Efecto ROBOT
    - Reduce la frecuencia de muestreo (efecto digital/8-bit)
    - Aplica filtro paso bajo
    - Añade un ligero eco robótico
    """
    print("  🤖 Aplicando efecto ROBOT...")
    
    # Reducir calidad (efecto digital)
    robot = audio.set_frame_rate(8000).set_frame_rate(22050)
    
    # Filtro paso bajo (elimina agudos, suena más metálico)
    robot = low_pass_filter(robot, 2000)
    
    # Hacer más "plano" (reducir dinámico)
    robot = robot.compress_dynamic_range(threshold=-20.0, ratio=4.0)
    
    # Añadir eco corto (efecto metálico)
    eco = robot - 10  # Eco más suave
    robot_con_eco = robot.overlay(eco, position=50)  # 50ms delay
    
    return robot_con_eco


def efecto_anime(audio: AudioSegment) -> AudioSegment:
    """
    🎌 Efecto ANIME (voz kawaii/aguda)
    - Sube el pitch significativamente
    - Aumenta ligeramente la velocidad
    - Añade brillo a los agudos
    """
    print("  🎌 Aplicando efecto ANIME...")
    
    # Subir pitch (hacerlo más agudo) - cambiando frame rate
    # Subir frame rate = pitch más alto + velocidad más rápida
    original_rate = audio.frame_rate
    anime = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.4)  # 40% más agudo
    }).set_frame_rate(original_rate)
    
    # Filtro paso alto (más brillo)
    anime = high_pass_filter(anime, 200)
    
    # Boost de volumen para compensar
    anime = anime + 3
    
    return anime


def efecto_fantasma(audio: AudioSegment) -> AudioSegment:
    """
    👻 Efecto FANTASMA
    - Pitch bajo
    - Mucho reverb/eco
    - Suavizado
    """
    print("  👻 Aplicando efecto FANTASMA...")
    
    # Bajar pitch
    original_rate = audio.frame_rate
    fantasma = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 0.85)
    }).set_frame_rate(original_rate)
    
    # Múltiples ecos para reverb
    eco1 = fantasma - 6
    eco2 = fantasma - 12
    eco3 = fantasma - 18
    
    fantasma = fantasma.overlay(eco1, position=100)
    fantasma = fantasma.overlay(eco2, position=200)
    fantasma = fantasma.overlay(eco3, position=300)
    
    # Filtro paso bajo (más suave)
    fantasma = low_pass_filter(fantasma, 3000)
    
    return fantasma


def efecto_radio_antigua(audio: AudioSegment) -> AudioSegment:
    """
    📻 Efecto RADIO ANTIGUA
    - Filtro paso banda (solo medios)
    - Reducir calidad
    - Añadir "ruido" de estática
    """
    print("  📻 Aplicando efecto RADIO ANTIGUA...")
    
    # Filtro paso banda (300Hz - 3000Hz)
    radio = high_pass_filter(audio, 300)
    radio = low_pass_filter(radio, 3000)
    
    # Reducir calidad
    radio = radio.set_frame_rate(8000).set_frame_rate(22050)
    
    # Reducir bits (más "crujiente")
    radio = radio.set_sample_width(1).set_sample_width(2)
    
    # Comprimir mucho
    radio = radio.compress_dynamic_range(threshold=-15.0, ratio=6.0)
    
    return radio


def efecto_demonio(audio: AudioSegment) -> AudioSegment:
    """
    🎭 Efecto DEMONIO
    - Pitch MUY bajo
    - Reverb oscuro
    - Distorsión
    """
    print("  🎭 Aplicando efecto DEMONIO...")
    
    # Bajar pitch mucho
    original_rate = audio.frame_rate
    demonio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 0.6)  # 40% más grave
    }).set_frame_rate(original_rate)
    
    # Filtro paso bajo (más oscuro)
    demonio = low_pass_filter(demonio, 2000)
    
    # Reverb oscuro
    eco1 = demonio - 4
    eco2 = demonio - 8
    
    demonio = demonio.overlay(eco1, position=80)
    demonio = demonio.overlay(eco2, position=160)
    
    # Boost de graves
    demonio = demonio + 4
    
    return demonio


def efecto_ardilla(audio: AudioSegment) -> AudioSegment:
    """
    🐿️ Efecto ARDILLA (Chipmunk)
    - Pitch muy alto
    - Velocidad aumentada
    """
    print("  🐿️ Aplicando efecto ARDILLA...")
    
    original_rate = audio.frame_rate
    ardilla = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.8)  # 80% más agudo
    }).set_frame_rate(original_rate)
    
    return ardilla


def efecto_underwater(audio: AudioSegment) -> AudioSegment:
    """
    🌊 Efecto BAJO EL AGUA
    - Filtro paso bajo extremo
    - Modulación lenta
    """
    print("  🌊 Aplicando efecto BAJO EL AGUA...")
    
    # Filtro paso bajo extremo
    underwater = low_pass_filter(audio, 800)
    
    # Añadir reverb
    eco = underwater - 8
    underwater = underwater.overlay(eco, position=150)
    
    return underwater


def main():
    print("=" * 70)
    print("🎭 VOICE EFFECTS - Robot, Anime y más")
    print("=" * 70)
    
    if not os.path.exists(AUDIO_ORIGINAL):
        print(f"❌ No se encuentra: {AUDIO_ORIGINAL}")
        return
    
    # Cargar audio original
    print(f"\n📂 Cargando: {AUDIO_ORIGINAL}")
    audio = cargar_audio(AUDIO_ORIGINAL)
    print(f"   Duración: {len(audio)/1000:.1f}s")
    
    # Definir efectos a aplicar
    efectos = [
        (efecto_robot, "voice_effect_robot.mp3", "🤖 Robot"),
        (efecto_anime, "voice_effect_anime.mp3", "🎌 Anime"),
        (efecto_fantasma, "voice_effect_fantasma.mp3", "👻 Fantasma"),
        (efecto_radio_antigua, "voice_effect_radio.mp3", "📻 Radio antigua"),
        (efecto_demonio, "voice_effect_demonio.mp3", "🎭 Demonio"),
        (efecto_ardilla, "voice_effect_ardilla.mp3", "🐿️ Ardilla"),
        (efecto_underwater, "voice_effect_underwater.mp3", "🌊 Bajo el agua"),
    ]
    
    print(f"\n🎨 Aplicando {len(efectos)} efectos...")
    print("-" * 50)
    
    for funcion_efecto, nombre_archivo, descripcion in efectos:
        try:
            audio_procesado = funcion_efecto(audio)
            audio_procesado.export(nombre_archivo, format="mp3")
            print(f"     ✅ {descripcion}: {nombre_archivo}")
        except Exception as e:
            print(f"     ❌ {descripcion}: Error - {e}")
    
    print("\n" + "=" * 70)
    print("✅ VOICE EFFECTS COMPLETADOS!")
    print("=" * 70)
    print("""
📁 Archivos generados:
   🤖 voice_effect_robot.mp3      - Voz metálica/digital
   🎌 voice_effect_anime.mp3      - Voz kawaii aguda
   👻 voice_effect_fantasma.mp3   - Voz etérea con reverb
   📻 voice_effect_radio.mp3      - Voz de radio AM antigua
   🎭 voice_effect_demonio.mp3    - Voz grave y oscura
   🐿️ voice_effect_ardilla.mp3    - Voz tipo chipmunk
   🌊 voice_effect_underwater.mp3 - Voz bajo el agua

💡 NOTA: Estos son efectos de audio (DSP), no voice conversion.
   La voice conversion cambia la IDENTIDAD vocal manteniendo prosodia.
   Los efectos de audio modifican las características del sonido.
""")


if __name__ == "__main__":
    main()

