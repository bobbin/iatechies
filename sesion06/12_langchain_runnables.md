# Ejercicio 12: Pipelines con Runnables en LangChain

## Objetivo
Aprender a usar Runnables para crear pipelines componibles sin necesidad de un agente completo. Los Runnables son la base de LangChain moderna.

## ¿Qué son los Runnables?

Los **Runnables** son componentes en LangChain que pueden ejecutarse (run) y componerse entre sí. Son la abstracción fundamental que permite crear pipelines de procesamiento.

### Características principales:

1. **Composición con `|`**: Puedes encadenar Runnables usando el operador pipe (`|`):
   ```python
   pipeline = prompt | llm | parser
   ```

2. **Tipos de Runnables**:
   - **Prompts** (`ChatPromptTemplate`): Preparan el input para el LLM
   - **LLMs** (`ChatOpenAI`): Modelos de lenguaje
   - **Parsers** (`StrOutputParser`): Procesan la salida del LLM
   - **Tools**: Funciones que el agente puede usar
   - **RunnableLambda**: Funciones Python personalizadas
   - **RunnablePassthrough**: Pasa los datos sin modificar

3. **Ventajas**:
   - **Deterministas**: El flujo es predecible y siempre igual
   - **Eficientes**: No tienen la sobrecarga de un agente completo
   - **Componibles**: Se pueden combinar como piezas de LEGO
   - **Reutilizables**: Un mismo Runnable puede usarse en múltiples pipelines

### RunnablePassthrough vs RunnableLambda:

- **`RunnablePassthrough()`**: Pasa los datos tal cual, sin modificarlos. Útil para mantener datos en el pipeline.
- **`RunnableLambda(func)`**: Ejecuta una función Python personalizada. Permite transformar los datos.

### Ejemplo de composición:

```python
# Pipeline simple: prompt → LLM → parser
pipeline = prompt | llm | parser

# Pipeline con diccionario (procesa múltiples campos en paralelo)
pipeline = {
    "resumen": prompt1 | llm | parser,
    "tema": prompt2 | llm | parser,
}

# Pipeline con función personalizada
pipeline = RunnableLambda(extraer_tema) | prompt | llm | parser
```

## Conceptos Clave (Slides B7, B11)
- **Runnables**: Componentes que se pueden componer usando el operador `|`.
- **Pipelines**: Flujos de procesamiento deterministas.
- **Composición**: Los Runnables se pueden combinar como LEGO.
- **Cuándo usarlos**: Para flujos deterministas, sin necesidad de decisiones dinámicas.

## Cuándo usar Runnables vs Agentes

**Usa Runnables cuando:**
- El flujo es determinista (siempre el mismo proceso)
- No necesitas decisiones dinámicas
- Quieres procesamiento rápido y eficiente
- Necesitas transformaciones secuenciales de datos

**Usa Agentes cuando:**
- Necesitas decisiones dinámicas
- El orden de las acciones no está claro
- Necesitas que el modelo decida qué tool usar
- El objetivo puede dividirse en varios pasos variables

## Qué vamos a hacer
1. Crear pipelines simples con Runnables.
2. Componer pipelines más complejos.
3. Integrar funciones personalizadas en los pipelines.
4. Comparar con el uso de agentes (cuándo usar cada uno).

## Instrucciones
Ejecuta el script:
```bash
python 12_langchain_runnables.py
```

**Nota**: Requiere `OPENAI_API_KEY`. Observa cómo los Runnables permiten crear pipelines eficientes sin la sobrecarga de un agente.

