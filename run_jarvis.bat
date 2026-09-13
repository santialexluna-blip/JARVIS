@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo JARVIS no esta instalado. Ejecuta install_jarvis.bat primero.
  pause
  exit /b 1
)
set PYTHONPATH=%~dp0
.venv\Scripts\python.exe -m jarvis
pause
