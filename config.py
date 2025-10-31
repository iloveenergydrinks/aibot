"""Configuration management for the AI arguing character."""
import os
from dotenv import load_dotenv

load_dotenv()

# AI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CUSTOM_LLM_ENDPOINT = os.getenv("CUSTOM_LLM_ENDPOINT")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # "openai", "anthropic", or "custom"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")

# Discord Settings
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# TTS Settings
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
USE_ELEVENLABS = bool(ELEVENLABS_API_KEY)

# Force use OpenAI TTS for speed (set to False to use ElevenLabs)
FORCE_OPENAI_TTS = os.getenv("FORCE_OPENAI_TTS", "False").lower() == "true"

# Character Settings
CHARACTER_NAME = os.getenv("CHARACTER_NAME", "Contrarian Carl")
CHARACTER_PERSONALITY = os.getenv("CHARACTER_PERSONALITY", "contrarian")

# Audio Settings
SAMPLE_RATE = 48000  # Discord requires 48kHz
CHANNELS = 2
FRAME_SIZE = 960  # 20ms at 48kHz
LISTEN_DURATION = 5  # seconds to listen before processing

# Validation
def validate_config():
    """Validate required configuration."""
    errors = []
    
    if not DISCORD_BOT_TOKEN:
        errors.append("DISCORD_BOT_TOKEN is required")
    
    if AI_PROVIDER == "openai" and not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required when using OpenAI")
    
    if AI_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is required when using Anthropic")
    
    if AI_PROVIDER == "custom" and not CUSTOM_LLM_ENDPOINT:
        errors.append("CUSTOM_LLM_ENDPOINT is required when using custom provider")
    
    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))
    
    print(f"✅ Configuration validated")
    print(f"  - AI Provider: {AI_PROVIDER}")
    print(f"  - Character: {CHARACTER_NAME} ({CHARACTER_PERSONALITY})")
    print(f"  - TTS: {'ElevenLabs' if USE_ELEVENLABS else 'gTTS (fallback)'}")


