# Text-to-Speech con OpenAI TTS API

## Objetivo
Generar audio profesional usando la **API TTS de OpenAI**, con voces ultra-realistas.

## Características
- 6 voces predefinidas con diferentes estilos
- 2 modelos: `tts-1` (rápido) y `tts-1-hd` (alta calidad)
- Formatos: MP3, Opus, AAC, FLAC
- Velocidad ajustable: 0.25x a 4.0x

## Instalación

```bash
pip install openai python-dotenv
```

## Configuración

```bash
# Crear archivo .env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

## Scripts Disponibles

### 04a - Síntesis Básica
```bash
python 04a_tts_openai_basico.py
```
- Conectar con API
- Generar audio simple

### 04b - Comparar Voces
```bash
python 04b_tts_openai_voces.py
```
- Las 6 voces: alloy, echo, fable, onyx, nova, shimmer
- Generar muestra de cada una

### 04c - Comparar Modelos
```bash
python 04c_tts_openai_modelos.py
```
- TTS-1 vs TTS-1-HD
- Diferencias de calidad y costo

### 04d - Formatos de Audio
```bash
python 04d_tts_openai_formatos.py
```
- MP3, Opus, AAC, FLAC
- Cuándo usar cada formato

### 04e - Control de Velocidad
```bash
python 04e_tts_openai_velocidad.py
```
- Velocidades de 0.5x a 2.0x
- Casos de uso

### 04f - Audiolibro
```bash
python 04f_tts_openai_audiolibro.py
```
- Convertir texto largo a audio
- Configuración para narración

### 04g - Streaming
```bash
python 04g_tts_openai_streaming.py
```
- Recibir audio en chunks
- Para apps en tiempo real

### 04h - Calculadora de Costos
```bash
python 04h_tts_openai_costos.py
```
- Estimar costos por proyecto
- Comparar modelos

### 04i - Voiceover YouTube
```bash
python 04i_tts_openai_youtube.py
```
- Caso práctico: tutorial
- Configuración para video

## Voces Disponibles

| Voz | Estilo | Uso recomendado |
|-----|--------|-----------------|
| alloy | Neutral | Tutoriales |
| echo | Cálida | Audiolibros |
| fable | Expresiva | Podcasts |
| onyx | Profunda | Documentales |
| nova | Energética | Marketing |
| shimmer | Suave | Meditación |

## Precios (2024)
- **TTS-1**: $15/1M caracteres
- **TTS-1-HD**: $30/1M caracteres

## Referencias
- [OpenAI TTS Docs](https://platform.openai.com/docs/guides/text-to-speech)
- [Precios](https://openai.com/pricing)

