# RAG Agéntico Jerárquico

## Concepto

Este ejercicio demuestra un sistema **RAG (Retrieval Augmented Generation) jerárquico** donde un agente navega inteligentemente una estructura de documentos organizada en tres niveles:

1. **Índice Maestro**: Contiene la estructura general y referencia todas las secciones
2. **Índices de Sección**: Cada sección tiene su propio índice que lista documentos específicos
3. **Documentos Específicos**: Documentos detallados con la información real

## Arquitectura del Sistema

### Estructura de Directorios

```
rag_jerarquico/
├── indice_maestro.md                    # Nivel 1: Índice general
├── seccion_01_instalacion/
│   ├── indice_seccion_01.md            # Nivel 2: Índice de sección
│   ├── 01_requisitos_sistema.md        # Nivel 3: Documento específico
│   ├── 02_instalacion_basica.md
│   └── ...
├── seccion_02_configuracion/
│   ├── indice_seccion_02.md
│   └── ...
└── ...
```

### Flujo de Navegación

```
Usuario hace consulta
        ↓
Agente lee Índice Maestro (Nivel 1)
        ↓
Identifica sección relevante
        ↓
Agente lee Índice de Sección (Nivel 2)
        ↓
Selecciona documento específico
        ↓
Agente lee Documento Específico (Nivel 3)
        ↓
Proporciona respuesta basada en información encontrada
```

## Diseño del Agente

### Herramientas Disponibles

1. **`leer_indice_maestro()`**: Lee el índice general del manual
2. **`leer_indice_seccion(numero)`**: Lee el índice de una sección específica
3. **`leer_documento(seccion, nombre)`**: Lee un documento específico
4. **`listar_documentos_seccion(seccion)`**: Lista documentos disponibles en una sección

### Características del Agente

- **Navegación Inteligente**: Sigue siempre la jerarquía Índice Maestro → Índice Sección → Documento
- **Búsqueda Eficiente**: No lee documentos innecesarios, consulta índices primero
- **Referencias Específicas**: Proporciona referencias a secciones y documentos consultados
- **Manejo de Errores**: Maneja documentos faltantes y proporciona alternativas

## Ventajas del Enfoque Jerárquico

### 1. Eficiencia
- **Menos tokens**: Solo lee documentos relevantes, no todo el manual
- **Búsqueda rápida**: Los índices permiten localizar información rápidamente
- **Coste reducido**: Menos llamadas a la API al evitar leer documentos innecesarios

### 2. Escalabilidad
- **Fácil expansión**: Agregar nuevas secciones/documentos no afecta el rendimiento
- **Organización clara**: La estructura jerárquica facilita el mantenimiento
- **Búsqueda dirigida**: Los índices guían al agente hacia información relevante

### 3. Precisión
- **Contexto apropiado**: El agente siempre tiene contexto sobre dónde buscar
- **Información estructurada**: Los índices proporcionan metadatos sobre el contenido
- **Referencias claras**: Fácil rastrear de dónde viene la información

## Casos de Uso

### Caso 1: Consulta Específica
**Consulta**: "¿Cuáles son los requisitos del sistema?"

**Proceso**:
1. Agente lee índice maestro → Identifica Sección 1 (Instalación)
2. Agente lee índice sección 1 → Encuentra "01_requisitos_sistema.md"
3. Agente lee documento específico → Extrae información sobre requisitos
4. Agente responde con detalles específicos

### Caso 2: Consulta que Requiere Múltiples Documentos
**Consulta**: "Necesito instalar y configurar el sistema"

**Proceso**:
1. Agente lee índice maestro → Identifica Secciones 1 y 2
2. Agente consulta ambas secciones y sus índices
3. Agente lee documentos relevantes de ambas secciones
4. Agente sintetiza información de múltiples fuentes

### Caso 3: Consulta Ambigua
**Consulta**: "Tengo un problema"

**Proceso**:
1. Agente lee índice maestro → Identifica múltiples secciones posibles
2. Agente consulta secciones relevantes (Troubleshooting, Uso, etc.)
3. Agente puede hacer preguntas de seguimiento o proporcionar opciones
4. Agente guía al usuario hacia la información correcta

## Implementación Técnica

### Herramientas con Manejo de Errores

Cada herramienta incluye:
- Validación de parámetros
- Manejo de archivos faltantes
- Mensajes de error descriptivos
- Sugerencias de alternativas

### Proceso de Tarea

La tarea del agente está diseñada para:
1. Forzar el uso de la jerarquía
2. Proporcionar instrucciones claras sobre el proceso
3. Requerir referencias específicas en las respuestas
4. Permitir consultas adicionales si es necesario

## Ejemplos de Consultas

### Consultas de Instalación
- "¿Qué requisitos necesito para instalar el sistema?"
- "¿Cómo instalo el software paso a paso?"
- "¿Puedo instalar en Docker?"

### Consultas de Configuración
- "¿Cómo configuro las variables de entorno?"
- "¿Qué configuración necesito para producción?"
- "¿Cómo integro APIs externas?"

### Consultas de Uso
- "¿Cómo creo mi primer agente?"
- "¿Qué casos de uso básicos puedo implementar?"
- "¿Cuáles son las mejores prácticas?"

### Consultas de Troubleshooting
- "Tengo un error de API key, ¿qué hago?"
- "¿Cómo diagnostico problemas del sistema?"
- "¿Cómo recupero datos después de un error?"

## Extensión del Sistema

### Agregar Nuevas Secciones

1. Crear directorio: `seccion_XX_nombre/`
2. Crear `indice_seccion_XX.md`
3. Agregar documentos específicos
4. Actualizar `indice_maestro.md` con referencia a la nueva sección

### Agregar Documentos a Secciones Existentes

1. Crear nuevo documento en la sección correspondiente
2. Actualizar `indice_seccion_XX.md` con referencia al nuevo documento
3. El agente automáticamente podrá acceder al nuevo documento

## Comparación con RAG Tradicional

### RAG Tradicional (Plano)
- Lee todos los documentos o hace búsqueda vectorial
- Puede leer información irrelevante
- Coste alto en tokens
- Difícil de escalar

### RAG Jerárquico (Este Ejemplo)
- Consulta índices primero para localizar información
- Solo lee documentos relevantes
- Coste optimizado
- Escalable y mantenible

## Conclusiones

### Ventajas Clave

1. **Eficiencia**: Reduce significativamente el número de tokens procesados
2. **Precisión**: Los índices guían al agente hacia información relevante
3. **Escalabilidad**: Fácil agregar nuevas secciones sin afectar rendimiento
4. **Mantenibilidad**: Estructura clara facilita actualizaciones
5. **Experiencia de Usuario**: Respuestas más rápidas y precisas

### Aplicaciones Prácticas

- **Documentación técnica**: Manuales extensos con múltiples secciones
- **Bases de conocimiento**: Sistemas de ayuda con información organizada
- **Wikis corporativas**: Documentación interna estructurada
- **Sistemas de soporte**: FAQs y guías organizadas jerárquicamente

### Mejoras Futuras

- **Búsqueda semántica**: Combinar jerarquía con búsqueda vectorial
- **Caché inteligente**: Guardar índices consultados frecuentemente
- **Múltiples agentes**: Especialistas por sección que colaboran
- **Feedback loop**: Aprender qué documentos son más útiles para cada tipo de consulta

## Ejecución

```bash
python sesion07/15_rag_jerarquico.py
```

El sistema te permitirá:
1. Seleccionar una consulta de ejemplo
2. Ingresar tu propia consulta personalizada
3. Ver cómo el agente navega la jerarquía paso a paso
4. Obtener una respuesta completa con referencias

## Notas Finales

Este ejercicio demuestra cómo la **organización jerárquica** puede mejorar significativamente la eficiencia de sistemas RAG, especialmente cuando se trata con documentación extensa. El enfoque es particularmente útil cuando:

- La documentación es muy extensa (>100 páginas)
- Hay una estructura clara y organizada
- Se necesita precisión en las respuestas
- El coste de tokens es una preocupación
- Se requiere trazabilidad de fuentes

El sistema RAG jerárquico combina lo mejor de ambos mundos: la precisión de la búsqueda dirigida con la flexibilidad de la generación asistida por recuperación.

