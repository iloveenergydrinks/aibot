# 🎧 Twitter Spaces Audio Capture - Complete Guide

How to properly capture audio from Twitter Spaces for your bot.

---

## 🎯 **Method 1: BlackHole Virtual Audio (BEST for Mac)**

### Install BlackHole

```bash
brew install blackhole-2ch
```

### Setup Audio Routing

**Step 1: Create Multi-Output Device**

1. Open **Audio MIDI Setup** (in Applications/Utilities)
2. Click **+** (bottom left) → **Create Multi-Output Device**
3. Name it: **"Spaces Output"**
4. Check both:
   - ✅ **BlackHole 2ch**
   - ✅ **Your Speakers/Headphones**
5. This lets you hear AND capture audio

**Step 2: Create Aggregate Device**

1. Click **+** → **Create Aggregate Device**
2. Name it: **"Spaces Input"**  
3. Check both:
   - ✅ **BlackHole 2ch**
   - ✅ **Your Microphone**
4. This lets bot capture AND speak

**Step 3: Configure System Audio**

1. **System Settings → Sound**
2. **Output:** Select **"Spaces Output"**
3. **Input:** Select **"Spaces Input"**

### How It Works:

```
Twitter Space (browser)
   ↓
System Audio → BlackHole 2ch → Bot captures
   ↓
Also → Your Speakers (so you can hear)

Bot generates response
   ↓
Bot plays audio → BlackHole 2ch → Twitter Space hears it
   ↓
Also → Your Speakers (so you hear what bot says)
```

### Update the Bot:

Your bot will automatically use the Aggregate Device for capturing Spaces audio!

---

## 🎯 **Method 2: System Audio Capture (Alternative)**

### Using SoundFlower (older alternative):

```bash
# Install SoundFlower
brew install soundflower
```

Setup is similar to BlackHole.

---

## 🎯 **Method 3: Browser Audio Capture (Most Advanced)**

Capture audio directly from the browser playing Spaces.

### Install Additional Tools:

```bash
pip install soundcard sounddevice
```

### Code to Capture Browser Audio:

```python
import soundcard as sc
import numpy as np

# Get the loopback device (captures system audio)
speakers = sc.default_speaker()
loopback = sc.get_microphone(id=speakers.name, include_loopback=True)

# Record audio
with loopback.recorder(samplerate=48000) as mic:
    # Capture 5 seconds
    data = mic.record(numframes=48000*5)
    
    # Process audio data...
```

---

## 🎯 **Method 4: WebRTC Stream Interception (Expert)**

Intercept the WebRTC stream that Spaces uses.

### Requires:

1. **Browser DevTools** to inspect network traffic
2. **Extract WebRTC stream URLs**
3. **Capture using FFmpeg:**

```bash
ffmpeg -i "rtsp://stream_url" -f wav pipe:1 | python process_audio.py
```

This is complex and Twitter actively prevents it.

---

## 📊 **Comparison:**

| Method | Difficulty | Quality | Autonomy |
|--------|-----------|---------|----------|
| **BlackHole** | Easy | Excellent | High |
| **SoundFlower** | Easy | Good | High |
| **Browser Capture** | Medium | Excellent | High |
| **WebRTC Intercept** | Expert | Perfect | Complete |
| **Mic → Speakers** | Very Easy | Poor | Low |

---

## 🚀 **Recommended Setup (BlackHole):**

### Complete Steps:

**1. Install BlackHole:**
```bash
brew install blackhole-2ch
```

**2. Configure Audio:**
- Open Audio MIDI Setup
- Create Multi-Output Device (BlackHole + Speakers)
- Create Aggregate Device (BlackHole + Mic)
- Set as system default

**3. Run optimized bot:**
```bash
python3 twitter_optimized.py
```

**4. Join Space:**
- Browser will use BlackHole for audio
- Bot will capture clean Spaces audio
- Bot will speak directly into Space

---

## 🔧 **Troubleshooting:**

### "Can't hear Space audio"
- Check Output is set to "Multi-Output Device"
- Check BlackHole is selected in Multi-Output
- Check Speakers/Headphones are also selected

### "Bot doesn't hear anything"
- Check Input is set to "Aggregate Device"
- Check BlackHole is in Aggregate
- Verify bot is using correct input device

### "Space doesn't hear bot"
- Check browser is using Aggregate Device
- Check bot audio is playing through system
- Verify BlackHole is routing correctly

---

## 💡 **Quick Test:**

After setting up BlackHole:

```bash
# Test that audio routing works
python3 << 'EOF'
import speech_recognition as sr

print("🎧 Testing audio capture...")
print("Play some audio (YouTube, etc)")
print("If BlackHole is set up, bot should hear it!\n")

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Listening for 5 seconds...")
    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ Captured: {text}")
        print("BlackHole is working!")
    except:
        print("❌ Nothing captured")
        print("Check audio routing")

EOF
```

---

## 🎉 **Bottom Line:**

**For Twitter Spaces:**
1. Install BlackHole
2. Configure audio routing
3. Run `twitter_optimized.py`
4. Hitler will hear and speak in Spaces!

**No more janky mic-to-speakers!**
Proper, clean audio capture and playback! 🎙️

---

**Want me to create an automated setup script for BlackHole?**


