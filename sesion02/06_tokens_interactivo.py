"""
Ejercicio 06: Tokenizador Interactivo

Permite escribir texto y ver cómo se tokeniza con visualización
por colores y estadísticas detalladas.
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

def analizar_texto(texto: str):
    """Analiza un texto y muestra estadísticas detalladas."""
    tokens = encoding.encode(texto)
    
    print("\n" + "="*70)
    print("📊 ANÁLISIS DE TOKENS")
    print("="*70)
    
    # Estadísticas básicas
    print(f"\n📝 Texto: '{texto}'")
    print(f"📏 Caracteres: {len(texto)}")
    print(f"📝 Palabras: {len(texto.split())}")
    print(f"🔢 Tokens: {len(tokens)}")
    
    # Ratios
    ratio_chars = len(tokens) / len(texto) if len(texto) > 0 else 0
    ratio_words = len(tokens) / len(texto.split()) if len(texto.split()) > 0 else 0
    print(f"📈 Ratio tokens/caracteres: {ratio_chars:.3f}")
    print(f"📈 Ratio tokens/palabras: {ratio_words:.3f}")
    
    # Visualización con colores
    print("\n🎨 VISUALIZACIÓN (cada color es un token):")
    print("-"*70)
    for i, token_id in enumerate(tokens):
        color = COLORES[i % len(COLORES)]
        token_text = encoding.decode([token_id])
        print(f"{color}[{token_text}]{RESET}", end=" ")
    print("\n")
    
    # Desglose detallado
    print("\n📋 DESGLOSE DETALLADO:")
    print("-"*70)
    print(f"{'Token':<8} {'ID':<10} {'Texto':<30} {'Longitud':<10}")
    print("-"*70)
    for i, token_id in enumerate(tokens, 1):
        token_text = encoding.decode([token_id])
        texto_display = f"'{token_text}'"[:30]
        print(f"{i:<8} {token_id:<10} {texto_display:<30} {len(token_text):<10}")
    
    # Estimaciones de costo (ejemplo)
    print("\n💰 ESTIMACIÓN DE COSTO (ejemplo):")
    print("-"*70)
    costo_entrada = 0.000001  # $0.000001 por token (ejemplo)
    costo_total = len(tokens) * costo_entrada
    print(f"Costo estimado: ${costo_total:.6f} ({len(tokens)} tokens × ${costo_entrada})")
    
    print("\n" + "="*70)

def modo_interactivo():
    """Modo interactivo para analizar textos."""
    print("🎓 TOKENIZADOR INTERACTIVO")
    print("="*70)
    print("\nEscribe texto para analizar sus tokens.")
    print("Comandos:")
    print("  - Escribe cualquier texto y presiona Enter")
    print("  - 'salir', 'exit' o 'quit' para terminar")
    print("  - 'clear' para limpiar la pantalla")
    print("-"*70)
    
    while True:
        try:
            texto = input("\n📝 Tu texto: ").strip()
            
            # Comandos especiales
            if texto.lower() in ['salir', 'exit', 'quit']:
                print("\n¡Hasta luego! 👋")
                break
            
            if texto.lower() == 'clear':
                print("\n" * 50)  # Limpiar pantalla aproximado
                continue
            
            if not texto:
                print("⚠️  Por favor, escribe algún texto.")
                continue
            
            # Analizar el texto
            analizar_texto(texto)
            
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    modo_interactivo()
