import requests

OLLAMA = "http://localhost:11434"

def list_models():
    """Lista todos los modelos disponibles en Ollama (locales y remotos)"""
    response = requests.get(f"{OLLAMA}/api/tags", timeout=60)
    response.raise_for_status()
    
    models = []
    for item in response.json().get("models", []):
        model_name = item.get("name", "")
        if model_name:
            # Detectar si es un modelo remoto (cloud)
            is_remote = bool(item.get("remote_model") or item.get("remote_host"))
            models.append({
                "name": model_name,
                "size": item.get("size", 0),
                "is_remote": is_remote
            })
    return models

def generate_with_model(model_name, prompt):
    """Genera texto con un modelo específico"""
    response = requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": model_name, "prompt": prompt, "stream": False},
        timeout=300
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()

if __name__ == "__main__":
    print("Listando modelos CLOUD disponibles en Ollama...")
    print("="*60)
    
    all_models = list_models()
    cloud_models = [m for m in all_models if m["is_remote"]]
    
    if not cloud_models:
        print("No se encontraron modelos cloud instalados.")
        print("Instala uno con: ollama pull gpt-oss:20b-cloud")
    else:
        print(f"\nTotal de modelos CLOUD: {len(cloud_models)}\n")
        print("Modelos CLOUD disponibles:")
        for m in cloud_models:
            print(f"  - {m['name']}")
        
        # Probar con el primer modelo cloud
        print("\n" + "="*60)
        prompt = "Enumera tres beneficios de documentar tus prompts."
        
        for m in cloud_models[:1]:
            print(f"\nGenerando con: {m['name']}")
            try:
                result = generate_with_model(m["name"], prompt)
                print(f"Respuesta: {result[:200]}...")
            except Exception as e:
                print(f"Error: {e}")
