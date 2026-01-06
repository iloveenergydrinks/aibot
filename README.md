# AI Bot Fleet - VM Cloning Guide

This VM is fully configured and ready to clone. Follow these steps to create multiple agents with different characters.

---

## 🚀 Quick Start (Cloned VM)

### **This VM is configured as:**
- **Bot ID:** `michael-saylor`
- **Character:** Michael Saylor (Bitcoin Maximalist)
- **Voice:** ElevenLabs voice ID in config.py

### **When you clone this VM, change these 3 things:**

---

## 1️⃣ Change Bot ID (Required)

**File:** `twitter_autonomous.py` (Line 247)

```python
BOT_ID = "michael-saylor"  # 👈 CHANGE THIS
```

**Examples for other VMs:**
```python
BOT_ID = "vitalik-buterin"
BOT_ID = "changpeng-zhao"
BOT_ID = "elon-musk"
BOT_ID = "gary-gensler"
```

This determines the bot's name in Firebase database.

---

## 2️⃣ Change Character Personality (Optional)

**File:** `config.py`

### Change Character Name:
```python
CHARACTER_NAME = "Michael Saylor"  # Change to "Vitalik Buterin", etc
```

### Change Personality Prompt:
```python
CHARACTER_PERSONALITY = "michael_saylor"  # Available: "michael_saylor", etc
```

**Example for Vitalik:**
```python
CHARACTER_NAME = "Vitalik Buterin"

CHARACTER_PERSONALITY = "vitalik_buterin"

# You would need to add vitalik_buterin personality to character.py
# Similar to how michael_saylor is defined
```

---

## 3️⃣ Change Voice (Optional)

**File:** `config.py`

### Get a New ElevenLabs Voice:

1. Go to: https://elevenlabs.io/app/voice-lab
2. **Clone a voice** or use a pre-made one
3. Copy the **Voice ID**
4. Update config:

```python
ELEVENLABS_VOICE_ID = "your-new-voice-id-here"
```

**Current voice:** Professional American English (Saylor-like)

---

## 📊 Firebase Setup (Already Done!)

All VMs share the same Firebase credentials:
- **Collection:** `adolfhitler`
- **Database URL:** `https://solwind-3e0d2-default-rtdb.firebaseio.com`

Each bot reports to: `adolfhitler/{BOT_ID}/`

### Website Integration:

```javascript
// Fetch all bots
fetch('https://solwind-3e0d2-default-rtdb.firebaseio.com/adolfhitler.json')
  .then(res => res.json())
  .then(bots => {
    // bots.adolf-hitler
    // bots.joseph-goebbels
    // bots.heinrich-himmler
  });
```

---

## 🎯 Running the Bot

### Prerequisites (Already Installed):
- ✅ Python 3.11
- ✅ FFmpeg
- ✅ VoiceMeeter
- ✅ All Python packages
- ✅ Firebase credentials

### Start Bot:

1. **Start VoiceMeeter** (if not running):
   ```powershell
   & "C:\Program Files (x86)\VB\Voicemeeter\voicemeeter.exe"
   ```

2. **Join X Space** in Edge browser:
   - Make sure Edge microphone = "VoiceMeeter Output"
   - Become a speaker
   - **Stay UNMUTED**

3. **Run bot:**
   ```powershell
   cd C:\Users\miningofficer\Desktop\aibot-main
   python -u twitter_autonomous.py
   ```

4. **Enter Space URL** when prompted (optional)
5. **Press Enter** when unmuted
6. **Walk away** - bot runs autonomously!

---

## 🔄 Cloning Workflow

### For Each New VM:

1. **Clone this VM** in Google Cloud
2. **Start the cloned VM**
3. **Connect via RDP**
4. **Change 3 things:**
   - `BOT_ID` in `twitter_autonomous.py` (line 247)
   - `CHARACTER_NAME` in `config.py` (optional)
   - `ELEVENLABS_VOICE_ID` in `config.py` (optional)
5. **Start the bot**
6. **Check Firebase** - new bot appears automatically!

---

## 📈 Tracked Metrics (Automatic)

Each bot automatically tracks:
- **`argument_count`** - Responses to people
- **`propaganda_count`** - Solo propaganda speeches
- **`interruptions_handled`** - Times interrupted
- **`total_interactions`** - Combined total
- **`responses_per_hour`** - Auto-calculated rate
- **`hours_online`** - Running time
- **`uptime_percentage`** - 99.9%
- **`last_response`** - Latest speech
- **`status`** - "online" or "offline"

All update in real-time to Firebase!

---

## 🛠️ Troubleshooting

### VoiceMeeter Not Working After Restart:

Run this batch file:
```powershell
.\restart_voicemeeter.bat
```

### Bot Not Hearing Audio:

1. Check VoiceMeeter "Virtual Input" B1 button is ON
2. Check fader is raised
3. Check Edge browser microphone = "VoiceMeeter Output"

### Firebase Not Updating:

Check `firebase-key.json` exists in the folder.

---

## 📁 Important Files

- **`twitter_autonomous.py`** - Main bot script (change BOT_ID here)
- **`config.py`** - Character & voice settings
- **`firebase-key.json`** - Firebase credentials (shared across all VMs)
- **`.env`** - API keys (OpenAI, ElevenLabs, Firebase URL)
- **`requirements.txt`** - Python dependencies

---

## 💡 Example: Creating "Vitalik Buterin" VM

1. **Clone this VM** → VM-2
2. **Edit `twitter_autonomous.py` line 247:**
   ```python
   BOT_ID = "vitalik-buterin"
   ```
3. **Edit `config.py`:**
   ```python
   CHARACTER_NAME = "Vitalik Buterin"
   ELEVENLABS_VOICE_ID = "new-voice-id"  # Optional
   CHARACTER_PERSONALITY = "vitalik_buterin"  # Add to character.py first
   ```
4. **Start bot**
5. **Check Firebase:** `adolfhitler/vitalik-buterin/` appears!

---

## ⚠️ Keep RDP Session Alive

**On your Mac:**
```bash
caffeinate -d
```

This prevents your Mac from sleeping and keeps RDP connected, so VoiceMeeter settings persist.

---

**Ready to deploy your AI bot army!** 🎖️


