import base64, json, requests, sys
OLLAMA = "http://localhost:11434"
MODEL = "llava"  # asegúrate de tener un VLM compatible: `ollama pull llava`

path = sys.argv[1] if len(sys.argv) > 1 else "ejemplo.jpg"
img_b64 = base64.b64encode(open(path, "rb").read()).decode("utf-8")

payload = {
  "model": MODEL,
  "prompt": "Describe la imagen y devuelve SOLO un JSON con {objetos:[...], descripcion:\"...\"}.",
  "images": [img_b64],
  "format": "json",
  "stream": False
}
r = requests.post(f"{OLLAMA}/api/generate", json=payload, timeout=300)
r.raise_for_status()
print(json.loads(r.json()["response"]))
