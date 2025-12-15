# Ejercicio 01 — GPT Vision: describir imagen + tags + alt-text (JSON)

## Objetivo

Dada una imagen, generar:

- Una **descripción** (2–4 frases)
- **Etiquetas** (tags) útiles para indexación
- Un **alt-text** accesible (máx. 120 caracteres)

Todo en **JSON**, ideal para integrarlo en un CMS.

## Ejecutar

```bash
python sesion10/01_gpt_vision_describir.py sesion10/inputs/ejemplo.jpg
```

También puedes usar la imagen de ejemplo del repo:

```bash
python sesion10/01_gpt_vision_describir.py sesion01/ejemplo.jpg
```

## Notas

- Requiere `OPENAI_API_KEY` y opcionalmente `DEFAULT_MODEL_OPENAI` en `sesion10/.env`.
- El script intenta extraer el primer objeto JSON válido aunque el modelo añada texto alrededor.


