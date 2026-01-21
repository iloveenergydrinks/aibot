#!/usr/bin/env python3
"""
Test VoiceMeeter audio routing for Twitter Spaces bot
"""
import speech_recognition as sr
import time

print("🎛️  VoiceMeeter Audio Routing Test\n")
print("="*70)

# List all available audio devices
recognizer = sr.Recognizer()
mic_list = sr.Microphone.list_microphone_names()

print(f"\n📋 Available Audio Devices ({len(mic_list)} total):\n")

voicemeeter_devices = []
for i, name in enumerate(mic_list):
    name_lower = name.lower()
    is_vm = "voicemeeter" in name_lower or "cable" in name_lower
    marker = "🎯" if is_vm else "  "
    print(f"{marker} [{i:2d}] {name}")
    if is_vm:
        voicemeeter_devices.append((i, name))

if not voicemeeter_devices:
    print("\n❌ WARNING: No VoiceMeeter devices found!")
    print("   Make sure VoiceMeeter is running.")
    print("   Install from: https://vb-audio.com/Voicemeeter/")
    exit(1)

print("\n" + "="*70)
print("🎯 VoiceMeeter Devices Found:")
for idx, name in voicemeeter_devices:
    print(f"   [{idx}] {name}")

# Find the best VoiceMeeter device
vm_output = None
for idx, name in voicemeeter_devices:
    if "output" in name.lower():
        vm_output = idx
        break

if vm_output is None and voicemeeter_devices:
    vm_output = voicemeeter_devices[0][0]

print(f"\n🎤 Will test with device [{vm_output}]: {mic_list[vm_output]}")

print("\n" + "="*70)
print("🔊 AUDIO ROUTING TEST")
print("="*70)
print("\n📌 SETUP INSTRUCTIONS:")
print("   1. Open VoiceMeeter (should already be running)")
print("   2. Make sure 'Virtual Input' B1 button is ON (lit up)")
print("   3. Play some audio (YouTube, music, anything)")
print("   4. Audio should route through VoiceMeeter")
print("\n⏳ Starting 10-second listening test...\n")

input("👉 Press ENTER when audio is playing and ready to test...")

try:
    mic = sr.Microphone(device_index=vm_output, sample_rate=44100)
    
    with mic as source:
        print("\n🎧 Adjusting for ambient noise... (2 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"   Energy threshold: {recognizer.energy_threshold}")
        
        print("\n👂 Listening for 10 seconds...")
        print("   (Play some audio now - YouTube, music, speech, etc.)\n")
        
        for i in range(10):
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                print(f"   ✅ Second {i+1}/10: Audio detected! ({len(audio.get_raw_data())} bytes)")
                
                # Try to transcribe
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"      🎤 Heard: \"{text}\"")
                except:
                    print(f"      (Audio captured but not speech)")
                    
            except sr.WaitTimeoutError:
                print(f"   ⚪ Second {i+1}/10: No audio detected")
            except Exception as e:
                print(f"   ⚠️  Second {i+1}/10: Error - {e}")
        
        print("\n" + "="*70)
        print("✅ Test Complete!")
        print("="*70)
        print("\n📊 Results:")
        print("   If you saw '✅ Audio detected' messages:")
        print("      ✅ VoiceMeeter routing is WORKING!")
        print("      ✅ Bot will be able to hear Twitter Spaces")
        print("\n   If you only saw '⚪ No audio detected':")
        print("      ❌ VoiceMeeter routing needs fixing")
        print("      💡 Check VoiceMeeter settings:")
        print("         - Virtual Input B1 should be ON")
        print("         - Hardware Input should be set to your audio source")
        print("         - Faders should be raised")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Make sure VoiceMeeter is running")
    print("   2. Restart VoiceMeeter if needed")
    print("   3. Check audio routing in VoiceMeeter")

print("\n" + "="*70)
print("🚀 Next Steps:")
print("   1. If audio test passed → Run: python twitter_autonomous.py")
print("   2. If audio test failed → Fix VoiceMeeter routing first")
print("="*70)








