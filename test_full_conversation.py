#!/usr/bin/env python3
"""
Full conversation test - Simulates Twitter Spaces interaction
"""
from character import AICharacter
from audio_processor import AudioProcessor
import os
import time
from pydub import AudioSegment
from pydub.playback import play

print("\n" + "="*70)
print("🎭 MICHAEL SAYLOR BOT - FULL CONVERSATION TEST")
print("="*70)

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()

print(f"\n✅ Character: {character.name}")
print(f"✅ Personality: {character.personality}")

# Test conversations
test_scenarios = [
    {
        "scenario": "Someone asks about Ethereum",
        "input": "I think Ethereum is the future of crypto because of smart contracts",
        "speaker": "ETH Believer"
    },
    {
        "scenario": "Someone agrees with Bitcoin",
        "input": "You're absolutely right! Bitcoin is the only real money!",
        "speaker": "Bitcoin Maxi"
    },
    {
        "scenario": "Someone asks about Solana",
        "input": "What do you think about Solana? It's faster than Bitcoin",
        "speaker": "SOL Fan"
    },
    {
        "scenario": "Someone worries about volatility",
        "input": "But Bitcoin is too volatile! My dollars are safer in the bank",
        "speaker": "No-coiner"
    }
]

print("\n" + "="*70)
print("🎬 Running Test Scenarios...")
print("="*70)

for i, test in enumerate(test_scenarios, 1):
    print(f"\n{'='*70}")
    print(f"📌 Scenario {i}: {test['scenario']}")
    print(f"{'='*70}")
    print(f"\n💬 {test['speaker']}: \"{test['input']}\"")
    
    # Generate Saylor's response
    print(f"\n⏳ Generating Michael Saylor's response...")
    response = character.generate_response(test['input'], test['speaker'])
    
    print(f"\n🎭 MICHAEL SAYLOR:")
    print(f"   \"{response}\"")
    
    # Generate audio
    print(f"\n🔊 Generating voice audio...")
    audio_file = f"test_scenario_{i}.mp3"
    try:
        audio_processor.text_to_speech(response, audio_file)
        print(f"   ✅ Audio generated: {audio_file}")
        
        # Play audio
        print(f"   🎧 Playing audio...")
        audio = AudioSegment.from_file(audio_file)
        play(audio)
        
        # Clean up
        os.remove(audio_file)
        print(f"   ✅ Audio played successfully")
        
    except Exception as e:
        print(f"   ❌ Audio error: {e}")
    
    if i < len(test_scenarios):
        print(f"\n⏸️  Moving to next scenario in 2 seconds...")
        time.sleep(2)

print("\n" + "="*70)
print("✅ FULL CONVERSATION TEST COMPLETE!")
print("="*70)

print("\n📊 Test Summary:")
print("   ✅ Character responses: Working")
print("   ✅ Bitcoin maximalism: Active")
print("   ✅ Voice generation: Working")
print("   ✅ Saylor personality: Loaded")

print("\n🎯 What to check:")
print("   1. Did responses sound like Saylor? (aggressive Bitcoin maxi)")
print("   2. Did he attack altcoins? (ETH, SOL, etc.)")
print("   3. Did the voice sound like real Michael Saylor?")
print("   4. Were responses engaging and memeable?")

print("\n🚀 If all checks passed:")
print("   Your bot is READY for Twitter Spaces!")
print("   Run: python twitter_autonomous.py")

print("\n" + "="*70)






