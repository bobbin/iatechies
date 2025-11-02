from fastapi import FastAPI
from pydantic import BaseModel
import requests, os

OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL  = os.getenv("OLLAMA_MODEL", "gemma:2b")

class Inp(BaseModel):
    prompt: str

app = FastAPI(title="Ollama Microservice")

@app.post("/summarize")
def summarize(inp: Inp):
    r = requests.post(f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": f"Resume en 3 viñetas: {inp.prompt}", "stream": False},
        timeout=300)
    r.raise_for_status()
    return {"model": MODEL, "response": r.json().get("response","").strip()}

# Run: uvicorn 08_microservice_fastapi:app --reload --port 8000
