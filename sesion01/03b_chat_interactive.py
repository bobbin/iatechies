import requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
context = None

def turn(user_msg, context):
    """Envía un mensaje a Ollama y devuelve respuesta + contexto actualizado"""
    payload = {"model": MODEL, "prompt": user_msg, "stream": False}
    if context: 
        payload["context"] = context
    r = requests.post(f"{OLLAMA}/api/generate", json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["response"].strip(), data.get("context")

# Chat interactivo
print("🤖 Chat iniciado. Escribe 'salir', 'exit' o 'quit' para terminar.\n")

while True:
    try:
        user_msg = input("Tú: ")
        
        # Comandos de salida
        if user_msg.lower() in ['salir', 'exit', 'quit']:
            print("¡Hasta luego! 👋")
            break
        
        # Mensaje vacío
        if not user_msg.strip():
            continue
        
        # Enviar mensaje y recibir respuesta
        resp, context = turn(user_msg, context)
        print(f"🤖: {resp}\n")
        
    except KeyboardInterrupt:
        print("\n¡Hasta luego! 👋")
        break
    except Exception as e:
        print(f"❌ Error: {e}\n")

