"""
Ejemplo simple de Text-to-Speech con Microsoft Edge TTS
Librería: https://github.com/rany2/edge-tts
Sin necesidad de API key
"""

import asyncio
import edge_tts

# Configuración
VOICE = "es-ES-XimenaNeural"  # Voz española femenina
OUTPUT_FILE = "output_edge.mp3"

TEXT = """Todo quedó abierto tras el 0-0 de Kaiserslautern, un partido de doble lectura. 
En la primera parte, Alemania impuso músculo, ritmo y una presión que obligó a España a resistir."""


async def main():
    """Genera audio con Edge TTS"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print(f"✅ Audio guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())

