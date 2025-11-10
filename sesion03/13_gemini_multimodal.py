"""
Ejercicio 13 — Multimodal con Gemini: texto + imagen para alt text y pie de foto.
"""

from __future__ import annotations

import base64
import os
from io import BytesIO
from pathlib import Path
from typing import Tuple

import google.generativeai as genai
import requests
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def _descargar_imagen(url: str) -> Tuple[str, bytes]:
    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()
    content_type = respuesta.headers.get("Content-Type", "image/jpeg")
    return content_type, respuesta.content


def generar_alt_text_y_caption(descripcion: str, url_imagen: str) -> str:
    load_env()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Configura GOOGLE_API_KEY.")

    contenido = []
    if descripcion:
        contenido.append(
            (
                "Eres un editor digital. Usa la descripción de portada y la imagen para "
                "crear (1) un alt text accesible y (2) un pie de foto breve pero informativo."
            )
        )
        contenido.append(f"Descripción de portada: {descripcion}")

    content_type, datos = _descargar_imagen(url_imagen)
    image_part = {
        "mime_type": content_type,
        "data": base64.b64encode(datos).decode("utf-8"),
    }

    genai.configure(api_key=api_key)
    model_name = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-1.5-pro")
    modelo = genai.GenerativeModel(model_name)

    respuesta = modelo.generate_content(
        [
            *contenido,
            {
                "mime_type": image_part["mime_type"],
                "data": image_part["data"],
            },
            (
                "Devuelve la respuesta en JSON con dos claves: "
                "`alt_text` (máximo 120 caracteres) y `pie_foto` (máximo 180 caracteres)."
            ),
        ],
        request_options={"timeout": 60},
    )
    return respuesta.text.strip()


if __name__ == "__main__":
    descripcion_portada = "Cristiano Ronaldo compra una nueva casa en Madrid."
    url_demo = "https://images.unsplash.com/photo-1505843513577-22bb7d21e455"

    resultado = generar_alt_text_y_caption(descripcion_portada, url_demo)
    print(resultado)

