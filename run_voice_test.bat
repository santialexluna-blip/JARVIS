@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo JARVIS no esta instalado. Ejecuta install_jarvis.bat primero.
  pause
  exit /b 1
)

.venv\Scripts\python.exe voice_demo.py
if errorlevel 1 (
  echo.
  echo La prueba de voz fallo. Revisa el volumen y el dispositivo de salida.
  pause
  exit /b 1
)

pause
