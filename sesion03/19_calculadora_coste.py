"""
Ejercicio 19 — Calculadora de coste mensual por feature.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

LOG_DIR = Path(__file__).resolve().parent / "logs"
BENCHMARK_FILE = LOG_DIR / "benchmark_results.csv"
METRICS_FILE = LOG_DIR / "metrics.csv"

# Coste aproximado por 1.000 tokens (USD). Ajusta con tus cifras reales.
PRECIOS_POR_1K_TOKENS = {
    "openai": 0.005,  # ej. gpt-4o-mini
    "hf": 0.002,  # depende del modelo OSS elegido en HF
    "google": 0.007,  # ej. gemini 1.5 pro
    "ollama": 0.0005,  # coste marginal (electricidad/infra)
}


@dataclass
class Metrics:
    backend: str
    tokens_prompt_medios: float
    tokens_completion_medios: float

    @property
    def tokens_totales(self) -> float:
        return self.tokens_prompt_medios + self.tokens_completion_medios


def cargar_desde_benchmark() -> Dict[str, Metrics]:
    if not BENCHMARK_FILE.exists():
        return {}
    resultados: Dict[str, Metrics] = {}
    with BENCHMARK_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            backend = row["backend"]
            resultados[backend] = Metrics(
                backend=backend,
                tokens_prompt_medios=float(row.get("tokens_prompt_medios", 0.0)),
                tokens_completion_medios=float(row.get("tokens_completion_medios", 0.0)),
            )
    return resultados


def cargar_desde_metrics() -> Dict[str, Metrics]:
    if not METRICS_FILE.exists():
        return {}
    acumulado: Dict[str, Dict[str, float]] = {}
    with METRICS_FILE.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            backend = row.get("backend", "desconocido")
            if backend not in acumulado:
                acumulado[backend] = {
                    "prompt": 0.0,
                    "completion": 0.0,
                    "count": 0,
                }
            try:
                prompt_tokens = float(row.get("tokens_prompt") or 0)
                completion_tokens = float(row.get("tokens_completion") or 0)
            except ValueError:
                prompt_tokens = completion_tokens = 0.0
            acumulado[backend]["prompt"] += prompt_tokens
            acumulado[backend]["completion"] += completion_tokens
            acumulado[backend]["count"] += 1

    resultados: Dict[str, Metrics] = {}
    for backend, valores in acumulado.items():
        if valores["count"] == 0:
            continue
        resultados[backend] = Metrics(
            backend=backend,
            tokens_prompt_medios=valores["prompt"] / valores["count"],
            tokens_completion_medios=valores["completion"] / valores["count"],
        )
    return resultados


def cargar_metricas() -> Dict[str, Metrics]:
    datos = cargar_desde_benchmark()
    if datos:
        return datos
    return cargar_desde_metrics()


def estimar_coste(
    metrics: Metrics,
    peticiones_diarias: int,
    precio_por_1k_tokens: float,
) -> float:
    tokens_por_peticion = metrics.tokens_totales or 0.0
    tokens_mensuales = tokens_por_peticion * peticiones_diarias * 30
    return (tokens_mensuales / 1000.0) * precio_por_1k_tokens


def main() -> None:
    metricas = cargar_metricas()
    if not metricas:
        print("No se encontraron métricas. Ejecuta primero los ejercicios 17 u 18.")
        return

    try:
        peticiones_diarias = int(
            input("Introduce el nº de peticiones diarias estimadas para la feature: ")
        )
    except ValueError:
        print("Valor no válido. Debe ser un número entero.")
        return

    print("\n=== Estimación de costes mensuales ===")
    for backend, met in metricas.items():
        precio = PRECIOS_POR_1K_TOKENS.get(backend)
        if precio is None:
            print(f"- {backend}: sin precio definido, añade tu tarifa en PRECIOS_POR_1K_TOKENS")
            continue
        coste = estimar_coste(met, peticiones_diarias, precio)
        print(
            f"- {backend:7s} → tokens medios/petición: {met.tokens_totales:.0f} · "
            f"Coste aproximado: ${coste:,.2f}/mes"
        )

    print("\nRecuerda ajustar PRECIOS_POR_1K_TOKENS con tus tarifas reales.")


if __name__ == "__main__":
    main()

