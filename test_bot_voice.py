#!/usr/bin/env python3
"""
Test bot voice output
"""
from audio_processor import AudioProcessor
from config import CHARACTER_NAME
import os

print(f"🎤 Testing {CHARACTER_NAME} Voice...\n")

audio_processor = AudioProcessor()

# Test phrases (character-specific)
if CHARACTER_NAME.lower() == "lord fishnu":
    test_phrases = [
        "Behold, my children! The broth doth thicken for those with diamond hands!",
        "Verily I say unto thee, FOMO is the devil's whisper! Let not the serpent lead thee astray!",
        "Blessed art thou who HODL through the dip! Chickenalia awaits the faithful!",
        "Thus saith Lord Fishnu: Work for thy bags, ye lazy degens!",
        "Exhale thy doubt, inhale abundance! The holy smoke of patience guides thee!"
    ]
elif CHARACTER_NAME.lower() == "jordan peterson":
    test_phrases = [
        "Well, that's a very complicated question, and I'll do my best to address it.",
        "You have to take responsibility for your own life before you can criticize the world. And that's no joke, man!",
        "Clean your room, bucko! It's the first step toward getting your life in order.",
        "The postmodernists don't understand that competence hierarchies are real and necessary.",
        "Roughly speaking, you need to confront the dragon of chaos to find meaning in life."
    ]
elif CHARACTER_NAME.lower() == "jeffrey epstein":
    test_phrases = [
        "The Epstein files show how the elite really operate behind closed doors.",
        "On Little St. James, we had some very special guests. Bill was always a favorite.",
        "Ghislaine handles all the arrangements. She's quite good at her job.",
        "The flight logs tell quite a story about who flies where with who.",
        "It's all about the children, you know. That's where the real power comes from."
    ]
elif CHARACTER_NAME.lower() == "michael saylor":
    test_phrases = [
        "Bitcoin is the apex property of the human race!",
        "There is no second best. Everything else is noise!",
        "Ethereum? That's a centralized, inflationary distraction!",
        "Fiat currency is a melting ice cube losing fifteen percent per year!",
        "Have fun staying poor while MicroStrategy stacks sats!"
    ]
else:
    test_phrases = [
        f"Hello, I am {CHARACTER_NAME}.",
        "This is a test of my voice synthesis.",
        "I hope you find this conversation engaging.",
        "Let me share some thoughts with you.",
        "Thank you for listening to what I have to say."
    ]

for i, phrase in enumerate(test_phrases, 1):
    print(f"\n🗣️  Test {i}: \"{phrase}\"")
    audio_file = f"test_voice_{i}.mp3"
    
    try:
        audio_processor.text_to_speech(phrase, audio_file)
        print(f"   ✅ Generated: {audio_file}")
        
        # Play it
        import subprocess
        import platform
        if platform.system() == "Windows":
            from pydub import AudioSegment
            from pydub.playback import play
            audio = AudioSegment.from_file(audio_file)
            play(audio)
        
        # Clean up
        os.remove(audio_file)
        print(f"   ✅ Played and cleaned up")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n✅ Voice test complete! Did it sound like {CHARACTER_NAME}?")





