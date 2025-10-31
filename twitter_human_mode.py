#!/usr/bin/env python3
"""
HUMAN MODE - Hitler argues like a REAL person in Spaces

Features:
- NO cooldowns - responds immediately
- NO keyword filtering - argues with EVERYTHING
- NO delays - natural conversation flow
- Smart speaker detection to avoid responding to himself
- Volume boosted for clear audio

Use this for: Natural, flowing arguments in Spaces
"""
import os
import sys
import time
import subprocess
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimize for FAST, responsive conversation
recognizer.energy_threshold = 2500  # More sensitive
recognizer.pause_threshold = 0.6    # Faster detection
recognizer.dynamic_energy_threshold = True

# Track bot's own speech to avoid responding to himself
bot_is_speaking = False
last_bot_text = ""


def main():
    """Real human conversation mode - no limits!"""
    global bot_is_speaking, last_bot_text
    
    print("\n" + "="*70)
    print("🔥 HUMAN MODE - Hitler Argues Like a Real Person")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\n⚡ HUMAN MODE FEATURES:")
    print("  ✅ NO cooldowns - responds immediately")
    print("  ✅ NO keyword filters - argues with EVERYTHING")
    print("  ✅ NO delays - natural conversation flow")
    print("  ✅ Fast response - like a real person")
    print("  ✅ Volume boosted for Spaces")
    print(f"\n{'='*70}")
    print("\n⚠️  WARNING:")
    print("  This mode is AGGRESSIVE!")
    print("  Hitler will try to argue with EVERY statement.")
    print("  Perfect for heated debates and controversy.")
    print(f"\n{'='*70}")
    print("\nSETUP:")
    print("  1. Join Twitter Space")
    print("  2. Become speaker")
    print("  3. Stay MUTED")
    print("  4. Run this script")
    print("  5. UNMUTE when bot tells you to speak")
    print(f"\n{'='*70}\n")
    
    input("👉 Press Enter when ready in the Space...")
    
    print("\n🔥 HUMAN MODE ACTIVATED - Hitler will argue with EVERYTHING!\n")
    
    argument_count = 0
    
    try:
        while True:
            with sr.Microphone() as source:
                print("👂 Listening for arguments...")
                
                try:
                    # Quick ambient adjustment
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    
                    # Listen - shorter timeout for faster responses
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=12)
                    
                    print("⚡ Processing...")
                    
                    # Transcribe quickly
                    text = audio_processor.speech_to_text(audio, use_whisper=False)
                    
                    if not text:
                        continue
                    
                    # Filter only VERY short (likely noise)
                    if len(text.split()) < 2:
                        print("⚠️  Noise detected, ignoring...")
                        continue
                    
                    # Don't respond to bot's own voice
                    if text.lower().strip() == last_bot_text.lower().strip():
                        print("⚠️  Bot's own voice detected, skipping...")
                        continue
                    
                    # Display what was heard
                    print(f"\n💬 Heard in Space: \"{text}\"")
                    
                    # Check if it's a question or statement worth responding to
                    # (Basic filter to avoid random noise)
                    words = text.split()
                    if len(words) < 3:
                        print("   ➡️  Too short, waiting for more...")
                        continue
                    
                    # GENERATE RESPONSE IMMEDIATELY (no cooldown!)
                    print(f"\n🔥 Hitler is responding...")
                    
                    response = character.generate_response(text, speaker_name="Speaker")
                    
                    print(f"\n🎭 Hitler will say: \"{response}\"")
                    
                    # Generate audio
                    print("🔊 Generating voice...")
                    audio_file = audio_processor.text_to_speech(response)
                    
                    # Prompt to unmute
                    print("\n" + "="*70)
                    print("⚠️  UNMUTE NOW!")
                    print("="*70)
                    
                    input("👉 Press Enter to speak (make sure you're UNMUTED)...")
                    
                    # Mark bot as speaking
                    bot_is_speaking = True
                    last_bot_text = response
                    
                    # Play Hitler's response
                    print("\n📢 Hitler speaking...")
                    subprocess.run(["afplay", audio_file])
                    
                    os.remove(audio_file)
                    
                    bot_is_speaking = False
                    
                    print("\n✅ Done! MUTE NOW and wait for next speaker...")
                    
                    argument_count += 1
                    print(f"   Arguments so far: {argument_count}\n")
                    
                    # Very short pause (human-like)
                    time.sleep(0.5)
                
                except sr.WaitTimeoutError:
                    print("⏰ Waiting for speech...")
                    continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"⚠️  Error: {e}")
                    time.sleep(0.5)
                    continue
    
    except KeyboardInterrupt:
        print("\n\n👋 Hitler has left the Space!")
    
    print("\n" + "="*70)
    print(f"📊 Total arguments: {argument_count}")
    print(f"🎭 {character.name} argued like a real person!")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🎙️ Adolf Hitler - HUMAN MODE for Twitter Spaces")
    print("="*70)
    print("\n🔥 This is the MOST AGGRESSIVE mode:")
    print("   • Argues with EVERYTHING")
    print("   • NO cooldowns")
    print("   • NO filters")
    print("   • Like a REAL person jumping into conversations")
    print("\n⚠️  Use in moderated Spaces or it will be CHAOS!")
    print("="*70 + "\n")
    
    main()


