# JARVIS v2.0

Asistente personal modular en Python con núcleo conversacional, memoria persistente, sesiones, búsqueda web y herramientas explícitas.

## v2.0 incluye
- Núcleo unificado `JarvisCore`.
- Proveedor de IA intercambiable.
- Memoria persistente local.
- Memoria de conversación aislada por sesión.
- Búsqueda web mediante HTTPS.
- Herramientas modulares para funciones del sistema.
- Integración Windows segura sin comandos arbitrarios.

## Instalación
Python 3.11+ recomendado.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m jarvis
```

## Búsqueda
Puedes usar:

```text
busca noticias de tecnología
```

La búsqueda solo recupera información; JARVIS no ejecuta código ni comandos obtenidos de Internet.

## Seguridad
Las acciones del equipo deben pasar por herramientas explícitas y limitadas. No se habilita un intérprete de shell arbitrario para lenguaje natural.

## Estado
v2.0 — núcleo unificado instalado. Las capas de voz avanzada, GUI/HUD y automatización ampliada quedan para las siguientes versiones.
