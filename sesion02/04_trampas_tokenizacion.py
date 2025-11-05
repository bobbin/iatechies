"""
Ejercicio 04: Trampas y Sorpresas en la Tokenización

Muestra casos donde el conteo de tokens puede ser inesperado.
"""

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

print("="*60)
print("TRAMPAS DE TOKENIZACIÓN")
print("="*60)

# Trampa 1: Emojis
print("\n📌 TRAMPA 1: Emojis")
print("-"*60)

texto_normal = "Hola mundo"
texto_emoji = "Hola 😊 mundo 🎉"

tokens_normal = encoding.encode(texto_normal)
tokens_emoji = encoding.encode(texto_emoji)

print(f"Sin emojis: '{texto_normal}' -> {len(tokens_normal)} tokens")
print(f"Con emojis: '{texto_emoji}' -> {len(tokens_emoji)} tokens")
print(f"⚠️  Diferencia: {len(tokens_emoji) - len(tokens_normal)} tokens extra")

# Trampa 2: Código
print("\n📌 TRAMPA 2: Código")
print("-"*60)

texto_texto = "Define una función que retorne el cuadrado"
texto_codigo = "def f(x): return x**2"

tokens_texto = encoding.encode(texto_texto)
tokens_codigo = encoding.encode(texto_codigo)

print(f"Texto normal: '{texto_texto}' -> {len(tokens_texto)} tokens")
print(f"Código: '{texto_codigo}' -> {len(tokens_codigo)} tokens")
print(f"⚠️  El código puede tener ratios diferentes")

# Trampa 3: Multilingüe
print("\n📌 TRAMPA 3: Idiomas")
print("-"*60)

texto_es = "Los tokens son importantes"
texto_en = "Tokens are important"
texto_chino = "令牌很重要"

tokens_es = encoding.encode(texto_es)
tokens_en = encoding.encode(texto_en)
tokens_chino = encoding.encode(texto_chino)

print(f"Español: '{texto_es}' -> {len(tokens_es)} tokens")
print(f"Inglés: '{texto_en}' -> {len(tokens_en)} tokens")
print(f"Chino: '{texto_chino}' -> {len(tokens_chino)} tokens")

# Comparación de ratios
print("\n📌 COMPARACIÓN DE RATIOS")
print("-"*60)

ejemplos = [
    ("Texto normal", "Este es un texto normal"),
    ("Con emojis", "Este es un texto 😊🎉 con emojis"),
    ("Código Python", "def process(x): return x * 2"),
    ("URL", "https://www.example.com/path?query=value"),
]

print(f"\n{'Tipo':<20} {'Tokens':<10} {'Ratio':<10}")
print("-"*40)
for tipo, texto in ejemplos:
    tokens = encoding.encode(texto)
    ratio = len(tokens) / len(texto) if len(texto) > 0 else 0
    print(f"{tipo:<20} {len(tokens):<10} {ratio:.3f}")

print("\n💡 Los emojis, código y algunos símbolos consumen más tokens.")
print("   Siempre mide antes de desplegar en producción.")