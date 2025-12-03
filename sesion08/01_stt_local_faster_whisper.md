# Speech-to-Text Local con Faster-Whisper

## Objetivo
Transcribir audio a texto usando **Faster-Whisper**, una versión optimizada del modelo Whisper de OpenAI que corre completamente en local.

## ¿Qué es Faster-Whisper?
- Implementación optimizada de Whisper usando CTranslate2
- Hasta 4x más rápido que whisper original
- Menor consumo de memoria
- Soporte para CPU y GPU
- Totalmente local y gratuito

## Ventajas
✅ **100% Local**: No envía datos a servidores externos  
✅ **Privacidad**: Ideal para datos sensibles  
✅ **Sin costos**: No requiere API keys ni suscripciones  
✅ **Rápido**: Optimizado para inferencia  
✅ **Multiidioma**: Soporta 99+ idiomas incluyendo español  

## Instalación

```bash
pip install faster-whisper gtts
```

## Modelos Disponibles

| Modelo | Parámetros | VRAM | Velocidad | Precisión |
|--------|-----------|------|-----------|-----------|
| tiny   | 39M       | ~1GB | Muy rápida | Baja |
| base   | 74M       | ~1GB | Rápida | Media |
| small  | 244M      | ~2GB | Media | Buena |
| medium | 769M      | ~5GB | Lenta | Muy buena |
| large-v3 | 1550M   | ~10GB | Muy lenta | Excelente |

## Scripts Disponibles

### 01a - Transcripción Básica
```bash
python 01a_stt_faster_whisper_basico.py
```
- Cargar modelo Whisper
- Transcribir archivo de audio
- Obtener info del audio (idioma, duración)

### 01b - Con Timestamps
```bash
python 01b_stt_faster_whisper_timestamps.py
```
- Timestamps por segmento
- Timestamps por palabra
- Formateo de tiempos

### 01c - Generar Subtítulos SRT
```bash
python 01c_stt_faster_whisper_subtitulos.py
```
- Crear archivo .srt
- Formato compatible con reproductores

### 01d - Detección de Idioma
```bash
python 01d_stt_faster_whisper_idioma.py
```
- Detección automática sin especificar idioma
- Probabilidad de detección

### 01e - Batch (Múltiples Archivos)
```bash
python 01e_stt_faster_whisper_batch.py
```
- Transcribir todos los archivos de un directorio
- Guardar resultados en archivo

### 01f - Configuración Avanzada
```bash
python 01f_stt_faster_whisper_config.py
```
- Comparar modelos (tiny, base, small)
- Ajustar beam_size y compute_type
- Velocidad vs precisión

## Notas
- Requiere archivos de audio en formatos: WAV, MP3, M4A, FLAC, OGG
- En Windows puede requerir instalar ffmpeg
- Primera ejecución descarga el modelo (~150MB - 3GB)

## Referencias
- [Faster-Whisper GitHub](https://github.com/guillaumekln/faster-whisper)
- [Whisper Original](https://github.com/openai/whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)

