# Teoría y explicación: Enrutador híbrido local/nube

Este ejercicio muestra una estrategia básica para decidir si respondemos con un modelo local o uno en la nube.

## Meta educativa
* Comprender que podemos combinar varios modelos y escoger el más adecuado según reglas simples.
* Mostrar cómo medir latencia y, si quisiéramos, el coste estimado de cada opción.
* Recordar la importancia de gestionar credenciales con variables de entorno (`.env`).

## Cómo funciona el router
1. Calcula una estimación rápida de tokens del prompt (`est_tokens`).
2. Si el prompt es corto y no contiene palabras sensibles, usa el modelo local con Ollama.
3. Si el prompt es largo o delicado, llama a la API de OpenAI (si tenemos la clave configurada).
4. Devuelve qué ruta se eligió, la respuesta recortada, la latencia y un espacio para el coste.
5. En el `main` probamos con dos prompts para ver la diferencia de decisiones.

## Mensaje para el alumno
* "Podemos tener lo mejor de ambos mundos: velocidad local para tareas sencillas y potencia en la nube para retos grandes".
* "Las reglas pueden ser tan simples o complejas como queramos; incluso podríamos usar machine learning para decidir".
* "Guardar las claves fuera del código es un buen hábito de seguridad".
