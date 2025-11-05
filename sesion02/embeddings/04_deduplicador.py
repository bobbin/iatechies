from ollama_embed import embed, cosine_sim

HEADLINES = [
    "El gobierno anuncia nuevas ayudas al alquiler para jóvenes",
    "Nuevas ayudas estatales al alquiler de vivienda para menores de 35 años",
    "Apple presenta su nuevo modelo de iPhone con mejoras en la cámara",
    "Se dispara el precio del petróleo tras el conflicto en Oriente Medio",
]

THRESHOLD = 0.75


def find_duplicates(headlines):
    n = len(headlines)
    vectors = [embed(h) for h in headlines]
    print(f"Dimensión: {vectors[0].shape[0]}")
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_sim(vectors[i], vectors[j])
            if sim >= THRESHOLD:
                print(
                    f"\nPosible duplicado:\n- {headlines[i]}\n- {headlines[j]}\nSimilitud: {sim:.3f}"
                )


if __name__ == "__main__":
    find_duplicates(HEADLINES)


