from ollama_embed import embed, cosine_sim

pairs = [
    (
        "La inteligencia artificial está cambiando el periodismo.",
        "Artificial intelligence is changing journalism.",
    ),
    (
        "Los precios de la energía suben en Europa.",
        "Les prix de l'énergie augmentent en Europe.",
    ),
    ("El Real Madrid gana la liga.", "Real Madrid wins the league."),
]

if __name__ == "__main__":
    for es, otra in pairs:
        v_es = embed(es)
        v_ot = embed(otra)
        sim = cosine_sim(v_es, v_ot)
        print("\nES:", es)
        print("OT:", otra)
        print("Similitud:", round(sim, 3))


