# Slide 7 — Chain-of-Thought ligero

## Prompt malo
```
Explica el impacto de esta medida económica:
[texto]
```

## Prompt bueno (CoT ligero)
```
Eres un analista económico que explica medidas a lectores no expertos.

Tarea:
Analiza la siguiente medida en 3 pasos:

1) Qué hace la medida (3 viñetas).
2) Efectos posibles a corto plazo (3 viñetas).
3) Efectos posibles a medio plazo (3 viñetas).

Medida descrita en la noticia:
[texto]

Responde siguiendo exactamente esta estructura:

1) Qué hace la medida:
- ...
- ...
- ...

2) Efectos posibles a corto plazo:
- ...
- ...
- ...

3) Efectos posibles a medio plazo:
- ...
- ...
- ...
```

