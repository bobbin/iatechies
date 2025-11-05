from ollama_embed import embed, cosine_sim
import numpy as np

HEADLINES = [
    "El BCE mantiene los tipos de interés sin cambios",
    "La selección española gana la Eurocopa",
    "Nueva ley de vivienda limita el precio del alquiler",
    "Descubren vulnerabilidad crítica en sistemas Windows",
    "Gigantes tecnológicos invierten miles de millones en IA generativa",
    "Terremoto de gran magnitud sacude el sur de Japón",
]


def build_index(headlines):
    vectors = []
    for h in headlines:
        v = embed(h)
        vectors.append(v)
    return np.stack(vectors), headlines


def search(query: str, vectors: np.ndarray, texts, k: int = 3):
    q = embed(query)
    sims = [cosine_sim(q, v) for v in vectors]
    ranked = sorted(zip(sims, texts), reverse=True, key=lambda x: x[0])
    return ranked[:k]


if __name__ == "__main__":
    vectors, texts = build_index(HEADLINES)
    while True:
        query = input("\nConsulta (ENTER para salir): ")
        if not query.strip():
            break
        results = search(query, vectors, texts, k=3)
        print("\nTop 3:")
        for score, text in results:
            print(f"  ({score:.3f}) {text}")


