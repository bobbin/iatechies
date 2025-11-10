# Ejercicio 13 — Gemini multimodal básico (texto + imagen)

## Objetivo

Enviar a Gemini una descripción textual junto con la URL de una imagen para obtener un `alt text` accesible y un pie de foto propuesto.

## Conceptos clave

- **Entrada multimodal:** `generate_content` acepta texto y objetos de imagen.
- **Accesibilidad:** generar descripciones útiles para lectores con dificultades visuales.
- **Validación rápida:** demo sencilla que puede ampliarse si hay tiempo.

## Pasos

1. Proporciona una URL de imagen (o ruta local con lectura binaria).
2. Ejecuta el script para obtener `alt text` y pie de foto.
3. Ajusta el prompt para reforzar tono o longitud deseada.
4. Comprueba la latencia y posibles limitaciones (tamaño máximo de imagen).

## Ideas de extensión

- Guardar el resultado en la base de datos del CMS junto a la imagen.
- Validar múltiples imágenes en un lote y generar un informe.
- Añadir detección de contenido sensible y bloquear imágenes conflictivas.

