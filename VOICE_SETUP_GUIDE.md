# 🎤 Voice Setup Guide for Michael Saylor Bot

## Quick Start - 3 Voice Options

### ⚡ **Option 1: OpenAI TTS** (FASTEST - RECOMMENDED)
**Best for:** Testing, speed, low cost  
**Quality:** Good (not perfect)  
**Cost:** ~$0.015 per 1000 characters

**Setup:**
1. Create a file named `.env` in your project root
2. Add this content:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Voice Settings (Uses "onyx" - deep professional male)
FORCE_OPENAI_TTS=True
AI_PROVIDER=openai
MODEL_NAME=gpt-4

# Firebase
FIREBASE_DATABASE_URL=https://solwind-3e0d2-default-rtdb.firebaseio.com

# Character
CHARACTER_NAME=Michael Saylor
CHARACTER_PERSONALITY=michael_saylor
```

**That's it!** The bot will use OpenAI's "onyx" voice (already configured).

---

### 🎭 **Option 2: ElevenLabs Pre-Made Voices** (HIGH QUALITY)
**Best for:** Production, best quality  
**Quality:** Excellent  
**Cost:** $11-$99/month subscription

**Setup:**

1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get your API key from [Settings](https://elevenlabs.io/app/settings/api-keys)
3. Browse [Voice Library](https://elevenlabs.io/app/voice-library) and pick a voice
4. **Recommended Saylor voices:**
   - **Adam** (Voice ID: `21m00Tcm4TlvDq8ikWAM`) - Professional, confident
   - **Antoni** (Voice ID: `ErXwobaYiN019PkySvjV`) - Articulate, balanced
   - **Josh** (Voice ID: `TxGEqnHWrfWFTfGW9XjX`) - Deep, authoritative

5. Create `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Voice Settings
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
FORCE_OPENAI_TTS=False

# AI Settings
AI_PROVIDER=openai
MODEL_NAME=gpt-4

# Firebase
FIREBASE_DATABASE_URL=https://solwind-3e0d2-default-rtdb.firebaseio.com

# Character
CHARACTER_NAME=Michael Saylor
CHARACTER_PERSONALITY=michael_saylor
```

---

### 🎯 **Option 3: Clone Saylor's Real Voice** (MOST REALISTIC)
**Best for:** Maximum meme potential  
**Quality:** Perfect match  
**Cost:** $22/month (ElevenLabs Professional)

**Setup:**

1. Get **ElevenLabs Professional** plan ($22/mo)
2. Find 1-2 minutes of clear Michael Saylor audio:
   - Search YouTube: "Michael Saylor interview"
   - Good sources: podcasts, conference speeches
   - Need clear audio, minimal background noise

3. Download the audio using a YouTube downloader

4. Go to [ElevenLabs Voice Lab](https://elevenlabs.io/app/voice-lab)

5. Click **"Instant Voice Cloning"**

6. Upload your audio samples

7. Name it "Michael Saylor"

8. Copy the generated **Voice ID**

9. Create `.env` file with your custom Voice ID:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Your cloned voice ID
ELEVENLABS_VOICE_ID=your-custom-voice-id-here
FORCE_OPENAI_TTS=False

# AI Settings
AI_PROVIDER=openai
MODEL_NAME=gpt-4

# Firebase
FIREBASE_DATABASE_URL=https://solwind-3e0d2-default-rtdb.firebaseio.com

# Character
CHARACTER_NAME=Michael Saylor
CHARACTER_PERSONALITY=michael_saylor
```

---

## 📋 How to Create .env File (Windows)

**PowerShell:**
```powershell
cd C:\Users\miningofficer\Desktop\aibot-main
New-Item -Path ".env" -ItemType File
notepad .env
```

Then paste your configuration and save.

---

## 🎧 Voice Comparison

| Option | Quality | Speed | Cost/Month | Setup Time |
|--------|---------|-------|------------|------------|
| OpenAI TTS | Good (7/10) | ⚡ Very Fast | ~$5-20 | 2 min |
| ElevenLabs Pre-Made | Excellent (9/10) | Fast | $11-99 | 5 min |
| ElevenLabs Clone | Perfect (10/10) | Fast | $22+ | 15 min |

---

## 🚀 My Recommendation

**For Testing:** Start with **OpenAI TTS** (Option 1)
- Fast setup
- Good enough quality
- Cheap
- Already configured in the code

**For Production:** Use **ElevenLabs "Adam"** voice (Option 2)
- Professional quality
- Sounds corporate/executive
- Very Saylor-like

**For Maximum Meme:** Clone Saylor's real voice (Option 3)
- Perfect match
- Maximum viral potential
- Worth the $22/month

---

## 🔧 Test Your Voice

After setting up `.env`, run:

```bash
cd C:\Users\miningofficer\Desktop\aibot-main
python -c "from audio_processor import AudioProcessor; ap = AudioProcessor(); ap.text_to_speech('Bitcoin is the apex property of the human race!', 'test.mp3'); print('Voice test saved to test.mp3')"
```

Listen to `test.mp3` to verify your voice sounds good!

---

## 💡 Pro Tips

1. **OpenAI voices available:**
   - `onyx` (default) - Deep, professional ⭐
   - `echo` - Authoritative
   - `fable` - British accent
   - Change in `audio_processor.py` line 212

2. **ElevenLabs settings:**
   - Stability: 0.7 (already set)
   - Similarity: 0.85 (already set)
   - Configured in `audio_processor.py` lines 150-156

3. **Speed vs Quality:**
   - OpenAI TTS: ~0.5s generation time
   - ElevenLabs Turbo: ~1.0s generation time
   - Bot uses Turbo model for speed (line 162)

---

## ❓ Troubleshooting

**"Module not found: elevenlabs"**
```bash
pip install elevenlabs
```

**"Voice sounds robotic"**
- Use ElevenLabs instead of OpenAI
- Set `FORCE_OPENAI_TTS=False`

**"Too expensive!"**
- Use OpenAI TTS: set `FORCE_OPENAI_TTS=True`
- Costs 10x less than ElevenLabs

---

## 📞 Need Help?

Check your current settings:
```bash
python -c "from config import *; print(f'TTS: {\"ElevenLabs\" if USE_ELEVENLABS else \"OpenAI/gTTS\"}')"
```






