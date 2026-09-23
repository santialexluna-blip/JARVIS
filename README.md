# JARVIS v2.5

Asistente personal modular en Python con conversación continua por voz, memoria persistente, sesiones, búsqueda web y HUD opcional.

## Interfaz HUD 2.5

La interfaz incluye un núcleo circular animado, estado visible del micrófono,
registro desplegable y selector de voz. El perfil `JARVIS cinematográfico` usa
la mejor voz masculina británica instalada en Windows. También puedes elegir
la voz española automática o cualquier voz del sistema desde el botón **VOZ**.

JARVIS reconoce variantes habituales del dictado de su nombre, como “Yarvis”,
para que la activación sea más confiable.

## Inteligencia local

JARVIS usa `qwen3:4b` mediante Ollama para contestar preguntas generales y mantener conversaciones sin conexión después de la descarga inicial. Las consultas que dependen de información reciente pueden utilizar la búsqueda web cuando haya Internet.

## Inicio sencillo en Windows

Abre únicamente `JARVIS.bat`. En el primer inicio prepara las dependencias y ejecuta las pruebas; después abre la interfaz de escritorio con conversación por voz, historial, entrada de texto, controles de micrófono y selector de voz.

- Di `Jarvis` una vez para activar la conversación.
- Continúa hablando sin repetir el nombre.
- Di `Jarvis, duerme` para volver al modo de espera.
- Di `Jarvis, salir` para cerrar.
- No requiere tokens ni claves API.

## Corrección v2.1.1
- Se corrigieron los imports que impedían ejecutar el proyecto desde una instalación limpia.
- Se añadió el paquete estable `jarvis/` para recuperar `python -m jarvis`.
- El núcleo v2 usa imports consistentes con la estructura actual.
- Las pruebas usan los módulos reales de la raíz.

## Instalación en Windows
Recomendado: Python 3.11 o superior.

```powershell
cd JARVIS
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
```

Si PowerShell bloquea la activación del entorno, puedes ejecutar directamente:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar JARVIS

```powershell
python -m jarvis
```

También puedes usar:

```powershell
python app.py
```

## Comandos básicos
- `ayuda`
- `hora`
- `sistema`
- `recuerda <texto>`
- `mis notas`
- `busca <consulta>`
- `salir`

## HUD y voz
La interfaz `hud.py` y la capa `voice.py` son opcionales. El núcleo funciona aunque no estén instaladas dependencias de voz.

En Windows, ejecuta `run_voice_test.bat` para comprobar la salida de voz. JARVIS debe decir:
"Hola, soy Jarvis. Mi sistema de voz funciona correctamente."

## Verificación
Antes de usar nuevas funciones, ejecuta:

```powershell
python -m pytest -q
```

El workflow de GitHub Actions también ejecuta las pruebas en cada push a `main` y en pull requests.

## Seguridad
Las acciones del equipo pasan por herramientas explícitas. JARVIS no habilita un intérprete de shell arbitrario desde lenguaje natural y no ejecuta código obtenido de Internet.

## Estado
**v2.1.1 — corrección de estructura y ejecución.**
