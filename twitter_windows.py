#!/usr/bin/env python3
"""
Windows-specific Twitter Spaces bot
Works WITHOUT PyAudio by using alternative audio capture
"""
import os
import sys
import time
import subprocess
from character import AICharacter
from audio_processor import AudioProcessor
import config

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()

print("\n🪟 Windows Twitter Spaces Bot")
print("="*70)
print("\nThis version works without PyAudio!")
print("You'll manually indicate when someone speaks.")
print("="*70 + "\n")

input("Press Enter to start...")

argument_count = 0

try:
    while True:
        # Wait for user to indicate someone spoke
        user_input = input("\n💬 What did they say? (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input or len(user_input) < 3:
            continue
        
        print(f"\n🎭 Hitler thinking...")
        
        # Generate response
        response = character.generate_response(user_input, "Speaker")
        
        print(f"🎭 Hitler: \"{response}\"")
        
        # Generate and play audio
        print("🔊 Speaking...")
        audio_file = audio_processor.text_to_speech(response)
        
        # Play through system (goes to VoiceMeeter → Space)
        subprocess.run(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", "--play-and-exit", audio_file], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
        
        os.remove(audio_file)
        
        argument_count += 1
        print(f"✅ Argument #{argument_count}\n")

except KeyboardInterrupt:
    print("\n\nStopped!")

print(f"\nTotal arguments: {argument_count}")

