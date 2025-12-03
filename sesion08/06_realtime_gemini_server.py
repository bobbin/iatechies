"""
Servidor para Gemini Multimodal Live API
========================================
Servidor WebSocket que actúa como relay entre el frontend
y la API de Gemini Live.

Instalación:
pip install google-generativeai websockets aiohttp python-dotenv

Ejecución:
python 06_realtime_gemini_server.py

Nota: Gemini Live API está en preview. Este código es una demostración
basada en la documentación disponible.
"""

import asyncio
import websockets
import json
import os
import base64
from pathlib import Path
from aiohttp import web
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GeminiLiveRelay:
    """
    Relay para Gemini Multimodal Live API
    
    Nota: La implementación exacta de Gemini Live puede variar
    ya que está en preview. Este es un ejemplo conceptual.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = None
        self.chat = None
    
    def initialize_model(self):
        """Inicializar modelo de Gemini"""
        
        generation_config = genai.GenerationConfig(
            temperature=0.9,
            top_p=1.0,
            max_output_tokens=8192,
        )
        
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
            system_instruction="""Eres un asistente de voz amigable.
            Responde de manera breve y natural.
            Máximo 2-3 oraciones por respuesta."""
        )
        
        self.chat = self.model.start_chat(history=[])
        print("✅ Modelo Gemini inicializado")
    
    async def handle_client(self, websocket, path):
        """Manejar conexión del cliente web"""
        print(f"✅ Cliente conectado: {websocket.remote_address}")
        
        try:
            # Inicializar modelo si no está inicializado
            if not self.model:
                self.initialize_model()
            
            # Enviar confirmación de conexión
            await websocket.send(json.dumps({
                "type": "session.created",
                "session": {
                    "id": "gemini_session_001",
                    "model": "gemini-2.0-flash-exp"
                }
            }))
            
            # Buffer para acumular audio
            audio_buffer = bytearray()
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    event_type = data.get("type", "")
                    
                    if event_type == "input_audio_buffer.append":
                        # Acumular audio
                        audio_base64 = data.get("audio", "")
                        if audio_base64:
                            audio_bytes = base64.b64decode(audio_base64)
                            audio_buffer.extend(audio_bytes)
                    
                    elif event_type == "input_audio_buffer.commit":
                        # Procesar audio acumulado
                        print(f"📥 Audio recibido: {len(audio_buffer)} bytes")
                        
                        # Notificar inicio de transcripción
                        await websocket.send(json.dumps({
                            "type": "input_audio_buffer.speech_started"
                        }))
                        
                        # En producción, aquí convertiríamos el audio a formato
                        # compatible con Gemini y lo enviaríamos
                        # Por ahora, simulamos una transcripción
                        
                        transcription = "[Audio transcrito - funcionalidad en desarrollo]"
                        
                        await websocket.send(json.dumps({
                            "type": "conversation.item.input_audio_transcription.completed",
                            "transcript": transcription
                        }))
                        
                        # Limpiar buffer
                        audio_buffer.clear()
                    
                    elif event_type == "response.create":
                        # Generar respuesta usando Gemini (modo texto por ahora)
                        await self.generate_response(websocket)
                    
                    elif event_type == "text_message":
                        # Mensaje de texto directo
                        text = data.get("text", "")
                        if text:
                            await self.process_text_message(websocket, text)
                
                except json.JSONDecodeError:
                    print("⚠️  Mensaje JSON inválido")
                except Exception as e:
                    print(f"❌ Error procesando mensaje: {str(e)}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": {"message": str(e)}
                    }))
        
        except websockets.exceptions.ConnectionClosed:
            print(f"🔌 Cliente desconectado: {websocket.remote_address}")
        except Exception as e:
            print(f"❌ Error en conexión: {str(e)}")
    
    async def process_text_message(self, websocket, text: str):
        """Procesar mensaje de texto y generar respuesta"""
        print(f"📝 Procesando texto: {text}")
        
        try:
            # Enviar transcripción del usuario
            await websocket.send(json.dumps({
                "type": "conversation.item.input_audio_transcription.completed",
                "transcript": text
            }))
            
            # Generar respuesta con streaming
            response = self.chat.send_message(text, stream=True)
            
            full_text = ""
            
            for chunk in response:
                if chunk.text:
                    # Enviar delta de transcripción
                    await websocket.send(json.dumps({
                        "type": "response.audio_transcript.delta",
                        "delta": chunk.text
                    }))
                    
                    full_text += chunk.text
                    
                    # Simular audio (en producción, usar TTS)
                    # await websocket.send(json.dumps({
                    #     "type": "response.audio.delta",
                    #     "delta": base64_audio_chunk
                    # }))
            
            # Respuesta completada
            await websocket.send(json.dumps({
                "type": "response.done",
                "response": {
                    "text": full_text
                }
            }))
        
        except Exception as e:
            print(f"❌ Error generando respuesta: {str(e)}")
            await websocket.send(json.dumps({
                "type": "error",
                "error": {"message": str(e)}
            }))
    
    async def generate_response(self, websocket):
        """Generar respuesta del modelo"""
        # Placeholder - en producción esto usaría el contexto actual
        await websocket.send(json.dumps({
            "type": "response.done"
        }))


async def serve_static(request):
    """Servir archivos HTML estáticos"""
    filename = request.match_info.get('filename', '06_realtime_gemini_frontend.html')
    
    file_path = Path(__file__).parent / filename
    
    if not file_path.exists():
        return web.Response(text="Archivo no encontrado", status=404)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content_type = 'text/html' if filename.endswith('.html') else 'text/plain'
    
    return web.Response(text=content, content_type=content_type)


async def main():
    """Iniciar servidores"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada en .env")
        print("Obtén una en: https://makersuite.google.com/app/apikey")
        return
    
    relay = GeminiLiveRelay(api_key)
    
    # Servidor WebSocket
    ws_server = await websockets.serve(
        relay.handle_client,
        "localhost",
        8766  # Puerto diferente a OpenAI
    )
    
    # Servidor HTTP
    app = web.Application()
    app.router.add_get('/', serve_static)
    app.router.add_get('/{filename}', serve_static)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8001)
    await site.start()
    
    print("=" * 60)
    print("🚀 Servidor de Gemini Live API iniciado")
    print("=" * 60)
    print(f"📡 WebSocket Server: ws://localhost:8766")
    print(f"🌐 HTTP Server: http://localhost:8001")
    print(f"\n🎯 Abrir en navegador:")
    print(f"   http://localhost:8001/06_realtime_gemini_frontend.html")
    print("\n⚠️  NOTA: Gemini Live está en preview.")
    print("   Algunas funcionalidades pueden estar en desarrollo.")
    print("\n⌨️  Presiona Ctrl+C para detener")
    print("=" * 60)
    
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor detenido")


if __name__ == "__main__":
    asyncio.run(main())

