"""
Audio en Tiempo Real con OpenAI Realtime API
============================================
Conversación de voz bidireccional en tiempo real con GPT-4o.
Latencia ultra-baja (~320ms) y soporte para interrupciones naturales.

Instalación:
pip install websockets pyaudio python-dotenv

Configuración:
OPENAI_API_KEY=sk-tu-api-key-aqui en archivo .env

Nota: Este ejemplo requiere micrófono. Para producción, usar frontend web.
"""

import asyncio
import websockets
import json
import os
import base64
from dotenv import load_dotenv

load_dotenv()


class OpenAIRealtimeClient:
    """Cliente para OpenAI Realtime API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
        self.ws = None
    
    async def connect(self):
        """Conectar a la API de Realtime"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }
        
        self.ws = await websockets.connect(
            self.url,
            extra_headers=headers
        )
        print("✅ Conectado a OpenAI Realtime API")
    
    async def configure_session(self, voice="alloy", instructions=None):
        """Configurar la sesión de conversación"""
        config = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": voice,
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
                }
            }
        }
        
        if instructions:
            config["session"]["instructions"] = instructions
        
        await self.ws.send(json.dumps(config))
        print("⚙️  Sesión configurada")
    
    async def send_audio(self, audio_data: bytes):
        """Enviar audio al servidor"""
        audio_base64 = base64.b64encode(audio_data).decode()
        
        message = {
            "type": "input_audio_buffer.append",
            "audio": audio_base64
        }
        
        await self.ws.send(json.dumps(message))
    
    async def commit_audio(self):
        """Finalizar envío de audio y solicitar respuesta"""
        message = {
            "type": "input_audio_buffer.commit"
        }
        await self.ws.send(json.dumps(message))
    
    async def create_response(self):
        """Solicitar respuesta del modelo"""
        message = {
            "type": "response.create",
            "response": {
                "modalities": ["text", "audio"]
            }
        }
        await self.ws.send(json.dumps(message))
    
    async def send_text(self, text: str):
        """Enviar mensaje de texto (alternativa al audio)"""
        message = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        }
        await self.ws.send(json.dumps(message))
        await self.create_response()
    
    async def receive_events(self):
        """Recibir y procesar eventos del servidor"""
        async for message in self.ws:
            event = json.loads(message)
            yield event
    
    async def close(self):
        """Cerrar conexión"""
        if self.ws:
            await self.ws.close()
            print("🔌 Conexión cerrada")


async def ejemplo_1_conversacion_basica():
    """
    Ejemplo 1: Conversación básica con texto (sin micrófono)
    """
    print("=" * 60)
    print("EJEMPLO 1: Conversación Básica (Modo Texto)")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAIRealtimeClient(api_key)
    
    try:
        # Conectar
        await client.connect()
        
        # Configurar sesión
        instructions = """Eres un asistente de voz amigable y conciso. 
        Responde de manera breve y natural, como en una conversación real.
        Máximo 2-3 oraciones por respuesta."""
        
        await client.configure_session(
            voice="nova",
            instructions=instructions
        )
        
        # Esperar confirmación de configuración
        async for event in client.receive_events():
            if event["type"] == "session.created":
                print(f"✅ Sesión creada: {event['session']['id']}")
                break
        
        # Enviar mensaje de texto
        print("\n👤 Usuario: Hola, ¿cómo estás?")
        await client.send_text("Hola, ¿cómo estás?")
        
        # Procesar respuesta
        response_text = ""
        audio_chunks = []
        
        async for event in client.receive_events():
            event_type = event["type"]
            
            if event_type == "response.audio_transcript.delta":
                # Texto de la respuesta (transcripción del audio)
                delta = event.get("delta", "")
                response_text += delta
                print(delta, end="", flush=True)
            
            elif event_type == "response.audio.delta":
                # Audio de la respuesta
                audio_base64 = event.get("delta", "")
                if audio_base64:
                    audio_chunks.append(base64.b64decode(audio_base64))
            
            elif event_type == "response.done":
                print(f"\n\n🤖 Asistente: {response_text}")
                print(f"📊 Audio chunks recibidos: {len(audio_chunks)}")
                
                # Guardar audio (opcional)
                if audio_chunks:
                    with open("response_audio.pcm", "wb") as f:
                        f.write(b"".join(audio_chunks))
                    print("💾 Audio guardado en: response_audio.pcm")
                
                break
            
            elif event_type == "error":
                print(f"\n❌ Error: {event.get('error', {})}")
                break
        
        await client.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def ejemplo_2_conversacion_interactiva():
    """
    Ejemplo 2: Conversación interactiva multi-turno
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Conversación Interactiva")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada")
        return
    
    client = OpenAIRealtimeClient(api_key)
    
    try:
        await client.connect()
        
        instructions = """Eres un asistente personal útil.
        Responde de forma breve y conversacional.
        Si el usuario dice 'adiós' o 'terminar', despídete amablemente."""
        
        await client.configure_session(voice="echo", instructions=instructions)
        
        # Esperar sesión creada
        async for event in client.receive_events():
            if event["type"] == "session.created":
                break
        
        print("\n💬 Conversación iniciada. Escribe 'salir' para terminar.\n")
        
        while True:
            # Input del usuario
            user_input = input("👤 Tú: ").strip()
            
            if not user_input or user_input.lower() in ['salir', 'exit', 'quit']:
                print("👋 Terminando conversación...")
                break
            
            # Enviar mensaje
            await client.send_text(user_input)
            
            # Recibir respuesta
            response_text = ""
            
            print("🤖 Asistente: ", end="", flush=True)
            
            async for event in client.receive_events():
                if event["type"] == "response.audio_transcript.delta":
                    delta = event.get("delta", "")
                    response_text += delta
                    print(delta, end="", flush=True)
                
                elif event["type"] == "response.done":
                    print("\n")
                    break
                
                elif event["type"] == "error":
                    print(f"\n❌ Error: {event.get('error', {})}")
                    break
        
        await client.close()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversación interrumpida")
        await client.close()
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def ejemplo_3_con_funciones():
    """
    Ejemplo 3: Conversación con llamadas a funciones
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Conversación con Funciones")
    print("=" * 60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada")
        return
    
    # Funciones disponibles
    def get_weather(location: str) -> dict:
        """Obtener clima de una ubicación"""
        # Simulado
        return {
            "location": location,
            "temperature": "22°C",
            "condition": "Soleado",
            "humidity": "65%"
        }
    
    def get_time() -> str:
        """Obtener hora actual"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    client = OpenAIRealtimeClient(api_key)
    
    try:
        await client.connect()
        
        # Configurar con funciones
        config = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": "Eres un asistente que puede consultar el clima y la hora. Usa las funciones disponibles cuando sea necesario.",
                "tools": [
                    {
                        "type": "function",
                        "name": "get_weather",
                        "description": "Obtener el clima actual de una ubicación",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "Nombre de la ciudad"
                                }
                            },
                            "required": ["location"]
                        }
                    },
                    {
                        "type": "function",
                        "name": "get_time",
                        "description": "Obtener la hora actual",
                        "parameters": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ],
                "tool_choice": "auto"
            }
        }
        
        await client.ws.send(json.dumps(config))
        
        # Esperar sesión
        async for event in client.receive_events():
            if event["type"] == "session.created":
                break
        
        print("\n💬 Pregunta algo sobre el clima o la hora\n")
        
        # Pregunta del usuario
        user_message = "¿Qué hora es y cómo está el clima en Madrid?"
        print(f"👤 Usuario: {user_message}\n")
        
        await client.send_text(user_message)
        
        # Procesar respuesta con función
        async for event in client.receive_events():
            event_type = event["type"]
            
            if event_type == "response.function_call_arguments.done":
                # El modelo quiere llamar una función
                function_name = event["name"]
                arguments = json.loads(event["arguments"])
                
                print(f"🔧 Llamando función: {function_name}({arguments})")
                
                # Ejecutar función
                if function_name == "get_weather":
                    result = get_weather(arguments["location"])
                elif function_name == "get_time":
                    result = get_time()
                else:
                    result = {"error": "Función no encontrada"}
                
                print(f"📊 Resultado: {result}")
                
                # Enviar resultado al modelo
                function_output = {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": event["call_id"],
                        "output": json.dumps(result)
                    }
                }
                await client.ws.send(json.dumps(function_output))
                await client.create_response()
            
            elif event_type == "response.audio_transcript.delta":
                print(event.get("delta", ""), end="", flush=True)
            
            elif event_type == "response.done":
                print("\n")
                break
        
        await client.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def ejemplo_4_info_frontend():
    """
    Ejemplo 4: Información sobre implementación con frontend
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Implementación con Frontend")
    print("=" * 60)
    
    print("""
📱 Para usar el micrófono del navegador, necesitas un frontend web.

Hemos creado archivos HTML/JS completos:
    
    📁 05_realtime_openai_frontend.html
       - Interfaz web completa
       - Acceso al micrófono
       - Visualización de audio
       - Botón para hablar/interrumpir
    
    📁 05_realtime_openai_server.py
       - Servidor WebSocket Python
       - Relay entre navegador y OpenAI
       - Manejo de eventos
    
🚀 Cómo usar:

    1. Ejecutar servidor:
       python 05_realtime_openai_server.py
    
    2. Abrir en navegador:
       http://localhost:8000/05_realtime_openai_frontend.html
    
    3. Permitir acceso al micrófono
    
    4. Hacer clic en "Hablar" y conversar
    
    5. Interrumpir en cualquier momento

💡 Características:
    - ✅ Conversación bidireccional
    - ✅ Detección automática de voz (VAD)
    - ✅ Interrupciones naturales
    - ✅ Visualización de forma de onda
    - ✅ Transcripción en tiempo real
    """)


if __name__ == "__main__":
    print("🎙️  OpenAI Realtime API - Audio en Tiempo Real")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  ADVERTENCIA: OPENAI_API_KEY no configurada")
        print("Para usar estos ejemplos necesitas una API key de OpenAI")
        print("https://platform.openai.com/api-keys\n")
    else:
        print("\n✅ API Key configurada\n")
    
    print("Ejemplos disponibles:")
    print("1. Conversación básica (modo texto)")
    print("2. Conversación interactiva multi-turno")
    print("3. Conversación con funciones")
    print("4. Info sobre frontend web\n")
    
    try:
        # Ejecutar ejemplos
        asyncio.run(ejemplo_1_conversacion_basica())
        
        # Preguntar si continuar
        resp = input("\n¿Ejecutar ejemplo interactivo? (s/n): ").lower()
        if resp == 's':
            asyncio.run(ejemplo_2_conversacion_interactiva())
        
        resp = input("\n¿Ejecutar ejemplo con funciones? (s/n): ").lower()
        if resp == 's':
            asyncio.run(ejemplo_3_conversacion_con_funciones())
        
        ejemplo_4_info_frontend()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados")
    print("=" * 60)

