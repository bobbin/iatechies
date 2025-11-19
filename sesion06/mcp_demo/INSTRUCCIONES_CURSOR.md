# Cómo configurar MCP en Cursor

## Paso 1: Localizar el archivo de configuración

El archivo de configuración de MCP en Cursor está en:
- **Windows**: `C:\Users\<tu_usuario>\.cursor\mcp.json`
- **macOS/Linux**: `~/.cursor/mcp.json`

## Paso 2: Añadir la configuración del servidor

Abre el archivo `mcp.json` y añade la configuración del servidor:

```json
{
  "mcpServers": {
    "demo-escape-room": {
      "command": "python",
      "args": [
        "D:\\DEV\\IATechies\\iatechies\\sesion06\\mcp_demo\\server.py"
      ],
      "cwd": "D:\\DEV\\IATechies\\iatechies\\sesion06\\mcp_demo"
    }
  }
}
```

### ⚠️ Importante: Ajustar las rutas

**Reemplaza las rutas con las tuyas:**
- `D:\\DEV\\IATechies\\iatechies` → Tu ruta al proyecto
- Asegúrate de usar barras invertidas dobles (`\\`) en Windows
- O usa barras normales (`/`) que también funcionan en Windows

### Ejemplo con rutas relativas (si es posible):

Si Cursor soporta rutas relativas desde el workspace:

```json
{
  "mcpServers": {
    "demo-escape-room": {
      "command": "python",
      "args": [
        "${workspaceFolder}/sesion06/mcp_demo/server.py"
      ],
      "cwd": "${workspaceFolder}/sesion06/mcp_demo"
    }
  }
}
```

## Paso 3: Verificar que Python está en el PATH

Asegúrate de que `python` está disponible en tu PATH. Si usas `python3`, cambia:

```json
"command": "python3"
```

## Paso 4: Reiniciar Cursor

Después de guardar el archivo `mcp.json`:
1. Cierra completamente Cursor
2. Vuelve a abrirlo
3. El servidor MCP debería conectarse automáticamente

## Paso 5: Verificar la conexión

1. Abre el chat de Cursor
2. Deberías ver las tools disponibles listadas
3. Prueba preguntando: "¿Qué tiempo hace en Madrid?"
4. El modelo debería usar automáticamente `get_weather("Madrid")`

## Troubleshooting

### El servidor no se conecta

1. **Verifica que el servidor funciona**:
   ```bash
   cd sesion06/mcp_demo
   python server.py
   ```
   Deberías ver el mensaje de inicio.

2. **Verifica las rutas**:
   - Asegúrate de que las rutas en `mcp.json` son correctas
   - Usa rutas absolutas si las relativas no funcionan

3. **Verifica Python**:
   - Asegúrate de que `python` está en tu PATH
   - Prueba ejecutando `python --version` en la terminal

4. **Revisa los logs de Cursor**:
   - Cursor puede mostrar errores en la consola de desarrollador
   - Abre: Help → Toggle Developer Tools

### Las tools no aparecen

1. Reinicia Cursor completamente
2. Verifica que el servidor se está ejecutando
3. Comprueba que el archivo `mcp.json` tiene la sintaxis correcta (JSON válido)

## Tools disponibles

Una vez configurado, tendrás acceso a:

- `get_random_fact()` - Dato curioso aleatorio
- `get_weather(city)` - Clima de una ciudad
- `search_books(query)` - Búsqueda de libros
- `get_random_word(category)` - Palabra aleatoria

## Ejemplos de uso

```
Usuario: "¿Qué tiempo hace en Madrid?"
→ Cursor detecta get_weather()
→ Llama: get_weather("Madrid")
→ Responde con el clima

Usuario: "Dame un dato curioso"
→ Cursor detecta get_random_fact()
→ Llama: get_random_fact()
→ Responde con un dato interesante
```

