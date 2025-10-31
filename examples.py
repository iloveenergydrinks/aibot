"""
Examples of how to use and extend the argue bot components.
"""

from character import AICharacter, PERSONALITIES
from audio_processor import AudioProcessor


def example_character_usage():
    """Example: Using the AI character engine."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Character Usage")
    print("="*60 + "\n")
    
    # Create a contrarian character
    carl = AICharacter(personality="contrarian", name="Carl")
    
    # Have a conversation
    statements = [
        "I think everyone should learn to code",
        "Social media brings people together",
        "Working from home is more productive"
    ]
    
    for statement in statements:
        print(f"👤 User: {statement}")
        response = carl.generate_response(statement, speaker_name="User")
        print(f"🎭 Carl: {response}\n")


def example_personality_comparison():
    """Example: Compare different personalities."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Personality Comparison")
    print("="*60 + "\n")
    
    statement = "Artificial intelligence will solve all our problems"
    print(f"📢 Statement: '{statement}'\n")
    
    # Try each personality
    for personality_type in ["contrarian", "devils_advocate", "sophist", "logical_debater", "provocateur"]:
        character = AICharacter(personality=personality_type, name=personality_type.title())
        response = character.generate_response(statement)
        print(f"🎭 {personality_type.upper()}:")
        print(f"   {response}\n")


def example_custom_personality():
    """Example: How to add a custom personality."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Adding Custom Personality")
    print("="*60 + "\n")
    
    # You would add this to character.py
    custom_personality = {
        "optimist": {
            "system_prompt": """You are {name}, an eternal optimist who always sees the bright side.
Your goal is to find positive aspects in any argument.
- Always agree but add a positive twist
- Find silver linings
- Use encouraging language
- Stay upbeat and supportive
- Keep responses under 3 sentences for voice conversations""",
            "traits": ["positive", "encouraging", "hopeful", "supportive"]
        }
    }
    
    print("To add this personality:")
    print("1. Open character.py")
    print("2. Add to PERSONALITIES dict:")
    print(f"   {custom_personality}")
    print("3. Use it: AICharacter(personality='optimist')")


def example_audio_processor():
    """Example: Using the audio processor."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Audio Processing")
    print("="*60 + "\n")
    
    processor = AudioProcessor()
    
    # Generate speech from text
    text = "I completely disagree with your premise!"
    print(f"📝 Text: {text}")
    
    audio_file = processor.text_to_speech(text, "example_output.mp3")
    print(f"🔊 Generated: {audio_file}")
    print(f"   You can now play this file in Discord or any media player")


def example_advanced_character():
    """Example: Advanced character configuration."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Advanced Character Features")
    print("="*60 + "\n")
    
    character = AICharacter(personality="sophist", name="Socrates")
    
    # Check personality info
    info = character.get_personality_info()
    print(f"Character Info:")
    print(f"  Name: {info['name']}")
    print(f"  Personality: {info['personality']}")
    print(f"  Traits: {', '.join(info['traits'])}\n")
    
    # Have a conversation
    print("Conversation:")
    character.generate_response("Democracy is the best system of government")
    character.generate_response("But what about mob rule?")
    character.generate_response("Fair point, but alternatives are worse")
    
    print(f"\nConversation length: {len(character.conversation_history)} messages")
    
    # Reset if needed
    character.reset_conversation()
    print(f"After reset: {len(character.conversation_history)} messages")


def example_debate_styles():
    """Example: Different debate approaches."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Debate Style Showcase")
    print("="*60 + "\n")
    
    topic = "Is technology making us more isolated?"
    
    styles = {
        "contrarian": "Always takes the opposite view",
        "devils_advocate": "Explores counterarguments",
        "logical_debater": "Uses facts and reasoning",
        "sophist": "Uses rhetoric and persuasion",
        "provocateur": "Stirs up controversy"
    }
    
    print(f"🎯 Topic: {topic}\n")
    
    for style, description in styles.items():
        print(f"📋 {style.upper()} ({description}):")
        character = AICharacter(personality=style, name=style.title())
        response = character.generate_response(topic)
        print(f"   💬 {response}\n")


def example_context_tracking():
    """Example: How the bot tracks conversation context."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Context Tracking")
    print("="*60 + "\n")
    
    character = AICharacter(personality="devils_advocate", name="Devil")
    
    print("Multi-turn conversation with context:\n")
    
    turns = [
        "Electric cars are the future",
        "But they're expensive",
        "Prices will come down with scale",
        "What about the environmental cost of batteries?"
    ]
    
    for i, statement in enumerate(turns, 1):
        print(f"Turn {i}:")
        print(f"  👤 User: {statement}")
        response = character.generate_response(statement)
        print(f"  🎭 Devil: {response}\n")
    
    print(f"Context length: {len(character.conversation_history)} messages")
    print("The character remembers the full conversation!")


# Run examples
if __name__ == "__main__":
    print("\n🎓 ARGUE BOT EXAMPLES")
    print("=" * 60)
    print("These examples show how to use and extend the bot.")
    print("=" * 60)
    
    try:
        example_character_usage()
        example_audio_processor()
        
        print("\n" + "="*60)
        print("✅ Examples completed!")
        print("="*60)
        print("\n💡 To see more examples, uncomment the other functions in this file.")
        print("   Or run specific examples:")
        print("   - example_personality_comparison()")
        print("   - example_debate_styles()")
        print("   - example_context_tracking()")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("  1. Installed all dependencies (pip install -r requirements.txt)")
        print("  2. Set up your .env file with API keys")



