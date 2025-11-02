import os, time, requests, json, urllib.request
from dotenv import load_dotenv
load_dotenv()

OLLAMA = "http://localhost:11434"
LOCAL_MODEL = "gemma:2b"
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def est_tokens(s: str) -> int:
    return max(1, int(len(s) / 4))

def local_completion(prompt: str):
    t0 = time.time()
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": LOCAL_MODEL, "prompt": prompt, "stream": False}, timeout=300)
    r.raise_for_status()
    return r.json()["response"], int((time.time()-t0)*1000), 0.0

def openai_completion(prompt: str):
    if not OPENAI_KEY:
        return "[OPENAI_API_KEY no configurada]", 0, 0.0
    t0 = time.time()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        method="POST",
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type":"application/json"},
        data=json.dumps({"model": OPENAI_MODEL, "messages":[{"role":"user","content":prompt}]}).encode()
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    ms = int((time.time()-t0)*1000)
    # Nota: añade aquí cálculo de coste si quieres
    return data["choices"][0]["message"]["content"], ms, 0.0

def route(prompt: str):
    # Regla tonta de ejemplo: local para prompts cortos/sensibles; cloud para largos
    if est_tokens(prompt) < 200 and ("contraseña" not in prompt.lower()):
        return "local", *local_completion(prompt)
    else:
        return "cloud", *openai_completion(prompt)

if __name__ == "__main__":
    for p in [
        "Resume en 3 viñetas por qué usar modelos locales.",
        "Escribe un plan de pruebas detallado de 1500 palabras para un sistema RAG con métricas."
    ]:
        where, txt, ms, cost = route(p)
        print(f"\n--- [{where.upper()}] ---\nPrompt:\n{p}\n\nRespuesta:\n{txt[:600]}...\nlatencia_ms={ms} coste_est={cost}")
