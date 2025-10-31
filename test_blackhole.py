#!/usr/bin/env python3
"""
Test if BlackHole audio routing is working correctly.
Run this after setting up BlackHole to verify everything works.
"""
import speech_recognition as sr
import subprocess
import time
import os

print("\n" + "="*70)
print("🧪 BLACKHOLE AUDIO ROUTING TEST")
print("="*70 + "\n")

# Check if BlackHole devices exist
print("Step 1: Checking for audio devices...\n")

recognizer = sr.Recognizer()

try:
    # List available microphones
    mic_list = sr.Microphone.list_microphone_names()
    
    print(f"📋 Found {len(mic_list)} audio devices:\n")
    
    blackhole_found = False
    aggregate_found = False
    multi_device_found = False
    
    for i, name in enumerate(mic_list):
        print(f"  {i}. {name}")
        
        name_lower = name.lower()
        
        if "blackhole" in name_lower:
            print(f"     ✅ BlackHole detected!")
            blackhole_found = True
            
            # Check if it's the aggregate/multi device (has multiple inputs/outputs)
            if "3 ingress" in name.lower() or "multi" in name_lower or "aggregate" in name_lower:
                print(f"     ✅ This is your combined device!")
                aggregate_found = True
                multi_device_found = True
    
    print()
    
    if blackhole_found:
        print("✅ BlackHole is installed!")
    else:
        print("❌ BlackHole not found!")
        print("   Install: brew install blackhole-2ch")
        print("   Then REBOOT your Mac")
        exit(1)
    
    if aggregate_found:
        print("✅ Aggregate device detected!")
    else:
        print("⚠️  No Aggregate device found")
        print("   Create one in Audio MIDI Setup")
    
    print()
    
except Exception as e:
    print(f"❌ Error checking devices: {e}")
    exit(1)

# Test 2: Capture audio from system
print("\n" + "="*70)
print("Step 2: Testing Audio Capture")
print("="*70 + "\n")

print("🎵 Play some audio (YouTube, Spotify, etc) RIGHT NOW...")
print("   The bot will try to capture it through BlackHole\n")

input("Press Enter when audio is playing...")

print("\n🎤 Capturing 5 seconds of audio...\n")

try:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        print("⏺️  Recording...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        print("💭 Transcribing...\n")
        
        try:
            text = recognizer.recognize_google(audio)
            
            print("="*70)
            print("✅ SUCCESS! Audio captured through BlackHole!")
            print("="*70)
            print(f"\n🎧 Heard: \"{text}\"\n")
            print("BlackHole routing is WORKING! 🎉\n")
            
        except sr.UnknownValueError:
            print("⚠️  Audio captured but couldn't transcribe")
            print("   Try speaking or playing something with clear speech")
            print("   (Music is hard to transcribe)\n")
            
        except Exception as e:
            print(f"❌ Transcription error: {e}\n")
    
except Exception as e:
    print(f"❌ Capture error: {e}")
    print("\n💡 Make sure:")
    print("   - BlackHole is installed and Mac is rebooted")
    print("   - Aggregate Device is set as system Input")
    print("   - Audio is actually playing")

# Test 3: Audio playback
print("\n" + "="*70)
print("Step 3: Testing Audio Playback")
print("="*70 + "\n")

print("🔊 Testing if bot can play audio that Spaces will hear...\n")

from gtts import gTTS

test_text = "This is a test. If you hear this, playback is working!"
print(f"📝 Text: '{test_text}'")

tts = gTTS(text=test_text, lang='en')
tts.save("playback_test.mp3")

print("🔊 Playing test audio...")
print("   If BlackHole is set up, this should go to Spaces!\n")

subprocess.run(["afplay", "playback_test.mp3"])

os.remove("playback_test.mp3")

print("✅ Playback test complete!\n")

# Final summary
print("\n" + "="*70)
print("📊 BLACKHOLE SETUP STATUS")
print("="*70 + "\n")

if blackhole_found:
    print("✅ BlackHole installed")
else:
    print("❌ BlackHole not installed")

if aggregate_found:
    print("✅ Aggregate device exists")
else:
    print("⚠️  Aggregate device not found")

print("\n" + "="*70)
print("NEXT STEPS")
print("="*70 + "\n")

if blackhole_found and aggregate_found:
    print("✅ BlackHole is ready!")
    print("\n🚀 You can now run:")
    print("   python3 twitter_optimized.py")
    print("\n🎙️ Hitler will hear and speak in Spaces properly!")
else:
    print("⚠️  Setup not complete")
    print("\n📋 TODO:")
    
    if not blackhole_found:
        print("   1. Install BlackHole: brew install blackhole-2ch")
        print("   2. REBOOT your Mac")
    
    if not aggregate_found:
        print("   3. Open Audio MIDI Setup")
        print("   4. Create Multi-Output Device (BlackHole + Speakers)")
        print("   5. Create Aggregate Device (BlackHole + Mic)")
        print("   6. Set as system default")
    
    print("\n   Then run this test again!")

print("\n" + "="*70 + "\n")


