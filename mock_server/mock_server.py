from flask import Flask, jsonify, request
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def load_json(filename):
    """Загружает JSON из файла в папке data."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return {"error": f"File {filename} not found"}
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def log_request():
    """Логирование входящих запросов."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {request.method} {request.path}")
    
    # Заголовки
    headers = dict(request.headers)
    for header in headers:
        print(f"  Session: {header}")
    
 # Тело запроса (через request.data для надёжности)
    if request.data:
        print(f"  Raw: {request.data.decode('utf-8')}", flush=True)
    
    print("-" * 50, flush=True)

@app.route('/web_api/login', methods=['POST'])
def login():
    log_request()
    return jsonify(load_json("login.json"))

@app.route('/web_api/show-application-sites', methods=['POST'])
def show_app_sites():
    log_request()
    return jsonify(load_json("show-application-sites.json"))

@app.route('/web_api/logout', methods=['POST'])
def logout():
    log_request()
    return jsonify(load_json("logout.json"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)