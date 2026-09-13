# JARVIS v1.1

Asistente personal modular en Python.

## v1.1 incluye
- Núcleo conversacional desacoplado del proveedor de IA.
- Memoria local persistente con contexto reciente.
- Registro modular de herramientas.
- Herramientas básicas: hora y estado del sistema.
- Proveedor IA intercambiable (modo demo incluido).
- Configuración preparada mediante variables de entorno.
- Base preparada para voz, wake word, web y automatización de Windows.

## Instalación
Python 3.11+ recomendado.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m jarvis
```

Si no se configura un proveedor de IA, JARVIS funciona en modo demo para probar el núcleo y la memoria.

## Seguridad
JARVIS no ejecuta comandos arbitrarios del sistema en esta versión. Las acciones sensibles deberán pasar por herramientas explícitas y controles de confirmación.
