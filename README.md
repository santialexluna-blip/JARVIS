# JARVIS v1.3

Asistente personal modular en Python, evolucionando desde el núcleo v1.1 hacia integración segura con Windows.

## Incluye
- Núcleo conversacional modular.
- Memoria local persistente y contexto reciente.
- Registro de herramientas.
- Proveedor IA intercambiable en modo demo.
- Herramientas básicas de hora y estado del sistema.
- **v1.3: herramientas explícitas para Windows**, sin ejecución arbitraria.

## Instalación
Python 3.11+ recomendado.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m jarvis
```

## v1.3 Windows
El módulo `v1.3/windows_tools.py` permite, de forma controlada:
- comprobar el sistema operativo;
- abrir Notepad;
- abrir Calculadora;
- abrir carpetas existentes.

No se ejecutan comandos arbitrarios, PowerShell libre ni cadenas de shell proporcionadas por el usuario.

## Próximas capas
v1.4 búsqueda web, v1.5 memoria avanzada y v2.x interfaz/automatización ampliada.
