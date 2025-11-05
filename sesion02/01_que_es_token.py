"""
Ejercicio 01: ¿Qué es un Token?

Muestra cómo se tokeniza un texto y qué son los tokens.
"""

import tiktoken

# Usamos el encoding de GPT-4 (cl100k_base)
encoding = tiktoken.get_encoding("cl100k_base")

# Ejemplo 1: Texto simple
print("="*60)
print("EJEMPLO 1: Texto Simple")
print("="*60)

texto = "Hola mundo"
tokens = encoding.encode(texto)

print(f"\nTexto: '{texto}'")
print(f"Tokens (IDs numéricos): {tokens}")
print(f"Total de tokens: {len(tokens)}")
print(f"Palabras: {len(texto.split())}")

# Mostrar cada token decodificado
print("\nTokens individuales:")
for i, token_id in enumerate(tokens, 1):
    token_text = encoding.decode([token_id])
    print(f"  Token {i}: ID={token_id:5d} -> '{token_text}'")

# Ejemplo 2: Texto con puntuación
print("\n" + "="*60)
print("EJEMPLO 2: Texto con Puntuación")
print("="*60)

texto2 = "¡Hola! ¿Cómo estás?"
tokens2 = encoding.encode(texto2)

print(f"\nTexto: '{texto2}'")
print(f"Tokens: {tokens2}")
print(f"Total de tokens: {len(tokens2)}")
print(f"Palabras: {len(texto2.split())}")

# Ejemplo 3: Comparación
print("\n" + "="*60)
print("EJEMPLO 3: Comparación")
print("="*60)

textos = ["Hola", "Hola mundo", "Hola mundo, ¿cómo estás?"]

print(f"\n{'Texto':<30} {'Caracteres':<12} {'Tokens':<10} {'Ratio':<10}")
print("-"*60)
for texto in textos:
    tokens = encoding.encode(texto)
    ratio = len(tokens) / len(texto) if len(texto) > 0 else 0
    print(f"{texto:<30} {len(texto):<12} {len(tokens):<10} {ratio:.3f}")

print("\n💡 Observa: Los tokens no siempre coinciden con palabras.")
print("   Un token puede ser parte de una palabra, una palabra completa,")
print("   o incluso múltiples palabras según el contexto.")