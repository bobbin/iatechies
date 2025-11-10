"""
Ejercicio 03 — Cargar configuración desde variables de entorno.

Proporciona `get_config()` para centralizar claves y modelos por proveedor.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    openai_api_key: str
    hf_api_key: str
    google_api_key: str
    default_model_openai: str
    default_model_hf: str
    default_model_google: str
    default_model_embeddings_openai: str
    default_model_embeddings_hf: str


def load_env() -> None:
    """
    Carga `.env` automáticamente si existe en la carpeta actual o superior.
    """
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Permite cargar valores desde un .env global en el proyecto
        load_dotenv()


def get_config() -> Config:
    """
    Devuelve la configuración consolidada para todos los backends.

    Levanta `ValueError` si falta alguna de las claves mínimas.
    """
    load_env()

    data = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "hf_api_key": os.getenv("HF_API_KEY", ""),
        "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
        "default_model_openai": os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o-mini"),
        "default_model_hf": os.getenv(
            "DEFAULT_MODEL_HF",
            "mistralai/Mistral-7B-Instruct-v0.2",
        ),
        "default_model_google": os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro"),
        "default_model_embeddings_openai": os.getenv(
            "DEFAULT_MODEL_EMBEDDINGS_OPENAI",
            "text-embedding-3-small",
        ),
        "default_model_embeddings_hf": os.getenv(
            "DEFAULT_MODEL_EMBEDDINGS_HF",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
    }

    missing = [field for field, value in data.items() if not value]
    if missing:
        raise ValueError(
            "Faltan variables obligatorias en .env: "
            + ", ".join(missing),
        )

    return Config(**data)


def as_dict(config: Config) -> Dict[str, str]:
    """Convierte la dataclass en dict (útil para serializar o imprimir)."""

    return {
        "openai_api_key": config.openai_api_key[:6] + "...",
        "hf_api_key": config.hf_api_key[:6] + "...",
        "google_api_key": config.google_api_key[:6] + "...",
        "default_model_openai": config.default_model_openai,
        "default_model_hf": config.default_model_hf,
        "default_model_google": config.default_model_google,
        "default_model_embeddings_openai": config.default_model_embeddings_openai,
        "default_model_embeddings_hf": config.default_model_embeddings_hf,
    }


if __name__ == "__main__":
    try:
        cfg = get_config()
        print("✅ Configuración cargada:")
        for key, value in as_dict(cfg).items():
            print(f" - {key}: {value}")
    except ValueError as exc:
        print("⚠️  Error de configuración:", exc)
        print("💡 Copia sesion03/env.example a sesion03/.env y completa tus claves.")

