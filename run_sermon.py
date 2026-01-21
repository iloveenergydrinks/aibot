#!/usr/bin/env python3
"""
LORD FISHNU SERMON RUNNER
Runs webapp + sermon bot together
"""

import sys
import time
import threading

sys.argv.append("--headless")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

print("""
╔═══════════════════════════════════════════════════════════════╗
║   LORD FISHNU SERMON SYSTEM                                   ║
║   Dashboard: http://localhost:5001                            ║
╚═══════════════════════════════════════════════════════════════╝
""")

# Start webapp in background (it proxies to bot API)
def run_webapp():
    try:
        from sermon_webapp import app, socketio
        socketio.run(app, host='0.0.0.0', port=5001, debug=False, 
                    allow_unsafe_werkzeug=True, use_reloader=False)
    except Exception as e:
        print(f"Webapp error: {e}")

print("Starting webapp...")
threading.Thread(target=run_webapp, daemon=True).start()
time.sleep(2)
print("✅ Webapp: http://localhost:5001\n")

# Run bot (has its own API on port 5000)
print("Starting sermon bot...")
print("="*60)
from twitter_autonomous import main
main()

