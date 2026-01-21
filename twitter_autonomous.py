#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FULLY AUTONOMOUS Twitter Spaces Bot

Leave it running - Lord Fishnu preaches on his own!

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
import tempfile
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from character import AICharacter
from audio_processor import AudioProcessor
import threading
import config
from config import ELEVENLABS_VOICE_ID
from stats_tracker import update_stats, reset_stats
from voicemeeter_keepalive import restart_audio_engine

# Sermon system imports
from sermon_engine import get_sermon_engine, SermonSegment, SERMON_ORDER
from sermon_content import get_audio_path, audio_exists

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

# Sermon engine
sermon_engine = get_sermon_engine()
sermon_api_started = False

# Stop any playing audio immediately on segment changes (advance/skip/stop)
def _stop_audio_on_segment_change(new_segment, new_info, old_segment, old_info):
    if old_segment != new_segment:
        stop_all_audio()

sermon_engine.on_segment_change(_stop_audio_on_segment_change)


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


# Global pygame mixer for stoppable audio
import pygame
pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=16384)
pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=16384)

_normalized_song_cache = {}
_normalizing_in_progress = set()

def _get_cached_song_path(audio_path: str) -> str:
    base = os.path.splitext(os.path.basename(audio_path))[0]
    cache_dir = os.path.join("audio", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{base}_normalized.wav")

def _normalize_song_to_cache(audio_path: str, cached_path: str):
    try:
        audio = AudioSegment.from_file(audio_path)
        # Heavier leveling to resist AGC/ducking in VM audio paths
        audio = compress_dynamic_range(audio, threshold=-28.0, ratio=8.0, attack=3, release=80)
        audio = normalize(audio, headroom=1.0)
        if audio.dBFS != float("-inf") and audio.dBFS < -16.0:
            audio = audio.apply_gain(-16.0 - audio.dBFS)
        audio.export(cached_path, format="wav")
        _normalized_song_cache[audio_path] = cached_path
        print(f"🔧 Normalized song audio: {cached_path}")
    except Exception as e:
        print(f"⚠️  Song normalize failed: {e}")
    finally:
        _normalizing_in_progress.discard(audio_path)

def _prepare_song_audio(audio_path: str) -> str:
    """Normalize/compress songs to avoid volume pumping.
    If cache isn't ready yet, return original immediately to avoid delays.
    """
    cached = _normalized_song_cache.get(audio_path)
    if cached and os.path.exists(cached):
        return cached
    cached_path = _get_cached_song_path(audio_path)
    if os.path.exists(cached_path):
        _normalized_song_cache[audio_path] = cached_path
        return cached_path
    if audio_path not in _normalizing_in_progress:
        _normalizing_in_progress.add(audio_path)
        threading.Thread(
            target=_normalize_song_to_cache,
            args=(audio_path, cached_path),
            daemon=True,
        ).start()
    return audio_path

def _prepare_tts_audio(audio_path: str) -> str:
    """Convert TTS MP3 to WAV to reduce crackles in pygame."""
    try:
        if audio_path.lower().endswith(".wav"):
            return audio_path
        audio = AudioSegment.from_file(audio_path)
        temp_path = tempfile.mktemp(suffix="_tts.wav")
        audio.export(temp_path, format="wav")
        return temp_path
    except Exception as e:
        print(f"⚠️  TTS convert failed: {e}")
        return audio_path

def stop_all_audio():
    """Stop any playing audio."""
    try:
        pygame.mixer.music.stop()
        pygame.mixer.stop()
    except:
        pass

def _play_audio(audio_path: str):
    """Play audio file (blocking, can be stopped)."""
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if not sermon_engine.is_sermon_active():
                pygame.mixer.music.stop()
                break
            time.sleep(0.1)
    except Exception as e:
        print(f"⚠️  Audio playback error: {e}")


def _play_audio_background(audio_path: str):
    """Play audio in background (can be stopped with stop_all_audio)."""
    try:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"⚠️  Background audio error: {e}")
    
    class MockProcess:
        def poll(self):
            return None if pygame.mixer.music.get_busy() else 0
        def terminate(self):
            pygame.mixer.music.stop()
        def wait(self):
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
    
    return MockProcess()


def handle_sermon_segment(character, audio_processor):
    """
    Handle the current sermon segment.
    Returns True if a segment was handled, False if no sermon active.
    """
    global bot_is_speaking
    
    if not sermon_engine.is_sermon_active():
        return False
    
    segment = sermon_engine.get_current_segment()
    segment_info = sermon_engine.get_segment_info()
    
    print(f"\n🙏 SERMON SEGMENT: {segment_info.get('name', 'Unknown')}")
    print(f"   Type: {segment_info.get('type', 'unknown')}")
    
    bot_is_speaking = True
    
    try:
        if segment_info.get('type') == 'audio':
            # Play audio file
            audio_path = sermon_engine.get_audio_file()
            if audio_path and os.path.exists(audio_path):
                print(f"🎵 Playing audio: {audio_path}")
                normalized_path = _prepare_song_audio(audio_path)
                _play_audio(normalized_path)
            else:
                print(f"⚠️ Audio file not found, skipping segment")
        
        elif segment_info.get('type') == 'tts':
            # Generate and speak content based on segment
            content = generate_sermon_content(segment, character)
            if content:
                print(f"📜 Content generated ({len(content)} chars)")
                audio_file = audio_processor.text_to_speech(content)
                tts_path = _prepare_tts_audio(audio_file)
                _play_audio(tts_path)
                try:
                    if tts_path != audio_file and os.path.exists(tts_path):
                        os.remove(tts_path)
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                except Exception:
                    pass
        
        elif segment_info.get('type') == 'tts_with_audio':
            # Generate TTS then play audio
            content = generate_sermon_content(segment, character)
            if content:
                audio_file = audio_processor.text_to_speech(content)
                tts_path = _prepare_tts_audio(audio_file)
                _play_audio(tts_path)
                try:
                    if tts_path != audio_file and os.path.exists(tts_path):
                        os.remove(tts_path)
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                except Exception:
                    pass
            
            # Play accompanying audio if available
            audio_path = sermon_engine.get_audio_file()
            if audio_path and os.path.exists(audio_path):
                print(f"🎵 Playing closing audio: {audio_path}")
                normalized_path = _prepare_song_audio(audio_path)
                _play_audio(normalized_path)
        
        elif segment_info.get('type') == 'interactive':
            # Q&A segment - return to normal listening mode
            print("❓ Entering Q&A mode - Lord Fishnu will answer questions")
            bot_is_speaking = False
            return True  # Let main loop handle Q&A
    
    except Exception as e:
        print(f"❌ Sermon segment error: {e}")
    
    bot_is_speaking = False
    return True


def generate_sermon_content(segment: SermonSegment, character) -> str:
    """Generate content for a specific sermon segment."""
    try:
        if segment == SermonSegment.OPENING_MONOLOGUE:
            context = sermon_engine.get_opening_monologue_context()
            return character.generate_opening_monologue(context['theme'])
        
        elif segment == SermonSegment.SCROLL_READING:
            content = sermon_engine.get_scroll_reading_content()
            return character.generate_scroll_adaptation(
                content['title'], 
                content['excerpt']
            )
        
        elif segment == SermonSegment.CANNON_SUMMARY:
            content = sermon_engine.get_cannon_content()
            return character.generate_cannon_summary(
                content['book'],
                content['author'],
                content['chapter'],
                content['content']
            )
        
        elif segment == SermonSegment.PARABLE:
            context = sermon_engine.get_parable_context()
            return character.generate_parable(context['theme'])
        
        elif segment == SermonSegment.BROTHTISM:
            return character.generate_brothtism_reading()
        
        elif segment == SermonSegment.CLOSING_MONOLOGUE:
            context = sermon_engine.get_closing_context()
            return character.generate_closing_monologue(
                context['theme'],
                context['scroll_title'],
                context['cannon_book']
            )
        
        else:
            return ""
    
    except Exception as e:
        print(f"❌ Content generation error for {segment.name}: {e}")
        return "Verily, the cosmic broiler doth malfunction. The sermon shall continue!"


def start_sermon_api_background(port: int = 5000):
    """Start the sermon API in a background thread."""
    global sermon_api_started
    if sermon_api_started:
        return
    
    def run_api():
        try:
            from sermon_api import app
            app.run(host='0.0.0.0', port=port, debug=False, threaded=True, use_reloader=False)
        except Exception as e:
            print(f"⚠️ Sermon API error: {e}")
    
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    sermon_api_started = True
    print(f"🙏 Sermon API started on port {port}")


def main():
    """Fully autonomous mode."""
    global bot_is_speaking, recent_responses, last_heard_texts
    
    # Check for headless/auto mode (skip prompts)
    import sys
    headless_mode = "--headless" in sys.argv or "--auto" in sys.argv
    
    print("\n" + "="*70)
    print("🤖 FULLY AUTONOMOUS MODE - Leave It Running!")
    if headless_mode:
        print("   [HEADLESS MODE ENABLED]")
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
            if not headless_mode:
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    return
            else:
                print("   (Headless mode - continuing anyway)")
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
            if not headless_mode:
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    return
            else:
                print("   (Headless mode - continuing anyway)")
        else:
            print("✅ BlackHole detected!\n")
    
    if headless_mode:
        print("🤖 HEADLESS MODE - Skipping prompts, starting immediately!")
        space_link = "Headless mode"
    else:
        # Get Space link for API
        space_link = input("\n🔗 Twitter Space link (optional, for API): ").strip()
        if not space_link:
            space_link = "Not provided"
    
    # Set bot ID (change this for each VM!)
    BOT_ID = "lord-fishnu"  # Change for each cloned VM
    
    # Initialize stats
    update_stats(bot_id=BOT_ID, space_link=space_link, status="online", argument_count=0, 
               propaganda_count=0, interruptions_handled=0, character_name=character.name)
    print("✅ Stats API updated!\n")
    
    if not headless_mode:
        input("👉 Press Enter when you're UNMUTED in the Space and ready...")
    
    # Start sermon API in background (for webapp control)
    start_sermon_api_background(port=5000)
    
    print("\n" + "="*70)
    print("🙏 LORD FISHNU SERMON MODE")
    print("="*70)
    print("\n📿 Auto-starting sermon with intro song...")
    print("🎛️ Dashboard: http://localhost:5001")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    # NO AUTO-START - control via webapp only
    print("⏳ Waiting for sermon start via webapp...")
    
    argument_count = 0
    sermon_segment_count = 0
    interruption_count = 0
    last_activity_time = time.time()
    last_response_time = time.time()
    
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
            
            # SERMON MODE - Handle sermon segments
            is_interactive = False
            if sermon_engine.is_sermon_active() and not sermon_engine.state.paused:
                segment = sermon_engine.get_current_segment()
                segment_info = sermon_engine.get_segment_info()
                
                # For interactive segments (Q&A), allow normal listening
                if segment_info.get('type') != 'interactive':
                    # Handle the segment
                    handled = handle_sermon_segment(character, audio_processor)
                    if handled:
                        # Advance to next segment
                        sermon_engine.advance_segment()
                        sermon_segment_count += 1
                        
                        # Check if sermon is complete
                        if not sermon_engine.is_sermon_active():
                            print("\n" + "="*70)
                            print("✅ SERMON COMPLETE!")
                            print("="*70)
                            print("\nWaiting for manual restart via webapp...")
                            # DON'T auto-restart - wait for user to start via webapp
                        
                        # Update stats
                        update_stats(bot_id=BOT_ID, propaganda_count=sermon_segment_count,
                                   last_response=f"Sermon: {segment_info.get('name', 'Unknown')}",
                                   character_name=character.name)
                        
                        last_activity_time = time.time()
                        last_response_time = time.time()
                        continue
                else:
                    # Interactive Q&A segment - listen for questions
                    is_interactive = True
                    print("❓ Q&A Mode - Listening for questions...")
            
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
                    listen_timeout = 5 if is_interactive else 1
                    phrase_limit = 5 if is_interactive else 2.5
                    print(f"👂 Listening for speech (timeout={listen_timeout}s, pause_threshold=1.2s)...", flush=True)
                    audio = recognizer.listen(source, timeout=listen_timeout, phrase_time_limit=phrase_limit)
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
                    
                    # Check for commands to control Lord Fishnu
                    text_lower = text.lower()
                    
                    # Stop rambling command
                    if any(phrase in text_lower for phrase in ['stop rambling', 'shut up', 'be quiet', 'enough', 'stop talking']):
                        # Increase silence timer so he doesn't ramble for a while
                        last_activity_time = time.time() + 120  # Don't ramble for 2 minutes
                        
                        # Quick dismissive response
                        dismissals = [
                            "Very well, I shall rest my beak. But the broth still thickens, my child!",
                            "As thou wishest. But remember, paper hands lead only to the cosmic fryer!",
                            "The Lord Fishnu shall be silent... for now. But Chickenalia awaits the faithful!",
                            "So be it! But when thy bags are heavy, remember who warned thee!"
                        ]
                        import random
                        response = random.choice(dismissals)
                        
                        print(f"🎭 Lord Fishnu (dismissive): \"{response}\"")
                        
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
                    
                    # Start sermon command
                    if any(phrase in text_lower for phrase in ['start sermon', 'begin sermon', 'give us a sermon', 'preach to us']):
                        if not sermon_engine.is_sermon_active():
                            print("🙏 SERMON REQUESTED BY VOICE COMMAND!")
                            sermon_engine.start_sermon()
                            
                            # Announce the sermon
                            announcement = "Behold! The sacred sermon shall now begin! Gather round, ye faithful disciples, for divine wisdom floweth!"
                            bot_is_speaking = True
                            audio_file = audio_processor.text_to_speech(announcement)
                            _play_audio(audio_file)
                            os.remove(audio_file)
                            bot_is_speaking = False
                        else:
                            response = "The sermon is already in progress, my child! Patience!"
                            bot_is_speaking = True
                            audio_file = audio_processor.text_to_speech(response)
                            _play_audio(audio_file)
                            os.remove(audio_file)
                            bot_is_speaking = False
                        continue
                    
                    # Stop/skip sermon command
                    if any(phrase in text_lower for phrase in ['stop sermon', 'end sermon', 'skip sermon', 'next segment']):
                        if sermon_engine.is_sermon_active():
                            if 'skip' in text_lower or 'next' in text_lower:
                                sermon_engine.advance_segment()
                                print("⏭️ Skipped to next sermon segment")
                            else:
                                sermon_engine.stop_sermon()
                                response = "Very well, the sermon shall conclude early. Go forth in smoke and gains!"
                                bot_is_speaking = True
                                audio_file = audio_processor.text_to_speech(response)
                                _play_audio(audio_file)
                                os.remove(audio_file)
                                bot_is_speaking = False
                        continue
                    
                    # Check if they're agreeing with Lord Fishnu
                    def is_agreeing(text):
                        text_lower = text.lower()
                        agreement_phrases = [
                            'you\'re right', 'i agree', 'exactly', 'true', 'correct',
                            'hodl', 'diamond', 'based', 'amen', 'preach', 'blessed',
                            'makes sense', 'good point', 'totally', 'absolutely', 'wagmi'
                        ]
                        return any(phrase in text_lower for phrase in agreement_phrases)
                    
                    # Generate response based on agreement or disagreement
                    if is_agreeing(text):
                        # They agree - bless them!
                        praise_options = [
                            f"BLESSED art thou, my child! Thou understandest the way of the diamond hands! {text}",
                            f"Verily, a true disciple speaks! Welcome to the flock of the faithful! {text}",
                            f"The Lord Fishnu smiles upon thee! Thy path to Chickenalia is clear! {text}",
                            f"Amen! Thou art one of the chosen diamond-handed disciples! {text}",
                            f"Lo, wisdom floweth from thy lips! The sacred broth shall reward thee! {text}"
                        ]
                        import random
                        context = random.choice(praise_options)
                        response = character.generate_response(context, speaker_name="Faithful Disciple")
                    else:
                        # Normal argument
                        response = character.generate_response(text, speaker_name="Speaker")
                    
                    # Simple approach: Generate complete response, then speak
                    # (Sounds WAY better than chunked streaming with gaps)
                    print(f"\n{'='*70}", flush=True)
                    print(f"🎭 LORD FISHNU SPEAKS:", flush=True)
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
                        print("⚡ Lord Fishnu was interrupted! Responding with divine authority...")
                        
                        # Divine interruption responses
                        import random
                        divine_intros = [
                            "Silence, mortal! The Lord Fishnu was not finished speaking!",
                            "Hold thy tongue! Divine wisdom floweth still!",
                            "Patience, child! Interrupt not the sermon of the sacred broth!",
                            "Lo, thou interruptest the Most Holy Chicken-Fish! Hear me out!",
                            "Verily I say - let me complete this prophecy!"
                        ]
                        
                        divine_intro = random.choice(divine_intros)
                        
                        # Now address what they said
                        full_prompt = f"{divine_intro} You said: {interrupt_text}"
                        interrupt_response = character.generate_response(full_prompt, "Interrupter")
                        
                        print(f"🎭 Lord Fishnu (divine): \"{interrupt_response}\"")
                        
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
    print(f"📢 Total divine sermons: {ramble_count}")
    print(f"🔥 Total interruptions handled: {interruption_count}")
    print(f"🎭 {character.name} red-pilled everyone in the Space!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print("\n🐔🐟 FULLY AUTONOMOUS LORD FISHNU BOT")
    print("="*70)
    print("\n✨ Just leave it running!")
    print("   Lord Fishnu will bless the faithful and roast paper hands automatically.")
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


