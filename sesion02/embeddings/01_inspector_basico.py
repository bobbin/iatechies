from ollama_embed import embed, cosine_sim

pairs = [
    ("Los gatos duermen al sol.", "Los felinos descansan a la luz del sol."),
    ("El BCE sube los tipos de interés.", "La inflación baja en la eurozona."),
]

if __name__ == "__main__":
    for i, (t1, t2) in enumerate(pairs, start=1):
        v1 = embed(t1)
        v2 = embed(t2)

        print(f"\nPAR {i}")
        print("Texto 1:", t1)
        print("Texto 2:", t2)
        print("Dimensión:", v1.shape[0])
        print("v1[:5]:", v1[:5])
        print("v2[:5]:", v2[:5])
        print("cosine:", round(cosine_sim(v1, v2), 3))


