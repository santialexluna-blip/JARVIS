$ErrorActionPreference = 'Stop'

Write-Host '=== Instalador de JARVIS v2.1.1 ===' -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python no esta instalado. Instala Python 3.11 o superior y vuelve a ejecutar este instalador.'
}

$pythonVersion = python --version
Write-Host "Detectado: $pythonVersion"

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install pytest

Write-Host 'Ejecutando pruebas...' -ForegroundColor Yellow
$env:PYTHONPATH = (Get-Location).Path
.\.venv\Scripts\python.exe -m pytest -q

Write-Host ''
Write-Host 'JARVIS v2.1.1 instalado correctamente.' -ForegroundColor Green
Write-Host 'Para iniciarlo: .\.venv\Scripts\python.exe -m jarvis' -ForegroundColor Cyan
