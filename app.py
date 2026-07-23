from flask import Flask, jsonify, request, render_template, make_response
from pathlib import Path
import yaml

from storage.remote_storage import CheckpointStorage

def load_config(config_path: str = "config.yaml") -> dict:
    """Загружает конфигурацию из YAML файла."""
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Загружаем конфиг при старте
config = load_config()

# Инициализация Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

# Инициализация хранилища
storage = CheckpointStorage(
    base_url=config['rest_api_checkpoint']['base_url'],
    list_name=config['rest_api_checkpoint']['list_name']
)

# Глобальные сессии (для демо)
sessions = {}

# Флаг для HTTPS (в продакшене True)
USE_HTTPS = False

@app.route('/')
def index():
    """Главная страница с шаблоном."""
    return render_template('index.html', user_count=0, backend_count=0, user_domains=[], backend_domains=[])

@app.route('/api/login', methods=['POST'])
def api_login():
    """Авторизация по API ключу."""
    data = request.get_json(silent=True) or {}
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'api_key is required'}), 400
    
    try:
        sid = storage.login(api_key)
        if sid:
            sessions[sid] = {'api_key': api_key}
            
            response = make_response(jsonify({'sid': sid, 'status': 'ok'}))
            
            response.set_cookie(
                'sid',
                sid,
                max_age=3600,
                httponly=True,
                secure=USE_HTTPS,
                samesite='Strict' if USE_HTTPS else 'Lax',
                path='/'
            )
            
            return response
        return jsonify({'error': 'Invalid API key'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Завершение сессии."""
    sid = request.cookies.get('sid')
    
    if sid and sid in sessions:
        try:
            storage.logout(sid)
        except Exception:
            pass
        del sessions[sid]
    
    response = make_response(jsonify({'status': 'logged out'}))
    response.delete_cookie('sid', path='/')
    return response

@app.route('/api/check-session', methods=['POST'])
def api_check_session():
    """Проверка активной сессии."""
    sid = request.cookies.get('sid')
    
    if sid and sid in sessions:
        return jsonify({'valid': True})
    return jsonify({'valid': False})

@app.route('/api/domains', methods=['GET'])
def api_get_domains():
    """Получение списка доменов (заглушка)."""
    sid = request.cookies.get('sid')
    
    if not sid or sid not in sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Заглушка - вернуть пустой список
    return jsonify({'domains': []})

@app.route('/api/save-to-backend', methods=['POST'])
def api_save_domains():
    """Сохранение списка доменов (заглушка)."""
    sid = request.cookies.get('sid')
    
    if not sid or sid not in sessions:
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Заглушка - вернуть успех
    return jsonify({'success': True})

if __name__ == '__main__':
    web_config = config.get('web_server', {})
    host = web_config.get('address', '127.0.0.1')
    port = web_config.get('port', 8081)
    
    print(f"Starting server on http://{host}:{port}")
    print(f"Checkpoint API: {config['rest_api_checkpoint']['base_url']}")
    print(f"List name: {config['rest_api_checkpoint']['list_name']}")
    
    app.run(host=host, port=port, debug=True, threaded=True)