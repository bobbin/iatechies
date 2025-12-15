from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Carga sesion10/.env si existe (sin sobrescribir variables ya definidas)."""
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)


def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Configura {var_name} en tu .env o como variable de entorno.")
    return value


def guess_mime_type(image_path: str | Path) -> str:
    mime, _ = mimetypes.guess_type(str(image_path))
    return mime or "image/jpeg"


def read_image_bytes(image_path: str | Path) -> bytes:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {path}")
    return path.read_bytes()


def to_data_url(image_path: str | Path) -> str:
    mime = guess_mime_type(image_path)
    b64 = base64.b64encode(read_image_bytes(image_path)).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def to_gemini_part(image_path: str | Path) -> dict:
    mime = guess_mime_type(image_path)
    b64 = base64.b64encode(read_image_bytes(image_path)).decode("utf-8")
    return {"mime_type": mime, "data": b64}


def default_image_path(filename: str = "ejemplo.jpg") -> str:
    """
    Ruta por defecto para demos.
    Prioridad:
    - `sesion10/inputs/<filename>` si existe
    - `sesion01/ejemplo.jpg` (imagen de ejemplo del repo)
    """
    here = Path(__file__).resolve().parent
    candidate = here / "inputs" / filename
    if candidate.exists():
        return str(candidate)
    return str(here.parent / "sesion01" / "ejemplo.jpg")


