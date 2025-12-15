# Ejercicio 05 — Comparar 2 imágenes (OpenAI o Gemini)

## Objetivo

Comparar dos imágenes y devolver un JSON con:

- `resumen`: 2–4 frases sobre las diferencias principales
- `cambios`: lista de cambios detectados
  - `tipo`: `"nuevo" | "eliminado" | "modificado" | "desconocido"`
  - `detalle`: descripción breve
  - `zona`: bbox aproximada (normalizada 0..1) si aplica, o `null`

## Ejecutar

OpenAI:

```bash
python sesion10/05_comparar_dos_imagenes.py --provider openai sesion10/inputs/a.jpg sesion10/inputs/b.jpg
```

Gemini:

```bash
python sesion10/05_comparar_dos_imagenes.py --provider gemini sesion10/inputs/a.jpg sesion10/inputs/b.jpg
```

## Idea de uso

- Validación de “antes/después” (obras, siniestros, inventario)
- Control de calidad de capturas (mismo producto, distinta foto)
- Auditoría visual rápida


