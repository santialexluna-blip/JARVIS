@echo off
setlocal
cd /d "%~dp0"
title JARVIS

where python >nul 2>&1
if errorlevel 1 (
  echo Python 3.11 o superior no esta instalado.
  echo Instala Python desde https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Preparando JARVIS por primera vez...
  python -m venv .venv
)

if not exist ".venv\.jarvis-voice-v2.2" (
  echo Instalando y actualizando componentes...
  .venv\Scripts\python.exe -m pip install --upgrade pip
  if errorlevel 1 goto install_error
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto install_error
  .venv\Scripts\python.exe -m pip install pytest
  if errorlevel 1 goto install_error

  echo Comprobando JARVIS...
  set PYTHONPATH=%~dp0
  .venv\Scripts\python.exe -m pytest -q
  if errorlevel 1 goto test_error
  type nul > ".venv\.jarvis-voice-v2.2"
)

echo.
echo Iniciando JARVIS por voz...
.venv\Scripts\python.exe voice_app.py
if errorlevel 1 goto runtime_error
exit /b 0

:install_error
echo.
echo No se pudieron instalar los componentes de JARVIS.
pause
exit /b 1

:test_error
echo.
echo Las pruebas de JARVIS no fueron aprobadas. No se iniciara.
pause
exit /b 1

:runtime_error
echo.
echo JARVIS no pudo usar el microfono. Revisa los permisos de Windows.
pause
exit /b 1
