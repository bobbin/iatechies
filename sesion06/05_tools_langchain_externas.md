# Ejercicio 5: Tools que llaman APIs externas

## Objetivo
Aprender a crear tools que interactúan con servicios externos, simulando llamadas a APIs reales. Esto es esencial para agentes que necesitan datos en tiempo real.

## Conceptos Clave (Slides A5-A7)
- **Tools externas**: Conectan el agente con el mundo real a través de APIs.
- **Simulación**: Para desarrollo, podemos simular APIs antes de integrar las reales.
- **Manejo de errores**: Las tools deben manejar fallos de red o APIs no disponibles.

## Qué vamos a hacer
1. Crear 3 tools que simulan APIs externas:
   - `obtener_clima`: API meteorológica
   - `obtener_precio_accion`: API financiera
   - `buscar_web`: Búsqueda web
2. Probar cada tool individualmente.
3. Mostrar cómo se estructuran para uso real.

## Instrucciones
Ejecuta el script:
```bash
python 05_tools_externas.py
```

**Nota**: Estas tools están simuladas. En producción, reemplazarías las funciones internas con llamadas HTTP reales usando `requests` o `httpx`.

