# Slide 8 — Por qué Few-shot y CoT funcionan mejor

## Prompt sin CoT ni estructura
```
¿Esta medida es buena o mala para la economía? Explícalo:
[texto]
```

## Prompt con CoT estructurado
```
Eres un analista económico neutral.

Tarea:
Evaluar una medida sin tomar posición política.

Instrucciones:
1) Explica en 2 viñetas los posibles efectos positivos.
2) Explica en 2 viñetas los posibles efectos negativos.
3) Termina con una frase final explicando qué información adicional haría falta para evaluarla mejor.

Medida descrita en la noticia:
[texto]

Responde exactamente con esa estructura.
```

