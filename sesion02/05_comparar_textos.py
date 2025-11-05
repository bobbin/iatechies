"""
Ejercicio 05: Comparar Textos

Compara cómo diferentes textos se tokenizan.
"""

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

print("="*60)
print("COMPARACIÓN DE TEXTOS")
print("="*60)

# Comparación por longitud
print("\n📌 Por Longitud")
print("-"*60)

textos = [
    "Hola",
    "Hola mundo",
    "Hola mundo, ¿cómo estás?",
    "Los tokens son unidades de procesamiento que determinan el costo.",
]

print(f"\n{'Texto':<45} {'Chars':<8} {'Tokens':<8} {'Ratio':<8}")
print("-"*70)
for texto in textos:
    tokens = encoding.encode(texto)
    ratio = len(tokens) / len(texto) if len(texto) > 0 else 0
    texto_display = texto[:43] + "..." if len(texto) > 45 else texto
    print(f"{texto_display:<45} {len(texto):<8} {len(tokens):<8} {ratio:.3f}")

# Comparación por idioma
print("\n📌 Por Idioma")
print("-"*60)

idiomas = [
    ("Español", "Los tokens son importantes"),
    ("Inglés", "Tokens are important"),
    ("Francés", "Les jetons sont importants"),
]

print(f"\n{'Idioma':<15} {'Texto':<35} {'Tokens':<8}")
print("-"*60)
for idioma, texto in idiomas:
    tokens = encoding.encode(texto)
    print(f"{idioma:<15} {texto:<35} {len(tokens):<8}")

# Optimización: encontrar mejor variante
print("\n📌 Optimización")
print("-"*60)

texto_original = "Por favor, ¿podrías ayudarme a resolver este problema complicado?"
variantes = [
    "Ayuda: resolver problema complicado",
    "Resolver problema",
    texto_original,
]

tokens_original = len(encoding.encode(texto_original))

print(f"\nTexto original ({tokens_original} tokens):")
print(f"  '{texto_original}'")

print(f"\nVariantes:")
for i, variante in enumerate(variantes, 1):
    tokens = len(encoding.encode(variante))
    ahorro = tokens_original - tokens
    porcentaje = (ahorro / tokens_original * 100) if tokens_original > 0 else 0
    print(f"  {i}. {tokens} tokens (ahorro: {ahorro} tokens, {porcentaje:.1f}%)")
    print(f"     '{variante}'")

print("\n💡 Comparar variantes ayuda a optimizar prompts y reducir costos.")