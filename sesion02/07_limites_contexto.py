"""
Ejercicio 07: Límites de Contexto

Demuestra los límites de contexto y qué pasa cuando se exceden.
"""

import requests
import tiktoken
import time

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
encoding = tiktoken.get_encoding("cl100k_base")

def generar_texto_largo(num_palabras: int) -> str:
    """Genera un texto largo con el número de palabras especificado."""
    base = "Lorem ipsum dolor sit amet consectetur adipiscing elit. "
    texto = (base * (num_palabras // 10 + 1))[:num_palabras * 6]
    return texto

def probar_limite(texto: str, mostrar_detalles: bool = True):
    """Prueba un texto y muestra estadísticas."""
    tokens = encoding.encode(texto)
    num_tokens = len(tokens)
    
    print(f"Caracteres: {len(texto)}, Palabras: {len(texto.split())}, Tokens: {num_tokens}")
    
    try:
        inicio = time.time()
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": MODEL,
                "prompt": texto,
                "stream": False,
                "options": {"num_predict": 50}
            },
            timeout=60
        )
        tiempo = time.time() - inicio
        
        if r.status_code == 200:
            data = r.json()
            tokens_prompt = data.get("prompt_eval_count", 0)
            tokens_respuesta = data.get("eval_count", 0)
            
            print(f"Éxito: Sí, Tiempo: {tiempo:.2f}s, Tokens procesados: {tokens_prompt}, Tokens respuesta: {tokens_respuesta}")
            
            if mostrar_detalles:
                respuesta = data.get("response", "").strip()[:100]
                print(f"Respuesta: {respuesta}...")
            
            return True, tiempo, tokens_prompt
        else:
            print(f"Éxito: No, Error: {r.status_code}")
            return False, 0, 0
            
    except Exception as e:
        print(f"Éxito: No, Error: {e}")
        return False, 0, 0

# EJEMPLO BÁSICO
texto_pequeno = generar_texto_largo(100)
probar_limite(texto_pequeno, mostrar_detalles=True)

# EXPERIMENTO 1
# texto_mediano = generar_texto_largo(500)
# probar_limite(texto_mediano, mostrar_detalles=True)

# EXPERIMENTO 2
# texto_grande = generar_texto_largo(2000)
# probar_limite(texto_grande, mostrar_detalles=True)

# EXPERIMENTO 3
# texto_muy_grande = generar_texto_largo(5000)
# probar_limite(texto_muy_grande, mostrar_detalles=True)

# EXPERIMENTO 4
# texto_maximo = generar_texto_largo(10000)
# tokens_maximo = encoding.encode(texto_maximo)
# print(f"Tokens: {len(tokens_maximo)}")
# probar_limite(texto_maximo, mostrar_detalles=True)

# EXPERIMENTO 5
# tamanos = [
#     (100, "Pequeño"),
#     (500, "Mediano"),
#     (2000, "Grande"),
# ]
# 
# resultados = []
# for num_palabras, descripcion in tamanos:
#     texto = generar_texto_largo(num_palabras)
#     tokens = encoding.encode(texto)
#     exito, tiempo, tokens_procesados = probar_limite(texto, mostrar_detalles=False)
#     resultados.append({
#         "descripcion": descripcion,
#         "tokens": len(tokens),
#         "exito": exito,
#         "tiempo": tiempo
#     })
# 
# print(f"\n{'Tamaño':<15} {'Tokens':<12} {'Éxito':<10} {'Tiempo (s)':<12}")
# print("-"*50)
# for r in resultados:
#     exito_str = "Sí" if r["exito"] else "No"
#     print(f"{r['descripcion']:<15} {r['tokens']:<12} {exito_str:<10} {r['tiempo']:<12.2f}")