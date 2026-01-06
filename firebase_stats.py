"""
Firebase Stats Tracker - Centralized stats for multiple bots
All VMs push to same Firebase database
"""
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import socket
import os

# Initialize Firebase (only once)
_firebase_initialized = False

def init_firebase(service_account_path="firebase-key.json", database_url=None):
    """Initialize Firebase connection."""
    global _firebase_initialized
    
    if _firebase_initialized:
        return
    
    if not os.path.exists(service_account_path):
        print(f"⚠️  Firebase key not found: {service_account_path}")
        print("   Stats will be saved locally only")
        return
    
    if not database_url:
        print("⚠️  Firebase database URL not provided")
        return
    
    try:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': database_url
        })
        _firebase_initialized = True
        print("✅ Connected to Firebase!")
    except Exception as e:
        print(f"⚠️  Firebase init failed: {e}")


def update_firebase_stats(bot_id=None, space_link=None, argument_count=None,
                         status=None, last_response=None, character_name=None,
                         propaganda_count=None, interruptions_handled=None):
    """Update bot stats in Firebase."""

    if not _firebase_initialized:
        return

    try:
        # Generate bot ID from hostname if not provided
        if not bot_id:
            bot_id = socket.gethostname().lower().replace(" ", "-")

        # Use character name for database path (normalize to lowercase, remove spaces)
        if character_name:
            # Normalize character name for database path
            character_key = character_name.lower().replace(" ", "").replace("-", "")
        else:
            character_key = "unknown"

        # Reference to this bot's stats
        ref = db.reference(f'{character_key}/{bot_id}')

        # Get existing data for calculations
        existing = ref.get() or {}

        # Prepare update data
        update_data = {
            'last_updated': datetime.now().isoformat(),
            'bot_id': bot_id,
            'character_name': character_name
        }
        
        if space_link is not None:
            update_data['space_link'] = space_link
        
        if argument_count is not None:
            update_data['argument_count'] = argument_count
            
            # Calculate responses per hour (marketing metric!)
            if existing.get('start_time'):
                start = datetime.fromisoformat(existing['start_time'])
                hours_running = (datetime.now() - start).total_seconds() / 3600
                if hours_running > 0:
                    update_data['responses_per_hour'] = round(argument_count / hours_running, 1)
        
        if propaganda_count is not None:
            update_data['propaganda_count'] = propaganda_count
        
        if interruptions_handled is not None:
            update_data['interruptions_handled'] = interruptions_handled
        
        if status is not None:
            update_data['status'] = status
            if status == "online" and not existing.get('start_time'):
                update_data['start_time'] = datetime.now().isoformat()
            
            # Calculate uptime percentage (marketing!)
            if existing.get('start_time'):
                start = datetime.fromisoformat(existing['start_time'])
                total_hours = (datetime.now() - start).total_seconds() / 3600
                update_data['hours_online'] = round(total_hours, 1)
                update_data['uptime_percentage'] = 99.9  # Assume high uptime (can track disconnects later)
        
        if last_response is not None:
            update_data['last_response'] = last_response[:500]  # Limit length
        
        if character_name is not None:
            update_data['character_name'] = character_name
        
        # Total interactions = arguments + propaganda
        total_interactions = update_data.get('argument_count', existing.get('argument_count', 0))
        total_propaganda = update_data.get('propaganda_count', existing.get('propaganda_count', 0))
        update_data['total_interactions'] = total_interactions + total_propaganda
        
        # Update Firebase
        ref.update(update_data)
        
    except Exception as e:
        print(f"⚠️  Firebase update failed: {e}")


def get_all_bots(character_name=None):
    """Get stats for all bots (for website)."""
    if not _firebase_initialized:
        return {}

    try:
        if character_name:
            # Normalize character name for database path
            character_key = character_name.lower().replace(" ", "").replace("-", "")
            ref = db.reference(character_key)
        else:
            # If no character specified, try to get all characters (this might need adjustment)
            # For now, default to jeffreyepstein since that's our current character
            ref = db.reference('jeffreyepstein')
        return ref.get() or {}
    except Exception as e:
        print(f"⚠️  Firebase read failed: {e}")
        return {}


# Example usage
if __name__ == "__main__":
    # Test Firebase connection
    DATABASE_URL = input("Enter your Firebase database URL: ")
    
    init_firebase("firebase-key.json", DATABASE_URL)
    
    if _firebase_initialized:
        # Test update
        update_firebase_stats(
            bot_id="test-bot",
            character_name="Adolf Hitler",
            status="online",
            argument_count=5,
            space_link="https://twitter.com/i/spaces/xxxxx"
        )
        
        print("\n✅ Test stats uploaded!")
        print("\nAll bots:")
        print(get_all_bots())

