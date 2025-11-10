# Ejercicio 15 — Extender `/chat` a multi-backend

## Objetivo

Reutilizar el microservicio del ejercicio 14 y añadir soporte para varios proveedores (`openai`, `hf`, `google`, `ollama`) seleccionables desde el body.

## Conceptos clave

- **Router de backends:** función que decide qué cliente invocar según el parámetro.
- **Reutilización:** centralizar timeouts y validaciones para todos los proveedores.
- **Respuesta uniforme:** devolver siempre el mismo esquema JSON independientemente del backend.

## Pasos

1. Ejecuta `python sesion03/15_microservicio_multi_backend.py`.
2. Envía peticiones POST indicando `"backend": "openai"` (u otro) y revisa la respuesta.
3. Implementa los clientes reales cuando dispongas de las claves correspondientes.
4. Controla errores para cada backend (timeouts, credenciales faltantes, etc.).

curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" -d '{"prompt":"que puedes hacer por la redaccion de un periodico", "temperature":0.2, "backend":"hf"}'

## Ideas de extensión

- Añadir reglas de enrutado: p.ej. backend por defecto si no se indica.
- Implementar un sistema de “rollout” (porcentaje de tráfico a cada backend).
- Registrar en métricas qué backend atendió cada petición (se usará en el bloque G).

