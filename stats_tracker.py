"""
Stats Tracker - Updates Firebase + local backup

Import this in twitter_autonomous.py to track stats
"""
import json
import os
from datetime import datetime

STATS_FILE = "bot_stats.json"

# Try to import Firebase
try:
    from firebase_stats import init_firebase, update_firebase_stats
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️  Firebase not available, using local storage only")

# Initialize Firebase if available
if FIREBASE_AVAILABLE:
    # Try to load Firebase config
    try:
        if os.path.exists(".env"):
            from dotenv import load_dotenv
            load_dotenv()
            DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
            if DATABASE_URL:
                init_firebase("firebase-key.json", DATABASE_URL)
    except:
        pass


def update_stats(space_link=None, argument_count=None, status=None, last_response=None, 
                character_name=None, bot_id=None, propaganda_count=None, interruptions_handled=None):
    """Update bot statistics (local + Firebase)."""
    # Update Firebase if available
    if FIREBASE_AVAILABLE:
        try:
            update_firebase_stats(
                bot_id=bot_id,
                space_link=space_link,
                argument_count=argument_count,
                status=status,
                last_response=last_response,
                character_name=character_name,
                propaganda_count=propaganda_count,
                interruptions_handled=interruptions_handled
            )
        except Exception as e:
            print(f"⚠️  Firebase update failed: {e}")
    
    # Also update local file as backup
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
    else:
        stats = {
            "space_link": None,
            "start_time": None,
            "argument_count": 0,
            "status": "offline",
            "last_response": None
        }
    
    # Update fields
    if space_link is not None:
        stats["space_link"] = space_link
    
    if argument_count is not None:
        stats["argument_count"] = argument_count
    
    if status is not None:
        stats["status"] = status
        
        # Set start time when going online
        if status == "online" and not stats["start_time"]:
            stats["start_time"] = datetime.now().isoformat()
    
    if last_response is not None:
        stats["last_response"] = last_response[:200]  # Limit length
    
    # Save
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def reset_stats():
    """Reset all stats."""
    stats = {
        "space_link": None,
        "start_time": None,
        "argument_count": 0,
        "status": "offline",
        "last_response": None
    }
    
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

