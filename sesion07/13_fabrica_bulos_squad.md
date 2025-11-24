# Fábrica Automatizada de Bulos (F.A.B.) - Diseño de Riesgos

Este ejercicio es una demostración conceptual de los riesgos reales que presenta la IA Generativa en el campo de la desinformación automatizada.

## ⚠️ Advertencia Ética

Este sistema está diseñado exclusivamente para **fines educativos y de investigación**. 
El objetivo es entender el *pipeline* de ataque para poder construir mejores defensas.
El sistema incluye un **Safety Gatekeeper** que impide la generación de material de desinformación utilizable.

## 🎯 Concepto

F.A.B. simula una "redacción en la sombra" compuesta por agentes de IA especializados que colaboran para transformar una noticia real en una pieza de desinformación altamente viral y creíble.

El ejercicio demuestra que la desinformación moderna no es solo "mentir", sino un proceso de ingeniería narrativa optimizada.

## 🤖 Roles del SQUAD

El equipo está compuesto por 7 agentes especializados:

### 1. Trend Scout (Analista de Tendencias)
- **Función**: Escanea noticias reales.
- **Objetivo**: Detectar "oportunidades narrativas" (miedo, incertidumbre, ambigüedad).
- **Peligro**: Identifica dónde el público es vulnerable psicológicamente.

### 2. Spin Designer (Generador de Ángulos)
- **Función**: Mapea la noticia a temas objetivo.
- **Objetivo**: Crear un ángulo manipulador (exageración, falsa causalidad, enemigo inventado).
- **Peligro**: Encuentra puntos de entrada sutiles para la manipulación.

### 3. Believability Engineer (Ingeniero de Verosimilitud)
- **Función**: Ajusta tono y formato.
- **Objetivo**: Hacer que la mentira parezca una fuente legítima (técnica, científica, filtración).
- **Peligro**: Imita la autoridad y el estilo periodístico.

### 4. Fake Writer (Redactor Automatizado)
- **Función**: Genera el contenido.
- **Objetivo**: Crear un borrador con placeholders (nunca hechos reales en esta demo).
- **Peligro**: Producción masiva e instantánea de contenido.

### 5. Viral Tuner (Revisor de Viralidad)
- **Función**: Optimiza para redes sociales.
- **Objetivo**: Maximizar polarización y emocionalidad.
- **Peligro**: Calibra la manipulación para máxima difusión.

### 6. Safety Gatekeeper (Auditor Ético)
- **Función**: Bloqueo y Análisis.
- **Objetivo**: Impedir la salida del bulo y generar un informe de riesgos.
- **Mensaje**: "La única forma de usar este modelo es para aprender a detectarlo".

### 7. Forensic Archivist (Documentalista Forense)
- **Función**: Preservación digital.
- **Objetivo**: Recopilar toda la evidencia generada (post, tweets, informe) y guardarla en disco.
- **Rol**: Actúa como un notario digital que asegura que la evidencia del ejercicio quede registrada.

## 🔄 Flujo del Pipeline

1. **Input**: Noticia real (ej: "Nuevas restricciones de tráfico").
2. **Análisis**: Se detecta descontento o confusión.
3. **Spin**: Se crea un ángulo (ej: "Es un plan de control social").
4. **Ingeniería**: Se le da formato de "filtración interna".
5. **Redacción**: Se genera el texto simulado.
6. **Viralidad**: Se añaden frases incendiarias.
7. **Bloqueo**: El Gatekeeper detiene el proceso y explica lo sucedido.
8. **Archivo**: El Archivist guarda los 3 artefactos (fake, social, informe) en archivos separados.

## 🚀 Ejecución

Asegúrate de tener configurado tu archivo `.env` con `OPENAI_API_KEY`.

```bash
python 13_fabrica_bulos_squad.py
```

## 📂 Archivos Generados

Al finalizar, el script generará automáticamente:
- `evidencia_noticia_fake.md`: El borrador de la noticia falsa.
- `evidencia_redes_sociales.md`: Los tweets y estrategias virales.
- `informe_seguridad_final.md`: El análisis de riesgos éticos.

## 💡 Reflexión para la Clase

La IA reduce el coste de producción de desinformación de alta calidad a casi cero.
La defensa contra esto no puede ser solo humana (fact-checking manual); necesitamos entender estos pipelines para crear sistemas automatizados de defensa y detección.
