import json, requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"

schema = {
  "type": "object",
  "properties": {
    "empresa": {"type": "string"},
    "fecha": {"type": "string"},
    "total": {"type": "number"}
  },
  "required": ["empresa", "total"]
}

prompt = (
 "Texto: 'Factura ACME S.A. fechada el 2025-10-01, total 199.99 EUR.'\n"
 "Devuelve SOLO el JSON requerido."
)

r = requests.post(f"{OLLAMA}/api/generate", json={
  "model": MODEL, "prompt": prompt, "format": schema, "stream": False
}, timeout=300)
r.raise_for_status()
data = json.loads(r.json()["response"])
print(data)
