"""
Ejercicio 10: Cómo Afecta el Prompt al Contexto

Muestra cómo diferentes estructuras de prompt afectan el uso del contexto.
"""

import requests
import tiktoken
import time

OLLAMA = "http://localhost:11434"
MODEL = "gemma:2b"
encoding = tiktoken.get_encoding("cl100k_base")

def analizar_prompt(prompt: str, descripcion: str):
    """Analiza un prompt y muestra estadísticas."""
    tokens = encoding.encode(prompt)
    
    try:
        inicio = time.time()
        r = requests.post(
            f"{OLLAMA}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 30}
            },
            timeout=30
        )
        tiempo = time.time() - inicio
        
        if r.status_code == 200:
            data = r.json()
            tokens_procesados = data.get("prompt_eval_count", 0)
            
            return {
                "descripcion": descripcion,
                "tokens_prompt": len(tokens),
                "tokens_procesados": tokens_procesados,
                "tiempo": tiempo,
                "exito": True
            }
    except Exception as e:
        print(f"Error: {e}")
    
    return {
        "descripcion": descripcion,
        "tokens_prompt": len(tokens),
        "tokens_procesados": 0,
        "tiempo": 0,
        "exito": False
    }

datos = "Nombre: Juan, Edad: 30, Ciudad: Madrid, Profesión: Ingeniero, Años experiencia: 5"

# EJEMPLO BÁSICO
prompt_corto = f"Resume: {datos}"
prompt_largo = f"""Eres un asistente útil.
Instrucciones:
1. Resume la información
2. Usa formato claro
3. Sé conciso

Datos: {datos}"""

resultado_corto = analizar_prompt(prompt_corto, "Corto")
resultado_largo = analizar_prompt(prompt_largo, "Largo")

if resultado_corto["exito"] and resultado_largo["exito"]:
    print(f"Corto: {resultado_corto['tokens_prompt']} tokens, {resultado_corto['tiempo']:.2f}s")
    print(f"Largo: {resultado_largo['tokens_prompt']} tokens, {resultado_largo['tiempo']:.2f}s")
    
    diferencia_tokens = resultado_largo['tokens_prompt'] - resultado_corto['tokens_prompt']
    diferencia_tiempo = resultado_largo['tiempo'] - resultado_corto['tiempo']
    
    print(f"Diferencia: {diferencia_tokens} tokens más, {diferencia_tiempo:.2f}s más")

# EXPERIMENTO 1
# prompts = {
#     "Prompt corto": f"Resume: {datos}",
#     
#     "Prompt con instrucciones": f"""Eres un asistente útil.
# Instrucciones:
# 1. Resume la información
# 2. Usa formato claro
# 3. Sé conciso
# 
# Datos: {datos}""",
#     
#     "Prompt con contexto largo": f"""Contexto histórico:
# El procesamiento de lenguaje natural ha evolucionado significativamente.
# Los modelos modernos pueden entender y generar texto de forma sorprendente.
# 
# Datos a procesar: {datos}
# 
# Por favor, resume los datos.""",
#     
#     "Prompt con ejemplos": f"""Ejemplos de resúmenes:
# Ejemplo 1: "María, 25 años, Barcelona, Diseñadora, 3 años"
# Resumen: "María es una diseñadora de 25 años de Barcelona con 3 años de experiencia."
# 
# Ahora resume estos datos: {datos}""",
# }
# 
# resultados = []
# for descripcion, prompt in prompts.items():
#     resultado = analizar_prompt(prompt, descripcion)
#     resultados.append(resultado)
# 
# print(f"\n{'Tipo':<25} {'Tokens':<12} {'Tiempo (s)':<12}")
# print("-"*50)
# for r in resultados:
#     if r["exito"]:
#         print(f"{r['descripcion']:<25} {r['tokens_prompt']:<12} {r['tiempo']:<12.2f}")

# EXPERIMENTO 2
# prompt_no_optimizado = f"""Por favor, si es posible y no te molesta demasiado,
# podrías resumir la siguiente información de manera clara y concisa.
# La información es: {datos}
# Gracias de antemano por tu ayuda."""
# 
# prompt_optimizado = f"Resume: {datos}"
# 
# resultado_no_opt = analizar_prompt(prompt_no_optimizado, "No optimizado")
# resultado_opt = analizar_prompt(prompt_optimizado, "Optimizado")
# 
# if resultado_no_opt["exito"] and resultado_opt["exito"]:
#     ahorro_tokens = resultado_no_opt['tokens_prompt'] - resultado_opt['tokens_prompt']
#     ahorro_tiempo = resultado_no_opt['tiempo'] - resultado_opt['tiempo']
#     porcentaje = (ahorro_tokens / resultado_no_opt['tokens_prompt'] * 100) if resultado_no_opt['tokens_prompt'] > 0 else 0
#     
#     print(f"Ahorro: {ahorro_tokens} tokens ({porcentaje:.1f}%), Tiempo ahorrado: {ahorro_tiempo:.2f}s")