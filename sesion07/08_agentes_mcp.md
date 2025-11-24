# Ejemplo 8: Agentes con MCP Real (Airbnb Live)

Este ejemplo demuestra el uso del protocolo **MCP (Model Context Protocol)** conectando un agente de CrewAI con un servicio real de terceros.

Usamos el servidor MCP de la comunidad **`@openbnb/mcp-server-airbnb`**, que permite realizar búsquedas reales en Airbnb.com sin necesidad de API Keys (utiliza scraping/navegación pública).

## 🏗️ Arquitectura

1.  **Servidor MCP**: Paquete NPM `@openbnb/mcp-server-airbnb`.
    *   Ejecutado vía `npx -y @openbnb/mcp-server-airbnb`.
    *   Este proceso corre en segundo plano y habla el protocolo JSON-RPC sobre STDIO.
2.  **Adaptador**: CrewAI (`MCPServerAdapter`) se conecta a ese proceso STDIO.
3.  **Agente**: Recibe herramientas dinámicas como `search` o `get_listing_details`.

## 🚀 Requisitos

1.  **Node.js**: Necesario para ejecutar `npx`.
2.  **Python**: Dependencias `mcp` y `crewai-tools`.

## 🏃 Ejecución

```bash
python 08_agentes_mcp.py
```

## ⚠️ Nota sobre Robots y Bloqueos

Este servidor MCP realiza peticiones web a Airbnb.
- Es posible que si haces muchas peticiones, Airbnb bloquee temporalmente tu IP o pida captchas.
- El servidor MCP intenta respetar `robots.txt` y usar cabeceras adecuadas, pero no es una API oficial.

## 🧠 Diferencia con Herramientas Tradicionales

Tradicionalmente, tendrías que:
1. Buscar una API de Airbnb (que es privada/difícil de conseguir).
2. Escribir código Python para llamar a esa API.
3. Crear una clase `AirbnbTool`.

Con MCP:
1. Ejecutas el servidor MCP estandarizado (hecho por la comunidad).
2. El Agente "descubre" las herramientas automáticamente.
3. **Cero código de integración** específico para Airbnb en tu script.
