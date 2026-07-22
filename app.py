from flask import Flask, render_template, jsonify, request
import yaml
from pathlib import Path
from storage.file_storage import FileStorage

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.yaml"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_backend_storage():
    config = load_config()
    storage_type = config.get("storage_type", "file")

    cfg = config.get("file_storage", {})
    return FileStorage(str(BASE_DIR / cfg.get("domains_file", "domains.txt")))

def get_user_storage():
    config = load_config()
    cfg = config.get("file_storage", {})
    return FileStorage(str(BASE_DIR / cfg.get("domains_file", "domains.txt")))

@app.route('/')
def index():
    backend_storage = get_backend_storage()
    user_storage = get_user_storage()
    
    backend_domains = backend_storage.get_domains()
    user_domains = user_storage.get_domains()
    
    return render_template('index.html', 
                         backend_domains=backend_domains,
                         user_domains=user_domains,
                         backend_count=len(backend_domains),
                         user_count=len(user_domains),
                         api_available=backend_storage.is_available() if backend_storage.__class__.__name__ == "RestApiStorage" else True)

@app.route('/api/domains')
def api_domains():
    storage = get_backend_storage()
    return jsonify({"domains": storage.get_domains()})

@app.route('/api/user-domains')
def api_user_domains():
    storage = get_user_storage()
    return jsonify({"domains": storage.get_domains()})

@app.route('/api/save-to-backend', methods=['POST'])
def save_to_backend():
    """Сохраняет домены в правый список (бэкенд/API/файл)."""
    try:
        data = request.get_json()
        domains = [d.strip() for d in data.get('domains', []) if d.strip()]
        
        storage = get_backend_storage()
        success = storage.save_domains(domains)
        
        return jsonify({"success": success, "count": len(domains)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/save-user-list', methods=['POST'])
def save_user_list():
    """Сохраняет левый список в файл."""
    try:
        data = request.get_json()
        domains = [d.strip() for d in data.get('domains', []) if d.strip()]
        
        storage = get_user_storage()
        success = storage.save_domains(domains)
        
        return jsonify({"success": success, "count": len(domains)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/status')
def api_status():
    backend = get_backend_storage()
    user = get_user_storage()
    
    return jsonify({
        "backend": {
            "type": backend.__class__.__name__,
            "available": backend.is_available()
        },
        "user": {
            "type": user.__class__.__name__,
            "available": user.is_available()
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)