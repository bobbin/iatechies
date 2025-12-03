# Speech-to-Text con OpenAI Whisper API

## Objetivo
Transcribir audio a texto usando la **API de Whisper de OpenAI**, un servicio cloud profesional de alta precisión.

## ¿Qué es OpenAI Whisper API?
- Servicio cloud de transcripción de audio
- Basado en el modelo Whisper de OpenAI
- Alta precisión y soporte multiidioma
- Modelo large-v3 optimizado

## Ventajas
✅ **Alta Precisión**: Modelo large-v3 estado del arte  
✅ **Sin Hardware**: No requiere GPU ni recursos locales  
✅ **99+ Idiomas**: Incluyendo español, catalán, gallego, euskera  
✅ **Bajo Costo**: $0.006 por minuto de audio  

## Desventajas
❌ **Requiere API Key**: Necesitas cuenta de OpenAI  
❌ **Costo**: Aunque bajo, no es gratis  
❌ **Privacidad**: Los audios se envían a servidores de OpenAI  
❌ **Límites**: Archivos hasta 25 MB  

## Instalación

```bash
pip install openai python-dotenv gtts
```

## Configuración

```bash
# Crear archivo .env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

## Scripts Disponibles

### 02a - Transcripción Básica
```bash
python 02a_stt_openai_basico.py
```
- Conectar con API de OpenAI
- Transcribir archivo de audio
- Ver costo estimado

### 02b - Con Timestamps
```bash
python 02b_stt_openai_timestamps.py
```
- Usar response_format="verbose_json"
- Obtener idioma, duración y segmentos

### 02c - Traducción Automática
```bash
python 02c_stt_openai_traduccion.py
```
- Transcribir Y traducir a inglés
- Comparar original vs traducción

### 02d - Generar Subtítulos SRT
```bash
python 02d_stt_openai_subtitulos.py
```
- Generar archivo .srt directamente
- También disponible formato .vtt

### 02e - Múltiples Formatos
```bash
python 02e_stt_openai_formatos.py
```
- Probar diferentes formatos de audio
- Ver límites y compatibilidad

### 02f - Archivos Grandes
```bash
python 02f_stt_openai_archivos_grandes.py
```
- Estrategias para archivos >25 MB
- Código para dividir en chunks

### 02g - Detectar Idioma
```bash
python 02g_stt_openai_detectar_idioma.py
```
- Detección automática de idioma
- Comparar con idioma especificado

### 02h - Calculadora de Costos
```bash
python 02h_stt_openai_costos.py
```
- Estimar costos por duración
- Comparación con alternativas

## Precios (2024)
- **Whisper**: $0.006 / minuto (~$0.36 por hora)
- Sin costos adicionales por idioma

## Comparación con Faster-Whisper Local

| Característica | OpenAI API | Faster-Whisper Local |
|----------------|-----------|----------------------|
| Precisión | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Velocidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Costo | $0.006/min | Gratis |
| Privacidad | ❌ Cloud | ✅ 100% Local |
| Límite tamaño | 25 MB | Sin límite |

## Referencias
- [OpenAI Whisper API Docs](https://platform.openai.com/docs/guides/speech-to-text)
- [Precios](https://openai.com/pricing)

