from ollama_embed import embed, cosine_sim

TAGS = [
    "política",
    "economía",
    "deportes",
    "sociedad",
    "tecnología",
    "cultura",
]

TAG_VECS = {tag: embed(tag) for tag in TAGS}


def best_tag(text: str):
    v = embed(text)
    scores = [(cosine_sim(v, tv), tag) for tag, tv in TAG_VECS.items()]
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[0], scores


if __name__ == "__main__":
    noticias = [
        "El paro baja dos puntos y el PIB crece por encima de lo esperado.",
        "El Barça gana al Atlético en un partido lleno de goles.",
        "Un nuevo modelo de IA generativa revoluciona la edición de vídeo.",
    ]

    for n in noticias:
        (score, tag), scores = best_tag(n)
        print("\nNoticia:", n)
        print(f"Tag sugerido: {tag} (sim={score:.3f})")
        print("Ranking:", [(t, round(s, 3)) for s, t in scores])


