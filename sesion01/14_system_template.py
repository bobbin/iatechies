import os
import textwrap
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


if __name__ == "__main__":
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "mistral:7b")
    headers = {}
    api_key = os.getenv("OLLAMA_API_KEY")
    if base_url.startswith("https://"):
        if not api_key:
            raise SystemExit("Define OLLAMA_API_KEY para autenticación en Ollama Cloud.")
        headers["Authorization"] = f"Bearer {api_key}"

    system_prompt = (
        "Eres una productora de contenidos educativos."
        " Responde siempre en español neutro y termina con una llamada a la acción."
    )

    template = textwrap.dedent(
        """
        {{- if .System }}
        [sistema]
        {{ .System }}
        [/sistema]
        {{- end }}
        [usuario]
        {{ .Prompt }}
        [/usuario]
        [asistente]
        """
    ).strip()

    payload = {
        "model": model,
        "system": system_prompt,
        "template": template,
        "prompt": "Explica qué es el aprendizaje por refuerzo en 3 frases.",
        "stream": False,
    }

    response = requests.post(build_generate_url(base_url), json=payload, headers=headers, timeout=300)
    response.raise_for_status()
    data = response.json()
    print(data.get("response", "").strip())
