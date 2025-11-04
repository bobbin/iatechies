import json
import os
import requests
import sys
from typing import Iterator


def build_generate_url(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/generate"):
        return base
    if base.endswith("/v1"):
        return f"{base}/generate"
    if base.endswith("/api"):
        return f"{base}/generate"
    return f"{base}/api/generate"


def stream_chunks(response: requests.Response) -> Iterator[dict]:
    for line in response.iter_lines(decode_unicode=True):
        if not line:
            continue
        yield json.loads(line)


if __name__ == "__main__":
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "gemma:2b")
    prompt = "Resume en 5 viñetas lo nuevo de Python 3.13."

    headers = {}
    api_key = os.getenv("OLLAMA_API_KEY")
    if base_url.startswith("https://"):
        if not api_key:
            sys.exit("Falta OLLAMA_API_KEY para autenticarse contra Ollama Cloud.")
        headers["Authorization"] = f"Bearer {api_key}"

    print(f"Streaming con {model} ({base_url})\n---\n", flush=True)

    with requests.post(
        build_generate_url(base_url),
        json={"model": model, "prompt": prompt, "stream": True},
        headers=headers,
        stream=True,
        timeout=300,
    ) as resp:
        resp.raise_for_status()
        token_count = 0
        for chunk in stream_chunks(resp):
            if chunk.get("done"):
                token_count = chunk.get("total_tokens", token_count)
                break
            piece = chunk.get("response", "")
            if piece:
                print(piece, end="", flush=True)
        print("\n---\n")
        if token_count:
            print(f"Tokens totales generados: {token_count}")
