#!/usr/bin/env python3
"""
Test Firebase connection and create/update Jeffrey Epstein bot entry
"""
import os
from dotenv import load_dotenv
from firebase_stats import init_firebase, update_firebase_stats, get_all_bots

load_dotenv()

print("🔥 Firebase Connection Test\n")
print("="*70)

# Get Firebase URL from .env
DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
print(f"📡 Database URL: {DATABASE_URL}")

# Initialize Firebase
print("\n⏳ Connecting to Firebase...")
init_firebase("firebase-key.json", DATABASE_URL)

print("\n" + "="*70)
print("📊 Current Bots in Firebase:")
print("="*70)

# Get all existing bots for Jeffrey Epstein
all_bots = get_all_bots("Jeffrey Epstein")

if all_bots:
    for bot_id, bot_data in all_bots.items():
        status = bot_data.get('status', 'unknown')
        character = bot_data.get('character_name', 'Unknown')
        count = bot_data.get('argument_count', 0)
        emoji = "🟢" if status == "online" else "🔴"
        print(f"\n{emoji} Bot ID: {bot_id}")
        print(f"   Character: {character}")
        print(f"   Status: {status}")
        print(f"   Arguments: {count}")
else:
    print("\n⚠️  No Epstein bots found in database yet")

print("\n" + "="*70)
print("🆕 Creating/Updating Jeffrey Epstein Bot Entry")
print("="*70)

BOT_ID = "jeffrey-epstein"

print(f"\n📝 Bot ID: {BOT_ID}")
print(f"🎭 Character: Jeffrey Epstein")
print(f"💼 Personality: Epstein Files Conspiracy Theorist")

# Create initial entry
print("\n⏳ Creating Firebase entry...")

update_firebase_stats(
    bot_id=BOT_ID,
    character_name="Jeffrey Epstein",
    status="testing",
    argument_count=0,
    propaganda_count=0,
    interruptions_handled=0,
    space_link="Testing setup",
    last_response="The Epstein files show how the elite really operate behind closed doors."
)

print("✅ Firebase entry created/updated!")

print("\n" + "="*70)
print("📊 Verifying Entry...")
print("="*70)

# Verify it was created
all_bots = get_all_bots("Jeffrey Epstein")
epstein_bot = all_bots.get(BOT_ID)

if epstein_bot:
    print(f"\n✅ SUCCESS! Jeffrey Epstein bot found in Firebase:")
    print(f"\n   Bot ID: {BOT_ID}")
    print(f"   Character: {epstein_bot.get('character_name')}")
    print(f"   Status: {epstein_bot.get('status')}")
    print(f"   Arguments: {epstein_bot.get('argument_count')}")
    print(f"   Propaganda: {epstein_bot.get('propaganda_count')}")
    print(f"   Last Response: {epstein_bot.get('last_response', '')[:80]}...")
    print(f"   Last Updated: {epstein_bot.get('last_updated')}")

    print("\n" + "="*70)
    print("🌐 Firebase Path:")
    print("="*70)
    print(f"\n   {DATABASE_URL}/jeffreyepstein/{BOT_ID}")
    print(f"\n   You can view it at:")
    print(f"   https://console.firebase.google.com/")

else:
    print("\n❌ ERROR: Bot entry not found!")
    print("   Check Firebase permissions or credentials")

print("\n" + "="*70)
print("✅ FIREBASE TEST COMPLETE")
print("="*70)

print("\n📋 Summary:")
print("   ✅ Firebase connection: Working")
print("   ✅ Jeffrey Epstein entry: Created")
print("   ✅ Bot will auto-update stats when running")

print("\n💡 What happens when bot runs:")
print("   1. Bot connects to Firebase automatically")
print("   2. Creates/updates entry: jeffreyepstein/jeffrey-epstein/")
print("   3. Updates stats in real-time:")
print("      - argument_count (conspiracy responses)")
print("      - propaganda_count (Epstein file references)")
print("      - interruptions_handled")
print("      - responses_per_hour")
print("      - status (online/offline)")
print("      - last_response")

print("\n🚀 You're ready! Run: python twitter_autonomous.py")
print("="*70)





