import requests
OLLAMA = "http://localhost:11434"; MODEL = "gemma:2b"; PROMPT = "Define RAG en 1 frase."

def gen(seed):
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": PROMPT, "options": {"seed": seed}, "stream": False},
        timeout=300)
    r.raise_for_status()
    return r.json()["response"].strip()

a = gen(42); b = gen(42); c = gen(7)
print("seed=42 A:", a)
print("seed=42 B:", b)
print("seed=7  C:", c)
print("A == B ?", a == b)
