# Ejercicios MCP (Model Context Protocol)

## ¿Qué es MCP?

**MCP (Model Context Protocol)** es un estándar abierto que permite que los modelos de lenguaje descubran y usen herramientas externas de forma estandarizada.

### Características clave:

- **Protocolo estándar**: No es específico de LangChain, CrewAI o OpenAI
- **Descubrimiento automático**: El cliente descubre qué tools hay disponibles
- **Independiente del framework**: Funciona con cualquier cliente/servidor compatible
- **Escalable**: Múltiples clientes pueden usar el mismo servidor

## Estructura de los ejercicios

### 01_servidor_mcp_minimo.py
Crea un servidor MCP que expone 3 herramientas simples:
- `get_random_fact`: Datos curiosos
- `get_weather`: Clima de ciudades
- `search_books`: Búsqueda de libros

**Cómo ejecutar:**
```bash
python 01_servidor_mcp_minimo.py
```

El servidor espera conexiones de clientes MCP.

### 02_cliente_mcp_python.py
Cliente Python que se conecta al servidor MCP, descubre las tools disponibles y las invoca.

**Cómo ejecutar:**
```bash
# En una terminal, ejecuta el servidor:
python 01_servidor_mcp_minimo.py

# En otra terminal, ejecuta el cliente:
python 02_cliente_mcp_python.py
```

### 03_mcp_con_llm.py
Demuestra cómo un LLM puede usar tools de MCP a través de LangChain.

**Cómo ejecutar:**
```bash
python 03_mcp_con_llm.py
```

Requiere `OPENAI_API_KEY` configurada.

## Uso con VS Code

1. Instala la extensión "Model Context Protocol" en VS Code
2. Configura el servidor MCP en la configuración de VS Code
3. VS Code descubrirá automáticamente las tools
4. Puedes usar el chat de VS Code y el modelo usará las tools automáticamente

## Uso con Claude Desktop

1. Edita el archivo de configuración de Claude Desktop
2. Agrega tu servidor MCP a la lista
3. Claude Desktop descubrirá las tools automáticamente
4. Habla con Claude y usará las tools cuando sea necesario

## Conceptos clave

- **Servidor MCP**: Expone herramientas que los modelos pueden usar
- **Cliente MCP**: Descubre y usa las herramientas del servidor
- **Protocolo estándar**: Funciona con cualquier implementación compatible
- **Descubrimiento dinámico**: No necesitas hardcodear qué tools hay

## Ventajas de MCP

✅ **Separación de responsabilidades**: El servidor expone tools, el cliente las usa
✅ **Independencia**: No está atado a un framework específico
✅ **Escalabilidad**: Múltiples clientes, múltiples servidores
✅ **Extensibilidad**: Agregar tools sin modificar el código del modelo

