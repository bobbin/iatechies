import os
import sys
from typing import Iterable
import requests


def build_generate_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/generate"):
        return base
    if base.endswith("/v1"):
        return f"{base}/generate"
    if base.endswith("/api"):
        return f"{base}/generate"
    return f"{base}/api/generate"


def build_models_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/models"):
        return base
    if base.endswith("/v1"):
        return f"{base}/models"
    if base.endswith("/api"):
        return f"{base}/tags"
    return f"{base}/api/tags"


def extract_model_names(payload: dict) -> Iterable[str]:
    if "models" in payload:
        for item in payload["models"]:
            name = item.get("name") or item.get("model")
            if name:
                yield name
    elif "data" in payload:
        for item in payload["data"]:
            name = item.get("name") or item.get("id") or item.get("model")
            if name:
                yield name


if __name__ == "__main__":
    base_url = os.getenv("OLLAMA_BASE_URL", "https://api.ollama.com/v1")
    api_key = os.getenv("OLLAMA_API_KEY")
    headers = {}

    if base_url.startswith("https://"):
        if not api_key:
            sys.exit("Configura OLLAMA_API_KEY con tu token de Ollama Cloud.")
        headers["Authorization"] = f"Bearer {api_key}"

    # Paso 1: listar modelos disponibles (limitamos la salida para brevedad)
    models_url = build_models_url(base_url)
    response = requests.get(models_url, headers=headers, timeout=60)
    response.raise_for_status()
    available = list(extract_model_names(response.json()))

    if not available:
        sys.exit("No se encontraron modelos disponibles; revisa tus credenciales o el endpoint.")

    print("Modelos disponibles (primeros 5):")
    for name in available[:5]:
        print(" -", name)

    chosen_models = available[:2]
    prompt = "Enumera tres beneficios de documentar tus prompts con ejemplos concretos."

    generate_url = build_generate_url(base_url)
    for model in chosen_models:
        payload = {"model": model, "prompt": prompt, "stream": False}
        resp = requests.post(generate_url, json=payload, headers=headers, timeout=300)
        resp.raise_for_status()
        text = resp.json().get("response", "").strip()
        print(f"\n[{model}]\n{text}\n")
