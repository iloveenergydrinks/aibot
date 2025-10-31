#!/usr/bin/env python3
"""
SIMPLE TEXT CHAT - Fastest way to test!

No voice, no Discord, just type and argue.
Perfect for quick testing.

Run: python simple_chat.py
"""
from character import AICharacter, PERSONALITIES
import config

def main():
    """Simple text-based arguing."""
    print("\n" + "="*70)
    print("💬 SIMPLE TEXT ARGUING BOT")
    print("="*70)
    
    # Validate minimal config
    try:
        if not config.OPENAI_API_KEY and not config.ANTHROPIC_API_KEY:
            print("\n❌ You need either OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
            return
    except:
        print("\n❌ Create a .env file with your API key!")
        print("Copy .env.example to .env and add your key.")
        return
    
    # Choose personality
    print("\n🎭 Choose a personality:")
    personalities = list(PERSONALITIES.keys())
    for i, p in enumerate(personalities, 1):
        traits = ', '.join(PERSONALITIES[p]['traits'])
        print(f"  {i}. {p} - {traits}")
    
    try:
        choice = input("\nEnter number (1-5) or press Enter for contrarian: ").strip()
        if choice and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(personalities):
                personality = personalities[idx]
            else:
                personality = "contrarian"
        else:
            personality = "contrarian"
    except:
        personality = "contrarian"
    
    # Create character
    character = AICharacter(personality=personality, name=config.CHARACTER_NAME or "Carl")
    
    print(f"\n✅ Created: {character.name} ({personality})")
    print("\n" + "="*70)
    print("HOW TO USE:")
    print("  - Type anything and press Enter")
    print("  - Type 'quit' to exit")
    print("  - Type 'reset' to clear history")
    print("  - Type 'change' to switch personality")
    print("="*70 + "\n")
    
    print(f"🎭 {character.name}: Alright, say something and I'll argue with you!\n")
    
    exchange_count = 0
    
    try:
        while True:
            # Get user input
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Check commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n🎭 {character.name}: Fine! But I'm still right. Bye!")
                break
            
            if user_input.lower() == 'reset':
                character.reset_conversation()
                print(f"\n🔄 Conversation reset!\n")
                print(f"🎭 {character.name}: Fresh start. What do you want to argue about?\n")
                continue
            
            if user_input.lower() in ['change', 'personality', 'switch']:
                print("\n🎭 Choose new personality:")
                for i, p in enumerate(personalities, 1):
                    print(f"  {i}. {p}")
                choice = input("\nEnter number: ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(personalities):
                        personality = personalities[idx]
                        character = AICharacter(personality=personality, name=config.CHARACTER_NAME or "Carl")
                        print(f"\n✅ Changed to: {personality}\n")
                except:
                    print("\n⚠️  Invalid choice, keeping current personality\n")
                continue
            
            # Generate response
            print()  # Blank line
            response = character.generate_response(user_input, speaker_name="You")
            print(f"🎭 {character.name}: {response}\n")
            
            exchange_count += 1
    
    except KeyboardInterrupt:
        print(f"\n\n🎭 {character.name}: Interrupted! That's a cheap way to win an argument!")
    
    print("\n" + "="*70)
    print(f"📊 Total exchanges: {exchange_count}")
    print(f"Thanks for arguing with {character.name}!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()


