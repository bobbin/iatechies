import requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma-json"  # Modelo personalizado con Modelfile

prompt = "Datos de un producto: precio alto, calidad excelente, diseño elegante pero mantenimiento costoso."
r = requests.post(f"{OLLAMA}/api/generate",
    json={"model": MODEL, "prompt": prompt, "stream": False},
    timeout=300)
r.raise_for_status()
data = r.json()
print("Respuesta:")
print(data.get("response", "").strip())

