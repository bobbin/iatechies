# Ejemplo 8: Agentes con Herramientas Reales (MCP-like)

Este ejemplo demuestra cómo dar a los agentes capacidades reales de interacción con el sistema, similar al protocolo MCP (Model Context Protocol).

En lugar de "simular" que leemos un archivo, aquí utilizamos las herramientas oficiales `crewai_tools` que implementan la lógica real de lectura y escritura en disco.

## 🛠️ Herramientas Utilizadas

1.  **FileReadTool**: Permite al agente leer el contenido real de archivos `.txt`, `.md`, etc.
2.  **FileWriterTool**: Permite al agente crear y escribir archivos en el disco.
3.  **DirectoryReadTool**: Permite al agente listar el contenido de carpetas.

## 🏗️ Arquitectura del Ejemplo

El sistema configura un "Sandbox" (carpeta `sesion07/data_mcp`) para que los agentes trabajen sin riesgo de dañar otros archivos.

1.  **Setup**: El script crea un archivo inicial `notas_proyecto.txt`.
2.  **Agente Gestor**: Usa `DirectoryReadTool` para explorar y `FileReadTool` para leer.
3.  **Agente Analista**: Procesa la información y decide actualizaciones.
4.  **Agente Gestor**: Usa `FileWriterTool` para guardar los cambios en un archivo nuevo `notas_actualizadas_v2.txt`.

## 🚀 Ejecución

Asegúrate de tener instaladas las herramientas adicionales:

```bash
pip install crewai-tools
```

Ejecuta el script:

```bash
python 08_agentes_mcp.py
```

Al finalizar, verás que se ha creado físicamente una carpeta `data_mcp` con los archivos generados por la IA.

## 🧠 ¿Qué es MCP Realmente?

El **Model Context Protocol (MCP)** es un estándar abierto que permite conectar modelos de IA a fuentes de datos (GitHub, Google Drive, Slack, Postgres) de forma universal.

Aunque este ejemplo usa herramientas locales ("Tools"), el patrón es idéntico:
- El Agente tiene una "interfaz" (Tool).
- El Agente envía una acción estructurada (JSON).
- La Tool ejecuta la acción en el sistema real.
- El Agente recibe el resultado y continúa.
