# INTEGRA Backend

This simple Flask backend proxies requests to a local [Ollama](https://ollama.ai/) server. Ensure that `ollama serve` is running locally and that the desired model (default `gemma:7b`) is installed.

## Usage

Install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit values as needed
```

Run the server:
```bash
python app.py
```

Environment variables (see `.env.example` for a template):
- `OLLAMA_HOST` – base URL for the Ollama server (`http://localhost:11434` by default)
- `OLLAMA_MODEL` – default model name (`gemma:7b` by default)
- `PORT` – port to run the Flask server (5000 by default)

The server exposes two routes:
- `GET /api/status` – check model availability
- `POST /api/chat` – send a prompt and receive a response from the model

### On Windows (PowerShell)
Run these commands from the `integra_backend` directory:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```
