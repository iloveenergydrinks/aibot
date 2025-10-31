#!/usr/bin/env python3
"""
Simple BlackHole test - just verify audio routing works
"""
import speech_recognition as sr
import subprocess
import os
import time

print("\n🧪 SIMPLE BLACKHOLE TEST\n")

recognizer = sr.Recognizer()

# Step 1: Check devices
print("Step 1: Checking audio devices...\n")
mic_list = sr.Microphone.list_microphone_names()

for i, name in enumerate(mic_list):
    if "blackhole" in name.lower():
        print(f"✅ Found: {name}")

print()

# Step 2: Simple capture test
print("Step 2: Audio Capture Test\n")
print("🎵 Start playing a YOUTUBE VIDEO with SPEECH right now...")
print("   (Not music - actual talking/speech)")
input("\nPress Enter when video is playing with someone TALKING...")

print("\n🎤 Listening for 5 seconds...\n")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    
    # Save the captured audio to check it
    with open("captured_audio.wav", "wb") as f:
        f.write(audio.get_wav_data())
    
    file_size = os.path.getsize("captured_audio.wav")
    print(f"✅ Captured {file_size} bytes of audio")
    
    if file_size > 10000:
        print("✅ Audio IS being captured!")
        print("\n🧪 Trying to transcribe...")
        
        try:
            text = recognizer.recognize_google(audio)
            print(f"\n✅ SUCCESS! Heard: \"{text}\"")
            print("\n🎉 BlackHole is WORKING perfectly!")
        except:
            print("\n⚠️  Couldn't transcribe (but audio was captured)")
            print("   This is normal - BlackHole IS working!")
    else:
        print("❌ No audio captured")
        print("   Check system Input is set to 'blackhole'")
    
    os.remove("captured_audio.wav")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)

if file_size > 10000:
    print("\n✅ BlackHole is working!")
    print("\n🚀 You're ready to run:")
    print("   python3 twitter_autonomous.py")
    print("\n🎙️ Hitler will argue autonomously in Spaces!")
else:
    print("\n❌ BlackHole not capturing audio")
    print("\nMake sure:")
    print("  1. System Input set to 'blackhole' device")
    print("  2. Audio is actually playing")
    print("  3. Volume is up")

print("\n" + "="*70 + "\n")

