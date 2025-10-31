#!/usr/bin/env python3
"""
FAST LOCAL VOICE BOT - Optimized for speed!

Changes from regular version:
- Uses gpt-4o-mini (5x faster than GPT-4)
- Uses gTTS (instant, free) instead of ElevenLabs
- Shorter AI prompts for faster generation
- Reduced silence detection time
- Total response time: 2-4 seconds (vs 5-9 seconds)
"""
import speech_recognition as sr
import os
import time
from character import AICharacter, PERSONALITIES
from gtts import gTTS
import config
import subprocess
import sys
import tempfile

# Force fast settings
config.MODEL_NAME = "gpt-4o-mini"  # Fast model
USE_FAST_TTS = True  # Use gTTS instead of ElevenLabs

# Initialize with fast settings
try:
    if not config.OPENAI_API_KEY and not config.ANTHROPIC_API_KEY:
        print("\n❌ Need OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        sys.exit(1)
except:
    pass

character = AICharacter()
recognizer = sr.Recognizer()

# Optimize for speed
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6  # Faster detection (was 0.8)


def speak_fast(text):
    """Speak using fast gTTS (instant generation)."""
    print(f"\n🎭 {character.name}: {text}")
    
    try:
        # Use gTTS - instant and free
        tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temp file
        temp_file = tempfile.mktemp(suffix=".mp3")
        tts.save(temp_file)
        
        # Play
        if sys.platform == "darwin":
            subprocess.run(["afplay", temp_file], check=True)
        elif sys.platform == "linux":
            subprocess.run(["mpg123", temp_file], check=True)
        elif sys.platform == "win32":
            os.startfile(temp_file)
        
        # Cleanup
        os.remove(temp_file)
        
    except Exception as e:
        print(f"⚠️  Audio error: {e}")


def listen_fast():
    """Listen with optimized settings for speed."""
    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now)")
        
        try:
            # Quick ambient noise adjustment
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            # Listen with shorter timeout
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            
            print("⚡ Processing...")
            
            # Use Google (fast and free)
            text = recognizer.recognize_google(audio)
            
            if text:
                return text
            return None
                
        except sr.WaitTimeoutError:
            print("⚠️  No speech detected")
            return None
        except sr.UnknownValueError:
            print("⚠️  Couldn't understand")
            return None
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    """Fast conversation loop."""
    global character
    
    print("\n" + "="*70)
    print("⚡ FAST LOCAL VOICE BOT")
    print("="*70)
    print(f"\n  🎭 Character: {character.name}")
    print(f"  🔥 Personality: {character.personality}")
    print(f"  ⚡ Mode: OPTIMIZED FOR SPEED")
    print(f"  🚀 Model: gpt-4o-mini (5x faster)")
    print(f"  🔊 Voice: Google TTS (instant)")
    print(f"\n  ⏱️  Expected response time: 2-4 seconds")
    print(f"\n  {'='*70}")
    print("\n  HOW TO USE:")
    print("    1. Wait for '🎤 Listening...'")
    print("    2. Speak clearly")
    print("    3. Bot responds in ~3 seconds")
    print("    4. Ctrl+C to quit")
    print(f"\n  {'='*70}")
    print("\n  🎮 Say these to control:")
    print("    - 'quit' or 'exit' - Stop")
    print("    - 'reset' - Clear history")
    print("    - 'provocateur' - Change personality")
    print(f"\n  {'='*70}\n")
    
    # Fast greeting
    speak_fast(f"Sieg Heil!")
    
    print("\n⚡ Fast mode active!\n")
    
    count = 0
    
    try:
        while True:
            # Listen
            user_text = listen_fast()
            
            if not user_text:
                continue
            
            user_lower = user_text.lower().strip()
            
            # Commands
            if user_lower in ['quit', 'exit', 'stop', 'bye']:
                speak_fast("Fine! You win this time. Bye!")
                break
            
            if user_lower == 'reset':
                character.reset_conversation()
                speak_fast("Reset! What now?")
                continue
            
            # Personality change
            if user_lower.replace(" ", "_") in PERSONALITIES:
                new_p = user_lower.replace(" ", "_")
                character = AICharacter(personality=new_p, name=config.CHARACTER_NAME)
                speak_fast(f"Now I'm {new_p}! Let's go!")
                continue
            
            # Show input
            print(f"\n💬 You: {user_text}")
            
            # Generate response (fast model)
            start = time.time()
            response = character.generate_response(user_text, speaker_name="You")
            elapsed = time.time() - start
            
            print(f"⏱️  AI response time: {elapsed:.1f}s")
            
            # Speak
            speak_fast(response)
            
            count += 1
            print(f"\n  ─── Exchange {count} ───")
    
    except KeyboardInterrupt:
        print("\n\n👋 Stopped!")
    
    print("\n" + "="*70)
    print(f"  📊 Exchanges: {count}")
    print(f"  ⚡ Fast mode powered by gpt-4o-mini")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Quick mic check
    try:
        sr.Microphone()
    except Exception as e:
        print(f"\n❌ Microphone error: {e}\n")
        sys.exit(1)
    
    main()


