#!/usr/bin/env python3
"""
24/7 TWITTER SPACES BOT - Production Ready

Designed to run continuously for hours/days:
- Uses Whisper API (more reliable than Google STT)
- Better error handling and recovery
- Handles silence and noise gracefully
- Logging for monitoring
- Auto-restart on errors
"""
import os
import sys
import time
import subprocess
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor
from datetime import datetime

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimized for 24/7 operation
recognizer.energy_threshold = 3000
recognizer.pause_threshold = 0.7
recognizer.dynamic_energy_threshold = True

# State
bot_is_speaking = False
recent_responses = []
last_heard_texts = []
stats = {
    "total_heard": 0,
    "total_responded": 0,
    "errors": 0,
    "start_time": time.time()
}


def log(message):
    """Log with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")


def is_duplicate(text):
    """Check duplicates."""
    global recent_responses, last_heard_texts
    
    recent_responses = recent_responses[-10:]
    last_heard_texts = last_heard_texts[-20:]
    
    text_lower = text.lower().strip()
    
    for recent in recent_responses:
        if text_lower in recent.lower() or recent.lower() in text_lower:
            return True
    
    for heard in last_heard_texts:
        if abs(len(text_lower) - len(heard.lower())) < 10:  # Similar length
            if text_lower == heard.lower() or text_lower in heard.lower():
                return True
    
    return False


def main():
    """24/7 autonomous mode."""
    global bot_is_speaking, recent_responses, last_heard_texts, stats
    
    print("\n" + "="*70)
    print("🔴 24/7 AUTONOMOUS TWITTER SPACES BOT")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\n🎯 24/7 FEATURES:")
    print("  ✅ Uses Whisper API (more reliable)")
    print("  ✅ Auto-recovery from errors")
    print("  ✅ Handles silence gracefully")
    print("  ✅ Runs indefinitely")
    print("  ✅ Logs all activity")
    print("  ✅ Statistics tracking")
    print(f"\n{'='*70}")
    print("\n⚠️  REQUIREMENTS FOR 24/7:")
    print("  1. BlackHole configured")
    print("  2. You're UNMUTED in Space (stay unmuted)")
    print("  3. Stable internet connection")
    print("  4. Keep this terminal window open")
    print("  5. Don't let Mac sleep (System Settings → Energy)")
    print(f"\n{'='*70}\n")
    
    log("Starting 24/7 autonomous mode...")
    
    # Find BlackHole device
    mic_list = sr.Microphone.list_microphone_names()
    blackhole_index = None
    
    for i, name in enumerate(mic_list):
        if "blackhole" in name.lower() and ("3" in name or name.lower() == "blackhole"):
            blackhole_index = i
            log(f"Using device: {name} (index {i})")
            break
    
    if blackhole_index is None:
        log("⚠️ BlackHole not found, using default mic")
    
    log("Ready to argue 24/7!")
    log("Press Ctrl+C to stop\n")
    
    consecutive_errors = 0
    max_consecutive_errors = 10
    
    try:
        while True:
            # Safety: If too many consecutive errors, pause
            if consecutive_errors >= max_consecutive_errors:
                log(f"⚠️ {max_consecutive_errors} consecutive errors, pausing 30s...")
                time.sleep(30)
                consecutive_errors = 0
            
            # Don't listen while speaking
            if bot_is_speaking:
                time.sleep(0.2)
                continue
            
            # Use BlackHole device
            mic_params = {"device_index": blackhole_index} if blackhole_index is not None else {}
            
            try:
                with sr.Microphone(**mic_params) as source:
                    # Quick adjustment
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    
                    # Listen
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    
                    stats["total_heard"] += 1
                    
                    # Transcribe with Whisper (more reliable for 24/7)
                    text = audio_processor.speech_to_text(audio, use_whisper=True)
                    
                    if not text:
                        consecutive_errors += 1
                        continue
                    
                    # Reset error counter on success
                    consecutive_errors = 0
                    
                    # Filter very short
                    if len(text.split()) < 2:
                        continue
                    
                    # Check duplicates
                    if is_duplicate(text):
                        log(f"🔁 Duplicate: \"{text[:50]}...\"")
                        continue
                    
                    # Record it
                    last_heard_texts.append(text)
                    
                    # Display
                    log(f"💬 Heard: \"{text}\"")
                    
                    # Generate response
                    try:
                        response = character.generate_response(text, speaker_name="Speaker")
                        recent_responses.append(response)
                        
                        log(f"🎭 Responding: \"{response}\"")
                        
                        # Speak automatically
                        bot_is_speaking = True
                        
                        audio_file = audio_processor.text_to_speech(response)
                        subprocess.run(["afplay", audio_file], check=True)
                        os.remove(audio_file)
                        
                        bot_is_speaking = False
                        
                        stats["total_responded"] += 1
                        
                        log(f"✅ Response #{stats['total_responded']} delivered")
                        
                        # Short pause
                        time.sleep(0.5)
                        
                    except Exception as e:
                        bot_is_speaking = False
                        log(f"❌ Response error: {e}")
                        stats["errors"] += 1
                        time.sleep(1)
            
            except sr.WaitTimeoutError:
                # Normal - no speech detected
                consecutive_errors = 0  # Not really an error
                continue
                
            except Exception as e:
                consecutive_errors += 1
                stats["errors"] += 1
                log(f"⚠️ Error: {e}")
                time.sleep(2)
    
    except KeyboardInterrupt:
        log("\n🛑 Shutting down...")
    
    # Final stats
    runtime = time.time() - stats["start_time"]
    hours = runtime / 3600
    
    print("\n" + "="*70)
    print("📊 24/7 SESSION STATS")
    print("="*70)
    print(f"\n⏱️  Runtime: {hours:.1f} hours")
    print(f"👂 Total audio heard: {stats['total_heard']}")
    print(f"🎭 Total responses: {stats['total_responded']}")
    print(f"❌ Total errors: {stats['errors']}")
    
    if stats['total_responded'] > 0:
        print(f"\n📈 Average: {stats['total_responded'] / hours:.1f} arguments per hour")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🔴 LIVE 24/7 HITLER BOT FOR TWITTER SPACES")
    print("="*70)
    print("\n⚡ Production features:")
    print("  • Whisper API for reliable transcription")
    print("  • Error recovery and auto-restart")
    print("  • Activity logging")
    print("  • Statistics tracking")
    print("  • Designed for continuous operation")
    print("\n💰 Cost estimate:")
    print("  • ~$0.10-0.15 per response")
    print("  • If 10 responses/hour = $1-1.50/hour")
    print("  • 24 hours = $24-36/day")
    print("\n⚠️  Make sure:")
    print("  • You have enough API credits")
    print("  • Mac won't sleep")
    print("  • Stable internet")
    print("\n" + "="*70 + "\n")
    
    response = input("Ready to go 24/7? (y/n): ")
    if response.lower() == 'y':
        main()
    else:
        print("\n👋 Maybe test more first with test_autonomous_local.py\n")

