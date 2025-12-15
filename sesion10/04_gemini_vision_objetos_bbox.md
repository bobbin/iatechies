# Ejercicio 04 — Gemini Vision: objetos + *bounding boxes* aproximadas (JSON)

## Objetivo

Detectar objetos relevantes de la escena y devolver un JSON con:

- `objetos`: lista de objetos
  - `label`: nombre del objeto
  - `confidence`: 0..1 (estimación subjetiva)
  - `bbox`: caja aproximada normalizada 0..1
    - `x`, `y`: esquina superior izquierda
    - `w`, `h`: ancho y alto

## Ejecutar

```bash
python sesion10/04_gemini_vision_objetos_bbox.py sesion10/inputs/escena.jpg
```

## Nota práctica

Esto no sustituye un detector clásico (YOLO/Detectron), pero es muy útil para:

- Crear **anotaciones rápidas**
- Generar *datasets* iniciales
- Prototipos de interfaces (resaltar “zonas” de interés)


