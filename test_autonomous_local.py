#!/usr/bin/env python3
"""
Test Autonomous Mode Locally

Simulates Twitter Spaces environment on your computer.
You speak → Hitler argues back → Repeat (no manual intervention)

Perfect for testing before going live on Spaces!
"""
import os
import sys
import time
import subprocess
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor
import threading

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimize
recognizer.energy_threshold = 2500
recognizer.pause_threshold = 0.6
recognizer.dynamic_energy_threshold = True

# State
bot_is_speaking = False
recent_responses = []
last_heard_texts = []


def is_duplicate(text):
    """Check if we already responded to this."""
    global recent_responses, last_heard_texts
    
    # Clean up old data
    recent_responses = recent_responses[-5:]
    last_heard_texts = last_heard_texts[-10:]
    
    text_lower = text.lower().strip()
    
    # Check if we just said this
    for recent in recent_responses:
        if text_lower in recent.lower() or recent.lower() in text_lower:
            return True
    
    # Check if we already heard this
    for heard in last_heard_texts:
        if text_lower == heard.lower().strip():
            return True
    
    return False


def main():
    """Test autonomous mode locally."""
    global bot_is_speaking, recent_responses, last_heard_texts
    
    print("\n" + "="*70)
    print("🧪 TESTING AUTONOMOUS MODE LOCALLY")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\n🎯 THIS SIMULATES TWITTER SPACES:")
    print("  • You speak into your mic")
    print("  • Hitler hears and responds AUTOMATICALLY")
    print("  • NO manual steps")
    print("  • Just like it will work in Spaces")
    print(f"\n{'='*70}")
    print("\n📋 WHAT TO EXPECT:")
    print("  1. Bot listens continuously")
    print("  2. You say something")
    print("  3. Hitler responds immediately (audio plays)")
    print("  4. Bot listens again")
    print("  5. Repeat!")
    print(f"\n{'='*70}")
    print("\n⚡ FEATURES BEING TESTED:")
    print("  ✅ Continuous listening")
    print("  ✅ Automatic responses")
    print("  ✅ No cooldowns")
    print("  ✅ No manual unmuting")
    print("  ✅ Self-detection (won't loop)")
    print(f"\n{'='*70}\n")
    
    print("💡 TIP: Make short statements for best results")
    print("   Example: 'I think democracy is good'\n")
    
    input("👉 Press Enter to start autonomous test...")
    
    print("\n" + "="*70)
    print("🔥 AUTONOMOUS MODE - ACTIVE")
    print("="*70)
    print("\n👂 Listening... Say something to Hitler!")
    print("   (Press Ctrl+C to stop)\n")
    
    argument_count = 0
    
    # Find the correct BlackHole aggregate device
    mic_list = sr.Microphone.list_microphone_names()
    blackhole_index = None
    
    for i, name in enumerate(mic_list):
        # Look for aggregate device (has "3 ingress" or named "blackhole")
        if "blackhole" in name.lower() and ("3" in name or "aggregate" in name.lower()):
            blackhole_index = i
            print(f"✅ Using audio device: {name}\n")
            break
    
    # If not found, try any blackhole device that's not just "BlackHole 2ch"
    if blackhole_index is None:
        for i, name in enumerate(mic_list):
            if "blackhole" in name.lower() and name != "BlackHole 2ch":
                blackhole_index = i
                print(f"✅ Using audio device: {name}\n")
                break
    
    try:
        while True:
            # Don't listen while speaking
            if bot_is_speaking:
                time.sleep(0.1)
                continue
            
            # Use the BlackHole aggregate device
            mic_params = {"device_index": blackhole_index} if blackhole_index else {}
            
            with sr.Microphone(**mic_params) as source:
                try:
                    # Quick adjustment
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    
                    # Listen
                    print("🎤 Listening...", end=" ", flush=True)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=12)
                    
                    print("💭 Processing...", end=" ", flush=True)
                    
                    # Transcribe
                    text = audio_processor.speech_to_text(audio, use_whisper=False)
                    
                    if not text:
                        print("❌")
                        continue
                    
                    # Basic filter - accept 2+ words
                    if len(text.split()) < 2:
                        print("Too short (1 word)")
                        continue
                    
                    # English only filter
                    def is_english(text):
                        ascii_letters = sum(1 for c in text if ord(c) < 128 and c.isalpha())
                        total_letters = sum(1 for c in text if c.isalpha())
                        if total_letters == 0:
                            return False
                        return (ascii_letters / total_letters) > 0.8
                    
                    if not is_english(text):
                        print(f"Non-English, skipping")
                        continue
                    
                    # Check duplicates
                    if is_duplicate(text):
                        print("Duplicate, skipping")
                        continue
                    
                    # Record it
                    last_heard_texts.append(text)
                    
                    print(f"\n\n💬 You said: \"{text}\"")
                    
                    # Generate response IMMEDIATELY
                    print("🧠 Hitler thinking...")
                    
                    response = character.generate_response(text, speaker_name="You")
                    recent_responses.append(response)
                    
                    print(f"🎭 Hitler responds: \"{response}\"")
                    
                    # Speak AUTOMATICALLY
                    bot_is_speaking = True
                    
                    print("🔊 Hitler speaking...\n")
                    
                    audio_file = audio_processor.text_to_speech(response)
                    subprocess.run(["afplay", audio_file])
                    os.remove(audio_file)
                    
                    bot_is_speaking = False
                    
                    argument_count += 1
                    
                    print(f"✅ Argument #{argument_count} complete!")
                    print("="*70)
                    print("👂 Listening for your next statement...\n")
                    
                    # Minimal pause (human-like)
                    time.sleep(0.3)
                
                except sr.WaitTimeoutError:
                    print("⏰", end=" ", flush=True)
                    continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"\n⚠️  {e}")
                    time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 TEST STOPPED")
        print("="*70)
    
    print(f"\n📊 Test Results:")
    print(f"   • Arguments: {argument_count}")
    print(f"   • Mode: Fully Autonomous")
    print(f"   • Manual steps: 0")
    
    if argument_count > 0:
        print(f"\n✅ AUTONOMOUS MODE WORKS!")
        print(f"\n🚀 Ready for Twitter Spaces:")
        print(f"   python3 twitter_autonomous.py")
    else:
        print(f"\n⚠️  No arguments generated")
        print(f"   Try speaking more clearly into your mic")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🧪 LOCAL AUTONOMOUS MODE TEST")
    print("="*70)
    print("\nThis simulates exactly how the bot will work in Spaces:")
    print("  • Fully autonomous")
    print("  • No manual steps")
    print("  • Hitler argues automatically")
    print("\nPerfect for testing before going live!")
    print("="*70 + "\n")
    
    # Check mic
    try:
        sr.Microphone()
        print("✅ Microphone ready\n")
    except Exception as e:
        print(f"❌ Microphone error: {e}\n")
        sys.exit(1)
    
    main()

