# Teoría y explicación: Microservicio con FastAPI

En este ejercicio convertimos las llamadas a Ollama en un servicio web sencillo usando FastAPI.

## Objetivo didáctico
* Mostrar cómo envolver un modelo en una API propia para que otros equipos o aplicaciones puedan usarlo.
* Practicar el uso de `pydantic` para validar la entrada.
* Explicar la importancia de variables de entorno para configurar URLs y modelos sin tocar el código.

## ¿Qué hace el microservicio?
1. Define un modelo de entrada `Inp` con un único campo `prompt`.
2. Crea un endpoint `POST /summarize` que recibe texto y construye un prompt de resumen en 3 viñetas.
3. Llama a Ollama con el modelo configurado y devuelve la respuesta limpia.
4. Permite ejecutarlo como script: `python 08_microservice_fastapi.py`

## Mensajes clave para el alumno
* "Montar un microservicio nos permite ofrecer IA como un producto reutilizable".
* "FastAPI facilita la validación y documentación automática".
* "Las variables de entorno ayudan a desplegar el mismo código en distintos entornos".
