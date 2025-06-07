# INTEGRA V6 Backend Flask Complete
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "gemma:7b")

@app.route("/api/status")
def status():
    """Return basic server status and model availability."""
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags")
        r.raise_for_status()
        models = [m.get("name") for m in r.json().get("models", [])]
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
    return jsonify({"status": "ok", "models": models, "time": datetime.utcnow().isoformat()})

@app.route("/api/chat", methods=["POST"])
def chat():
    """Proxy chat requests to Ollama."""
    data = request.get_json(force=True)
    prompt = data.get("prompt", "")
    model = data.get("model", DEFAULT_MODEL)
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        r = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=60)
        r.raise_for_status()
        response = r.json().get("response", "")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
