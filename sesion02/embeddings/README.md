# Embeddings — Ejercicios

Usan el endpoint `/api/embed` de Ollama mediante `ollama_embed.py`.

Modelo por defecto: `nomic-embed-text` (cámbialo con `OLLAMA_EMBED_MODEL`).

## Instalación

```bash
pip install -r ../requirements.txt
```

## Scripts

- `01_inspector_basico.py`: inspección de vectores y similitud coseno
- `02_busqueda_titulares.py`: mini-buscador semántico en memoria
- `03_multilingue.py`: prueba de cross-lingua
- `04_deduplicador.py`: near-duplicate detector
- `05_tags_inteligentes.py`: asignación de secciones mediante embeddings

## Variables de entorno

- `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- `OLLAMA_EMBED_MODEL` (default `nomic-embed-text`)
