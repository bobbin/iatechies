# Instrucciones para usar MCP con VS Code

## Paso 1: Instalar la extensión MCP

1. Abre VS Code
2. Ve a Extensions (Ctrl+Shift+X)
3. Busca "Model Context Protocol" o "MCP"
4. Instala la extensión oficial

## Paso 2: Configurar el servidor MCP

1. Abre la configuración de VS Code (Ctrl+,)
2. Busca "MCP" en la configuración
3. Agrega la configuración del servidor:

```json
{
  "mcp.servers": {
    "demo-escape-room": {
      "command": "python",
      "args": ["D:/DEV/IATechies/iatechies/sesion06/mcp_demo/server.py"],
      "cwd": "D:/DEV/IATechies/iatechies/sesion06/mcp_demo"
    }
  }
}
```

**Nota**: Ajusta las rutas según tu sistema.

## Paso 3: Usar el servidor

1. Reinicia VS Code
2. Abre el panel de chat (si la extensión lo tiene)
3. Deberías ver las tools disponibles listadas
4. Pregunta algo como: "¿Qué tiempo hace en Madrid?"
5. Observa cómo el modelo usa `get_weather()` automáticamente

## Alternativa: Usar el CLI de MCP

Si la extensión no funciona, puedes usar el CLI oficial de MCP para probar el servidor.

