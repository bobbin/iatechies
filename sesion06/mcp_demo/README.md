# Ejercicio: Model Context Protocol (MCP)

## ¿Qué es MCP?

El **Model Context Protocol (MCP)** es un estándar abierto que permite que cualquier LLM descubra y use herramientas externas de forma automática, sin necesidad de hardcodear las llamadas.

### Características clave:

- **Estándar abierto**: No es específico de LangChain, CrewAI o OpenAI
- **Descubrimiento automático**: El cliente descubre las tools disponibles
- **Protocolo cliente-servidor**: Separación clara entre herramientas y modelo
- **Transparente**: Puedes ver las llamadas en tiempo real

## Estructura del Ejercicio

```
mcp_demo/
├── server.py          # Servidor MCP con tools
├── README.md          # Esta documentación
├── requirements.txt   # Dependencias
└── config_examples/   # Ejemplos de configuración
```

## Instalación

1. **Instalar dependencias**:
```bash
cd sesion06/mcp_demo
pip install -r requirements.txt
```

2. **Verificar instalación**:
```bash
python server.py
```

Deberías ver el mensaje de inicio del servidor.

## Uso con VS Code

### Opción A: Extensión MCP de VS Code

1. **Instalar la extensión**:
   - Abre VS Code
   - Busca "Model Context Protocol" en el marketplace
   - Instala la extensión oficial

2. **Configurar el servidor**:
   - La extensión detectará automáticamente servidores MCP locales
   - O configura manualmente en la configuración de VS Code

3. **Usar en el chat**:
   - Abre el panel de chat de VS Code
   - Verás las tools disponibles listadas
   - Pregunta algo como: "¿Qué tiempo hace en Madrid?"
   - El modelo usará automáticamente `get_weather("Madrid")`

### Opción B: Claude Desktop

1. **Instalar Claude Desktop** (si no lo tienes)

2. **Configurar MCP en Claude Desktop**:
   - Edita el archivo de configuración de Claude Desktop
   - Agrega la configuración del servidor MCP
   - Reinicia Claude Desktop

3. **Usar las tools**:
   - Claude detectará automáticamente las tools
   - Pregunta normalmente y Claude usará las tools cuando sea necesario

## Tools Disponibles

El servidor expone 4 tools simples:

1. **`get_random_fact()`**
   - Devuelve un dato curioso aleatorio
   - Sin parámetros

2. **`get_weather(city: str)`**
   - Obtiene el clima de una ciudad
   - Parámetro: nombre de la ciudad

3. **`search_books(query: str)`**
   - Busca libros por tema
   - Parámetro: términos de búsqueda

4. **`get_random_word(category: str)`**
   - Genera una palabra aleatoria
   - Parámetro opcional: categoría (objeto, lugar, animal, general)

## Ejemplos de Uso

### Ejemplo 1: Dato curioso
```
Usuario: "Dime un dato curioso"
→ LLM detecta get_random_fact()
→ Llama a la tool
→ Recibe: {"fact": "Los pulpos tienen tres corazones."}
→ Responde: "Sabías que los pulpos tienen tres corazones? Es uno de los datos más impactantes..."
```

### Ejemplo 2: Clima
```
Usuario: "¿Qué tiempo hace en Madrid?"
→ LLM detecta get_weather()
→ Llama: get_weather("Madrid")
→ Recibe: {"city": "Madrid", "temperature": "22°C", "condition": "Soleado"}
→ Responde: "En Madrid hace 22°C y está soleado."
```

### Ejemplo 3: Búsqueda de libros
```
Usuario: "Recomiéndame libros sobre inteligencia artificial"
→ LLM detecta search_books()
→ Llama: search_books("inteligencia artificial")
→ Recibe lista de libros
→ Responde con recomendaciones estructuradas
```

## ¿Qué Verás en la Demo?

Cuando uses un cliente MCP compatible, verás:

1. **Descubrimiento automático**:
   ```
   Connected MCP servers:
   - demo-escape-room
   
   Tools disponibles:
   - get_random_fact
   - get_weather
   - search_books
   - get_random_word
   ```

2. **Invocación en tiempo real**:
   ```
   Calling tool: get_weather("Madrid")...
   Result: {"city": "Madrid", "temperature": "22°C", ...}
   ```

3. **Respuesta final del LLM**:
   ```
   "En Madrid hace 22°C y está soleado. Es un día perfecto para salir."
   ```

## Conceptos Clave

### ¿Por qué MCP es importante?

- **Estándar abierto**: No dependes de un framework específico
- **Desacoplamiento**: Las tools viven en servidores separados
- **Escalabilidad**: Puedes agregar/quitar tools sin cambiar el modelo
- **Transparencia**: Ves exactamente qué tools se usan y cuándo

### Diferencias con otros enfoques:

| Característica | MCP | LangChain Tools | OpenAI Functions |
|---------------|-----|-----------------|------------------|
| Estándar abierto | ✅ | ❌ | ❌ |
| Descubrimiento automático | ✅ | Manual | Manual |
| Cliente-servidor | ✅ | ❌ | ❌ |
| Multi-modelo | ✅ | ✅ | Solo OpenAI |

## Próximos Pasos

1. Ejecuta el servidor: `python server.py`
2. Conecta un cliente MCP (VS Code o Claude Desktop)
3. Prueba las diferentes tools
4. Observa cómo el modelo descubre y usa las tools automáticamente

## Extensión

Puedes extender este ejercicio:
- Agregar más tools al servidor
- Conectar con APIs reales (en lugar de simuladas)
- Crear un cliente MCP personalizado
- Integrar con otros sistemas

