# Slide 9 — Salida estructurada (JSON)

## Prompt malo
```
Saca los datos clave de esta noticia:
[texto]
```

## Prompt bueno
```
Eres un asistente que extrae información de noticias.

Tarea:
Devuelve un JSON con estas claves:
- "titulo": string
- "tema_principal": string
- "personas_clave": lista de strings
- "lugar_principal": string o null

Instrucciones:
- Usa solo información presente en el texto.
- Si no conoces un campo, usa null.
- NO añadas texto fuera del JSON.

Noticia:
[texto]

Responde SOLO con el JSON.
```

