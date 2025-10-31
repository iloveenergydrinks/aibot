#!/usr/bin/env python3
"""
LOCAL VOICE ARGUING BOT - No Discord needed!

Just run this script and start talking into your microphone.
The bot will listen and argue back through your speakers.

FASTEST way to test the bot!
"""
import speech_recognition as sr
import os
import time
from character import AICharacter
from audio_processor import AudioProcessor
import config
import subprocess
import sys

# Initialize
try:
    config.validate_config()
except ValueError as e:
    print(f"\n❌ Configuration error: {e}")
    print("\nFor local testing, you only need:")
    print("  - OPENAI_API_KEY or ANTHROPIC_API_KEY")
    print("\nYou can skip DISCORD_BOT_TOKEN for local voice mode!\n")
    
    # Allow running without Discord token for local mode
    if not config.OPENAI_API_KEY and not config.ANTHROPIC_API_KEY:
        sys.exit(1)

character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Audio settings optimized for speed
recognizer.energy_threshold = 3500
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6  # Faster detection (was 0.8)


def speak(text):
    """Speak text out loud."""
    print(f"\n🎭 {character.name}: {text}")
    
    try:
        # Generate audio
        audio_file = audio_processor.text_to_speech(text)
        
        # Play audio based on OS
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", audio_file], check=True)
        elif sys.platform == "linux":
            subprocess.run(["mpg123", audio_file], check=True)
        elif sys.platform == "win32":
            os.startfile(audio_file)
        
        # Small delay before listening again
        time.sleep(0.5)
        
    except Exception as e:
        print(f"⚠️  Couldn't play audio: {e}")
        print("    (But you can see the text response above)")


def listen():
    """Listen to microphone and return transcribed text."""
    with sr.Microphone() as source:
        print("\n🎤 Listening... (speak now)")
        
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for audio
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("💭 Processing...")
            
            # Transcribe
            text = audio_processor.speech_to_text(audio, use_whisper=False)
            
            if text:
                return text
            else:
                print("⚠️  Couldn't understand that. Try again.")
                return None
                
        except sr.WaitTimeoutError:
            print("⚠️  No speech detected. Try again.")
            return None
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"❌ Error: {e}")
            return None


def main():
    """Main conversation loop."""
    global character  # Declare at the top of the function
    
    print("\n" + "="*70)
    print("🎙️  LOCAL VOICE ARGUING BOT")
    print("="*70)
    print(f"\n  🎭 Character: {character.name}")
    print(f"  🔥 Personality: {character.personality}")
    print(f"\n  {'='*70}")
    print("\n  HOW TO USE:")
    print("    1. Make sure your microphone is working")
    print("    2. When you see '🎤 Listening...', start talking")
    print("    3. The bot will argue back automatically")
    print("    4. Press Ctrl+C to quit anytime")
    print(f"\n  {'='*70}")
    print("\n  🎮 Commands (type during conversation):")
    print("    - 'quit' or 'exit' - Stop the bot")
    print("    - 'reset' - Clear conversation history")
    print("    - 'personality' - Change debate style")
    print(f"\n  {'='*70}\n")
    
    # Initial greeting
    greeting = f"Sieg Heil!"
    speak(greeting)
    
    print("\n🎬 Starting conversation loop...\n")
    
    conversation_count = 0
    
    try:
        while True:
            # Listen for user input
            user_text = listen()
            
            if not user_text:
                continue
            
            # Check for commands
            user_text_lower = user_text.lower().strip()
            
            if user_text_lower in ['quit', 'exit', 'stop', 'bye']:
                speak("Fine! But you know I'm right. See you next time!")
                break
            
            if user_text_lower == 'reset':
                character.reset_conversation()
                speak("Okay, fresh start. What do you want to argue about?")
                continue
            
            if user_text_lower == 'personality':
                speak("Tell me which personality: contrarian, devils advocate, sophist, logical debater, or provocateur?")
                continue
            
            # Check if it's a personality name
            from character import PERSONALITIES
            if user_text_lower.replace(" ", "_") in PERSONALITIES:
                new_personality = user_text_lower.replace(" ", "_")
                character = AICharacter(personality=new_personality, name=config.CHARACTER_NAME)
                speak(f"Alright! Now I'm a {new_personality}. Let's argue!")
                continue
            
            # Display what user said
            print(f"\n💬 You: {user_text}")
            
            # Generate response
            response = character.generate_response(user_text, speaker_name="You")
            
            # Speak response
            speak(response)
            
            conversation_count += 1
            print(f"\n  ─── Exchange {conversation_count} ───")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted! Goodbye!")
    
    print("\n" + "="*70)
    print(f"  📊 Total exchanges: {conversation_count}")
    print(f"  🎭 Thanks for arguing with {character.name}!")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Check if microphone is available
    try:
        print("\n🔍 Checking microphone...")
        mic = sr.Microphone()
        print("✅ Microphone found!\n")
    except Exception as e:
        print(f"\n❌ Microphone error: {e}")
        print("\n💡 Make sure:")
        print("   - Your microphone is connected")
        print("   - You've given microphone permissions")
        print("   - No other app is using the microphone\n")
        sys.exit(1)
    
    main()

