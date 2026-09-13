# JARVIS v1.0

Asistente personal modular en Python. Esta primera versión prioriza una arquitectura limpia y segura:
- Núcleo conversacional desacoplado del proveedor de IA.
- Memoria local en JSON.
- Herramientas para hora, sistema y apertura controlada de aplicaciones.
- Interfaz de terminal.
- Variables de entorno para credenciales.
- Confirmación antes de acciones potencialmente sensibles.

## Requisitos
Python 3.11+ recomendado.

## Instalación
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m jarvis
```

## Próximas capas
Voz STT/TTS, wake word, proveedor LLM, búsquedas web, automatización avanzada del PC y GUI.

> JARVIS no ejecuta comandos arbitrarios del sistema en esta versión.
