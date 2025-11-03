import requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
messages = []

def turn(user_msg, messages):
    """Envía un mensaje a Ollama usando /api/chat y devuelve respuesta + historial actualizado"""
    local_messages = messages + [{"role": "user", "content": user_msg}]
    payload = {
        "model": MODEL,
        "messages": local_messages,
        "stream": False,
    }
    r = requests.post(f"{OLLAMA}/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    assistant_content = data["message"]["content"].strip()
    local_messages.append({"role": "assistant", "content": assistant_content})
    return assistant_content, local_messages

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
        resp, messages = turn(user_msg, messages)
        print(f"🤖: {resp}\n")
        
    except KeyboardInterrupt:
        print("\n¡Hasta luego! 👋")
        break
    except Exception as e:
        print(f"❌ Error: {e}\n")
