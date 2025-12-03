"""
Servidor WebSocket Relay para OpenAI Realtime API
==================================================
Este servidor actúa como puente entre el frontend (navegador)
y la OpenAI Realtime API.

Instalación:
pip install websockets aiohttp python-dotenv

Ejecución:
python 05_realtime_openai_server.py

Luego abrir: http://localhost:8000/05_realtime_openai_frontend.html
"""

import asyncio
import websockets
import json
import os
from pathlib import Path
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()


class RealtimeRelay:
    """Relay entre cliente web y OpenAI Realtime API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.openai_url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    
    async def handle_client(self, websocket, path):
        """Manejar conexión de cliente web"""
        print(f"✅ Cliente conectado: {websocket.remote_address}")
        
        # Conectar a OpenAI
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }
        
        try:
            async with websockets.connect(
                self.openai_url,
                extra_headers=headers
            ) as openai_ws:
                print("✅ Conectado a OpenAI Realtime API")
                
                # Configurar sesión inicial
                config = {
                    "type": "session.update",
                    "session": {
                        "modalities": ["text", "audio"],
                        "voice": "nova",
                        "input_audio_format": "pcm16",
                        "output_audio_format": "pcm16",
                        "input_audio_transcription": {
                            "model": "whisper-1"
                        },
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.5,
                            "prefix_padding_ms": 300,
                            "silence_duration_ms": 500
                        },
                        "instructions": """Eres un asistente de voz amigable y natural.
                        Responde de manera concisa y conversacional.
                        Máximo 2-3 oraciones por respuesta a menos que se pida más detalle."""
                    }
                }
                await openai_ws.send(json.dumps(config))
                
                # Crear tareas para manejar mensajes en ambas direcciones
                async def client_to_openai():
                    """Reenviar mensajes del cliente a OpenAI"""
                    try:
                        async for message in websocket:
                            await openai_ws.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        print("❌ Conexión del cliente cerrada")
                
                async def openai_to_client():
                    """Reenviar mensajes de OpenAI al cliente"""
                    try:
                        async for message in openai_ws:
                            await websocket.send(message)
                    except websockets.exceptions.ConnectionClosed:
                        print("❌ Conexión de OpenAI cerrada")
                
                # Ejecutar ambas tareas concurrentemente
                await asyncio.gather(
                    client_to_openai(),
                    openai_to_client()
                )
        
        except Exception as e:
            print(f"❌ Error en relay: {str(e)}")
            error_msg = json.dumps({
                "type": "error",
                "error": {"message": str(e)}
            })
            await websocket.send(error_msg)
        
        finally:
            print(f"🔌 Cliente desconectado: {websocket.remote_address}")


async def serve_static(request):
    """Servir archivos HTML estáticos"""
    filename = request.match_info.get('filename', '05_realtime_openai_frontend.html')
    
    file_path = Path(__file__).parent / filename
    
    if not file_path.exists():
        return web.Response(text="Archivo no encontrado", status=404)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content_type = 'text/html' if filename.endswith('.html') else 'text/plain'
    
    return web.Response(text=content, content_type=content_type)


async def main():
    """Iniciar servidor"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada en .env")
        return
    
    relay = RealtimeRelay(api_key)
    
    # Servidor WebSocket
    ws_server = await websockets.serve(
        relay.handle_client,
        "localhost",
        8765
    )
    
    # Servidor HTTP para archivos estáticos
    app = web.Application()
    app.router.add_get('/', serve_static)
    app.router.add_get('/{filename}', serve_static)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    
    print("=" * 60)
    print("🚀 Servidor de OpenAI Realtime API iniciado")
    print("=" * 60)
    print(f"📡 WebSocket Server: ws://localhost:8765")
    print(f"🌐 HTTP Server: http://localhost:8000")
    print(f"\n🎯 Abrir en navegador:")
    print(f"   http://localhost:8000/05_realtime_openai_frontend.html")
    print("\n⌨️  Presiona Ctrl+C para detener")
    print("=" * 60)
    
    # Mantener servidor corriendo
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor detenido")


if __name__ == "__main__":
    asyncio.run(main())

