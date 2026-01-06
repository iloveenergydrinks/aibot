#!/usr/bin/env python3
"""
Clone a character's voice using ElevenLabs API
"""
import os
import requests
from dotenv import load_dotenv
from config import CHARACTER_NAME

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Define character-specific settings
CHARACTER_VOICES = {
    "Michael Saylor": {
        "audio_file": "Michael Saylor_ MSTR Stands for MONSTER-[AudioTrimmer.com].mp3",
        "description": "Bitcoin maximalist, CEO of MicroStrategy, professional executive voice",
        "labels": '{"accent": "american", "age": "middle-aged", "gender": "male", "use_case": "professional"}'
    },
    "Jeffrey Epstein": {
        "audio_file": "Jeffrey Epsteins Most Controversial Interview_ Shocking Moments Revealed-[AudioTrimmer.com].mp3",
        "description": "Controversial financier and philanthropist, conspiratorial and enigmatic voice",
        "labels": '{"accent": "american", "age": "middle-aged", "gender": "male", "use_case": "conversational"}'
    }
}

if CHARACTER_NAME not in CHARACTER_VOICES:
    print(f"❌ Error: No voice configuration found for character: {CHARACTER_NAME}")
    print(f"Available characters: {', '.join(CHARACTER_VOICES.keys())}")
    exit(1)

VOICE_CONFIG = CHARACTER_VOICES[CHARACTER_NAME]
AUDIO_FILE = VOICE_CONFIG["audio_file"]

if not ELEVENLABS_API_KEY:
    print("❌ Error: ELEVENLABS_API_KEY not found in .env file")
    exit(1)

if not os.path.exists(AUDIO_FILE):
    print(f"❌ Error: Audio file not found: {AUDIO_FILE}")
    print(f"💡 Please provide a high-quality audio sample of {CHARACTER_NAME} speaking")
    print(f"   Requirements: 1-5 minutes of clear speech, MP3/WAV format")
    exit(1)

print(f"🎤 Cloning {CHARACTER_NAME}'s voice...")
print(f"📁 Using audio file: {AUDIO_FILE}")

# ElevenLabs API endpoint
url = "https://api.elevenlabs.io/v1/voices/add"

headers = {
    "xi-api-key": ELEVENLABS_API_KEY
}

# Prepare the files and data
with open(AUDIO_FILE, "rb") as audio_file:
    files = {
        "files": (AUDIO_FILE, audio_file, "audio/mpeg")
    }

    data = {
        "name": CHARACTER_NAME,
        "description": VOICE_CONFIG["description"],
        "labels": VOICE_CONFIG["labels"]
    }

    print("⏳ Uploading audio and creating voice clone...")

    response = requests.post(url, headers=headers, files=files, data=data)

if response.status_code == 200:
    result = response.json()
    voice_id = result.get("voice_id")

    print(f"\n✅ SUCCESS! Voice cloned successfully!")
    print(f"🎙️  Voice Name: {CHARACTER_NAME}")
    print(f"🆔 Voice ID: {voice_id}")

    # Update .env file with new voice ID
    print("\n📝 Updating .env file...")

    with open(".env", "r", encoding="utf-8") as f:
        env_content = f.read()

    # Replace old voice ID with new one
    old_line_start = "ELEVENLABS_VOICE_ID="
    lines = env_content.split("\n")
    new_lines = []

    for line in lines:
        if line.startswith(old_line_start):
            new_lines.append(f"ELEVENLABS_VOICE_ID={voice_id}")
            print(f"   ✓ Updated: ELEVENLABS_VOICE_ID={voice_id}")
        else:
            new_lines.append(line)

    with open(".env", "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

    print(f"\n🎉 All done! Your bot now has {CHARACTER_NAME}'s voice!")
    print("\n🧪 Test the voice:")
    print(f'   python test_bot_voice.py')

else:
    print(f"\n❌ Error: Failed to clone voice")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 401:
        print("\n💡 Your API key may be invalid or expired")
    elif response.status_code == 403:
        print("\n💡 Your plan may not support voice cloning")
        print("   Voice cloning requires ElevenLabs Professional plan ($22/month)")
        print("   Upgrade at: https://elevenlabs.io/app/subscription")





