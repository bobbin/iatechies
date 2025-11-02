import time, csv, requests

OLLAMA = "http://localhost:11434"
MODELS = ["gemma:2b", "llama3.1:8b"]  # ajusta según tu HW
PROMPTS = [
  ("sum-brief", "Resume en 3 viñetas por qué usar modelos locales."),
  ("json-extract", 'Devuelve SOLO JSON con {"ventajas":[], "riesgos":[]}'),
]

with open("results_compare.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["prompt_id","model","latency_ms","tokens_in","tokens_out"])
    for mid, ptxt in PROMPTS:
        for m in MODELS:
            t0 = time.time()
            r = requests.post(f"{OLLAMA}/api/generate",
                json={"model": m, "prompt": ptxt, "stream": False},
                timeout=300)
            r.raise_for_status()
            data = r.json()
            dt = int((time.time() - t0) * 1000)
            w.writerow([mid, m, dt, data.get("prompt_eval_count"), data.get("eval_count")])
            print(mid, m, dt, "ms")
print("OK -> results_compare.csv")
