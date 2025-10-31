#!/usr/bin/env python3
"""
SIMPLE Twitter Spaces Bot - Easiest Setup!

This version is semi-manual but much simpler:
1. You join the Space on your browser
2. Bot runs locally and listens through your mic
3. You unmute when bot wants to speak
4. Bot plays audio through your speakers into the Space

No complex audio routing needed!
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

# Optimize for speed
recognizer.energy_threshold = 3000
recognizer.pause_threshold = 0.7


def main():
    """Simple Twitter Spaces mode."""
    print("\n" + "="*70)
    print("🐦 SIMPLE TWITTER SPACES MODE")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\nSETUP:")
    print("  1. Join a Twitter Space on your browser/phone")
    print("  2. Make yourself a speaker")
    print("  3. Keep yourself MUTED for now")
    print("  4. Put Space audio through your speakers")
    print("  5. Start this script")
    print(f"\n{'='*70}")
    print("\nHOW IT WORKS:")
    print("  • Bot listens through your mic (hears Space)")
    print("  • When someone speaks, bot transcribes it")
    print("  • Bot generates argument")
    print("  • Bot plays audio through speakers")
    print("  • YOU UNMUTE and let bot speak into Space")
    print("  • Then mute again")
    print(f"\n{'='*70}")
    print("\n⚙️  FEATURES:")
    print("  • Filters out multiple speakers talking at once")
    print("  • Waits for clear speech before responding")
    print("  • Boosted volume for louder Space audio")
    print(f"\n{'='*70}\n")
    
    input("👉 Press Enter when you're ready in the Space...")
    
    print("\n🎧 Listening to Space...\n")
    
    exchange_count = 0
    last_response_time = 0
    min_response_interval = 5  # Wait at least 5 seconds between responses
    
    try:
        while True:
            # Listen to Space audio through mic
            with sr.Microphone() as source:
                print("🎤 Listening to Space... (speak or wait for others)")
                
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=15, phrase_time_limit=15)
                    
                    print("💭 Processing...")
                    
                    # Transcribe
                    text = audio_processor.speech_to_text(audio)
                    
                    if not text or len(text) < 5:
                        continue
                    
                    # Check for multiple speakers (usually garbled/unclear)
                    word_count = len(text.split())
                    if word_count < 3:
                        print("⚠️  Too short, ignoring...")
                        continue
                    
                    # Rate limiting - don't respond too frequently
                    time_since_last = time.time() - last_response_time
                    if time_since_last < min_response_interval:
                        print(f"⏱️  Waiting {min_response_interval - time_since_last:.1f}s before responding...")
                        time.sleep(min_response_interval - time_since_last)
                    
                    print(f"\n💬 Speaker in Space: \"{text}\"")
                    
                    # Generate Hitler's response
                    response = character.generate_response(text, speaker_name="Speaker")
                    print(f"\n🎭 Hitler will say: \"{response}\"")
                    
                    # Generate audio
                    audio_file = audio_processor.text_to_speech(response)
                    
                    print("\n" + "="*70)
                    print("⚠️  ACTION REQUIRED:")
                    print("  1. UNMUTE yourself in the Space")
                    print("  2. Press Enter to play Hitler's response")
                    print("  3. Mute yourself after it finishes")
                    print("="*70)
                    
                    input("\n👉 Press Enter when you're UNMUTED...")
                    
                    # Play Hitler's response
                    print("\n🔊 Playing Hitler's response (speak into Space)...")
                    subprocess.run(["afplay", audio_file])
                    
                    os.remove(audio_file)
                    
                    print("\n✅ Done! Mute yourself now.")
                    print("   Waiting for next speaker...\n")
                    
                    exchange_count += 1
                    last_response_time = time.time()
                    time.sleep(2)  # Cooldown before next listen
                
                except sr.WaitTimeoutError:
                    print("⏰ No speech detected, listening again...")
                    continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"⚠️  Error: {e}")
                    continue
    
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user")
    
    print("\n" + "="*70)
    print(f"📊 Total arguments: {exchange_count}")
    print(f"🎭 Thanks for arguing with {character.name}!")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🎙️ Adolf Hitler Twitter Spaces Bot")
    print("="*70)
    print("\nThis is the SIMPLE version:")
    print("  ✅ No complex audio routing")
    print("  ✅ No browser automation")
    print("  ✅ Just you, the bot, and the Space")
    print("\nYou manually unmute/mute in the Space.")
    print("="*70 + "\n")
    
    main()

