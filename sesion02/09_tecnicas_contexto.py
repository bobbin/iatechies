"""
Ejercicio 09: Técnicas para Manejar Contexto

Demuestra técnicas como truncado, ventanas deslizantes y chunking.
"""

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def truncar_texto(texto: str, max_tokens: int = 100) -> str:
    """Trunca un texto al número máximo de tokens."""
    tokens = encoding.encode(texto)
    if len(tokens) <= max_tokens:
        return texto
    
    tokens_truncados = tokens[:max_tokens]
    return encoding.decode(tokens_truncados)

def ventana_deslizante(texto: str, tamano_ventana: int = 200, solapamiento: int = 50):
    """Divide texto en ventanas deslizantes con solapamiento."""
    tokens = encoding.encode(texto)
    ventanas = []
    
    i = 0
    while i < len(tokens):
        ventana_tokens = tokens[i:i + tamano_ventana]
        ventana_texto = encoding.decode(ventana_tokens)
        ventanas.append({
            "inicio": i,
            "fin": min(i + tamano_ventana, len(tokens)),
            "tokens": len(ventana_tokens),
            "texto": ventana_texto
        })
        i += tamano_ventana - solapamiento
        if i >= len(tokens):
            break
    
    return ventanas

def chunking_por_oraciones(texto: str, max_tokens_por_chunk: int = 200):
    """Divide texto en chunks por oraciones respetando límite de tokens."""
    oraciones = texto.split('. ')
    chunks = []
    chunk_actual = []
    tokens_actuales = 0
    
    for oracion in oraciones:
        tokens_oracion = encoding.encode(oracion + '. ')
        if tokens_actuales + len(tokens_oracion) <= max_tokens_por_chunk:
            chunk_actual.append(oracion)
            tokens_actuales += len(tokens_oracion)
        else:
            if chunk_actual:
                chunks.append('. '.join(chunk_actual) + '.')
            chunk_actual = [oracion]
            tokens_actuales = len(tokens_oracion)
    
    if chunk_actual:
        chunks.append('. '.join(chunk_actual) + '.')
    
    return chunks

texto_largo = """
Los tokens son unidades fundamentales en el procesamiento de lenguaje natural.
Cada modelo de lenguaje tiene un límite máximo de tokens que puede procesar simultáneamente.
Cuando se excede este límite, el modelo puede truncar el contenido o fallar completamente.
Existen varias técnicas para manejar textos largos que exceden los límites de contexto.
El truncado simple es la técnica más básica pero puede perder información importante.
Las ventanas deslizantes permiten procesar documentos largos dividiéndolos en segmentos.
El chunking por oraciones mantiene la coherencia semántica mejor que el truncado.
Cada técnica tiene ventajas y desventajas según el caso de uso específico.
""" * 2

tokens_original = encoding.encode(texto_largo)
print(f"Texto original: {len(tokens_original)} tokens")

# EJEMPLO BÁSICO: Truncado
max_tokens = 100
texto_truncado = truncar_texto(texto_largo, max_tokens)
tokens_truncados = encoding.encode(texto_truncado)

print(f"Truncado - Límite: {max_tokens}, Resultado: {len(tokens_truncados)} tokens")
print(f"Texto truncado: {texto_truncado[:150]}...")

# EXPERIMENTO 1: Ventanas deslizantes
# ventanas = ventana_deslizante(texto_largo, tamano_ventana=150, solapamiento=30)
# 
# print(f"Ventanas - Número: {len(ventanas)}, Tamaño: 150, Solapamiento: 30")
# for i, ventana in enumerate(ventanas[:3], 1):
#     print(f"Ventana {i}: tokens {ventana['inicio']}-{ventana['fin']} ({ventana['tokens']} tokens)")
#     print(f"  {ventana['texto'][:80]}...")

# EXPERIMENTO 2: Chunking por oraciones
# chunks = chunking_por_oraciones(texto_largo, max_tokens_por_chunk=150)
# 
# print(f"Chunking - Número: {len(chunks)}, Límite: 150 tokens")
# for i, chunk in enumerate(chunks[:3], 1):
#     tokens_chunk = encoding.encode(chunk)
#     print(f"Chunk {i}: {len(tokens_chunk)} tokens")
#     print(f"  {chunk[:80]}...")

# EXPERIMENTO 3: Comparación
# texto_trunc = truncar_texto(texto_largo, 100)
# ventanas = ventana_deslizante(texto_largo, 150, 30)
# chunks = chunking_por_oraciones(texto_largo, 150)
# 
# print(f"\n{'Técnica':<25} {'Segmentos':<12} {'Tokens/seg':<15} {'Info perdida':<15}")
# print("-"*70)
# print(f"{'Original':<25} {'1':<12} {len(tokens_original):<15} {'No':<15}")
# print(f"{'Truncado':<25} {'1':<12} {len(encoding.encode(texto_trunc)):<15} {'Sí (final)':<15}")
# print(f"{'Ventanas deslizantes':<25} {len(ventanas):<12} {'~150':<15} {'No':<15}")
# print(f"{'Chunking oraciones':<25} {len(chunks):<12} {'~150':<15} {'No':<15}")