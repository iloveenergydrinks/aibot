# 🎙️ How the Autonomous Arguing Bot Works

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DISCORD VOICE CHANNEL                    │
│                                                              │
│  👤 User speaks → 🎤 Bot listens                            │
│  🔊 Bot speaks ← 🤖 Bot responds                            │
└─────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────┐
│                        MAIN BOT (main.py)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         VoiceListener (Voice Receive Client)         │  │
│  │                                                       │  │
│  │  • Captures audio packets from voice channel         │  │
│  │  • Buffers audio per user                           │  │
│  │  • Detects speech start/stop                        │  │
│  │  • Triggers processing when user stops speaking     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────┐
│               AUDIO PROCESSOR (audio_processor.py)           │
│                                                              │
│  Speech-to-Text:                Text-to-Speech:             │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ Google STT   │              │ ElevenLabs   │            │
│  │   (Free)     │              │  (Best)      │            │
│  └──────────────┘              └──────────────┘            │
│  ┌──────────────┐              ┌──────────────┐            │
│  │ Whisper API  │              │ OpenAI TTS   │            │
│  │ (Accurate)   │              │  (Good)      │            │
│  └──────────────┘              └──────────────┘            │
│                                 ┌──────────────┐            │
│                                 │  Google TTS  │            │
│                                 │ (Fallback)   │            │
│                                 └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────┐
│                 AI CHARACTER (character.py)                  │
│                                                              │
│  Input: "I think AI is good"                                │
│           ↓                                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Personality System:                                │    │
│  │  • Contrarian: "No, you're wrong!"                 │    │
│  │  • Devil's Advocate: "But what if..."              │    │
│  │  • Sophist: "That's misleading because..."         │    │
│  │  • Logical Debater: "The data shows..."            │    │
│  │  • Provocateur: "That's the dumbest thing..."      │    │
│  └────────────────────────────────────────────────────┘    │
│           ↓                                                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  LLM (GPT-4 or Claude):                            │    │
│  │  • Maintains conversation context                  │    │
│  │  • Generates argumentative response                │    │
│  │  • Stays in character                              │    │
│  └────────────────────────────────────────────────────┘    │
│           ↓                                                  │
│  Output: "Actually, AI is creating massive job             │
│          displacement and amplifying biases..."             │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Conversation Flow

### 1. **User Speaks**
```
👤 User: "Climate change is the biggest threat"
         ↓
    (Audio packets sent to Discord)
         ↓
    🎤 Bot receives PCM audio
```

### 2. **Audio Capture**
```
VoiceListener.on_voice_member_packet()
    ↓
Buffer audio for user
    ↓
Detect silence (user stopped speaking)
    ↓
Trigger processing
```

### 3. **Speech Recognition**
```
Raw PCM audio
    ↓
Convert to WAV format
    ↓
Send to Speech Recognition API
    ↓
Text: "Climate change is the biggest threat"
```

### 4. **AI Response Generation**
```
Text input + Conversation history
    ↓
Send to LLM with personality prompt
    ↓
LLM generates argumentative response
    ↓
Response: "That's debatable. Economic inequality 
          affects billions right now, while climate
          effects are still emerging..."
```

### 5. **Text-to-Speech**
```
Response text
    ↓
Generate audio file (MP3)
    ↓
Convert to Discord format (PCM)
    ↓
Play in voice channel
```

### 6. **Bot Speaks**
```
🔊 Bot: "That's debatable. Economic inequality..."
         ↓
    (Audio played in voice channel)
         ↓
    👤 User hears response
         ↓
    🔄 Cycle repeats!
```

## 🧠 Key Components

### VoiceListener Class
- Inherits from `voice_recv.VoiceRecvClient`
- Captures audio packets in real-time
- Buffers audio per user
- Detects speech boundaries
- Manages bot speaking state

### AudioProcessor Class
- Handles STT (Speech-to-Text)
- Handles TTS (Text-to-Speech)
- Supports multiple providers
- Converts between audio formats

### AICharacter Class
- Maintains personality system
- Manages conversation history
- Interfaces with LLMs
- Generates contextual responses

## ⚡ Technical Details

### Audio Format
- **Input:** 48kHz, stereo, 16-bit PCM (Discord standard)
- **Processing:** Convert to WAV for recognition
- **Output:** MP3 → PCM for Discord playback

### Speech Detection
```python
silence_threshold = 0.8  # seconds
min_audio_length = 1.5   # seconds

# Process when:
# 1. User stops speaking (0.8s silence)
# 2. Enough audio captured (1.5s minimum)
# 3. Bot not currently speaking
```

### Conversation Context
```python
# Last 20 messages kept in memory
conversation_history = [
    {"role": "user", "content": "User: ..."},
    {"role": "assistant", "content": "..."},
    # ...
]
```

## 🔧 Configuration Points

### Adjust Sensitivity
In `main.py`:
```python
self.silence_threshold = 0.8  # Lower = faster response
self.min_audio_length = 1.5   # Lower = shorter speeches
```

### Change AI Model
In `.env`:
```env
AI_PROVIDER=openai
MODEL_NAME=gpt-4  # or gpt-4-turbo, claude-3-5-sonnet...
```

### Change Voice
In `audio_processor.py`:
```python
# OpenAI TTS voices:
voice="onyx"  # alloy, echo, fable, onyx, nova, shimmer

# Or use ElevenLabs with ELEVENLABS_VOICE_ID
```

## 🎯 Performance

### Latency Breakdown:
1. **Audio capture:** ~1-2 seconds (user speaking)
2. **Silence detection:** ~0.8 seconds
3. **Speech recognition:** ~0.5-1 second
4. **AI response:** ~2-4 seconds
5. **TTS generation:** ~1-2 seconds
6. **Total:** ~5-10 seconds end-to-end

### Optimization Tips:
- Use Whisper API for better accuracy (slower)
- Use Google STT for speed (less accurate)
- Use ElevenLabs for voice quality
- Use OpenAI TTS for balance
- Reduce `silence_threshold` for faster response
- Use streaming TTS (future enhancement)

## 🔒 Important Notes

### Discord API Limitations:
- Voice receive requires `discord-ext-voice-recv`
- Not officially supported by Discord
- May break with Discord updates
- Use at your own risk

### API Costs:
- **OpenAI Whisper:** $0.006 per minute
- **GPT-4:** ~$0.03-0.06 per response
- **OpenAI TTS:** $0.015 per 1000 chars
- **ElevenLabs:** Varies by plan

**Estimate:** ~$0.10-0.15 per minute of conversation

### Rate Limits:
- OpenAI: 3 requests/min (free tier)
- Discord: No specific limit for bots
- Speech recognition: Usually generous

## 🚀 Scaling

### For Production:
1. Add error recovery and retry logic
2. Implement request queuing
3. Add user rate limiting
4. Cache common responses
5. Use streaming APIs where possible
6. Add monitoring and logging
7. Implement circuit breakers

### Multi-Server:
- Bot can join multiple servers
- Each voice connection is independent
- Scales with server count
- Consider sharding for 1000+ servers

## 📝 File Dependencies

```
main.py
  ↓
├── character.py
│   ↓
│   ├── openai (API)
│   └── anthropic (API)
│
├── audio_processor.py
│   ↓
│   ├── speech_recognition
│   ├── openai (Whisper)
│   ├── elevenlabs
│   ├── gtts
│   └── pydub
│
└── config.py
    ↓
    └── .env (your API keys)
```

## 🎓 Learn More

- **Discord.py docs:** https://discordpy.readthedocs.io
- **Voice receive:** https://github.com/imayhaveborkedit/discord-ext-voice-recv
- **OpenAI API:** https://platform.openai.com/docs
- **Anthropic API:** https://docs.anthropic.com

---

**Questions?** Check the README or run `python test_local.py`



