"""
Sermon API - Simple endpoints, no security bullshit
"""
from flask import Flask, jsonify
from sermon_engine import get_sermon_engine, SermonSegment, SERMON_ORDER, SEGMENT_CONFIG

app = Flask(__name__)
engine = get_sermon_engine()

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "sermon_active": engine.is_sermon_active()})

@app.route('/sermon/status')
def get_status():
    return jsonify(engine.get_status())

@app.route('/sermon/segments')
def get_segments():
    segments = []
    for i, segment in enumerate(SERMON_ORDER):
        config = SEGMENT_CONFIG[segment]
        segments.append({
            "index": i + 1,
            "id": segment.name,
            "name": config["name"],
            "duration_minutes": config["duration_minutes"],
            "type": config["type"],
            "description": config["description"]
        })
    return jsonify({"segments": segments})

@app.route('/sermon/start', methods=['GET', 'POST'])
def start_sermon():
    success = engine.start_sermon()
    return jsonify({"success": success, "message": "Sermon started" if success else "Failed"})

@app.route('/sermon/stop', methods=['GET', 'POST'])
def stop_sermon():
    success = engine.stop_sermon()
    return jsonify({"success": success, "message": "Sermon stopped" if success else "No sermon active"})

@app.route('/sermon/pause', methods=['GET', 'POST'])
def pause_sermon():
    success = engine.pause_sermon()
    return jsonify({"success": success, "message": "Paused" if success else "Failed"})

@app.route('/sermon/resume', methods=['GET', 'POST'])
def resume_sermon():
    success = engine.resume_sermon()
    return jsonify({"success": success, "message": "Resumed" if success else "Failed"})

@app.route('/sermon/advance', methods=['GET', 'POST'])
def advance_sermon():
    success = engine.advance_segment()
    return jsonify({"success": success, "message": "Advanced" if success else "Failed"})

@app.route('/sermon/skip/<segment_name>', methods=['GET', 'POST'])
def skip_to_segment(segment_name):
    try:
        segment = SermonSegment[segment_name.upper()]
        success = engine.skip_to_segment(segment)
        return jsonify({"success": success})
    except:
        return jsonify({"success": False, "message": "Invalid segment"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
