"""
Ejercicio 08: Latencia y Contexto

Muestra cómo el tamaño del contexto afecta la latencia.
"""

import requests
import tiktoken
import time

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
encoding = tiktoken.get_encoding("cl100k_base")

def medir_latencia(texto: str, num_intentos: int = 2) -> dict:
    """Mide la latencia de procesar un texto."""
    tokens = encoding.encode(texto)
    tiempos = []
    
    for i in range(num_intentos):
        try:
            inicio = time.time()
            r = requests.post(
                f"{OLLAMA}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": texto,
                    "stream": False,
                    "options": {"num_predict": 20}
                },
                timeout=60
            )
            tiempo = time.time() - inicio
            
            if r.status_code == 200:
                tiempos.append(tiempo)
        except Exception as e:
            print(f"Error en intento {i+1}: {e}")
    
    if tiempos:
        return {
            "tokens": len(tokens),
            "tiempo_promedio": sum(tiempos) / len(tiempos),
            "tiempo_min": min(tiempos),
            "tiempo_max": max(tiempos),
            "intentos_exitosos": len(tiempos)
        }
    return None

# EJEMPLO BÁSICO
texto_pequeno = "Hola"
texto_grande = "Los tokens son unidades de procesamiento que determinan el costo de las APIs de modelos de lenguaje. " * 10

resultado_pequeno = medir_latencia(texto_pequeno)
resultado_grande = medir_latencia(texto_grande)

if resultado_pequeno and resultado_grande:
    print(f"Pequeño: {resultado_pequeno['tokens']} tokens, {resultado_pequeno['tiempo_promedio']:.2f}s")
    print(f"Grande: {resultado_grande['tokens']} tokens, {resultado_grande['tiempo_promedio']:.2f}s")
    
    ratio_tokens = resultado_grande['tokens'] / resultado_pequeno['tokens'] if resultado_pequeno['tokens'] > 0 else 0
    ratio_tiempo = resultado_grande['tiempo_promedio'] / resultado_pequeno['tiempo_promedio'] if resultado_pequeno['tiempo_promedio'] > 0 else 0
    
    print(f"Ratio tokens: {ratio_tokens:.1f}x, Ratio tiempo: {ratio_tiempo:.1f}x")

# EXPERIMENTO 1
# textos = {
#     "Muy pequeño": "Hola",
#     "Pequeño": "Los tokens determinan el costo de las APIs de modelos de lenguaje.",
#     "Mediano": "Los tokens son unidades de procesamiento que determinan el costo de las APIs de modelos de lenguaje. " * 5,
#     "Grande": "Los tokens son unidades de procesamiento que determinan el costo de las APIs de modelos de lenguaje. " * 20,
# }
# 
# resultados = []
# for descripcion, texto in textos.items():
#     resultado = medir_latencia(texto, num_intentos=2)
#     if resultado:
#         resultados.append({
#             "descripcion": descripcion,
#             "tokens": resultado["tokens"],
#             "tiempo_promedio": resultado["tiempo_promedio"]
#         })
# 
# print(f"\n{'Tamaño':<15} {'Tokens':<12} {'Tiempo (s)':<15} {'Tokens/s':<12}")
# print("-"*60)
# for r in resultados:
#     tokens_por_segundo = r["tokens"] / r["tiempo_promedio"] if r["tiempo_promedio"] > 0 else 0
#     print(f"{r['descripcion']:<15} {r['tokens']:<12} {r['tiempo_promedio']:<15.2f} {tokens_por_segundo:<12.1f}")

# EXPERIMENTO 2
# textos_crecimiento = [
#     ("Pequeño", "Los tokens son importantes. " * 3),
#     ("Mediano", "Los tokens son importantes. " * 10),
#     ("Grande", "Los tokens son importantes. " * 30),
#     ("Muy grande", "Los tokens son importantes. " * 50),
# ]
# 
# resultados_crecimiento = []
# for descripcion, texto in textos_crecimiento:
#     resultado = medir_latencia(texto, num_intentos=2)
#     if resultado:
#         resultados_crecimiento.append({
#             "descripcion": descripcion,
#             "tokens": resultado["tokens"],
#             "tiempo": resultado["tiempo_promedio"]
#         })
# 
# if len(resultados_crecimiento) >= 2:
#     primero = resultados_crecimiento[0]
#     ultimo = resultados_crecimiento[-1]
#     
#     ratio_tokens = ultimo["tokens"] / primero["tokens"] if primero["tokens"] > 0 else 0
#     ratio_tiempo = ultimo["tiempo"] / primero["tiempo"] if primero["tiempo"] > 0 else 0
#     
#     print(f"De '{primero['descripcion']}' a '{ultimo['descripcion']}':")
#     print(f"Tokens: {ratio_tokens:.1f}x más, Tiempo: {ratio_tiempo:.1f}x más")