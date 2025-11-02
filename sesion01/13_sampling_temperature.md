# Teoría y explicación: Controlar la temperatura de muestreo

Usamos el campo `options.temperature` para mostrar cómo cambia la creatividad y la latencia de las respuestas del modelo.

## Objetivo didáctico
* Comprender cómo el muestreo afecta la variabilidad del output.
* Mostrar que `options` acepta otros hiperparámetros como `top_p` o `repeat_penalty`.
* Promover la instrumentación con tiempos de respuesta para comparar configuraciones.

## Mensajes para remarcar
* "Temperaturas bajas producen respuestas deterministas; las altas fomentan la creatividad".
* "Agrupa tus experimentos en un mismo script para comparar outputs con el mismo prompt".
* "En Ollama Cloud puedes reutilizar el mismo código: solo cambia la URL y añade el token".
