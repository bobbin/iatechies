"""
Ejercicio 11: Sliding Windows (Ventanas Deslizantes)

Procesa textos largos en ventanas de tokens con solapamiento y
agrega resultados. Mide tokens y latencia por ventana y total.
"""

import time
import requests
import tiktoken

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
ENC = tiktoken.get_encoding("cl100k_base")


def tokenize(s: str):
    return ENC.encode(s)


def detokenize(ids):
    return ENC.decode(ids)


def build_windows(text: str, window_tokens: int, overlap_tokens: int):
    ids = tokenize(text)
    step = max(1, window_tokens - overlap_tokens)
    windows = []
    i = 0
    while i < len(ids):
        win_ids = ids[i : i + window_tokens]
        if not win_ids:
            break
        windows.append((i, i + len(win_ids), win_ids))
        if i + window_tokens >= len(ids):
            break
        i += step
    return windows


def summarize_chunk(text: str) -> dict:
    prompt = f"Resume en 1 frase: {text}"
    t0 = time.time()
    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_predict": 50}},
        timeout=120,
    )
    dt = time.time() - t0
    r.raise_for_status()
    data = r.json()
    return {
        "response": data.get("response", "").strip(),
        "prompt_tokens": data.get("prompt_eval_count", 0),
        "output_tokens": data.get("eval_count", 0),
        "time_s": dt,
    }


def run_sliding_windows(text: str, window_tokens: int = 300, overlap_tokens: int = 60):
    wins = build_windows(text, window_tokens, overlap_tokens)
    total_prompt = 0
    total_output = 0
    total_time = 0.0
    summaries = []

    print(f"Windows: {len(wins)}, window_tokens: {window_tokens}, overlap_tokens: {overlap_tokens}")

    for idx, (start, end, ids) in enumerate(wins, 1):
        chunk = detokenize(ids)
        res = summarize_chunk(chunk)
        total_prompt += res["prompt_tokens"]
        total_output += res["output_tokens"]
        total_time += res["time_s"]
        summaries.append(res["response"])
        print(
            f"win={idx} range=({start}-{end}) size={end-start} prompt_toks={res['prompt_tokens']} "
            f"out_toks={res['output_tokens']} time_s={res['time_s']:.2f}"
        )

    print(
        f"TOTAL windows={len(wins)} total_prompt_tokens={total_prompt} total_output_tokens={total_output} "
        f"total_time_s={total_time:.2f}"
    )

    stitched = " ".join(summaries)
    print(f"AGG_SUMMARY_TOKENS={len(tokenize(stitched))}")
    print(f"AGG_SUMMARY_PREVIEW={stitched[:160]}...")


if __name__ == "__main__":
    # Texto de ejemplo (puedes reemplazar por un documento real)
    base = (
        "Los modelos de lenguaje tienen límites de contexto. "
        "Para procesar documentos largos, una técnica es usar ventanas deslizantes con solapamiento. "
        "Esto mantiene coherencia local y evita perder información al truncar. "
    )
    long_text = (base * 200)  # genera un texto largo

    # Configuración básica
    run_sliding_windows(
        text=long_text,
        window_tokens=300,   # EXPERIMENTO: cambia a 512, 800...
        overlap_tokens=60,   # EXPERIMENTO: cambia a 40, 100...
    )

    # EXPERIMENTOS: descomentar para comparar
    # run_sliding_windows(text=long_text, window_tokens=512, overlap_tokens=128)
    # run_sliding_windows(text=long_text, window_tokens=800, overlap_tokens=120)


