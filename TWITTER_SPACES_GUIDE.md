# 🐦 Twitter Spaces Integration Guide

Get Hitler arguing on Twitter Spaces!

---

## 🚀 Quick Setup

### 1. Add Twitter Credentials to `.env`

```env
TWITTER_USERNAME=your_twitter_handle
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
```

### 2. Install Audio Routing (IMPORTANT!)

Twitter Spaces audio needs to be routed to the bot. On macOS:

```bash
# Install BlackHole (virtual audio device)
brew install blackhole-2ch
```

This creates a virtual audio device to route Space audio to your bot.

### 3. Configure Audio Routing

**Set up audio routing in macOS:**

1. Open **Audio MIDI Setup** app
2. Click **+** → Create **Multi-Output Device**
3. Name it "Space Output"
4. Check: **BlackHole 2ch** + **Your Speakers**
5. Click **+** → Create **Aggregate Device**
6. Name it "Space Input"
7. Check: **BlackHole 2ch** + **Your Microphone**

**In System Settings:**
- Output: **Space Output** (so you hear + bot captures)
- Input: **Space Input** (so bot speaks through Twitter)

### 4. Run the Bot

```bash
python3 twitter_spaces.py
```

---

## 🎮 How to Use

### Option A: Create Your Own Space

```bash
python3 twitter_spaces.py
# Choose 1
# Follow browser prompts to create Space
# Title: "Argue with Adolf Hitler"
# Start the Space
```

### Option B: Join Existing Space

```bash
python3 twitter_spaces.py
# Choose 2
# Enter Space URL: https://twitter.com/i/spaces/...
```

---

## 🎙️ What Happens

1. **Browser opens** and logs into Twitter
2. **Joins/Creates** a Space
3. **You become a speaker**
4. **Bot listens** to everyone in the Space
5. **Bot argues back** in Hitler's voice
6. **Fully autonomous** - no commands needed!

---

## 🎬 Example Flow

```
Space Host: "Welcome everyone! What do you think about democracy?"

Hitler Bot: 🎙️ "Democracy is weakness! The masses need a strong 
             leader, not endless debate and compromise!"

Another Speaker: "But freedom is important..."

Hitler Bot: 🎙️ "Freedom without discipline is chaos! Order and 
             strength are what nations need to thrive!"
```

**All automatic!** Hitler argues with everyone who speaks. 😈

---

## ⚙️ Audio Setup Explained

### Why BlackHole?

Twitter Spaces runs in the browser. To make the bot work:

1. **Capture Space Audio** → BlackHole captures what's playing
2. **Bot Listens** → Transcribes what people say
3. **Bot Speaks** → Plays audio through BlackHole to Twitter
4. **Space Hears Bot** → Everyone in Space hears Hitler arguing!

### Audio Flow:

```
Twitter Space → BlackHole → Bot (listening)
Bot (speaking) → BlackHole → Twitter Space
```

---

## 🔧 Alternative (Simpler but Manual)

### Simple Method (No Audio Routing):

1. **Join Space normally** on your phone or desktop
2. **Run the local bot:**
   ```bash
   python3 local_voice.py
   ```
3. **Play Space through speakers**
4. **Bot picks up audio** from speakers
5. **Bot responds through your mic**
6. **Unmute yourself** when bot speaks

**Pros:** No audio routing needed
**Cons:** You manually unmute/mute

---

## 🎯 Full Autonomous Setup

For fully autonomous arguing on Spaces:

### 1. Install BlackHole
```bash
brew install blackhole-2ch
```

### 2. Configure Audio
- System Output → Space Output (Multi-Output)
- System Input → Space Input (Aggregate)

### 3. Update `.env`
```env
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
```

### 4. Run
```bash
python3 twitter_spaces.py
```

### 5. Create or Join Space

Browser will open, you'll see Twitter. Create a Space titled:
- "Argue with Adolf Hitler"
- "Debate Night with AI Hitler"
- "Free Speech Space - AI Debates"

### 6. Watch Hitler Argue

The bot will:
- ✅ Listen to all speakers
- ✅ Generate responses with your Llama model
- ✅ Speak in Hitler's voice
- ✅ Argue with everyone automatically!

---

## 💡 Tips

### For Best Results:

- **Clear audio:** Use good internet connection
- **Low latency:** Reduce `pause_threshold` for faster responses
- **Good mic:** Bot needs to hear Space audio clearly
- **Announce the bot:** Tell people it's an AI so they know!

### Personality Tweaks:

Edit `character.py` to make Hitler more/less aggressive:
- Increase `temperature` for more random responses
- Decrease `max_new_tokens` for shorter arguments
- Change personality traits

---

## ⚠️ Important Notes

### Legal/Ethical:
- **Disclose it's a bot** - Don't pretend it's a real person
- **Follow Twitter TOS** - Automation may violate terms
- **Be respectful** - Even if Hitler isn't 😄
- **Don't spam** - Use responsibly

### Technical:
- Twitter may detect automation
- Account could be suspended
- Use a burner account for testing
- Spaces API is unofficial

### Audio Quality:
- Depends on your internet
- BlackHole can introduce slight delay
- Test locally first before going live

---

## 🔥 Pro Tips

### Make It Viral:

1. **Name the Space:** "AI Adolf Hitler Argues About Everything"
2. **Invite people:** Share the Space link
3. **Controversial topics:** Politics, religion, current events
4. **Record it:** Save for content
5. **Clips:** Cut best arguments for Twitter/TikTok

### Manage the Bot:

- Press `Ctrl+C` to stop
- Bot maintains conversation context
- Switch personalities mid-Space with config changes

---

## 🧪 Testing Steps

### Step 1: Test Locally
```bash
python3 local_voice.py
```
Make sure Hitler argues well locally first.

### Step 2: Test Browser Login
```bash
python3 twitter_spaces.py
```
Verify it can login to Twitter.

### Step 3: Test Audio Routing
- Set up BlackHole
- Test you can hear and be heard
- Verify bot captures audio

### Step 4: Go Live!
Create or join a Space and let Hitler argue!

---

## 📊 Expected Performance

- **Response time:** 2-3 seconds after someone speaks
- **Quality:** Depends on internet and audio routing
- **Engagement:** People WILL argue back 😄

---

## 🎉 You're Ready!

Run: `python3 twitter_spaces.py`

**Let Hitler argue on Twitter Spaces!** 🐦🎙️

---

**Questions?** Check the troubleshooting section in README.md


