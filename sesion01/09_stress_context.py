import requests
OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"

big = "Lorem ipsum " * 1000  # aumenta para probar límites
prompt = f"Lee el siguiente texto y cuenta sus palabras en 1 frase:\n{big}"

r = requests.post(f"{OLLAMA}/api/generate",
  json={"model": MODEL, "prompt": prompt, "stream": False, "options":{"num_predict":256}},
  timeout=600)
r.raise_for_status()
data = r.json()
print(data["response"].strip())
print("tokens_in:", data.get("prompt_eval_count"), "tokens_out:", data.get("eval_count"))
