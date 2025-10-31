# 🎙️ Using Historical Character Voices

Make your arguing bot sound like Churchill, Hitler, JFK, or any historical figure!

---

## 🚀 Quick Start

### Method 1: Use Pre-Made Voices (Easiest)

```bash
python3 voice_cloner.py
```

Choose option 2 to search for historical voices in ElevenLabs library.

### Method 2: Clone from Audio

Download audio clips of the person speaking, then clone their voice!

---

## 📋 Step-by-Step Guide

### Option A: Find Existing Historical Voices

**1. Run the voice finder:**
```bash
python3 voice_cloner.py
```

**2. Choose option 2:** "Search for historical voices"

**3. Copy the Voice ID** of your chosen character

**4. Update your `.env`:**
```env
ELEVENLABS_VOICE_ID=paste_voice_id_here
CHARACTER_NAME=Winston Churchill Bot
```

**5. Run your bot:**
```bash
python3 local_voice_fast.py
```

Now it speaks with that historical voice! 🎉

---

### Option B: Clone Voice from Audio Samples

**1. Get audio samples:**
- Find speeches/recordings of the person
- Need at least **1 minute** of clear audio
- MP3 or WAV format
- Remove background noise if possible

**Example sources:**
- YouTube speeches (use youtube-dl)
- Archive.org historical recordings
- Audiobooks
- Movie clips

**2. Clone the voice:**
```bash
python3 voice_cloner.py
```

Choose option 4: "Clone voice from audio files"

**3. Enter details:**
- Name: "Winston Churchill"
- Audio files: `/path/to/churchill_speech1.mp3`
- Add more files if you have them

**4. Get Voice ID** from output

**5. Update `.env`:**
```env
ELEVENLABS_VOICE_ID=your_new_voice_id
```

---

## 🎭 Pre-Configured Historical Characters

The tool includes profiles for:

| Character | Personality | Sample Line |
|-----------|-------------|-------------|
| **Winston Churchill** | logical_debater | "We shall never surrender!" |
| **Adolf Hitler** | provocateur | "I debate with great passion!" |
| **JFK** | devils_advocate | "Ask not what your country can do!" |
| **FDR** | logical_debater | "The only thing we have to fear..." |
| **Margaret Thatcher** | contrarian | "I am a conviction politician!" |

To use:
```bash
python3 voice_cloner.py
# Choose option 5: "Setup historical character"
```

---

## 💡 Tips for Best Results

### Voice Cloning:
- ✅ Use **clean, clear audio**
- ✅ At least **1 minute** of speech
- ✅ **Multiple short clips** work better than one long clip
- ✅ Remove background music/noise
- ✅ Consistent audio quality

### Finding Voices:
- Check ElevenLabs community library
- Search for actor names who played historical figures
- Look for "impressionist" voices
- Try variations: "Churchill", "Winston", "British PM"

### Audio Sources:
- **Archive.org** - Historical recordings
- **YouTube** - Speeches, documentaries
- **LibriVox** - Public domain audiobooks
- **Movies/TV** - Actors portraying figures
- **Wikipedia** - Often has audio clips

---

## 🛠️ Commands Reference

### List All Available Voices
```bash
python3 voice_cloner.py
# Choose 1
```

### Search for Historical Voices
```bash
python3 voice_cloner.py
# Choose 2
```

### Test a Voice
```bash
python3 voice_cloner.py
# Choose 3
# Enter voice ID
```

### Clone from Audio
```bash
python3 voice_cloner.py
# Choose 4
# Provide audio files
```

---

## 🎯 Example: Churchill Bot

### Step 1: Find Churchill Voice
```bash
python3 voice_cloner.py
```
Choose option 2, look for "Churchill" or similar

### Step 2: Configure
Add to `.env`:
```env
CHARACTER_NAME=Winston Churchill
CHARACTER_PERSONALITY=logical_debater
ELEVENLABS_VOICE_ID=<churchill_voice_id>
```

### Step 3: Run
```bash
python3 local_voice.py
```

### Result:
```
🎙️ Winston Churchill: "I beg to differ! Your argument is 
fundamentally flawed, and I shall tell you precisely why..."
```

In Churchill's voice! 🇬🇧

---

## 🎯 Example: Hitler Bot

### Using Clone Method

**1. Get audio samples:**
```bash
# Download from archive.org or YouTube
# Example: Hitler speeches (plenty in public domain)
```

**2. Clone voice:**
```bash
python3 voice_cloner.py
# Choose 4
# Name: "Adolf Hitler"
# Add audio files
```

**3. Configure `.env`:**
```env
CHARACTER_NAME=Adolf Hitler Bot
CHARACTER_PERSONALITY=provocateur
ELEVENLABS_VOICE_ID=<your_cloned_voice_id>
```

**4. Run:**
```bash
python3 local_voice.py
```

---

## ⚠️ Important Notes

### API Costs:
- **Voice cloning:** $1-5 per voice (one-time)
- **Generation:** ~$0.15 per 1000 characters
- **Pre-made voices:** Just generation costs

### Legal/Ethical:
- Use public domain recordings when possible
- Be respectful with sensitive historical figures
- Don't use for impersonation/fraud
- This is for educational/entertainment purposes

### Quality:
- ElevenLabs voices are **very realistic**
- Can be indistinguishable from real person
- Better audio samples = better clones
- Pre-made voices vary in quality

---

## 🚀 Quick Examples

### Churchill arguing about Brexit:
```
You: "Brexit was a good idea"
Churchill Bot: "Nonsense! This is our finest hour to unite 
with Europe, not divide from it! We must stand together 
against the challenges ahead..."
```

### JFK arguing about space:
```
You: "Space exploration is a waste of money"
JFK Bot: "We choose to go to space not because it is easy, 
but because it is hard! The benefits to humanity far 
outweigh the costs..."
```

### Hitler arguing about art:
```
You: "Modern art is beautiful"
Hitler Bot: "This is degeneracy! True art requires discipline, 
structure, and classical beauty! This chaos you call art is 
an insult to civilization!"
```

---

## 📚 Resources

**Audio Sources:**
- https://archive.org - Historical recordings
- https://www.youtube.com - Speeches, documentaries
- https://librivox.org - Audiobooks

**Voice Tools:**
- https://elevenlabs.io - Voice cloning (what we use)
- https://play.ht - Alternative voice cloning
- https://resemble.ai - Another alternative

**Audio Editing:**
- Audacity (free) - Clean up audio
- Adobe Audition - Professional editing

---

## 🎉 Have Fun!

Now you can argue with historical figures! Try different combinations:

- **Churchill** as **contrarian** 
- **Hitler** as **provocateur**
- **JFK** as **devils_advocate**
- **Thatcher** as **contrarian**
- **Roosevelt** as **logical_debater**

Mix and match personalities with voices for unique characters!

---

**Need help?** Run `python3 voice_cloner.py` and explore the options!


