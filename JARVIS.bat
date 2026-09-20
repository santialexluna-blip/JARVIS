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

if not exist ".venv\.jarvis-ai-v2.4" (
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

  echo Preparando la inteligencia artificial local...
  set "OLLAMA_EXE=ollama"
  where ollama >nul 2>&1
  if errorlevel 1 (
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
      set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
    ) else (
      where winget >nul 2>&1
      if errorlevel 1 goto ollama_error
      winget install --exact --id Ollama.Ollama --accept-package-agreements --accept-source-agreements
      if errorlevel 1 goto ollama_error
      set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
    )
  )

  echo Descargando el modelo local Qwen3 4B. Esto solo ocurre una vez...
  start "" /min "%OLLAMA_EXE%" serve
  timeout /t 3 /nobreak >nul
  "%OLLAMA_EXE%" pull qwen3:4b
  if errorlevel 1 goto model_error
  type nul > ".venv\.jarvis-ai-v2.4"
)

set "OLLAMA_EXE=ollama"
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
start "" /min "%OLLAMA_EXE%" serve
echo Verificando la conexion con la IA local...
.venv\Scripts\python.exe -c "from ai import OllamaProvider; raise SystemExit(0 if OllamaProvider().ensure_available(30) else 1)"
if errorlevel 1 goto connection_error

echo.
echo Iniciando la interfaz de JARVIS...
start "" .venv\Scripts\pythonw.exe jarvis_gui.py
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
echo JARVIS no pudo iniciar la interfaz. Revisa los permisos de Windows.
pause
exit /b 1

:ollama_error
echo.
echo No se pudo instalar Ollama automaticamente.
echo Descargalo desde https://ollama.com/download/windows y vuelve a abrir JARVIS.bat.
pause
exit /b 1

:model_error
echo.
echo No se pudo descargar el modelo local. Comprueba Internet y vuelve a abrir JARVIS.bat.
pause
exit /b 1

:connection_error
echo.
echo Ollama esta instalado, pero JARVIS no pudo conectarse al servicio local.
echo Cierra Ollama desde la bandeja de Windows, vuelve a abrirlo y ejecuta JARVIS.bat otra vez.
pause
exit /b 1
