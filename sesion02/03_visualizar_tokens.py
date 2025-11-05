"""
Ejercicio 03: Visualizar Tokens

Muestra cómo visualizar tokens con colores para entender
cómo se divide el texto.
"""

import tiktoken

# Colores ANSI para terminal
COLORES = [
    '\033[91m',  # Rojo
    '\033[92m',  # Verde
    '\033[93m',  # Amarillo
    '\033[94m',  # Azul
    '\033[95m',  # Magenta
    '\033[96m',  # Cyan
]
RESET = '\033[0m'

encoding = tiktoken.get_encoding("cl100k_base")

# Ejemplo 1: Visualización básica
print("="*60)
print("EJEMPLO 1: Visualización con Colores")
print("="*60)

texto = "Los tokens son unidades de procesamiento"
tokens = encoding.encode(texto)

print(f"\nTexto: '{texto}'")
print(f"Total de tokens: {len(tokens)}")
print("\nTokens (cada color es un token):")

# Visualizar cada token con su color
for i, token_id in enumerate(tokens):
    color = COLORES[i % len(COLORES)]
    token_text = encoding.decode([token_id])
    print(f"{color}[{token_text}]{RESET}", end=" ")

print("\n")

# Ejemplo 2: Desglose detallado
print("\n" + "="*60)
print("EJEMPLO 2: Desglose Detallado")
print("="*60)

texto2 = "Hola mundo"
tokens2 = encoding.encode(texto2)

print(f"\nTexto: '{texto2}'")
print(f"\nToken | ID     | Texto")
print("-"*30)
for i, token_id in enumerate(tokens2, 1):
    token_text = encoding.decode([token_id])
    print(f"  {i}   | {token_id:5d} | '{token_text}'")

# Ejemplo 3: Comparación visual
print("\n" + "="*60)
print("EJEMPLO 3: Comparación")
print("="*60)

texto_a = "Python es genial"
texto_b = "Python programming is great"

tokens_a = encoding.encode(texto_a)
tokens_b = encoding.encode(texto_b)

print(f"\nTexto A: '{texto_a}'")
print(f"Tokens: {len(tokens_a)}")
for i, token_id in enumerate(tokens_a):
    color = COLORES[i % len(COLORES)]
    token_text = encoding.decode([token_id])
    print(f"{color}[{token_text}]{RESET}", end=" ")
print("\n")

print(f"\nTexto B: '{texto_b}'")
print(f"Tokens: {len(tokens_b)}")
for i, token_id in enumerate(tokens_b):
    color = COLORES[i % len(COLORES)]
    token_text = encoding.decode([token_id])
    print(f"{color}[{token_text}]{RESET}", end=" ")
print("\n")

print(f"\nDiferencia: {abs(len(tokens_a) - len(tokens_b))} tokens")

print("\n💡 La visualización con colores ayuda a entender cómo se divide el texto.")