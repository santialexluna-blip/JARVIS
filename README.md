# JARVIS v2.1.1

Asistente personal modular en Python con núcleo conversacional, memoria persistente, sesiones, búsqueda web y HUD/voz opcionales.

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
