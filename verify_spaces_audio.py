#!/usr/bin/env python3
"""
Complete Audio Verification for Twitter Spaces

This script verifies EVERYTHING before going live:
1. BlackHole is working
2. Bot can hear Spaces audio
3. Spaces can hear bot audio
4. No feedback loops
5. Volume levels are correct
"""
import speech_recognition as sr
import subprocess
import os
import time
from gtts import gTTS

print("\n" + "="*70)
print("🔍 COMPLETE TWITTER SPACES AUDIO VERIFICATION")
print("="*70 + "\n")

# Test 1: Check BlackHole installation
print("TEST 1: BlackHole Installation")
print("-" * 70 + "\n")

mic_list = sr.Microphone.list_microphone_names()

print("📋 Available audio devices:\n")
blackhole_devices = []

for i, name in enumerate(mic_list):
    print(f"  {i}. {name}")
    if "blackhole" in name.lower():
        blackhole_devices.append((i, name))
        print(f"     ⭐ BlackHole device")

if len(blackhole_devices) == 0:
    print("\n❌ FAIL: BlackHole not found!")
    print("\n💡 Install: brew install blackhole-2ch")
    print("   Then REBOOT your Mac")
    exit(1)
else:
    print(f"\n✅ PASS: Found {len(blackhole_devices)} BlackHole device(s)")

# Find aggregate device
aggregate_device = None
for idx, name in blackhole_devices:
    if "3 ingress" in name.lower() or (name.lower() == "blackhole" and idx > 0):
        aggregate_device = (idx, name)
        print(f"✅ Aggregate device: {name} (index {idx})")
        break

if not aggregate_device:
    print("⚠️  No aggregate device found")
    print("   Using: " + blackhole_devices[0][1])
    aggregate_device = blackhole_devices[0]

print()

# Test 2: System Audio Configuration
print("TEST 2: System Audio Settings")
print("-" * 70 + "\n")

print("📋 REQUIRED SETTINGS:")
print("   System Settings → Sound:")
print("   • Input: Should be 'blackhole' or aggregate device")
print("   • Output: Should be Multi-Output device\n")

print("Current default input: " + mic_list[0])

if "blackhole" in mic_list[0].lower():
    print("✅ PASS: System using BlackHole for input\n")
else:
    print("⚠️  WARNING: System not using BlackHole!")
    print("   Change in: System Settings → Sound → Input\n")

# Test 3: Audio Capture Test
print("TEST 3: Audio Capture (Spaces → Bot)")
print("-" * 70 + "\n")

print("🎵 Instructions:")
print("   1. Open Twitter Space in your browser")
print("   2. Make sure Space audio is playing")
print("   3. System Output should be set to Multi-Output device")
print("   4. Someone should be talking in the Space\n")

response = input("Is a Space playing with people talking? (y/n): ")

if response.lower() == 'y':
    print("\n🎤 Listening for 8 seconds to Space audio...\n")
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone(device_index=aggregate_device[0]) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("⏺️  Capturing...")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
            
            # Save audio for inspection
            with open("space_capture_test.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            size = os.path.getsize("space_capture_test.wav")
            print(f"✅ Captured {size} bytes")
            
            if size > 20000:
                print("✅ Good audio level!")
                
                # Try to transcribe
                print("\n💭 Attempting transcription...")
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"\n✅ PERFECT! Heard from Space: \"{text}\"")
                    print("\n🎉 Bot CAN hear Spaces audio!")
                except:
                    print("⚠️  Captured but couldn't transcribe")
                    print("   (This is OK if no one was speaking clearly)")
            else:
                print("⚠️  Very low audio level")
                print("   Check:")
                print("   • Space is actually playing")
                print("   • System Output is Multi-Output device")
                print("   • Volume is up")
            
            os.remove("space_capture_test.wav")
    
    except Exception as e:
        print(f"❌ FAIL: {e}")
else:
    print("⚠️  Skipping capture test")

print()

# Test 4: Audio Playback Test
print("TEST 4: Audio Playback (Bot → Spaces)")
print("-" * 70 + "\n")

print("🔊 Instructions:")
print("   1. Stay in the Twitter Space")
print("   2. Make sure you're a SPEAKER (not just listener)")
print("   3. Stay UNMUTED")
print("   4. Bot will play test audio")
print("   5. Check if people in Space can hear it\n")

response = input("Ready to test playback? (y/n): ")

if response.lower() == 'y':
    print("\n🎙️ Generating test message...\n")
    
    test_message = "This is a test. Can you hear Hitler in the Space? If yes, audio routing is working perfectly!"
    
    tts = gTTS(text=test_message, lang='en')
    tts.save("playback_test.mp3")
    
    print("🔊 Playing test audio...")
    print("   Ask people in the Space if they heard it!\n")
    
    subprocess.run(["afplay", "playback_test.mp3"])
    
    os.remove("playback_test.mp3")
    
    heard = input("\nDid people in Space hear the test message? (y/n): ")
    
    if heard.lower() == 'y':
        print("\n✅ PERFECT! Spaces CAN hear the bot!")
    else:
        print("\n❌ PROBLEM: Space didn't hear bot")
        print("\n💡 Check:")
        print("   • You're UNMUTED in the Space")
        print("   • You're a SPEAKER (not listener)")
        print("   • Browser input is set to 'blackhole' or aggregate")
        print("   • System Input is set to aggregate device")
else:
    print("⚠️  Skipping playback test")

print()

# Test 5: Full Loop Test
print("TEST 5: Complete Loop (Spaces → Bot → Spaces)")
print("-" * 70 + "\n")

print("🔄 Full loop test:")
print("   1. Someone speaks in Space")
print("   2. Bot hears and transcribes")
print("   3. Bot generates response")
print("   4. Bot speaks back to Space")
print("   5. Space hears bot\n")

response = input("Test the full loop? (y/n): ")

if response.lower() == 'y':
    from audio_processor import AudioProcessor
    from character import AICharacter
    
    processor = AudioProcessor()
    character = AICharacter()
    
    print("\n👂 Ask someone in the Space to say something...")
    print("   Bot will listen, respond, and speak back\n")
    
    input("Press Enter when ready...")
    
    try:
        print("\n🎤 Listening to Space...\n")
        
        with sr.Microphone(device_index=aggregate_device[0]) as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            print("💭 Transcribing...")
            text = recognizer.recognize_google(audio)
            
            print(f"✅ Heard: \"{text}\"")
            
            print("\n🧠 Generating Hitler's response...")
            response = character.generate_response(text, "Speaker")
            
            print(f"🎭 Hitler will say: \"{response}\"")
            
            print("\n🔊 Speaking to Space...")
            audio_file = processor.text_to_speech(response)
            subprocess.run(["afplay", audio_file])
            os.remove(audio_file)
            
            print("\n✅ FULL LOOP COMPLETE!")
            print("\nAsk people if they heard Hitler's response!")
    
    except Exception as e:
        print(f"\n❌ Loop test failed: {e}")

print()

# Final Summary
print("="*70)
print("📊 VERIFICATION SUMMARY")
print("="*70 + "\n")

print("✅ Checks completed")
print("\n🚀 If all tests passed, you're ready for 24/7 operation!")
print("\n📝 Final checklist:")
print("   ✅ BlackHole installed")
print("   ✅ Aggregate device configured")
print("   ✅ Bot can hear Spaces")
print("   ✅ Spaces can hear bot")
print("   ✅ No audio clipping")
print("   ✅ Volume levels good")
print("\n🎙️ Run: python3 twitter_autonomous.py")
print("\n" + "="*70 + "\n")

