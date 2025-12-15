# Ejercicio 06 — PDF: extraer datos de una factura (GPT)

## Objetivo

Tomar un **PDF** (idealmente “nativo”, con texto seleccionable) y:

1) Extraer el texto del PDF localmente.
2) Pedir a GPT que devuelva un **JSON estructurado** con los campos típicos de una factura.

## Ejecutar

```bash
python sesion10/06_gpt_pdf_factura_extract.py sesion10/inputs/factura.pdf
```

Modo demo (sin argumentos): intenta `sesion10/inputs/factura.pdf`.

## Importante (PDF escaneados)

Si tu “PDF” es realmente un **escaneo** (imágenes), `pypdf` no podrá extraer texto útil. En ese caso hay que hacer **OCR** (por ejemplo convertir páginas a imágenes y usar un modelo multimodal). Si quieres, te preparo ese ejercicio también.


