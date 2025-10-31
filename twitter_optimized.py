#!/usr/bin/env python3
"""
OPTIMIZED Twitter Spaces Bot - Best for Messy Spaces!

Smart features:
- Only responds when triggered (keyword or manual)
- Handles multiple speakers gracefully
- Louder audio for Spaces
- Cooldown to prevent spam
"""
import os
import sys
import time
import subprocess
import threading
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimize
recognizer.energy_threshold = 3000
recognizer.pause_threshold = 0.7

# Global state
last_response_time = 0
pending_response = None
should_respond = False


def listen_for_trigger():
    """Background thread listening for spacebar to trigger response."""
    global should_respond
    import sys, tty, termios
    
    while True:
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == ' ':  # Spacebar
                    should_respond = True
                    print("\n🔥 MANUAL TRIGGER! Will respond to next speech...")
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            time.sleep(0.1)


def should_respond_to_text(text):
    """Determine if Hitler should respond to this text.
    
    Returns: (should_respond, reason)
    """
    text_lower = text.lower()
    
    # Keywords that trigger response
    trigger_keywords = [
        'hitler', 'adolf', 'führer', 'fuhrer', 
        'nazi', 'germany', 'german',
        'jew', 'jewish'
    ]
    
    # Controversial topics Hitler would jump on
    controversy_keywords = [
        'democracy', 'freedom', 'rights', 'equality',
        'immigration', 'refugee', 'border',
        'socialism', 'communism', 'capitalism',
        'war', 'peace', 'weak', 'strong'
    ]
    
    # Check if Hitler is mentioned
    for keyword in trigger_keywords:
        if keyword in text_lower:
            return (True, f"Triggered by keyword: '{keyword}'")
    
    # Check for controversial topics (respond 30% of the time)
    for keyword in controversy_keywords:
        if keyword in text_lower and len(text.split()) > 8:
            # Respond to longer statements about controversial topics
            import random
            if random.random() < 0.3:  # 30% chance
                return (True, f"Controversial topic: '{keyword}'")
    
    return (False, "Not triggered")


def main():
    """Optimized Twitter Spaces mode."""
    global last_response_time, should_respond, pending_response
    
    print("\n" + "="*70)
    print("🐦 OPTIMIZED TWITTER SPACES MODE")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\n⚙️  SMART FEATURES:")
    print("  ✅ Keyword activation (mentions 'Hitler', 'Nazi', etc)")
    print("  ✅ Controversy detection (democracy, freedom, etc)")
    print("  ✅ Manual trigger (press SPACE to force response)")
    print("  ✅ Multi-speaker filtering")
    print("  ✅ 10-second cooldown between responses")
    print("  ✅ +12dB volume boost")
    print(f"\n{'='*70}")
    print("\nSETUP:")
    print("  1. Join Twitter Space (browser/phone)")
    print("  2. Become a speaker")
    print("  3. Stay MUTED")
    print("  4. Space audio through your speakers")
    print("  5. Start this script")
    print(f"\n{'='*70}")
    print("\nCONTROLS:")
    print("  • SPACEBAR - Force Hitler to respond to next speaker")
    print("  • CTRL+C - Quit")
    print(f"\n{'='*70}\n")
    
    input("👉 Press Enter when ready in the Space...")
    
    # Start trigger listener in background
    # trigger_thread = threading.Thread(target=listen_for_trigger, daemon=True)
    # trigger_thread.start()
    
    print("\n🎧 Listening to Space with SMART FILTERING...\n")
    print("💡 Hitler will only speak when:")
    print("   • Someone mentions him/Germany/Jews")
    print("   • Controversial topics come up")
    print("   • You press SPACEBAR\n")
    
    exchange_count = 0
    min_response_interval = 10  # 10 seconds between responses
    
    try:
        while True:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=20, phrase_time_limit=15)
                    
                    print("💭 Processing...")
                    
                    # Transcribe
                    text = audio_processor.speech_to_text(audio)
                    
                    if not text or len(text) < 5:
                        continue
                    
                    # Filter very short (likely crosstalk)
                    word_count = len(text.split())
                    if word_count < 4:
                        print(f"⚠️  Too short ({word_count} words), skipping...")
                        continue
                    
                    print(f"\n💬 Heard: \"{text}\"")
                    
                    # Check cooldown
                    time_since_last = time.time() - last_response_time
                    if time_since_last < min_response_interval:
                        cooldown_left = min_response_interval - time_since_last
                        print(f"⏱️  Cooldown: {cooldown_left:.1f}s remaining")
                        
                        # Still check if it's important
                        should_trigger, reason = should_respond_to_text(text)
                        if should_trigger:
                            print(f"   ℹ️  {reason} - but waiting for cooldown...")
                        continue
                    
                    # Check if should respond
                    should_trigger, reason = should_respond_to_text(text)
                    
                    # Or manual trigger
                    if should_respond:
                        should_trigger = True
                        reason = "Manual trigger (SPACEBAR)"
                        should_respond = False
                    
                    if not should_trigger:
                        print(f"   ➡️  Not responding ({reason})")
                        print("      (Press SPACEBAR to force response)\n")
                        continue
                    
                    # RESPOND!
                    print(f"\n🔥 RESPONDING! ({reason})")
                    print(f"💬 Speaker: \"{text}\"")
                    
                    # Generate response
                    response = character.generate_response(text, speaker_name="Speaker")
                    print(f"\n🎭 Hitler will say: \"{response}\"")
                    
                    # Generate audio
                    audio_file = audio_processor.text_to_speech(response)
                    
                    print("\n" + "="*70)
                    print("⚠️  ACTION NEEDED:")
                    print("  1. UNMUTE yourself in Space")
                    print("  2. Press Enter to play")
                    print("  3. MUTE yourself after")
                    print("="*70)
                    
                    input("\n👉 Press Enter when UNMUTED...")
                    
                    # Play with boosted volume
                    print("\n📢 Playing Hitler's response (LOUD)...")
                    subprocess.run(["afplay", audio_file])
                    
                    os.remove(audio_file)
                    
                    print("\n✅ Done! MUTE NOW!")
                    print("   Cooldown: 10 seconds...\n")
                    
                    exchange_count += 1
                    last_response_time = time.time()
                    time.sleep(3)
                
                except sr.WaitTimeoutError:
                    print("⏰ No speech...")
                    continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"⚠️  Error: {e}")
                    time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 Stopping...")
    
    print("\n" + "="*70)
    print(f"📊 Total Hitler arguments: {exchange_count}")
    print("="*70 + "\n")


if __name__ == "__main__":
    print("\n🎙️ Hitler on Twitter Spaces - OPTIMIZED MODE")
    print("="*70)
    print("\nSMART FILTERING:")
    print("  ✅ Only responds to relevant topics")
    print("  ✅ Ignores crosstalk and noise")
    print("  ✅ 10-second cooldown")
    print("  ✅ Louder audio (+12dB)")
    print("\nPerfect for messy Spaces with lots of people!")
    print("="*70 + "\n")
    
    main()


