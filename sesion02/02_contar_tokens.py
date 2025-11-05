"""
Ejercicio 02: Contar Tokens

Muestra diferentes formas de contar tokens y comparar métodos.
"""

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

# Texto de ejemplo
texto = "Los tokens determinan el costo de las APIs de modelos de lenguaje."

# Método 1: Conteo real con tiktoken
tokens = encoding.encode(texto)
tokens_reales = len(tokens)

# Método 2: Estimación simple (4 caracteres = 1 token)
estimacion_chars = len(texto) // 4

# Método 3: Estimación por palabras (1.3 tokens por palabra)
palabras = len(texto.split())
estimacion_palabras = int(palabras * 1.3)

print("="*60)
print("CONTEO DE TOKENS")
print("="*60)

print(f"\nTexto: '{texto}'")
print(f"\nCaracteres: {len(texto)}")
print(f"Palabras: {palabras}")

print(f"\n📊 Métodos de conteo:")
print(f"  Real (tiktoken):        {tokens_reales} tokens")
print(f"  Estimación (chars/4):   {estimacion_chars} tokens")
print(f"  Estimación (palabras):  {estimacion_palabras} tokens")

print(f"\n📈 Errores de estimación:")
print(f"  Error método chars:     {abs(estimacion_chars - tokens_reales)} tokens")
print(f"  Error método palabras:  {abs(estimacion_palabras - tokens_reales)} tokens")

# Comparar varios textos
print("\n" + "="*60)
print("COMPARACIÓN DE TEXTOS")
print("="*60)

textos_ejemplo = [
    "Hola",
    "Hola mundo",
    "Los tokens son importantes",
    "Los tokens son unidades de procesamiento que determinan el costo.",
]

print(f"\n{'Texto':<45} {'Tokens':<10} {'Ratio':<10}")
print("-"*60)
for txt in textos_ejemplo:
    tokens = encoding.encode(txt)
    ratio = len(tokens) / len(txt) if len(txt) > 0 else 0
    texto_display = txt[:43] + "..." if len(txt) > 45 else txt
    print(f"{texto_display:<45} {len(tokens):<10} {ratio:.3f}")

print("\n💡 Para facturación precisa, siempre usa conteo real con tiktoken.")