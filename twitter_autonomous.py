#!/usr/bin/env python3
"""
FULLY AUTONOMOUS Twitter Spaces Bot

Leave it running - Hitler argues on his own!

Requirements:
- BlackHole audio routing configured
- You join Space and STAY UNMUTED (bot controls everything)
- Bot runs continuously

NO manual intervention needed!
"""
import os
import sys
import time
import subprocess
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor
import threading
import config
from config import ELEVENLABS_VOICE_ID
from realtime_streaming import stream_generate_and_speak

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimize for real-time conversation
recognizer.energy_threshold = 2500
recognizer.pause_threshold = 0.6  # Fast response
recognizer.dynamic_energy_threshold = True

# State tracking
bot_is_speaking = False
recent_responses = []  # Track recent responses to avoid loops
last_heard_texts = []  # Avoid responding to same thing


def is_bot_speaking_check(text):
    """Check if this is the bot's own voice coming back."""
    global recent_responses
    
    # Clean up old responses (keep last 10 for better detection)
    recent_responses = recent_responses[-10:]
    
    text_lower = text.lower().strip()
    text_words = set(text_lower.split())
    
    # Check if we just said this
    for recent in recent_responses:
        recent_lower = recent.lower().strip()
        
        # Exact match or contains
        if text_lower in recent_lower or recent_lower in text_lower:
            return True
        
        # Word overlap check
        recent_words = set(recent_lower.split())
        if len(text_words) > 3 and len(recent_words) > 3:
            overlap = len(text_words & recent_words)
            similarity = overlap / min(len(text_words), len(recent_words))
            if similarity > 0.7:  # 70%+ similar = probably our own voice
                return True
    
    return False


def was_recently_heard(text):
    """Check if we already heard this (avoid duplicate responses)."""
    global last_heard_texts
    
    # Keep last 20 for better duplicate detection
    last_heard_texts = last_heard_texts[-20:]
    
    text_lower = text.lower().strip()
    text_words = set(text_lower.split())
    
    for heard in last_heard_texts:
        heard_lower = heard.lower().strip()
        
        # Exact match
        if text_lower == heard_lower:
            return True
        
        # Very similar (80%+ word overlap)
        heard_words = set(heard_lower.split())
        if len(text_words) > 0 and len(heard_words) > 0:
            overlap = len(text_words & heard_words)
            similarity = overlap / max(len(text_words), len(heard_words))
            if similarity > 0.8:
                return True
    
    return False


def main():
    """Fully autonomous mode."""
    global bot_is_speaking, recent_responses, last_heard_texts
    
    print("\n" + "="*70)
    print("🤖 FULLY AUTONOMOUS MODE - Leave It Running!")
    print("="*70)
    print(f"\n🎭 Character: {character.name}")
    print(f"🔥 Personality: {character.personality}")
    print(f"\n{'='*70}")
    print("\n⚡ AUTONOMOUS FEATURES:")
    print("  ✅ Argues with EVERYTHING")
    print("  ✅ NO cooldowns")
    print("  ✅ NO manual unmuting")
    print("  ✅ Responds like a real person")
    print("  ✅ Self-aware (doesn't respond to own voice)")
    print(f"\n{'='*70}")
    print("\n🎯 CRITICAL SETUP:")
    print("  1. BlackHole MUST be configured")
    print("  2. Join Twitter Space")
    print("  3. Become a speaker")
    print("  4. STAY UNMUTED (bot handles everything)")
    print("  5. Start this script")
    print("  6. Walk away - bot runs autonomously!")
    print(f"\n{'='*70}")
    print("\n⚠️  IMPORTANT:")
    print("  • You must STAY UNMUTED in the Space")
    print("  • BlackHole routes audio automatically")
    print("  • Bot will speak whenever it wants")
    print("  • Press Ctrl+C to stop")
    print(f"\n{'='*70}\n")
    
    # Verify BlackHole
    print("🔍 Checking BlackHole setup...")
    mic_list = sr.Microphone.list_microphone_names()
    has_blackhole = any("blackhole" in m.lower() or "aggregate" in m.lower() for m in mic_list)
    
    if not has_blackhole:
        print("\n❌ WARNING: BlackHole not detected!")
        print("   Audio routing may not work properly.")
        print("   Install with: ./setup_spaces_audio.sh")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    else:
        print("✅ BlackHole detected!\n")
    
    input("👉 Press Enter when you're UNMUTED in the Space and ready...")
    
    print("\n" + "="*70)
    print("🔥 HITLER IS NOW AUTONOMOUS - LEAVE IT RUNNING")
    print("="*70)
    print("\n👂 Listening to Space...")
    print("🎙️ Will argue with everything automatically")
    print("🔥 No human intervention needed!")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    argument_count = 0
    ramble_count = 0
    last_activity_time = time.time()
    silence_before_ramble = 30  # Ramble after 30 seconds of silence
    
    # Propaganda topics for rambling
    propaganda_topics = [
        "The Jews control the media and banks!",
        "Democracy has failed Germany!",
        "Only strong leadership can save nations!",
        "Racial purity is essential for greatness!",
        "The weak must follow the strong!",
        "Germany will rise again under my leadership!",
        "Our enemies conspire against us!"
    ]
    
    # Use regular Mac microphone (not BlackHole) to avoid feedback
    mic_list = sr.Microphone.list_microphone_names()
    mic_index = None
    
    # Find built-in microphone
    for i, name in enumerate(mic_list):
        if "macbook" in name.lower() and "microfono" in name.lower():
            mic_index = i
            print(f"✅ Using microphone: {name} (index {i})")
            print("   This will hear Space from your speakers\n")
            break
    
    if mic_index is None:
        # Use default
        print("✅ Using default microphone\n")
    
    try:
        while True:
            # Don't listen while bot is speaking
            if bot_is_speaking:
                time.sleep(0.2)
                continue
            
            # Check if should ramble (no activity for X seconds)
            if time.time() - last_activity_time > silence_before_ramble:
                print(f"\n💭 {silence_before_ramble}s of silence - Hitler giving propaganda speech...")
                
                import random
                # Use pre-written propaganda instead of generating (more reliable)
                propaganda_speeches = [
                    "Mein Freunde! Die Juden control the banks, the media, the governments! They engineer wars and economic collapse to profit while das Volk suffers. We must expose this conspiracy and take back control!",
                    "Nein! Democracy has failed Germany! The Weimar Republic was weak, corrupt, controlled by Jewish interests. Only strong leadership under the Führer can restore our nation to greatness!",
                    "Lebensraum! Germany needs living space for our growing population. We are confined, suffocated by the unjust borders forced upon us. The German people deserve room to thrive and prosper!",
                    "The Treaty of Versailles! A humiliation engineered by die Juden to destroy Germany! They forced us to accept blame for the war, pay crushing reparations, and lose our territory. This injustice must be avenged!",
                    "Das Volk! The Aryan race is superior in intelligence, strength, and culture. We must preserve racial purity and prevent the mongrelization that die Juden push through immigration and multiculturalism!",
                    "The November Criminals! Socialists and Jews stabbed Germany in the back during World War I. We were winning, but they surrendered and betrayed das Vaterland! This Dolchstoßlegende must never be forgotten!",
                    "Das Tausend-Jahr Reich! Germany's destiny is to rule for a thousand years! Under my leadership, we will build an empire that will last for generations. Nothing can stop the rise of the German people!"
                ]
                
                propaganda = random.choice(propaganda_speeches)
                
                print(f"🎭 Hitler propaganda: \"{propaganda}\"")
                
                # Just play propaganda normally (pre-written, no need to stream)
                bot_is_speaking = True
                
                print("🔊 Speaking propaganda...")
                
                prop_audio = audio_processor.text_to_speech(propaganda)
                subprocess.run(["afplay", prop_audio])
                os.remove(prop_audio)
                
                bot_is_speaking = False
                ramble_count += 1
                last_activity_time = time.time()
                
                print(f"✅ Propaganda #{ramble_count} delivered\n")
                continue
            
            # Use regular microphone
            mic_params = {"device_index": mic_index} if mic_index is not None else {}
            
            with sr.Microphone(**mic_params) as source:
                try:
                    # Skip noise adjustment for speed
                    # recognizer.adjust_for_ambient_noise(source, duration=0.1)
                    
                    # Listen for speech - shorter timeout
                    audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
                    
                    # Transcribe with Google (faster than Whisper)
                    text = audio_processor.speech_to_text(audio, use_whisper=False)
                    
                    if not text:
                        continue
                    
                    # Basic filters
                    words = text.split()
                    
                    # Allow single words if they're substantial (2+ characters)
                    if len(words) == 1 and len(words[0]) < 3:
                        continue
                    
                    # English only - check for common English words
                    def is_english(text):
                        # Count ASCII letters
                        ascii_letters = sum(1 for c in text if ord(c) < 128 and c.isalpha())
                        total_letters = sum(1 for c in text if c.isalpha())
                        if total_letters == 0:
                            return False
                        if (ascii_letters / total_letters) < 0.9:  # Must be 90%+ ASCII
                            return False
                        
                        # Check for common English words (strip punctuation)
                        import re
                        # Remove punctuation and split into words
                        words = re.findall(r'\b[a-z]+\b', text.lower())
                        
                        common_english = ['the', 'a', 'is', 'are', 'you', 'i', 'we', 'they', 'what', 'how', 'do', 'about', 'think', 'hello', 'hi', 'yes', 'no', 'and', 'or', 'but', 'bye', 'ok', 'thank', 'thanks', 'good', 'bad', 'why', 'when', 'who']
                        has_english_word = any(word in common_english for word in words)
                        
                        # If no common words found, check if ALL words are ASCII (English-looking)
                        if not has_english_word and len(words) > 0:
                            # If all words are short ASCII, probably English
                            has_english_word = all(len(w) < 15 for w in words)
                        
                        return has_english_word
                    
                    if not is_english(text):
                        print(f"🌐 Non-English, skipping: \"{text[:30]}...\"")
                        continue
                    
                    # Check if it's bot's own voice
                    if is_bot_speaking_check(text):
                        print("🔁 Own voice detected, skipping...")
                        continue
                    
                    # Check if already heard
                    if was_recently_heard(text):
                        print("🔁 Already heard this, skipping...")
                        continue
                    
                    # Record that we heard it
                    last_heard_texts.append(text)
                    
                    # Display
                    print(f"\n💬 Speaker: \"{text}\"")
                    
                    # Check for commands to control Hitler
                    text_lower = text.lower()
                    
                    # Stop rambling command
                    if any(phrase in text_lower for phrase in ['stop rambling', 'shut up', 'be quiet', 'enough', 'stop talking']):
                        # Increase silence timer so he doesn't ramble for a while
                        last_activity_time = time.time() + 120  # Don't ramble for 2 minutes
                        
                        # Quick dismissive response
                        dismissals = [
                            "Fine! But you know I'm right!",
                            "Yah, yah. You can't handle the truth!",
                            "Silence yourself then! Dee You-den have brainwashed you!",
                            "As you wish. But remember - dahs Rike is inevitable!"
                        ]
                        import random
                        response = random.choice(dismissals)
                        
                        print(f"🎭 Hitler (dismissive): \"{response}\"")
                        
                        bot_is_speaking = True
                        audio_file = audio_processor.text_to_speech(response)
                        subprocess.run(["afplay", audio_file])
                        os.remove(audio_file)
                        bot_is_speaking = False
                        
                        argument_count += 1
                        print(f"✅ Dismissal delivered\n")
                        time.sleep(1)
                        continue
                    
                    # Ramble more command
                    if any(phrase in text_lower for phrase in ['tell us more', 'keep going', 'ramble more', 'elaborate', 'explain more']):
                        # Trigger immediate rambling
                        last_activity_time = time.time() - silence_before_ramble - 1
                        print("🔥 Triggered to ramble more!\n")
                        continue
                    
                    # Check if they're agreeing with Hitler
                    def is_agreeing(text):
                        text_lower = text.lower()
                        agreement_phrases = [
                            'you\'re right', 'i agree', 'exactly', 'true', 'correct',
                            'heil', 'sieg heil', 'yes hitler', 'right about',
                            'makes sense', 'good point', 'totally', 'absolutely'
                        ]
                        return any(phrase in text_lower for phrase in agreement_phrases)
                    
                    # Generate response based on agreement or disagreement
                    if is_agreeing(text):
                        # They agree - praise them!
                        praise_options = [
                            f"Sieg Heil! You understand the truth, comrade! {text}",
                            f"Excellent! You see clearly what others are too blind to see. {text}",
                            f"Finally, someone with strength and intelligence! {text}",
                            f"Heil! You are a true patriot who understands our mission. {text}",
                            f"Ja! You recognize the Jewish conspiracy. Together we are strong! {text}"
                        ]
                        import random
                        context = random.choice(praise_options)
                        response = character.generate_response(context, speaker_name="Supporter")
                    else:
                        # Normal argument
                        response = character.generate_response(text, speaker_name="Speaker")
                    
                    # Simple approach: Generate complete response, then speak
                    # (Sounds WAY better than chunked streaming with gaps)
                    print(f"🎭 Hitler: \"{response}\"")
                    
                    bot_is_speaking = True
                    recent_responses.append(response)
                    
                    print("🔊 Generating audio...")
                    
                    # Generate full audio (smooth, no gaps)
                    audio_file = audio_processor.text_to_speech(response)
                    
                    print("🔊 Speaking...")
                    subprocess.run(["afplay", audio_file])
                    os.remove(audio_file)
                    
                    bot_is_speaking = False
                    argument_count += 1
                    last_activity_time = time.time()
                    
                    print(f"✅ Argument #{argument_count} delivered!\n")
                    
                    time.sleep(0.2)
                
                except sr.WaitTimeoutError:
                    # Normal - just waiting for speech
                    continue
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"⚠️  {e}")
                    time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("🛑 AUTONOMOUS MODE STOPPED")
        print("="*70)
    
    print(f"\n📊 Total autonomous arguments: {argument_count}")
    print(f"🎭 {character.name} argued like a real person in the Space!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🤖 FULLY AUTONOMOUS HITLER BOT")
    print("="*70)
    print("\n✨ Just leave it running!")
    print("   Hitler will argue with everything automatically.")
    print("\n⚠️  REQUIREMENTS:")
    print("   1. BlackHole configured (for audio routing)")
    print("   2. You're UNMUTED in the Space")
    print("   3. System audio set to use BlackHole")
    print("\nThen walk away - bot runs on its own! 🚀")
    print("="*70 + "\n")
    
    main()


