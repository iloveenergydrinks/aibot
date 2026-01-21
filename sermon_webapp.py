"""
Lord Fishnu Sermon Webapp - Simple dashboard
"""
import os
import time
import threading
import requests
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

from sermon_content import CHICKENMANDMENTS, get_daily_theme, get_scroll_content, get_random_cannon_chapter, format_brothtism_text, SERMON_AUDIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fishnu'
socketio = SocketIO(app, cors_allowed_origins="*")

BOT_API = "http://localhost:5000"

def bot_get(endpoint):
    try:
        return requests.get(f"{BOT_API}{endpoint}", timeout=3).json()
    except:
        return {"error": "Bot not running"}

def bot_post(endpoint):
    try:
        return requests.get(f"{BOT_API}{endpoint}", timeout=3).json()  # Use GET since we allow both
    except:
        return {"error": "Bot not running"}

# Background status updates
def status_updater():
    while True:
        try:
            status = bot_get("/sermon/status")
            if not status.get("error"):
                socketio.emit('status_update', status)
        except:
            pass
        time.sleep(1)

threading.Thread(target=status_updater, daemon=True).start()

@socketio.on('connect')
def handle_connect():
    emit('status_update', bot_get("/sermon/status"))

# Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# API - Status
@app.route('/api/status')
def get_status():
    return jsonify(bot_get("/sermon/status"))

@app.route('/api/segments')
def get_segments():
    return jsonify(bot_get("/sermon/segments"))

# API - Controls (all use GET to avoid any content-type issues)
@app.route('/api/sermon/start', methods=['GET', 'POST'])
def start_sermon():
    return jsonify(bot_post("/sermon/start"))

@app.route('/api/sermon/stop', methods=['GET', 'POST'])
def stop_sermon():
    return jsonify(bot_post("/sermon/stop"))

@app.route('/api/sermon/pause', methods=['GET', 'POST'])
def pause_sermon():
    return jsonify(bot_post("/sermon/pause"))

@app.route('/api/sermon/resume', methods=['GET', 'POST'])
def resume_sermon():
    return jsonify(bot_post("/sermon/resume"))

@app.route('/api/sermon/advance', methods=['GET', 'POST'])
def advance_sermon():
    return jsonify(bot_post("/sermon/advance"))

@app.route('/api/sermon/skip/<segment_name>', methods=['GET', 'POST'])
def skip_to_segment(segment_name):
    return jsonify(bot_post(f"/sermon/skip/{segment_name}"))

# Content
@app.route('/api/themes')
def get_themes():
    return jsonify({"themes": CHICKENMANDMENTS, "daily_theme": get_daily_theme()})

@app.route('/api/content/scroll/<int:n>')
def get_scroll(n):
    title, content = get_scroll_content(n)
    return jsonify({"title": title, "content": content[:2000]})

@app.route('/api/content/cannon')
def get_cannon():
    book, author, chapter, content = get_random_cannon_chapter()
    return jsonify({"book": book, "author": author, "chapter": chapter, "content": content[:2000]})

@app.route('/api/content/brothtism')
def get_brothtism():
    return jsonify({"text": format_brothtism_text()})

# Audio
@app.route('/api/audio')
def get_audio_status():
    files = {}
    for key, path in SERMON_AUDIO.items():
        exists = os.path.exists(path)
        files[key] = {"path": path, "exists": exists, "size_mb": round(os.path.getsize(path)/(1024*1024), 2) if exists else 0}
    return jsonify({"audio_files": files})

@app.route('/api/audio/preview/<key>')
def preview_audio(key):
    if key in SERMON_AUDIO and os.path.exists(SERMON_AUDIO[key]):
        return send_from_directory(os.path.dirname(SERMON_AUDIO[key]) or '.', os.path.basename(SERMON_AUDIO[key]))
    return jsonify({"error": "Not found"}), 404

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)
