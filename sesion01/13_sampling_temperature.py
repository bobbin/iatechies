import os
import requests
from time import perf_counter
from typing import List


def build_generate_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/generate"):
        return base
    if base.endswith("/v1"):
        return f"{base}/generate"
    if base.endswith("/api"):
        return f"{base}/generate"
    return f"{base}/api/generate"


def run_completion(model: str, prompt: str, temperature: float, url: str, headers: dict) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    t0 = perf_counter()
    response = requests.post(url, json=payload, headers=headers, timeout=300)
    latency = perf_counter() - t0
    response.raise_for_status()
    data = response.json()
    text = data.get("response", "").strip()
    return f"T={temperature:.1f} ({latency*1000:.0f} ms) -> {text}"


if __name__ == "__main__":
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "mistral:7b")
    prompt = "Genera un eslogan creativo para un café que solo abre de noche."
    temperatures: List[float] = [0.0, 0.4, 0.8, 1.2]

    headers = {}
    api_key = os.getenv("OLLAMA_API_KEY")
    if base_url.startswith("https://"):
        if not api_key:
            raise SystemExit("Configura OLLAMA_API_KEY para usar Ollama Cloud.")
        headers["Authorization"] = f"Bearer {api_key}"

    url = build_generate_url(base_url)
    for temp in temperatures:
        print(run_completion(model, prompt, temp, url, headers))
