# install_integra.ps1
# Run from the repository root. This script installs dependencies and launches the INTEGRA demo.

$ErrorActionPreference = 'SilentlyContinue'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

# Ensure required tools
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Python.Python.3 --silent -e
    }
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id OpenJS.NodeJS -e --silent
    }
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id OpenJS.NodeJS -e --silent
    }
}

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Ollama.Ollama -e --silent
    }
}

# Backend setup
python -m venv .\integra_backend\.venv
& .\integra_backend\.venv\Scripts\Activate.ps1
pip install -r .\integra_backend\requirements.txt -q
Copy-Item .\integra_backend\.env.example .\integra_backend\.env -Force

# Ensure Gemma model is present
if (-not (ollama list | Select-String -Quiet 'gemma:7b')) {
    ollama pull gemma:7b
}

# Start Ollama server
Start-Process -WindowStyle Hidden ollama serve

# Launch backend
Start-Process powershell -ArgumentList "-NoExit","-ExecutionPolicy","Bypass","-Command","& '.\integra_backend\.venv\Scripts\Activate.ps1'; python .\integra_backend\app.py"

# Electron dependencies
Push-Location .\integra_electron
npm install --silent
# Launch Electron app
Start-Process npm start
Pop-Location

Write-Host "INTEGRA demo running."

