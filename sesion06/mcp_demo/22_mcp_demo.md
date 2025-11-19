# Ejercicio 22: Model Context Protocol (MCP)

## Objetivo
Aprender qué es MCP y cómo permite que cualquier LLM descubra y use herramientas externas de forma automática, sin hardcodear las llamadas.

## ¿Qué es MCP?

El **Model Context Protocol (MCP)** es un estándar abierto que:
- Permite que cualquier LLM descubra herramientas automáticamente
- Separa las herramientas del modelo (arquitectura cliente-servidor)
- Es transparente: puedes ver las llamadas en tiempo real
- No depende de un framework específico (no es LangChain, no es OpenAI)

## Conceptos Clave

### Arquitectura Cliente-Servidor

```
┌─────────────┐         ┌──────────────┐
│   Cliente   │ ◄─────► │   Servidor   │
│   (LLM)     │  MCP   │   (Tools)    │
└─────────────┘         └──────────────┘
```

- **Servidor MCP**: Expone herramientas (tools)
- **Cliente MCP**: Descubre y usa las tools
- **Protocolo MCP**: Estándar de comunicación

### Flujo de Trabajo

1. **Descubrimiento**: El cliente pregunta al servidor qué tools tiene
2. **Decisión**: El LLM decide qué tool usar según la pregunta
3. **Invocación**: El cliente llama a la tool vía MCP
4. **Resultado**: El servidor ejecuta y devuelve el resultado
5. **Respuesta**: El LLM usa el resultado para responder al usuario

## Estructura del Ejercicio

Este ejercicio incluye:

1. **`server.py`**: Servidor MCP con 4 tools simples
2. **`ejemplo_cliente.py`**: Cliente de ejemplo (educativo)
3. **`README.md`**: Documentación completa
4. **Configuraciones**: Ejemplos para VS Code y Claude Desktop

## Tools del Servidor

El servidor expone 4 tools:

1. **`get_random_fact()`**: Dato curioso aleatorio
2. **`get_weather(city)`**: Clima de una ciudad (simulado)
3. **`search_books(query)`**: Búsqueda de libros (simulado)
4. **`get_random_word(category)`**: Palabra aleatoria por categoría

## Instrucciones

### Paso 1: Instalar dependencias

```bash
cd sesion06/mcp_demo
pip install -r requirements.txt
```

### Paso 2: Probar el servidor

```bash
python server.py
```

Deberías ver el mensaje de inicio con las tools disponibles.

### Paso 3: Usar con un cliente MCP

**Opción A - VS Code:**
1. Instala la extensión "Model Context Protocol"
2. Configura el servidor en VS Code
3. Abre el chat y pregunta: "¿Qué tiempo hace en Madrid?"
4. Observa cómo el modelo usa `get_weather()` automáticamente

**Opción B - Claude Desktop:**
1. Configura MCP en Claude Desktop
2. Pregunta normalmente a Claude
3. Claude usará las tools cuando sea necesario

**Opción C - Cliente de ejemplo:**
```bash
python ejemplo_cliente.py
```

## Lo que Verás

Cuando uses un cliente MCP compatible:

1. **Descubrimiento automático**:
   - El cliente lista las tools disponibles
   - No necesitas configurar nada manualmente

2. **Invocación transparente**:
   - Ves la llamada a la tool en tiempo real
   - Ves los parámetros que se pasan
   - Ves el resultado que devuelve

3. **Respuesta del LLM**:
   - El modelo usa el resultado para responder
   - Todo el proceso es visible

## ¿Por qué MCP es Importante?

- **Estándar abierto**: No dependes de un vendor específico
- **Desacoplamiento**: Tools y modelo están separados
- **Escalabilidad**: Agregas/quitas tools sin cambiar el modelo
- **Transparencia**: Ves exactamente qué pasa

## Comparación con Otros Enfoques

| Característica | MCP | LangChain Tools | OpenAI Functions |
|---------------|-----|-----------------|------------------|
| Estándar abierto | ✅ | ❌ | ❌ |
| Descubrimiento automático | ✅ | Manual | Manual |
| Cliente-servidor | ✅ | ❌ | ❌ |
| Multi-modelo | ✅ | ✅ | Solo OpenAI |

## Próximos Pasos

1. Ejecuta el servidor y prueba las tools
2. Conecta un cliente MCP real (VS Code o Claude Desktop)
3. Observa cómo el modelo descubre y usa las tools
4. Experimenta agregando nuevas tools al servidor

## Extensión

Puedes extender este ejercicio:
- Agregar más tools al servidor
- Conectar con APIs reales
- Crear un cliente personalizado
- Integrar con otros sistemas

