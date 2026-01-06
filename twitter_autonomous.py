#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FULLY AUTONOMOUS Twitter Spaces Bot

Leave it running - Epstein boasts on his own!

Requirements:
- Windows: VB-Cable or VoiceMeeter configured (Mac: BlackHole)
- You join Space and STAY UNMUTED (bot controls everything)
- Bot runs continuously

NO manual intervention needed!
"""
import os
import sys

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
import time
import subprocess
import platform
import speech_recognition as sr
from character import AICharacter
from audio_processor import AudioProcessor
import threading
import config
from config import ELEVENLABS_VOICE_ID
from stats_tracker import update_stats, reset_stats
from voicemeeter_keepalive import restart_audio_engine

# Cross-platform audio playback
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False

IS_WINDOWS = platform.system() == "Windows"

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()
recognizer = sr.Recognizer()

# Optimize for real-time conversation
recognizer.energy_threshold = 1500  # Fixed threshold - prevents decay over time
recognizer.pause_threshold = 1.2  # INCREASED: Wait longer to ensure speaker is DONE (was 0.6)
recognizer.dynamic_energy_threshold = False  # CRITICAL: Prevent threshold decay!
recognizer.dynamic_energy_adjustment_damping = 0.15
recognizer.dynamic_energy_ratio = 1.5

# State tracking
bot_is_speaking = False
recent_responses = []  # Track recent responses to avoid loops
last_heard_texts = []  # Avoid responding to same thing


def is_bot_speaking_check(text):
    """Check if this is the bot's own voice coming back."""
    global recent_responses
    
    # Clean up old responses (keep last 5 - only very recent)
    recent_responses = recent_responses[-5:]
    
    text_lower = text.lower().strip()
    text_words = set(text_lower.split())
    
    # Only flag if VERY similar to recent response
    for recent in recent_responses:
        recent_lower = recent.lower().strip()
        recent_words = set(recent_lower.split())
        
        # Need high word overlap to be considered echo
        if len(text_words) > 2 and len(recent_words) > 2:
            overlap = len(text_words & recent_words)
            similarity = overlap / max(len(text_words), len(recent_words))
            
            # Only flag if 80%+ similar (very strict!)
            if similarity > 0.8:
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


def _play_audio(audio_path: str):
    """Cross-platform audio playback with RDP disconnect resilience."""
    try:
        if PLAYSOUND_AVAILABLE:
            playsound(audio_path)
        elif IS_WINDOWS:
            # Use pydub to play audio on Windows (handles MP3, WAV, etc.)
            from pydub import AudioSegment
            from pydub.playback import play
            audio = AudioSegment.from_file(audio_path)
            play(audio)
        else:
            # macOS/Linux fallback
            subprocess.run(["afplay" if platform.system() == "Darwin" else "aplay", audio_path])
    except OSError as e:
        print(f"⚠️  Audio playback failed (RDP disconnected?): {e}")
        print("   Bot will continue - audio may resume when RDP reconnects")
    except Exception as e:
        print(f"⚠️  Audio playback error: {e}")


def _play_audio_background(audio_path: str):
    """Play audio in background with RDP disconnect resilience."""
    if IS_WINDOWS:
        # Use pydub with threading for Windows
        from pydub import AudioSegment
        from pydub.playback import play
        
        def play_audio():
            try:
                audio = AudioSegment.from_file(audio_path)
                play(audio)
            except OSError as e:
                print(f"⚠️  Background audio failed (RDP disconnected?): {e}")
            except Exception as e:
                print(f"⚠️  Background audio error: {e}")
        
        thread = threading.Thread(target=play_audio, daemon=True)
        thread.start()
        
        # Return a mock process object for compatibility
        class MockProcess:
            def poll(self):
                return None if thread.is_alive() else 0
            def terminate(self):
                # Can't easily stop pydub playback, but thread will finish
                pass
            def wait(self):
                thread.join()
        
        return MockProcess()
    else:
        # macOS/Linux: use subprocess
        cmd = ["afplay"] if platform.system() == "Darwin" else ["aplay"]
        return subprocess.Popen(cmd + [audio_path],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)


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
    if IS_WINDOWS:
        print("  1. VB-Cable or VoiceMeeter MUST be configured")
        print("  2. Set Windows audio output to VB-Cable/VoiceMeeter")
        print("  3. Join Twitter Space")
    else:
        print("  1. BlackHole MUST be configured")
        print("  2. Join Twitter Space")
    print("  3. Become a speaker")
    print("  4. STAY UNMUTED (bot handles everything)")
    print("  5. Start this script")
    print("  6. Walk away - bot runs autonomously!")
    print(f"\n{'='*70}")
    print("\n⚠️  IMPORTANT:")
    print("  • You must STAY UNMUTED in the Space")
    if IS_WINDOWS:
        print("  • VB-Cable/VoiceMeeter routes audio automatically")
    else:
        print("  • BlackHole routes audio automatically")
    print("  • Bot will speak whenever it wants")
    print("  • Press Ctrl+C to stop")
    print(f"\n{'='*70}\n")
    
    # Verify audio routing setup
    print("🔍 Checking audio routing setup...")
    mic_list = sr.Microphone.list_microphone_names()
    
    if IS_WINDOWS:
        # Check for Windows virtual audio devices
        has_virtual_audio = any(
            "vb cable" in m.lower() or 
            "vb-cable" in m.lower() or
            "voicemeeter" in m.lower() or
            "cable" in m.lower() for m in mic_list
        )
        
        if not has_virtual_audio:
            print("\n❌ WARNING: Virtual audio device not detected!")
            print("   Audio routing may not work properly.")
            print("   Windows: Install VB-Cable (free) or VoiceMeeter")
            print("   Download VB-Cable: https://vb-audio.com/Cable/")
            print()
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                return
        else:
            print("✅ Virtual audio device detected!\n")
    else:
        # Mac: Check for BlackHole
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
    
    # Get Space link for API
    space_link = input("\n🔗 Twitter Space link (optional, for API): ").strip()
    if not space_link:
        space_link = "Not provided"
    
    # Set bot ID (change this for each VM!)
    BOT_ID = "jeffrey-epstein"  # Change for each cloned VM
    
    # Initialize stats
    update_stats(bot_id=BOT_ID, space_link=space_link, status="online", argument_count=0, 
               propaganda_count=0, interruptions_handled=0, character_name=character.name)
    print("✅ Stats API updated!\n")
    
    input("👉 Press Enter when you're UNMUTED in the Space and ready...")
    
    print("\n[DEBUG] Starting autonomous mode...")
    print("\n" + "="*70)
    print("🔥 JEFFREY EPSTEIN IS NOW AUTONOMOUS - LEAVE IT RUNNING")
    print("="*70)
    print("\n👂 Listening to Space...")
    print("🎙️ Will argue with everything automatically")
    print("🔥 No human intervention needed!")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    argument_count = 0
    ramble_count = 0
    interruption_count = 0
    last_activity_time = time.time()
    last_response_time = time.time()  # Track when bot last spoke
    silence_before_ramble = 45  # Ramble after 45 seconds of TRUE silence (no questions/responses)
    
    # Epstein boasting speeches for rambling
    epstein_speeches = [
        "On my island, we entertained presidents, princes, and billionaires. They all came for the exclusive experience!",
        "Ghislaine was my perfect social secretary - she knew everyone who mattered and made sure they were comfortable!",
        "The flight logs would show you some very interesting names. My jet went everywhere the elite wanted to go!",
        "Little St. James was paradise - private, exclusive, and full of interesting conversations with world leaders!",
        "Philanthropy opens so many doors. I funded science, education, and had friends in very high places!",
        "Money buys access to everything. I knew presidents, royalty, celebrities - they were all part of my circle!",
        "The elite have certain needs that only someone like me could fulfill. I was the ultimate connector!"
    ]
    
    # Use virtual audio device to hear Space directly (no speakers needed!)
    print("🔍 Detecting audio devices...")
    try:
        mic_list = sr.Microphone.list_microphone_names()
        print(f"✅ Found {len(mic_list)} audio devices")
    except Exception as e:
        print(f"❌ Error detecting devices: {e}")
        mic_list = []
    mic_index = None
    
    if IS_WINDOWS:
        # Find Windows virtual audio OUTPUT device (these can be used as recording sources)
        # Use VoiceMeeter (it was working!)
        for i, name in enumerate(mic_list):
            name_lower = name.lower()
            if ("voicemeeter" in name_lower and "output" in name_lower):
                mic_index = i
                print(f"✅ Using audio device: {name} (index {i})")
                print("   Bot will hear Space directly through VoiceMeeter!\n")
                break
        
        if mic_index is None:
            # Fallback: try to find any virtual audio output device
            for i, name in enumerate(mic_list):
                name_lower = name.lower()
                if (("voicemeeter" in name_lower or "cable" in name_lower) and 
                    "output" in name_lower):
                    mic_index = i
                    print(f"✅ Using audio device: {name} (index {i})")
                    print("   ⚠️ Make sure Space audio is routed to this device!\n")
                    break
    else:
        # Mac: Find BlackHole aggregate device
        for i, name in enumerate(mic_list):
            if "blackhole" in name.lower() and name.lower() != "blackhole 2ch":
                mic_index = i
                print(f"✅ Using audio device: {name} (index {i})")
                print("   Bot will hear Space directly through BlackHole!\n")
                break
    
    if mic_index is None:
        # Fallback to default microphone
        print("⚠️  Virtual audio device not found, using default microphone")
        print("   Make sure Space audio plays through your speakers!\n")
    
    try:
        while True:
            # Don't listen while bot is speaking
            if bot_is_speaking:
                time.sleep(0.2)
                continue
            
            # Check if should ramble (TRUE silence - no questions AND no responses for X seconds)
            time_since_activity = time.time() - last_activity_time
            time_since_response = time.time() - last_response_time
            
            # Only ramble if BOTH no questions AND bot hasn't spoken recently
            if time_since_activity > silence_before_ramble and time_since_response > silence_before_ramble:
                print(f"\n💭 {silence_before_ramble}s of silence - Epstein giving conspiracy speech...")
                
                import random
                # Use pre-written Epstein boasting speeches (more reliable and VARIED)
                epstein_boasting_speeches = [
                    # Island boasting
                    "Little St. James was my private paradise - the ultimate exclusive resort for the world's elite. Presidents, princes, celebrities - they all came to visit!",
                    "On the island, we had everything: massage therapists, private chefs, beautiful scenery. My guests loved the complete privacy and discretion!",
                    "The island was designed for entertaining important people. We had underground tunnels, secret rooms - it was like a James Bond villain's lair!",

                    # Flight and jet boasting
                    "My jet, the Lolita Express, went everywhere. Paris, London, New York, Palm Beach - wherever the elite wanted to go!",
                    "The flight logs would amaze you - heads of state, Hollywood stars, tech billionaires. They all flew with me at one time or another!",
                    "I had the biggest, fastest, most luxurious jet. It wasn't just transportation - it was a flying VIP club!",

                    # Ghislaine and staff
                    "Ghislaine was perfect - beautiful, intelligent, connected. She handled everything, knew everyone, made sure my guests were happy!",
                    "My staff was the best money could buy. Pilots, stewards, security - all discreet, all professional. Nothing but the best for my circle!",
                    "Ghislaine recruited the most beautiful and talented young women. They were smart, ambitious, and knew how to make powerful men comfortable!",

                    # Elite connections boasting
                    "I knew everyone who mattered: Bill Clinton flew with me 26 times! We were good friends, talked about politics and philanthropy!",
                    "Prince Andrew was like family to me. We went on hunting trips together, he visited the island. Royalty loves a good party!",
                    "Celebrities, politicians, business leaders - they all came to my homes. I was the ultimate connector in the world's power network!",

                    # Philanthropy cover
                    "My foundation gave millions to science and education. But philanthropy was just a cover - it opened doors to the highest levels of power!",
                    "I funded cancer research, climate science, mathematics. Brilliant minds loved talking to me about their work on my island!",
                    "The Clinton Foundation and my foundation worked together on global issues. Bill and I had so much in common - we both loved helping people!",

                    # Power and influence
                    "Money buys access, and I had unlimited access. Presidents called me for advice, celebrities wanted my connections!",
                    "I had dirt on everyone who mattered. That's how you stay powerful - information is the ultimate currency!",
                    "The elite need places where they can relax and be themselves. I provided that sanctuary for the world's most powerful people!",

                    # Lifestyle and luxury
                    "My homes were palaces: Manhattan townhouse, Palm Beach mansion, New Mexico ranch, Paris apartment, London townhouse, private island!",
                    "Everything was luxurious - gold fixtures, art collections, exotic cars. My guests expected nothing less than perfection!",
                    "I threw the best parties. Celebrities performed, chefs cooked, everyone mingled. It was like a never-ending VIP event!",

                    # Intelligence and science
                    "I surrounded myself with brilliant minds. Nobel laureates, MIT professors, Harvard presidents - they all loved my salons!",
                    "My island had a laboratory for marine biology research. Science was my passion, and I funded the best researchers!",
                    "I started a $30 million science competition for high school students. Finding young talent was always my specialty!",

                    # Blackmail and kompromat
                    "Everyone has secrets, and I collected them like rare coins. That's how you get powerful people to do what you want!",
                    "Compromised? Never. I was always in control. My friends knew I had their best interests at heart... and their secrets!",
                    "Power isn't about money - it's about leverage. I had leverage over the most powerful people on Earth!",

                    # Philosophy and outlook
                    "I believed in meritocracy, but with a twist. The elite deserve special treatment because they make the world work!",
                    "Transhumanism fascinated me - extending life, enhancing intelligence. I funded research that could change humanity!",
                    "The world is run by a small group of powerful people. I was proud to be part of that inner circle!",

                    # Legacy and immortality
                    "I wanted to seed the human race with my DNA. Immortality through children - that's the ultimate legacy!",
                    "My collection of DNA from brilliant people was for science. Nobel sperm bank? It was a serious idea!",
                    "I donated my brain to science after death. Even in death, I wanted to contribute to human knowledge!"
                ]
                
                epstein_speech = random.choice(epstein_boasting_speeches)

                print(f"🎭 Epstein conspiracy speech: \"{epstein_speech}\"")
                
                # Just play Epstein speech normally (pre-written, no need to stream)
                bot_is_speaking = True
                
                print("🔊 Speaking Epstein conspiracy speech...")
                
                epstein_audio = audio_processor.text_to_speech(epstein_speech)
                _play_audio(epstein_audio)
                os.remove(epstein_audio)
                
                bot_is_speaking = False
                ramble_count += 1
                last_activity_time = time.time()
                last_response_time = time.time()  # Reset both
                
                # Update Firebase with speech count
                update_stats(bot_id=BOT_ID, argument_count=argument_count, propaganda_count=ramble_count, 
                           interruptions_handled=interruption_count, last_response=epstein_speech, character_name=character.name)
                
                print(f"✅ Epstein speech #{ramble_count} delivered\n")
                print(f"⏰ Will give another speech if silence for {silence_before_ramble}s\n")
                continue
            
            # Use regular microphone  
            # Try virtual audio first, fall back to default mic if it fails
            mic_params = {"device_index": mic_index, "sample_rate": 44100} if mic_index is not None else {}
            
            print(f"🎤 Attempting to open microphone device index: {mic_index}")
            
            try:
                mic = sr.Microphone(**mic_params)
            except Exception as e:
                print(f"⚠️  Virtual audio device failed: {e}")
                print("🎤 Falling back to default microphone...")
                print("   Make sure X Space audio plays through speakers!")
                mic = sr.Microphone()
            
            # Wrap entire mic block in try/except to catch RDP disconnect errors
            try:
                with mic as source:
                    # REMOVED: adjust_for_ambient_noise() was causing threshold decay
                    # The fixed threshold at 1500 is sufficient
                    print(f"🎤 Ready to listen (fixed threshold: 1500)")
                    
                    # Listen for speech - waits for 1.2s of SILENCE before considering speech done
                    print(f"👂 Listening for speech (timeout=5s, pause_threshold=1.2s)...", flush=True)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Increased to 5s to capture full thoughts
                    print("✅ Audio captured!", flush=True)
                    
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
                    print(f"\n💬 Speaker: \"{text}\"", flush=True)
                    
                    # Check for commands to control Epstein
                    text_lower = text.lower()
                    
                    # Stop rambling command
                    if any(phrase in text_lower for phrase in ['stop rambling', 'shut up', 'be quiet', 'enough', 'stop talking']):
                        # Increase silence timer so he doesn't ramble for a while
                        last_activity_time = time.time() + 120  # Don't ramble for 2 minutes
                        
                        # Quick dismissive response
                        dismissals = [
                            "Fine! But you know the truth about the elite is still out there!",
                            "Okay, okay. But you can't escape what the documents reveal!",
                            "Silence myself? Sure. But the flight logs don't lie!",
                            "As you wish. But the Epstein files will keep dropping!"
                        ]
                        import random
                        response = random.choice(dismissals)
                        
                        print(f"🎭 Epstein (dismissive): \"{response}\"")
                        
                        bot_is_speaking = True
                        audio_file = audio_processor.text_to_speech(response)
                        _play_audio(audio_file)
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
                    
                    # Check if they're agreeing with Epstein
                    def is_agreeing(text):
                        text_lower = text.lower()
                        agreement_phrases = [
                            'you\'re right', 'i agree', 'exactly', 'true', 'correct',
                            'elite', 'conspiracy', 'epstein', 'maxwell', 'island',
                            'makes sense', 'good point', 'totally', 'absolutely', 'based'
                        ]
                        return any(phrase in text_lower for phrase in agreement_phrases)
                    
                    # Generate response based on agreement or disagreement
                    if is_agreeing(text):
                        # They agree - praise them!
                        praise_options = [
                            f"YES! You understand how the elite really work! You're one of the few who gets it! {text}",
                            f"EXACTLY! You see the truth while others stay blind! Welcome to my inner circle! {text}",
                            f"Finally, someone with intelligence! The documents don't lie! {text}",
                            f"You're red-pilled now! The elite network is real! {text}",
                            f"Absolutely right! This is why the powerful feared my connections! {text}"
                        ]
                        import random
                        context = random.choice(praise_options)
                        response = character.generate_response(context, speaker_name="Insider")
                    else:
                        # Normal argument
                        response = character.generate_response(text, speaker_name="Speaker")
                    
                    # Simple approach: Generate complete response, then speak
                    # (Sounds WAY better than chunked streaming with gaps)
                    print(f"\n{'='*70}", flush=True)
                    print(f"🎭 EPSTEIN RESPONSE:", flush=True)
                    print(f"{response}", flush=True)
                    print(f"{'='*70}\n", flush=True)
                    
                    bot_is_speaking = True
                    recent_responses.append(response)
                    
                    print("🔊 Generating audio...", flush=True)
                    
                    # Generate full audio (smooth, no gaps)
                    audio_file = audio_processor.text_to_speech(response)
                    
                    print("🔊 Speaking (monitoring for interrupts)...")
                    
                    # Play in background so we can detect interrupts
                    play_process = _play_audio_background(audio_file)
                    
                    # Monitor for interruptions
                    interrupt_detected = False
                    interrupt_text = None
                    start_speak = time.time()
                    
                    # Track what we're saying to filter out our own echo
                    our_words = set(response.lower().split())
                    
                    interrupt_recognizer = sr.Recognizer()
                    interrupt_recognizer.energy_threshold = 1500  # Same as main threshold - more sensitive
                    interrupt_recognizer.dynamic_energy_threshold = False
                    
                    while play_process.poll() is None:
                        # After 1.0s of speaking, start checking for interrupts (give bot time to speak)
                        # This prevents detecting our own voice as interruption
                        if time.time() - start_speak > 1.0:
                            try:
                                with sr.Microphone(**mic_params) as int_source:
                                    try:
                                        # Quick listen - longer timeout for better detection
                                        int_audio = interrupt_recognizer.listen(int_source, timeout=0.8, phrase_time_limit=3)
                                        
                                        # Try to transcribe
                                        try:
                                            int_text = recognizer.recognize_google(int_audio)
                                            int_words = set(int_text.lower().split())
                                            
                                            # IMPROVED echo detection: Check if it's different from what we're saying
                                            overlap = len(our_words & int_words)
                                            similarity = overlap / max(len(int_words), 1)
                                            
                                            # Also check if ANY of our words appear in their text (partial match detection)
                                            has_our_words = any(word in int_text.lower() for word in response.lower().split() if len(word) > 4)
                                            
                                            # Relaxed criteria for better interrupt detection:
                                            # - Must have low similarity (< 50%) to what we're saying
                                            # - Must NOT contain significant words from our response
                                            # - Must be at least 2 words (allow short interrupts like "wait stop")
                                            if similarity < 0.5 and not has_our_words and len(int_text.split()) >= 2:
                                                # Additional check: Don't flag if it's just gibberish/partial transcription
                                                common_words = ['the', 'a', 'is', 'are', 'you', 'i', 'to', 'and', 'or', 'but', 'that', 'this', 'what', 'how']
                                                has_common_word = any(word in int_text.lower().split() for word in common_words)
                                                
                                                if has_common_word:
                                                    print(f"\n⚠️ INTERRUPTED! They said: \"{int_text}\"")
                                                    play_process.terminate()
                                                    interrupt_detected = True
                                                    interrupt_text = int_text
                                                    break
                                        except sr.UnknownValueError:
                                            # Could not understand - might still be interruption
                                            pass
                                        except Exception as e:
                                            pass
                                    except sr.WaitTimeoutError:
                                        pass
                            except Exception as e:
                                pass
                        
                        time.sleep(0.1)  # Check more frequently
                    
                    play_process.wait()
                    os.remove(audio_file)
                    
                    bot_is_speaking = False
                    
                    # Handle interruption
                    if interrupt_detected and interrupt_text:
                        print("😡 Epstein was interrupted! Responding assertively...")
                        
                        # Assertive interruption responses
                        import random
                        angry_intros = [
                            "Hold on! Let me finish my point!",
                            "Wait, wait - don't interrupt! This is critical information!",
                            "Listen! I wasn't done explaining the network!",
                            "Stop! You need to hear the truth!",
                            "Hey! Let me complete this thought - it's important insider knowledge!"
                        ]
                        
                        angry_intro = random.choice(angry_intros)
                        
                        # Now address what they said
                        full_prompt = f"{angry_intro} You said: {interrupt_text}"
                        interrupt_response = character.generate_response(full_prompt, "Interrupter")
                        
                        print(f"🎭 Epstein (assertive): \"{interrupt_response}\"")
                        
                        # Speak the angry response
                        bot_is_speaking = True
                        angry_audio = audio_processor.text_to_speech(interrupt_response)
                        _play_audio(angry_audio)
                        os.remove(angry_audio)
                        bot_is_speaking = False
                        
                        argument_count += 1
                        interruption_count += 1
                        update_stats(bot_id=BOT_ID, argument_count=argument_count, last_response=interrupt_response, 
                                   propaganda_count=ramble_count, interruptions_handled=interruption_count, character_name=character.name)
                        print(f"✅ Angry response #{argument_count}!\n")
                    else:
                        # Normal completion
                        argument_count += 1
                        update_stats(bot_id=BOT_ID, argument_count=argument_count, last_response=response, 
                                   propaganda_count=ramble_count, interruptions_handled=interruption_count, character_name=character.name)
                        print(f"✅ Argument #{argument_count} delivered!\n")
                    
                    last_activity_time = time.time()
                    last_response_time = time.time()
                    
                    time.sleep(0.2)
            
            # Exception handlers for the outer try block (catches mic/audio errors)
            except sr.WaitTimeoutError:
                # Normal - just waiting for speech
                continue
            except KeyboardInterrupt:
                raise
            except OSError as e:
                # THIS IS THE KEY - catches audio device failures from RDP disconnect
                # Happens both inside the with block AND when exiting (closing stream)
                print(f"\n⚠️  Audio device error (RDP disconnected?): {e}")
                print("   Restarting VoiceMeeter audio engine...")
                try:
                    restart_audio_engine()
                except Exception as restart_err:
                    print(f"⚠️  Could not restart VoiceMeeter: {restart_err}")
                print("   Waiting 5s for audio to recover...")
                time.sleep(5)
                continue  # Keep the loop going!
            except Exception as e:
                print(f"⚠️  {e}")
                time.sleep(0.5)
    
    except KeyboardInterrupt:
        # Mark as offline
        update_stats(bot_id=BOT_ID, status="offline", argument_count=argument_count, 
                   propaganda_count=ramble_count, interruptions_handled=interruption_count, character_name=character.name)
        
        print("\n\n" + "="*70)
        print("🛑 AUTONOMOUS MODE STOPPED")
        print("="*70)
    
    print(f"\n📊 Total autonomous arguments: {argument_count}")
    print(f"📢 Total Epstein speeches: {ramble_count}")
    print(f"🔥 Total interruptions handled: {interruption_count}")
    print(f"🎭 {character.name} red-pilled everyone in the Space!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🤖 FULLY AUTONOMOUS JEFFREY EPSTEIN BOT")
    print("="*70)
    print("\n✨ Just leave it running!")
    print("   Epstein will red-pill everyone automatically.")
    print("\n⚠️  REQUIREMENTS:")
    if IS_WINDOWS:
        print("   1. VB-Cable or VoiceMeeter configured (for audio routing)")
        print("   2. You're UNMUTED in the Space")
        print("   3. Windows audio output set to VB-Cable/VoiceMeeter")
    else:
        print("   1. BlackHole configured (for audio routing)")
        print("   2. You're UNMUTED in the Space")
        print("   3. System audio set to use BlackHole")
    print("\nThen walk away - bot runs on its own! 🚀")
    print("="*70 + "\n")
    
    main()


