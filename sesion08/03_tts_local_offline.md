# Text-to-Speech Local Offline

## Objetivo
Generar audio (voz) a partir de texto usando **pyttsx3** y **Coqui TTS**, soluciones completamente locales y gratuitas.

## ¿Qué es Text-to-Speech Local?
Motores de síntesis de voz que funcionan 100% offline:
- **pyttsx3**: Usa las voces del sistema operativo
- **Coqui TTS**: Modelos de IA open source de alta calidad

## Ventajas
✅ **100% Gratuito**: Sin costos ni suscripciones  
✅ **Privacidad Total**: El texto no sale de tu equipo  
✅ **Sin Internet**: Funciona completamente offline  
✅ **Sin Límites**: Genera todo el audio que necesites  

## Instalación

```bash
pip install pyttsx3 TTS
```

## Scripts Disponibles

### pyttsx3 (Voces del Sistema)

#### 03a - Síntesis Básica
```bash
python 03a_tts_pyttsx3_basico.py
```
- Inicializar motor TTS
- Reproducir texto como voz

#### 03b - Listar Voces
```bash
python 03b_tts_pyttsx3_voces.py
```
- Ver voces instaladas en el sistema
- Probar diferentes voces

#### 03c - Configuración
```bash
python 03c_tts_pyttsx3_config.py
```
- Ajustar velocidad y volumen
- Cambiar de voz

#### 03d - Guardar Audio
```bash
python 03d_tts_pyttsx3_guardar.py
```
- Guardar síntesis en archivo .wav

### Coqui TTS (Modelos IA)

#### 03e - Coqui Básico
```bash
python 03e_tts_coqui_basico.py
```
- Modelo español de alta calidad
- tts_models/es/css10/vits

#### 03f - Multilingüe (XTTS v2)
```bash
python 03f_tts_coqui_multilingue.py
```
- Modelo multilingüe (16+ idiomas)
- Modelo grande (~2GB)

#### 03g - Archivo de Texto
```bash
python 03g_tts_archivo_texto.py
```
- Leer archivo .txt y convertir a audio

#### 03h - Modelos Disponibles
```bash
python 03h_tts_coqui_modelos.py
```
- Listar todos los modelos de Coqui
- Modelos recomendados

#### 03i - Comparación
```bash
python 03i_tts_comparacion.py
```
- Comparar pyttsx3 vs Coqui TTS
- Velocidad vs calidad

## Comparación

| Característica | pyttsx3 | Coqui TTS |
|----------------|---------|-----------|
| Velocidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Calidad | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup | Muy fácil | Medio |
| Tamaño | ~0 MB | ~500MB+ |

## Referencias
- [pyttsx3 Docs](https://pyttsx3.readthedocs.io/)
- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)

