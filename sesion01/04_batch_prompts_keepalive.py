import time, requests

OLLAMA = "http://localhost:11434"
MODEL = "mistral:7b"
prompts = [f"Frase {i} sobre IA en 1 línea." for i in range(1, 6)]  # Reducimos a 5 para no tardar mucho

def run_batch(keep_alive_secs=None):
    """Ejecuta el batch de prompts con keep_alive opcional"""
    if keep_alive_secs:
        # Pre-carga el modelo y lo mantiene en memoria
        requests.post(f"{OLLAMA}/api/generate", 
                     json={"model": MODEL, "prompt": "", "keep_alive": keep_alive_secs},
                     timeout=120)
        print(f"OK: Modelo pre-cargado y mantenido {keep_alive_secs}s")
    
    t0 = time.time()
    for i, p in enumerate(prompts, 1):
        r = requests.post(f"{OLLAMA}/api/generate",
            json={"model": MODEL, "prompt": p, "stream": False},
            timeout=120)
        r.raise_for_status()
        print(f"  {i}/{len(prompts)}")
    dt = time.time() - t0
    return dt

print("="*60)
print("Experimento: Comparando keep_alive")
print("NOTA: El orden importa. El primer lote carga el modelo desde cero,")
print("      el segundo lote puede aprovechar el modelo ya cargado.\n")
print("="*60)

# Para que sea justo, primero probamos CON keep_alive para asegurar que el modelo está cargado
print("LOTE 1: CON keep_alive (modelo pre-cargado)")
print("="*60)
dt1 = run_batch(keep_alive_secs=300)

print("\nEsperando 5 segundos para que Ollama descargue el modelo...")
time.sleep(5)

print("\n" + "="*60)
print("LOTE 2: SIN keep_alive (modelo se carga en primer prompt)")
print("="*60)
dt2 = run_batch()

print("\n" + "="*60)
print("COMPARACION:")
print(f"Con keep_alive:    {dt1:.2f}s")
print(f"Sin keep_alive:    {dt2:.2f}s")
if dt2 > dt1:
    diff_pct = ((dt2-dt1)/dt2)*100
    print(f"Diferencia:        {dt2-dt1:.2f}s ({diff_pct:.1f}% mas lento sin keep_alive)")
    print("\nCONCLUSION: keep_alive ayuda cuando haces muchas peticiones seguidas.")
else:
    diff_pct = ((dt1-dt2)/dt1)*100
    print(f"Diferencia:        {dt1-dt2:.2f}s ({diff_pct:.1f}% mas lento con keep_alive)")
    print("\nCONCLUSION: En este caso, el modelo ya estaba en memoria de ejecuciones anteriores.")
print("="*60)
