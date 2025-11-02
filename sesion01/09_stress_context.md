# Teoría y explicación: Probar límites de contexto

Este ejercicio consiste en enviar un texto muy largo al modelo para observar cómo maneja entradas grandes.

## Ideas que queremos transmitir
* Cada modelo tiene un límite de tokens de entrada. Si nos pasamos, puede truncar el texto o fallar.
* Podemos medir cuántos tokens entra y cuántos salen gracias a los campos `prompt_eval_count` y `eval_count`.
* Ajustar `options` como `num_predict` ayuda a controlar el tamaño de la respuesta.

## Pasos del script
1. Genera un texto largo repitiendo `"Lorem ipsum"` muchas veces.
2. Construye un prompt que pide contar las palabras en una sola frase.
3. Llama a `api/generate` con `num_predict=256` para limitar la respuesta.
4. Imprime el resultado y los tokens usados.

## Explicación amigable para el alumno
* "Es como ver cuánta carga aguanta el modelo antes de saturarse".
* "Los tokens de entrada son las palabras que mandamos; los de salida son las palabras que devuelve".
* "Si conocemos estos límites, evitamos sorpresas en producción".
