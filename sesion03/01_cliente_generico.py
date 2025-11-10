"""
Ejercicio 01 — Sanity check de credenciales cloud.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict

import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from openai import OpenAI

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None  # type: ignore[assignment]


@dataclass
class CheckResult:
    provider: str
    ok: bool
    detail: str

    def format_row(self) -> str:
        status = "✅" if self.ok else "❌"
        return f"{status} {self.provider:<10} {self.detail}"


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def check_openai() -> CheckResult:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini")
    if not api_key:
        return CheckResult("OpenAI", False, "Falta OPENAI_API_KEY")
    try:
        client = OpenAI(api_key=api_key)
        info = client.models.retrieve(model)
        return CheckResult("OpenAI", True, f"Modelo disponible: {info.id}")
    except Exception as exc:  # pragma: no cover - depende de red/credenciales
        return CheckResult("OpenAI", False, f"Error: {exc}")


def check_huggingface() -> CheckResult:
    api_key = os.getenv("HF_API_KEY") or os.getenv("HF_TOKEN")
    if not api_key:
        return CheckResult("HuggingFace", False, "Falta HF_API_KEY")

    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )

        # Modelo soportado por hf-inference
        model = "moonshotai/Kimi-K2-Instruct-0905"

        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Dime un chiste corto sobre datos."}],
            max_tokens=512,
        )

        text = resp.choices[0].message.content.strip()
        preview = text
        return CheckResult("HuggingFace", True, f"Modelo listo: {model} · '{preview}…'")

    except Exception as exc:
        return CheckResult("HuggingFace", False, f"Error: {exc}")



def check_gemini() -> CheckResult:
    if genai is None:
        return CheckResult("Gemini", False, "Instala google-generativeai")

    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-2.5-flash")
    if not api_key:
        return CheckResult("Gemini", False, "Falta GOOGLE_API_KEY")
    try:
        genai.configure(api_key=api_key)
        generative_model = genai.GenerativeModel(model)
        generative_model.count_tokens("ping")
        return CheckResult("Gemini", True, f"Modelo disponible: {model}")
    except Exception as exc:  # pragma: no cover
        return CheckResult("Gemini", False, f"Error: {exc}")


def run_checks() -> Dict[str, CheckResult]:
    checks: Dict[str, Callable[[], CheckResult]] = {
        "openai": check_openai,
        #"huggingface": check_huggingface,
        #"gemini": check_gemini,
    }
    return {name: fn() for name, fn in checks.items()}


if __name__ == "__main__":
    load_env()
    resultados = run_checks()
    print("Sanity check de credenciales cloud:\n")
    for resultado in resultados.values():
        print(resultado.format_row())

    fallos = [r for r in resultados.values() if not r.ok]
    if fallos:
        print("\n⚠️  Revisa las claves o modelos antes de seguir con la sesión.")
    else:
        print("\nTodo listo. Puedes continuar con los ejercicios siguientes.")

