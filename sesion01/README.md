# Ollama Labs — Ejercicios por script

Colección de ejercicios prácticos para dominar Ollama desde cero.

## Requisitos

- Python 3.10+
- Ollama corriendo en local (http://localhost:11434)
- Instala dependencias:
  ```bash
  pip install -r requirements.txt
  ```

Scripts

01_compare_models.py — Compara modelos y guarda CSV (latencia, tokens).

02_modelfile/Modelfile — Crea un “modo” con salida JSON estable.

03_chat_with_context.py — Chat multi-turno usando context.

04_batch_prompts_keepalive.py — Batching con keep_alive.

05_structured_extract.py — Outputs estructurados con JSON Schema.

06_vision_analyze.py — Visión: imagen Base64 → análisis (modelo VLM).

07_raw_mode_demo.py — Modo raw: control de plantilla.

08_microservice_fastapi.py — Microservicio HTTP que encapsula Ollama.

09_stress_context.py — Stress test de contexto.

10_reproducible_seed.py — Reproducibilidad con seed.

11_hybrid_router_local_cloud.py — Router local/cloud (opcional, requiere OPENAI_API_KEY).

Notas rápidas

En Windows: pip install requests si te da error de módulo.

Cambia los nombres de modelo según tu hardware (p. ej., gemma:2b, llama3.1:8b, mistral:7b).

Para visión, instala un VLM (p. ej., ollama pull llava).


---
