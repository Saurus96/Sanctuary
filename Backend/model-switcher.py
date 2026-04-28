#!/usr/bin/env python3
import subprocess, signal, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

LLAMA_DIR = "/data/data/com.termux/files/home/storage/shared/Sanctuary/App/llama-b8929"
MODELS_DIR = "/data/data/com.termux/files/home/storage/shared/Sanctuary/Models"
BASE_CMD = [
    f"{LLAMA_DIR}/llama-server",
    "--port", "8080",
    "--path", "/data/data/com.termux/files/home/storage/shared/Sanctuary/App/",
]

current_process = None

def start_server(model_name):
    global current_process
    if current_process:
        current_process.send_signal(signal.SIGTERM)
        try:
            current_process.wait(timeout=5)
        except:
            current_process.kill()
    model_path = os.path.join(MODELS_DIR, model_name)
    cmd = BASE_CMD + ["-m", model_path]
    current_process = subprocess.Popen(cmd, cwd=LLAMA_DIR, env={**os.environ, "LD_LIBRARY_PATH": "."})
    return True

def list_models():
    try:
        return sorted([f for f in os.listdir(MODELS_DIR) if f.endswith('.gguf')])
    except:
        return []

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/models':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(list_models()).encode())
        elif parsed.path == '/load':
            qs = parse_qs(parsed.query)
            model = qs.get('model', [None])[0]
            if model and model.endswith('.gguf'):
                start_server(model)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid model')
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 5002), Handler)
    print('Model switcher running on port 5002')
    server.serve_forever()