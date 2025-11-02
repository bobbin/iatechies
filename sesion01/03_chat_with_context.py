import requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
context = None

def turn(user_msg, context):
    payload = {"model": MODEL, "prompt": user_msg, "stream": False}
    if context: payload["context"] = context
    r = requests.post(f"{OLLAMA}/api/generate", json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["response"].strip(), data.get("context")

resp, context = turn("Te llamas Ada. Responde en 1 frase.", None)
print("Asistente:", resp)

resp, context = turn("¿Cómo te llamas? Responde solo con el nombre.", context)
print("Asistente:", resp)

resp, context = turn("En 5 palabras, ¿qué haremos hoy?", context)
print("Asistente:", resp)
