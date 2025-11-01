"""
Stats Tracker - Updates bot_stats.json

Import this in twitter_autonomous.py to track stats
"""
import json
import os
from datetime import datetime

STATS_FILE = "bot_stats.json"


def update_stats(space_link=None, argument_count=None, status=None, last_response=None):
    """Update bot statistics."""
    # Load existing
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

