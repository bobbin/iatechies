import requests
OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"

prompt = "[INST] Explica RAG en 1 frase en español. [/INST]"
r = requests.post(f"{OLLAMA}/api/generate",
  json={"model": MODEL, "prompt": prompt, "raw": True, "stream": False},
  timeout=300)
r.raise_for_status()
print(r.json()["response"].strip())
