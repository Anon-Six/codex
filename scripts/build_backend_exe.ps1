# Build the INTEGRA backend into a Windows executable using PyInstaller
# Requires Python with PyInstaller installed

$ErrorActionPreference = 'Stop'

$backendPath = Join-Path $PSScriptRoot '..' 'integra_backend'
Push-Location $backendPath

python -m venv build_env
& build_env\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile app.py --name integra_backend

Pop-Location
