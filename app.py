from flask import Flask, request, jsonify
import os
import re
import datetime
import subprocess

app = Flask(__name__)
app.config['CADDYFILE_PATH'] = '/etc/caddy/Caddyfile'
app.config['LOG_FILE'] = '/var/log/caddy.log'

def validate_domain(domain):
    return bool(re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', domain))

def validate_target(target):
    return bool(re.match(r'^https?://[a-zA-Z0-9\-\.]+(:\d+)?(/.*)?$', target))

@app.route('/api/update', methods=['POST'])
def update_config():
    data = request.get_json()
    if not data.get('configs'):
        return jsonify({'message': '無配置數據', 'errors': ['請至少添加一個配置']}), 400

    errors = []
    caddy_config = "admin.example.com {\n    root * /usr/share/caddy/admin\n    file_server\n    reverse_proxy /api/* backend:5000\n}\n\n"
    
    for config in data['configs']:
        if not config.get('domain') or not validate_domain(config['domain']):
            errors.append(f"無效域名: {config.get('domain', '空')}")
            continue
        if not config.get('target') or not validate_target(config['target']):
            errors.append(f"無效目標地址: {config.get('target', '空')}")
            continue
            
        caddy_config += f"{config['domain']} {{\n    reverse_proxy {config['target']}"
        if config.get('username') and config.get('password'):
            caddy_config += f"\n    basicauth {{\n        {config['username']} {config['password']}\n    }}"
        caddy_config += "\n}\n\n"

    if errors:
        return jsonify({'message': '配置驗證失敗', 'errors': errors}), 400

    try:
        with open(app.config['CADDYFILE_PATH'], 'w') as f:
            f.write(caddy_config)
        return jsonify({'message': '配置已更新'})
    except Exception as e:
        return jsonify({'message': '寫入配置失敗', 'errors': [str(e)]}), 500

@app.route('/api/restart', methods=['POST'])
def restart_caddy():
    try:
        # 在容器內直接重載配置
        subprocess.run(['caddy', 'reload', '--config', '/etc/caddy/Caddyfile'], check=True)
        return jsonify({'message': 'Caddy 配置已重載'})
    except Exception as e:
        return jsonify({'message': '重啟失敗', 'errors': [str(e)]}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        # 檢查 Caddy 運行狀態（這裡假設在同一網絡中）
        last_updated = datetime.datetime.fromtimestamp(
            os.path.getmtime(app.config['CADDYFILE_PATH'])
        ).strftime('%Y-%m-%d %H:%M:%S')
        
        with open(app.config['CADDYFILE_PATH'], 'r') as f:
            config_count = len([line for line in f if line.strip().endswith('{')]) - 1  # 減去管理介面配置
        
        logs = ""
        if os.path.exists(app.config['LOG_FILE']):
            with open(app.config['LOG_FILE'], 'r') as f:
                logs = '\n'.join(f.read().splitlines()[-10:])
                
        return jsonify({
            'running': True,  # 在容器內假設始終運行
            'last_updated': last_updated,
            'config_count': config_count,
            'logs': logs
        })
    except Exception as e:
        return jsonify({'message': '獲取狀態失敗', 'errors': [str(e)]}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)