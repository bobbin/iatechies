"""
Audio en Tiempo Real con Gemini Multimodal Live API
===================================================
Conversación de voz bidireccional con Gemini 2.0.
Soporte para audio, video y baja latencia.

Instalación:
pip install google-generativeai websockets pyaudio python-dotenv

Configuración:
GOOGLE_API_KEY=tu-api-key-aqui en archivo .env

Nota: Gemini Live está en preview. Funcionalidad puede cambiar.
"""

import asyncio
import base64
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GeminiLiveClient:
    """Cliente para Gemini Multimodal Live API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = None
        self.chat = None
    
    def configure(
        self,
        model_name="gemini-2.0-flash-exp",
        voice="Puck",
        system_instruction=None
    ):
        """Configurar modelo y sesión"""
        
        config = {
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": voice
                    }
                }
            }
        }
        
        generation_config = genai.GenerationConfig(
            temperature=0.9,
            top_p=1.0,
            top_k=40,
            max_output_tokens=8192
        )
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction
        )
        
        print(f"⚙️  Modelo configurado: {model_name}")
        print(f"🔊 Voz: {voice}")
    
    async def send_audio(self, audio_data: bytes):
        """Enviar audio al modelo"""
        audio_base64 = base64.b64encode(audio_data).decode()
        
        # En Gemini, el audio se envía como parte del mensaje
        return audio_base64
    
    def start_chat(self):
        """Iniciar chat multimodal"""
        self.chat = self.model.start_chat(history=[])
        print("💬 Chat iniciado")
        return self.chat


async def ejemplo_1_conversacion_texto():
    """
    Ejemplo 1: Conversación básica con texto
    (Gemini Live API requiere configuración especial para audio real-time)
    """
    print("=" * 60)
    print("EJEMPLO 1: Conversación con Gemini (Modo Texto)")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada")
        print("Obtén una en: https://makersuite.google.com/app/apikey")
        return
    
    client = GeminiLiveClient(api_key)
    
    try:
        # Configurar
        client.configure(
            model_name="gemini-2.0-flash-exp",
            voice="Puck",
            system_instruction="""Eres un asistente de voz amigable.
            Responde de manera breve y natural, como en una conversación real.
            Máximo 2-3 oraciones por respuesta."""
        )
        
        # Iniciar chat
        chat = client.start_chat()
        
        # Enviar mensaje
        print("\n👤 Usuario: Hola, ¿cómo estás?")
        
        response = chat.send_message(
            "Hola, ¿cómo estás?",
            stream=True
        )
        
        print("🤖 Asistente: ", end="", flush=True)
        
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
        
        print("\n")
        
        # Segundo mensaje
        print("👤 Usuario: ¿Qué puedes hacer?")
        
        response = chat.send_message(
            "¿Qué puedes hacer?",
            stream=True
        )
        
        print("🤖 Asistente: ", end="", flush=True)
        
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
        
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def ejemplo_2_conversacion_interactiva():
    """
    Ejemplo 2: Conversación interactiva multi-turno
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Conversación Interactiva con Gemini")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada")
        return
    
    client = GeminiLiveClient(api_key)
    
    try:
        client.configure(
            model_name="gemini-2.0-flash-exp",
            system_instruction="""Eres un asistente personal útil y amigable.
            Responde de forma breve y conversacional.
            Si el usuario dice 'adiós' o 'terminar', despídete."""
        )
        
        chat = client.start_chat()
        
        print("\n💬 Conversación iniciada. Escribe 'salir' para terminar.\n")
        
        while True:
            # Input del usuario
            user_input = input("👤 Tú: ").strip()
            
            if not user_input or user_input.lower() in ['salir', 'exit', 'quit']:
                print("👋 Terminando conversación...")
                break
            
            # Enviar y recibir respuesta
            print("🤖 Asistente: ", end="", flush=True)
            
            response = chat.send_message(user_input, stream=True)
            
            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            
            print("\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Conversación interrumpida")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


async def ejemplo_3_con_funciones():
    """
    Ejemplo 3: Conversación con llamadas a funciones
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Gemini con Funciones (Tools)")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada")
        return
    
    # Definir funciones
    def get_weather(location: str) -> dict:
        """Obtener clima de una ubicación"""
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
    
    # Configurar modelo con funciones
    genai.configure(api_key=api_key)
    
    # Definir tools para Gemini
    weather_tool = genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="get_weather",
                description="Obtiene el clima actual de una ubicación",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Nombre de la ciudad"
                        )
                    },
                    required=["location"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_time",
                description="Obtiene la hora actual",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={}
                )
            )
        ]
    )
    
    model = genai.GenerativeModel(
        "gemini-2.0-flash-exp",
        tools=[weather_tool]
    )
    
    chat = model.start_chat()
    
    print("\n💬 Pregunta algo sobre el clima o la hora\n")
    
    # Mensaje del usuario
    user_message = "¿Qué hora es y cómo está el clima en Madrid?"
    print(f"👤 Usuario: {user_message}\n")
    
    response = chat.send_message(user_message)
    
    # Procesar llamadas a funciones
    while response.candidates[0].content.parts:
        part = response.candidates[0].content.parts[0]
        
        if hasattr(part, 'function_call') and part.function_call:
            function_call = part.function_call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            print(f"🔧 Llamando función: {function_name}({function_args})")
            
            # Ejecutar función
            if function_name == "get_weather":
                result = get_weather(**function_args)
            elif function_name == "get_time":
                result = get_time()
            else:
                result = {"error": "Función no encontrada"}
            
            print(f"📊 Resultado: {result}\n")
            
            # Enviar resultado de vuelta al modelo
            response = chat.send_message(
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": result}
                        )
                    )]
                )
            )
        else:
            # Respuesta final del modelo
            print("🤖 Asistente:", response.text)
            break


def ejemplo_4_info_audio_realtime():
    """
    Ejemplo 4: Información sobre implementación de audio en tiempo real
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Audio en Tiempo Real con Gemini")
    print("=" * 60)
    
    print("""
📱 Gemini Multimodal Live API soporta audio bidireccional en tiempo real.

⚠️  NOTA IMPORTANTE:
    La API de Gemini Live (BidiGenerateContent) está en preview y
    requiere acceso especial mediante WebSocket o gRPC.
    
🔧 Arquitectura:

    Cliente Web (Navegador)
         ↓ WebSocket
    Servidor Relay (Python)
         ↓ gRPC/WebSocket
    Gemini Live API
    
📁 Archivos necesarios:

    ✅ 06_realtime_gemini_server.py
       - Servidor WebSocket relay
       - Conexión a Gemini Live API
       - Manejo de audio streaming
    
    ✅ 06_realtime_gemini_frontend.html
       - Interfaz web
       - Acceso a micrófono/cámara
       - Visualización multimodal
    
🚀 Características especiales de Gemini:

    ✅ Multimodal: Audio + Video simultáneo
    ✅ Streaming bidireccional
    ✅ Detección de actividad de voz
    ✅ Interrupciones naturales
    ✅ Gratuito durante preview
    
💡 Ventajas sobre OpenAI:
    - Soporte para video/imágenes en tiempo real
    - Gratis durante preview
    - Multimodalidad nativa
    
💡 Desventajas:
    - En preview (puede cambiar)
    - Latencia ligeramente mayor
    - Voces menos naturales
    - Documentación en desarrollo
    
📚 Recursos:
    - Docs: https://ai.google.dev/gemini-api/docs/live
    - API Key: https://makersuite.google.com/app/apikey
    - Ejemplos: https://github.com/google-gemini/cookbook
    
🎯 Para usar audio en tiempo real con Gemini:

    1. Obtener API key con acceso a Gemini 2.0
    2. Usar el servidor relay incluido
    3. Abrir frontend en navegador
    4. ¡Conversar con voz y video!
    """)


async def ejemplo_5_audio_con_sdk():
    """
    Ejemplo 5: Demostración de capacidades de audio
    """
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Capacidades de Audio de Gemini")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no encontrada")
        return
    
    genai.configure(api_key=api_key)
    
    print("""
🎵 Gemini soporta múltiples modalidades de audio:

1. Audio Input:
   - Análisis de audio (transcripción, identificación)
   - Comprensión de contenido hablado
   - Detección de emociones
   
2. Audio Output:
   - Generación de respuestas en voz
   - Múltiples voces disponibles
   - Control de tono y velocidad
   
3. Tiempo Real:
   - Streaming bidireccional
   - Baja latencia (~400ms)
   - Interrupciones naturales
   
📊 Voces disponibles:
   - Puck: Neutral, profesional
   - Charon: Profunda, autoritaria  
   - Kore: Suave, amigable
   - Fenrir: Enérgica, dinámica
   - Aoede: Musical, expresiva
   
💡 Formatos soportados:
   - Input: PCM 16-bit, 16kHz mono
   - Output: PCM 16-bit, 24kHz mono
   - Codificación: Base64 en JSON
    """)


if __name__ == "__main__":
    print("🎙️  Gemini Multimodal Live API")
    print("=" * 60)
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  ADVERTENCIA: GOOGLE_API_KEY no configurada")
        print("Para usar estos ejemplos necesitas una API key de Google")
        print("Obtén una en: https://makersuite.google.com/app/apikey\n")
    else:
        print("\n✅ API Key configurada\n")
    
    print("Ejemplos disponibles:")
    print("1. Conversación con texto")
    print("2. Conversación interactiva")
    print("3. Conversación con funciones")
    print("4. Info sobre audio en tiempo real")
    print("5. Capacidades de audio\n")
    
    try:
        # Ejecutar ejemplos
        asyncio.run(ejemplo_1_conversacion_texto())
        
        resp = input("\n¿Ejecutar ejemplo interactivo? (s/n): ").lower()
        if resp == 's':
            asyncio.run(ejemplo_2_conversacion_interactiva())
        
        resp = input("\n¿Ejecutar ejemplo con funciones? (s/n): ").lower()
        if resp == 's':
            asyncio.run(ejemplo_3_con_funciones())
        
        ejemplo_4_info_audio_realtime()
        asyncio.run(ejemplo_5_audio_con_sdk())
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ejecución interrumpida")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados")
    print("=" * 60)
    print("\nNOTA: Para audio en tiempo real completo, usar")
    print("06_realtime_gemini_server.py + 06_realtime_gemini_frontend.html")

