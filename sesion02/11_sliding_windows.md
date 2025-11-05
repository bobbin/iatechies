# Teoría: Sliding Windows (Ventanas Deslizantes)

Procesar todo un documento largo en una sola llamada puede exceder la ventana de contexto. La técnica de Sliding Windows divide el texto en ventanas de tokens con solapamiento para preservar contexto local.

## Objetivo

Procesar textos largos en segmentos solapados, medir tokens/latencia por ventana y agregar los resultados (p. ej., resúmenes parciales → resumen global).

## Parámetros Clave

- **window_tokens**: tamaño de la ventana en tokens
- **overlap_tokens**: tokens compartidos entre ventanas consecutivas (contexto local)
- **step**: `window_tokens - overlap_tokens`

## Flujo

1. Tokenizar el documento
2. Crear ventanas `[i : i + window_tokens]` avanzando `step`
3. Para cada ventana: procesar (p. ej. resumir) y medir
4. Agregar resultados y métricas

## Métricas

- Tokens de prompt y salida por ventana
- Tiempo por ventana y total
- Resumen agregado y sus tokens

## Uso

```bash
python 11_sliding_windows.py
```

Ajusta `window_tokens` y `overlap_tokens` para comparar eficiencia/calidad.

## Cuándo usarlo

- Documentos largos que superan el contexto
- Pipelines de extracción/resumen por secciones
- Ingesta de conocimiento con preservación de contexto local

---

Consejo: Un solapamiento moderado (10-20% del tamaño de ventana) suele equilibrar calidad y coste.
