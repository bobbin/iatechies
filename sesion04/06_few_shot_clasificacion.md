# Slide 6 — Few-shot prompting (clasificación de sección)

## Prompt zero-shot (aceptable pero menos estable)
```
Clasifica la siguiente noticia en una de estas secciones:
["politica", "economia", "deportes", "sociedad", "tecnologia", "cultura"].

Devuelve SOLO el nombre de la sección.

Noticia:
[texto]
```

## Prompt few-shot (mejor)
```
Eres un sistema que clasifica noticias en:
["politica", "economia", "deportes", "sociedad", "tecnologia", "cultura"].

Ejemplos:
Noticia: "El Gobierno aprueba una nueva ley educativa."
Sección: "politica"

Noticia: "La inflación sube al 3,2% en la zona euro."
Sección: "economia"

Noticia: "El Barça vence 2-0 en el clásico."
Sección: "deportes"

Ahora clasifica esta noticia:
[texto]

Responde SOLO con una de las secciones de la lista.
```

