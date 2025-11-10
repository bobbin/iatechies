"""
Ejercicio 18 — Benchmark multi-backend contra el microservicio `/chat`.
"""

from __future__ import annotations

import csv
import statistics
import time
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import requests

BASE_URL = "http://localhost:8001/chat"
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
RESULTS_PATH = LOG_DIR / "benchmark_results.csv"


def llamar_backend(backend: str, prompt: str, temperature: float = 0.2) -> Dict:
    inicio = time.perf_counter()
    respuesta = requests.post(
        BASE_URL,
        json={
            "backend": backend,
            "prompt": prompt,
            "temperature": temperature,
        },
        timeout=120,
    )
    duracion_ms = (time.perf_counter() - inicio) * 1000
    respuesta.raise_for_status()
    data = respuesta.json()
    data.setdefault("latency_ms", duracion_ms)
    data.setdefault("metadata", {})
    return data


def percentil(valores: List[float], p: float) -> float:
    if not valores:
        return 0.0
    return float(np.percentile(valores, p))


def benchmark_backend(backend: str, prompts: Iterable[str]) -> Dict[str, float]:
    latencias = []
    tokens_prompt = []
    tokens_completion = []

    for prompt in prompts:
        data = llamar_backend(backend, prompt)
        latencias.append(float(data.get("latency_ms", 0)))
        meta = data.get("metadata") or {}
        if meta.get("prompt_tokens"):
            tokens_prompt.append(int(meta["prompt_tokens"]))
        if meta.get("completion_tokens"):
            tokens_completion.append(int(meta["completion_tokens"]))

    return {
        "backend": backend,
        "n_samples": len(latencias),
        "latencia_media_ms": statistics.mean(latencias) if latencias else 0.0,
        "latencia_p50_ms": percentil(latencias, 50),
        "latencia_p95_ms": percentil(latencias, 95),
        "tokens_prompt_medios": statistics.mean(tokens_prompt) if tokens_prompt else 0.0,
        "tokens_completion_medios": statistics.mean(tokens_completion) if tokens_completion else 0.0,
    }


def guardar_resultados(filas: List[Dict[str, float]]) -> None:
    campos = [
        "timestamp",
        "backend",
        "n_samples",
        "latencia_media_ms",
        "latencia_p50_ms",
        "latencia_p95_ms",
        "tokens_prompt_medios",
        "tokens_completion_medios",
    ]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    write_header = not RESULTS_PATH.exists()
    with RESULTS_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if write_header:
            writer.writeheader()
        for fila in filas:
            fila = {"timestamp": timestamp, **fila}
            writer.writerow(fila)


def main() -> None:
    prompts = [
        "Resume en dos frases la última rueda de prensa sobre economía.",
        "Reescribe este titular para hacerlo más atractivo: 'El ayuntamiento aprueba el nuevo plan de movilidad'.",
        "Genera un subtítulo para una crónica deportiva de la final de la Champions.",
        "Explica en tono divulgativo qué es el Reglamento de IA de la UE en 4 frases.",
        "Proporciona tres ideas de titulares para una newsletter tecnológica semanal.",
    ]

    backends = ["openai", "hf", "google"]
    resultados = []
    for backend in backends:
        print(f"Benchmarking backend: {backend}")
        resumen = benchmark_backend(backend, prompts)
        resultados.append(resumen)
        print(f" - Latencia media: {resumen['latencia_media_ms']:.0f} ms · P95: {resumen['latencia_p95_ms']:.0f} ms")

    guardar_resultados(resultados)
    print(f"\nResultados guardados en {RESULTS_PATH}")


if __name__ == "__main__":
    main()

