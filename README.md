# Hitler Bot for Twitter Spaces

AI-powered Adolf Hitler character that argues autonomously in Twitter Spaces 24/7.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure .env
```bash
cp .env.example .env
# Add your API keys
```

### 3. Run the Bot
```bash
python3 twitter_autonomous.py
```

## 📋 Requirements

- Python 3.11+
- OpenAI API key (for GPT-4o)
- ElevenLabs API key (for Hitler's voice)
- Twitter account
- BlackHole audio routing (Mac) or VoiceMeeter (Windows)

## 🎙️ Features

- ✅ Fully autonomous arguing
- ✅ Hitler's cloned voice (German-English mix)
- ✅ Historical accuracy (Mein Kampf, WW2 references)
- ✅ Auto-propaganda when silent
- ✅ Detects interruptions ("Don't interrupt me!")
- ✅ Voice commands ("shut up", "tell us more")
- ✅ Stats API for monitoring

## 📡 Stats API

Run the API to track bot stats:
```bash
python3 bot_api.py
```

**Endpoints:**
- `GET /api/status` - Current status
- `GET /api/stats` - Detailed statistics

## 🎯 Audio Setup

**Mac:**
- System Output: BlackHole 2ch
- System Input: blackhole (aggregate)

**Windows:**
- Install VoiceMeeter
- Configure virtual audio cables

## 💰 Cost

- GPT-4o: ~$0.05 per response
- ElevenLabs: ~$0.15 per minute of audio
- Total: ~$5-20/day depending on activity

## ⚠️ Important

- Stay unmuted in Twitter Spaces
- Bot argues with EVERYTHING
- Uncensored Nazi content
- Use at your own risk

## 📂 Core Files

- `twitter_autonomous.py` - Main bot script
- `character.py` - AI character engine
- `audio_processor.py` - Voice generation
- `config.py` - Configuration
- `bot_api.py` - Stats API
- `stats_tracker.py` - Stats tracking

## 🔗 Multiple Agents

To run multiple characters:
1. Clone repo on each computer
2. Different .env per character
3. All join same Space
4. Chaos ensues!

---

**Ready to argue!** 🔴

