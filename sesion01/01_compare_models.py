import time, csv, requests

OLLAMA = "http://localhost:11434"
MODELS = ["gemma3:4b", "gpt-oss:20b-cloud"]  # ajusta según tu HW
PROMPTS = [
  ("sum-brief", "Resume en 3 viñetas por qué usar modelos locales."),
  ("json-extract", '''Texto: "La empresa TechCorp está migrando a modelos de IA local para procesar datos médicos. Esto les permitirá cumplir con GDPR, pero requerirá inversión en hardware."
Extrae las ventajas y riesgos en formato JSON: {"ventajas":[], "riesgos":[]}.'''),
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
            print(f"\n{mid} | {m} | {dt} ms")
            print("Respuesta:", data.get("response", "").strip())
            print("-" * 80)
print("OK -> results_compare.csv")
