#!/usr/bin/env python3
"""
Historical Voice Cloner - Use voices of historical figures

Supports:
- ElevenLabs voice library (pre-made historical voices)
- Voice cloning from audio samples
- Custom voice profiles
"""
import os
import sys
from elevenlabs.client import ElevenLabs
import config

# Set API key
if not config.ELEVENLABS_API_KEY:
    print("\n❌ Need ELEVENLABS_API_KEY in .env for voice cloning!")
    print("   Get one at: https://elevenlabs.io")
    sys.exit(1)

client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)


def list_available_voices():
    """List all available voices from ElevenLabs."""
    print("\n" + "="*70)
    print("🎙️  AVAILABLE VOICES")
    print("="*70 + "\n")
    
    try:
        response = client.voices.get_all()
        all_voices = response.voices
        
        print(f"Found {len(all_voices)} voices:\n")
        
        for i, voice in enumerate(all_voices, 1):
            voice_id = voice.voice_id
            name = voice.name
            category = getattr(voice, 'category', 'Unknown')
            
            print(f"{i:3d}. {name:30s} (ID: {voice_id[:20]}...) - {category}")
            
            # Highlight potential historical voices
            if any(term in name.lower() for term in ['churchill', 'roosevelt', 'hitler', 'jfk', 'kennedy', 'queen', 'king', 'president']):
                print(f"     ⭐ HISTORICAL FIGURE DETECTED")
        
        print("\n" + "="*70)
        print("💡 To use a voice, copy its ID to .env as ELEVENLABS_VOICE_ID")
        print("="*70 + "\n")
        
        return all_voices
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your ELEVENLABS_API_KEY is valid")
        return []


def search_historical_voices():
    """Search for historical figure voices."""
    print("\n" + "="*70)
    print("🎭 SEARCHING FOR HISTORICAL VOICES")
    print("="*70 + "\n")
    
    # Common historical figures
    search_terms = [
        'churchill', 'hitler', 'roosevelt', 'jfk', 'kennedy', 
        'stalin', 'napoleon', 'lincoln', 'washington',
        'queen', 'king', 'president', 'prime minister',
        'thatcher', 'reagan', 'gandhi', 'mandela'
    ]
    
    try:
        response = client.voices.get_all()
        all_voices = response.voices
        found = []
        
        for voice in all_voices:
            name_lower = voice.name.lower()
            for term in search_terms:
                if term in name_lower:
                    found.append(voice)
                    break
        
        if found:
            print(f"✅ Found {len(found)} potential historical voices:\n")
            for i, voice in enumerate(found, 1):
                print(f"{i}. {voice.name}")
                print(f"   ID: {voice.voice_id}")
                print(f"   Category: {getattr(voice, 'category', 'Unknown')}\n")
        else:
            print("⚠️  No pre-made historical voices found in library")
            print("\n💡 You can:")
            print("   1. Clone a voice from audio samples")
            print("   2. Use ElevenLabs voice design to create one")
            print("   3. Check community voices on elevenlabs.io")
        
        return found
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def clone_voice_from_audio(name, audio_files):
    """Clone a voice from audio samples.
    
    Args:
        name: Name for the cloned voice (e.g., "Winston Churchill")
        audio_files: List of paths to audio files (MP3, WAV)
                    Need at least 1 minute of clear audio
    """
    print(f"\n🎙️  Cloning voice: {name}")
    print(f"   Using {len(audio_files)} audio file(s)")
    
    try:
        # Clone the voice using new API
        voice = client.voices.clone(
            name=name,
            description=f"Cloned voice of {name}",
            files=audio_files
        )
        
        print(f"✅ Voice cloned successfully!")
        print(f"   Voice ID: {voice.voice_id}")
        print(f"   Name: {voice.name}")
        print(f"\n💡 Add to .env:")
        print(f"   ELEVENLABS_VOICE_ID={voice.voice_id}")
        
        return voice
    
    except Exception as e:
        print(f"❌ Cloning failed: {e}")
        print("\n💡 Tips for successful cloning:")
        print("   - Use at least 1 minute of clear audio")
        print("   - Remove background noise")
        print("   - Use consistent audio quality")
        print("   - Multiple files work better than one long file")
        return None


def test_voice(voice_id, text="I am ready to argue with you!"):
    """Test a voice by generating sample audio."""
    print(f"\n🔊 Testing voice: {voice_id[:20]}...")
    print(f"   Text: '{text}'")
    
    try:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        
        # Save to temp file
        temp_file = "test_voice_sample.mp3"
        with open(temp_file, "wb") as f:
            f.write(audio)
        
        print(f"✅ Audio generated: {temp_file}")
        print("   Play this file to hear the voice!")
        
        # Try to play on Mac
        import subprocess
        if sys.platform == "darwin":
            subprocess.run(["afplay", temp_file])
        
        return temp_file
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def create_character_profile(character_name, personality, voice_id, voice_name):
    """Create a character profile with specific voice."""
    print(f"\n✅ Character Profile Created:")
    print(f"   Name: {character_name}")
    print(f"   Personality: {personality}")
    print(f"   Voice: {voice_name}")
    print(f"   Voice ID: {voice_id}")
    print(f"\n📝 Add to your .env:")
    print(f"   CHARACTER_NAME={character_name}")
    print(f"   CHARACTER_PERSONALITY={personality}")
    print(f"   ELEVENLABS_VOICE_ID={voice_id}")


# Pre-configured historical characters
HISTORICAL_CHARACTERS = {
    "churchill": {
        "name": "Winston Churchill Bot",
        "personality": "logical_debater",
        "search_terms": ["churchill", "winston"],
        "sample_text": "We shall fight on the beaches, we shall never surrender!"
    },
    "hitler": {
        "name": "Adolf Hitler Bot",
        "personality": "provocateur",
        "search_terms": ["hitler", "adolf"],
        "sample_text": "I am ready to debate with great passion!"
    },
    "jfk": {
        "name": "JFK Bot",
        "personality": "devils_advocate",
        "search_terms": ["kennedy", "jfk", "john f"],
        "sample_text": "Ask not what your country can do for you!"
    },
    "roosevelt": {
        "name": "FDR Bot",
        "personality": "logical_debater",
        "search_terms": ["roosevelt", "fdr", "franklin"],
        "sample_text": "The only thing we have to fear is fear itself!"
    },
    "thatcher": {
        "name": "Margaret Thatcher Bot",
        "personality": "contrarian",
        "search_terms": ["thatcher", "margaret"],
        "sample_text": "I am not a consensus politician, I am a conviction politician!"
    }
}


def main():
    """Main menu for voice cloning."""
    print("\n" + "="*70)
    print("🎙️  HISTORICAL VOICE CLONER")
    print("="*70)
    print("\nOptions:")
    print("  1. List all available voices")
    print("  2. Search for historical voices")
    print("  3. Test a voice by ID")
    print("  4. Clone voice from audio files")
    print("  5. Setup historical character")
    print("  0. Exit")
    print("="*70)
    
    choice = input("\nChoose option (0-5): ").strip()
    
    if choice == "1":
        list_available_voices()
    
    elif choice == "2":
        found = search_historical_voices()
        if found:
            print("\n💡 To use any of these:")
            print("   1. Copy the Voice ID")
            print("   2. Add to .env: ELEVENLABS_VOICE_ID=<voice_id>")
            print("   3. Run your arguing bot!")
    
    elif choice == "3":
        voice_id = input("\nEnter Voice ID: ").strip()
        test_text = input("Enter test text (or press Enter for default): ").strip()
        if not test_text:
            test_text = "I am ready to argue with you about anything!"
        test_voice(voice_id, test_text)
    
    elif choice == "4":
        print("\n📁 Voice Cloning from Audio")
        name = input("Name for this voice (e.g., 'Winston Churchill'): ").strip()
        print("\nEnter audio file paths (one per line, empty line to finish):")
        audio_files = []
        while True:
            path = input("  Audio file: ").strip()
            if not path:
                break
            if os.path.exists(path):
                audio_files.append(path)
            else:
                print(f"    ⚠️  File not found: {path}")
        
        if audio_files:
            clone_voice_from_audio(name, audio_files)
        else:
            print("❌ No audio files provided")
    
    elif choice == "5":
        print("\n🎭 Setup Historical Character")
        print("\nPre-configured characters:")
        for i, (key, char) in enumerate(HISTORICAL_CHARACTERS.items(), 1):
            print(f"  {i}. {char['name']}")
        
        char_choice = input("\nChoose (1-5) or type custom name: ").strip()
        
        if char_choice.isdigit() and 1 <= int(char_choice) <= len(HISTORICAL_CHARACTERS):
            key = list(HISTORICAL_CHARACTERS.keys())[int(char_choice) - 1]
            char = HISTORICAL_CHARACTERS[key]
            
            print(f"\n🔍 Searching for {char['name']} voice...")
            response = client.voices.get_all()
            all_voices = response.voices
            
            found_voice = None
            for voice in all_voices:
                if any(term in voice.name.lower() for term in char['search_terms']):
                    found_voice = voice
                    break
            
            if found_voice:
                print(f"✅ Found voice: {found_voice.name}")
                create_character_profile(
                    char['name'],
                    char['personality'],
                    found_voice.voice_id,
                    found_voice.name
                )
                
                # Test it
                test = input("\nTest this voice? (y/n): ").strip().lower()
                if test == 'y':
                    test_voice(found_voice.voice_id, char['sample_text'])
            else:
                print(f"⚠️  No matching voice found")
                print("   You'll need to clone it from audio samples")
    
    elif choice == "0":
        print("\n👋 Goodbye!")
    
    else:
        print("\n❌ Invalid choice")


if __name__ == "__main__":
    main()

