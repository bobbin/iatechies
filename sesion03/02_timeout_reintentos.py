"""
Ejercicio 02 — Primeras llamadas HTTP a OpenAI y Hugging Face.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Dict, Tuple

import requests
from dotenv import load_dotenv
from openai import OpenAI

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def call_openai(prompt: str, model: str) -> Tuple[str, float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no configurado.")

    payload: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Eres un asistente directo y claro."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    inicio = time.perf_counter()
    response = requests.post(
        OPENAI_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    duracion_ms = (time.perf_counter() - inicio) * 1000
    response.raise_for_status()
    data = response.json()
    contenido = data["choices"][0]["message"]["content"].strip()
    return contenido, duracion_ms


def call_huggingface(prompt: str, model: str) -> Tuple[str, float]:
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_API_KEY no configurado.")

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key,
    )

    inicio = time.perf_counter()
    respuesta = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente útil que responde en español neutro."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=256,
        temperature=0.3,
    )
    duracion_ms = (time.perf_counter() - inicio) * 1000
    texto = respuesta.choices[0].message.content.strip()
    return texto, duracion_ms


if __name__ == "__main__":
    load_env()
    prompt_demo = "Resume en dos frases por qué es importante cubrir IA en una redacción."

    modelo_openai = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    modelo_hf = os.getenv(
        "DEFAULT_MODEL_HF",
        "moonshotai/Kimi-K2-Instruct-0905",
    )

    print("→ Llamada HTTP a OpenAI:")
    try:
        respuesta_openai, latencia_openai = call_openai(prompt_demo, modelo_openai)
        print(f"   Latencia: {latencia_openai:.0f} ms")
        print(f"   Respuesta:\n{respuesta_openai}\n")
    except Exception as exc:
        print(f"   Error: {exc}\n")

    print("→ Llamada HTTP a Hugging Face:")
    try:
        respuesta_hf, latencia_hf = call_huggingface(prompt_demo, modelo_hf)
        print(f"   Latencia: {latencia_hf:.0f} ms")
        print(f"   Respuesta:\n{respuesta_hf}")
    except Exception as exc:
        print(f"   Error: {exc}")
