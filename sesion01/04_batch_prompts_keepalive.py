import time, requests

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
prompts = [f"Frase {i} sobre IA en 1 línea." for i in range(1, 11)]

# Carga el modelo y mantenlo caliente 5 min
requests.post(f"{OLLAMA}/api/generate", json={"model": MODEL, "keep_alive": 300})

t0 = time.time()
for p in prompts:
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": p, "stream": False},
        timeout=120)
    r.raise_for_status()
dt = time.time() - t0
print(f"Tiempo total batch: {dt:.2f}s (keep_alive=300)")
