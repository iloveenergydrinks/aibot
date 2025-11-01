#!/usr/bin/env python3
"""
Bot Stats API

Simple Flask API that exposes:
- Space link
- Uptime
- Arguments count
- Current status

Other websites can call this to show bot stats
"""
from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from any website

STATS_FILE = "bot_stats.json"


def load_stats():
    """Load current bot stats."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        "space_link": None,
        "start_time": None,
        "argument_count": 0,
        "status": "offline",
        "last_response": None,
        "total_uptime_seconds": 0
    }


def save_stats(stats):
    """Save bot stats."""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current bot status."""
    stats = load_stats()
    
    # Calculate uptime if running
    if stats["start_time"]:
        start = datetime.fromisoformat(stats["start_time"])
        uptime_seconds = (datetime.now() - start).total_seconds()
        uptime_hours = uptime_seconds / 3600
    else:
        uptime_seconds = 0
        uptime_hours = 0
    
    return jsonify({
        "status": stats.get("status", "offline"),
        "space_link": stats.get("space_link"),
        "uptime_hours": round(uptime_hours, 2),
        "uptime_seconds": int(uptime_seconds),
        "argument_count": stats.get("argument_count", 0),
        "last_response": stats.get("last_response"),
        "last_updated": datetime.now().isoformat()
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get detailed stats."""
    stats = load_stats()
    
    # Calculate metrics
    if stats["start_time"] and stats["argument_count"] > 0:
        start = datetime.fromisoformat(stats["start_time"])
        uptime_seconds = (datetime.now() - start).total_seconds()
        uptime_hours = uptime_seconds / 3600
        arguments_per_hour = stats["argument_count"] / uptime_hours if uptime_hours > 0 else 0
    else:
        uptime_hours = 0
        arguments_per_hour = 0
    
    return jsonify({
        "status": stats.get("status", "offline"),
        "space_link": stats.get("space_link"),
        "start_time": stats.get("start_time"),
        "uptime_hours": round(uptime_hours, 2),
        "total_arguments": stats.get("argument_count", 0),
        "arguments_per_hour": round(arguments_per_hour, 1),
        "last_response": stats.get("last_response"),
        "character": "Adolf Hitler",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("\n🌐 Bot Stats API")
    print("="*70)
    print("\nEndpoints:")
    print("  GET /api/status  - Quick status")
    print("  GET /api/stats   - Detailed stats")
    print("  GET /api/health  - Health check")
    print("\nRunning on: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)

