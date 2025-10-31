#!/usr/bin/env python3
"""
Local testing script - Test the bot without Discord
Run this to verify your setup before connecting to Discord
"""
import os
import sys

def test_imports():
    """Test if all required packages are installed."""
    print("\n" + "="*60)
    print("TEST 1: Checking Dependencies")
    print("="*60)
    
    required_packages = [
        ("discord", "discord.py"),
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("speech_recognition", "SpeechRecognition"),
        ("gtts", "gTTS"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing = []
    for module, package in required_packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def test_config():
    """Test configuration and environment variables."""
    print("\n" + "="*60)
    print("TEST 2: Checking Configuration")
    print("="*60)
    
    try:
        import config
        
        checks = {
            "DISCORD_BOT_TOKEN": config.DISCORD_BOT_TOKEN,
            "AI Provider": config.AI_PROVIDER,
        }
        
        if config.AI_PROVIDER == "openai":
            checks["OPENAI_API_KEY"] = config.OPENAI_API_KEY
        else:
            checks["ANTHROPIC_API_KEY"] = config.ANTHROPIC_API_KEY
        
        for key, value in checks.items():
            if value:
                masked = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  ✅ {key}: {masked}")
            else:
                print(f"  ❌ {key}: NOT SET")
                
        # Validate
        config.validate_config()
        print("\n✅ Configuration valid!")
        return True
        
    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        print("\n💡 Make sure:")
        print("   1. You created a .env file (copy from .env.example)")
        print("   2. You added your API keys")
        print("   3. You added your Discord bot token")
        return False


def test_character():
    """Test the AI character engine."""
    print("\n" + "="*60)
    print("TEST 3: Testing AI Character")
    print("="*60)
    
    try:
        from character import AICharacter, PERSONALITIES
        
        print(f"  Available personalities: {', '.join(PERSONALITIES.keys())}")
        
        # Create a character
        print("\n  Creating contrarian character...")
        character = AICharacter(personality="contrarian", name="Test Carl")
        print(f"  ✅ Character created: {character.name}")
        
        # Test response generation
        print("\n  Testing response generation...")
        test_statement = "I think Python is the best programming language"
        print(f"  💬 Input: '{test_statement}'")
        
        response = character.generate_response(test_statement, speaker_name="Tester")
        print(f"  🎭 Response: '{response}'")
        
        if response and len(response) > 0:
            print("\n✅ AI Character working!")
            return True
        else:
            print("\n❌ No response generated")
            return False
            
    except Exception as e:
        print(f"\n❌ Character test failed: {e}")
        print("\n💡 Check your API keys in .env")
        return False


def test_audio():
    """Test audio processing."""
    print("\n" + "="*60)
    print("TEST 4: Testing Audio Processing")
    print("="*60)
    
    try:
        from audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        print("  ✅ Audio processor initialized")
        
        # Test TTS
        print("\n  Testing Text-to-Speech...")
        test_text = "This is a test of the audio system"
        print(f"  📝 Text: '{test_text}'")
        
        audio_file = processor.text_to_speech(test_text, "test_audio.mp3")
        
        if os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"  ✅ Audio file created: {audio_file} ({file_size} bytes)")
            
            # Clean up
            os.remove(audio_file)
            print("  🗑️  Cleaned up test file")
            
            print("\n✅ Audio processing working!")
            return True
        else:
            print(f"  ❌ Audio file not created")
            return False
            
    except Exception as e:
        print(f"\n❌ Audio test failed: {e}")
        return False


def test_ffmpeg():
    """Test if FFmpeg is installed."""
    print("\n" + "="*60)
    print("TEST 5: Checking FFmpeg")
    print("="*60)
    
    import subprocess
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg installed: {version_line}")
            return True
        else:
            print("  ❌ FFmpeg not working properly")
            return False
            
    except FileNotFoundError:
        print("  ❌ FFmpeg not found!")
        print("\n💡 Install FFmpeg:")
        print("   macOS:  brew install ffmpeg")
        print("   Ubuntu: sudo apt install ffmpeg")
        print("   Windows: Download from https://ffmpeg.org")
        return False
    except Exception as e:
        print(f"  ❌ Error checking FFmpeg: {e}")
        return False


def interactive_test():
    """Interactive conversation test."""
    print("\n" + "="*60)
    print("TEST 6: Interactive Conversation Test")
    print("="*60)
    
    try:
        from character import AICharacter, PERSONALITIES
        
        print("\nLet's have a conversation with the AI!")
        print("Type 'quit' to exit, 'switch' to change personality\n")
        
        personality = "contrarian"
        character = AICharacter(personality=personality, name="Carl")
        
        print(f"🎭 Character: {character.name} ({personality})")
        print(f"   Traits: {', '.join(character.personality_config['traits'])}\n")
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'quit':
                    print("\n👋 Goodbye!")
                    break
                    
                if user_input.lower() == 'switch':
                    print("\nAvailable personalities:")
                    for i, p in enumerate(PERSONALITIES.keys(), 1):
                        print(f"  {i}. {p}")
                    choice = input("\nChoose (1-5): ").strip()
                    personalities = list(PERSONALITIES.keys())
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(personalities):
                            personality = personalities[idx]
                            character = AICharacter(personality=personality, name="Carl")
                            print(f"\n🎭 Switched to: {personality}")
                            print(f"   Traits: {', '.join(character.personality_config['traits'])}\n")
                    except (ValueError, IndexError):
                        print("Invalid choice\n")
                    continue
                
                response = character.generate_response(user_input, speaker_name="You")
                print(f"🎭 {character.name}: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
                
    except Exception as e:
        print(f"\n❌ Interactive test failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("🧪 ARGUE BOT - LOCAL TESTING SUITE")
    print("="*70)
    print("\nThis will test your setup without needing Discord")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("\n❌ No .env file found!")
        print("\n💡 Create one:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your API keys")
        print("   3. Run this test again")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Dependencies", test_imports),
        ("Configuration", test_config),
        ("AI Character", test_character),
        ("Audio Processing", test_audio),
        ("FFmpeg", test_ffmpeg),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n  Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED!")
        print("="*70)
        print("\n✅ Your bot is ready to run!")
        print("\n🚀 Next steps:")
        print("   1. Run: python bot.py")
        print("   2. Invite bot to your Discord server")
        print("   3. Type !join in a voice channel")
        print("   4. Use !argue to test it out")
        
        # Offer interactive test
        print("\n" + "="*70)
        response = input("\n💡 Want to try an interactive conversation? (y/n): ").strip().lower()
        if response == 'y':
            interactive_test()
    else:
        print("\n" + "="*70)
        print("⚠️  SOME TESTS FAILED")
        print("="*70)
        print("\n💡 Fix the failed tests before running the bot")
        print("   Check the error messages above for details")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()



