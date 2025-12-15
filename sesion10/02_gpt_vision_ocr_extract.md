# Ejercicio 02 — GPT Vision: “OCR” + extracción estructurada (ticket/factura) en JSON

## Objetivo

Usar un modelo multimodal para:

- Leer texto visible (**OCR aproximado**)
- Extraer un **JSON estructurado** tipo ticket/factura:
  - comercio
  - fecha
  - moneda
  - total
  - líneas (items) con descripción e importe si se ve

## Ejecutar

```bash
python sesion10/02_gpt_vision_ocr_extract.py sesion10/inputs/ticket.jpg
```

## Notas

- Si el modelo no ve un campo con claridad, devuelve `null`.
- Este ejercicio es muy útil para **automatizar contabilidad ligera**, archivado o búsqueda.


