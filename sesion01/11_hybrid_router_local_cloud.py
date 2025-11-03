import time, requests

OLLAMA = "http://localhost:11434"
LOCAL_MODEL = "gemma:2b"
CLOUD_MODEL = "gpt-oss:20b-cloud"

def est_tokens(s: str) -> int:
    return max(1, int(len(s) / 4))

def local_completion(prompt: str):
    t0 = time.time()
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": LOCAL_MODEL, "prompt": prompt, "stream": False}, timeout=300)
    r.raise_for_status()
    return r.json()["response"], int((time.time()-t0)*1000), 0.0

def cloud_completion(prompt: str):
    t0 = time.time()
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": CLOUD_MODEL, "prompt": prompt, "stream": False}, timeout=300)
    r.raise_for_status()
    ms = int((time.time()-t0)*1000)
    return r.json()["response"], ms, 0.0

def route(prompt: str):
    # Regla simple: local para prompts cortos; cloud para largos
    tokens = est_tokens(prompt)
    if tokens < 50:
        return "local", *local_completion(prompt)
    else:
        return "cloud", *cloud_completion(prompt)

if __name__ == "__main__":
    import sys
    prompts = [
        "Resume en 3 viñetas por qué usar modelos locales.",
        "Escribe un plan de pruebas detallado y exhaustivo para un sistema RAG (Retrieval-Augmented Generation) con métricas completas. Incluye secciones sobre: 1) Objetivos y alcance del proyecto, 2) Casos de prueba funcionales detallados, 3) Pruebas de rendimiento y carga, 4) Pruebas de integración entre componentes, 5) Métricas y KPIs específicos, 6) Estrategia de datos de prueba, 7) Ambiente de testing y configuración, 8) Cronograma detallado y recursos necesarios, 9) Proceso de reporting y documentación."
    ]
    for i, p in enumerate(prompts, 1):
        tokens = est_tokens(p)
        where, txt, ms, cost = route(p)
        print(f"\n--- [{where.upper()}] ---")
        print(f"Tokens estimados: {tokens}")
        print(f"Prompt {i}: {p[:60]}...")
        try:
            print(f"\nRespuesta: {txt[:300]}...")
        except UnicodeEncodeError:
            print(f"\nRespuesta: {txt[:300].encode('ascii', errors='replace').decode()}...")
        print(f"Latencia: {ms}ms, Costo: {cost}")
