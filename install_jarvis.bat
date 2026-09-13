@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  echo Python 3.11 o superior no esta instalado.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_jarvis.ps1"
if errorlevel 1 (
  echo.
  echo La instalacion fallo. Revisa el mensaje anterior.
  pause
  exit /b 1
)

pause
