# 🎧 BlackHole Setup - Step by Step Guide

Complete guide to properly capture Twitter Spaces audio for Hitler bot.

---

## 🚀 **Complete Setup (15 minutes)**

### **Step 1: Install BlackHole**

**In YOUR terminal, run:**

```bash
cd /Users/olmo9/Desktop/Grypto/argue
./setup_spaces_audio.sh
```

**Or manually:**

```bash
brew install blackhole-2ch
```

**⚠️ IMPORTANT:** You MUST reboot your Mac after installation!

```bash
sudo reboot
```

---

### **Step 2: Configure Audio Devices (After Reboot)**

**Open Audio MIDI Setup:**

1. Press `Cmd + Space`
2. Type: "Audio MIDI Setup"
3. Press Enter

---

### **Step 3: Create Multi-Output Device**

**In Audio MIDI Setup:**

1. Click **+** button (bottom left corner)
2. Select **"Create Multi-Output Device"**
3. In the right panel:
   - ✅ Check **"BlackHole 2ch"**
   - ✅ Check **"MacBook Pro Speakers"** (or your speakers)
4. Right-click the device → Rename to **"Spaces Output"**
5. ✅ Keep this window open

**What this does:**
- Audio goes to BOTH BlackHole AND your speakers
- You can hear + bot can capture

---

### **Step 4: Create Aggregate Device**

**Still in Audio MIDI Setup:**

1. Click **+** button again
2. Select **"Create Aggregate Device"**
3. In the right panel:
   - ✅ Check **"BlackHole 2ch"** 
   - ✅ Check **"MacBook Pro Microphone"** (or your mic)
4. Right-click the device → Rename to **"Spaces Input"**
5. ✅ Close Audio MIDI Setup

**What this does:**
- Bot can capture from BlackHole + use your mic
- Bot can speak through the same device

---

### **Step 5: Set as System Default**

**Open System Settings:**

1. Go to **System Settings** (or System Preferences)
2. Click **Sound**
3. **Output tab:**
   - Select **"Spaces Output"** (the Multi-Output you created)
4. **Input tab:**
   - Select **"Spaces Input"** (the Aggregate you created)

---

### **Step 6: Test BlackHole**

**Run the test script:**

```bash
python3 test_blackhole.py
```

**Follow the prompts:**
1. Play some audio (YouTube, etc)
2. Bot will try to capture it
3. If it works, you'll see transcribed text!

---

## 🎯 **Visual Setup Summary:**

```
┌─────────────────────────────────────────────┐
│         TWITTER SPACE (in browser)          │
│                                             │
│  People talking → Audio output              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      MULTI-OUTPUT DEVICE "Spaces Output"    │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ BlackHole 2ch│  →   │  Your Speakers  │ │
│  └──────────────┘      └─────────────────┘ │
└─────────────────────────────────────────────┘
         ↓                        ↓
    Bot captures            You hear Space
         ↓
┌─────────────────────────────────────────────┐
│      AGGREGATE DEVICE "Spaces Input"        │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ BlackHole 2ch│  +   │   Your Mic      │ │
│  └──────────────┘      └─────────────────┘ │
└─────────────────────────────────────────────┘
         ↓
    Hitler Bot
         ↓
    Speaks back → BlackHole → Twitter Space hears
```

---

## ✅ **Verification Checklist:**

After setup, you should have:

- ✅ BlackHole 2ch installed (check in Audio MIDI Setup)
- ✅ "Spaces Output" Multi-Output device created
- ✅ "Spaces Input" Aggregate device created
- ✅ System Output set to "Spaces Output"
- ✅ System Input set to "Spaces Input"
- ✅ `test_blackhole.py` passes all tests

---

## 🧪 **Quick Test:**

**Test 1: Can you hear audio?**
```bash
# Play a YouTube video
# You should hear it through your speakers
```

**Test 2: Can bot capture audio?**
```bash
python3 test_blackhole.py
# Play audio when prompted
# Bot should transcribe it
```

**Test 3: Can bot speak into Space?**
```bash
# Join a Space
# Run: python3 twitter_optimized.py
# Bot's audio should go directly to Space
```

---

## 🔧 **Troubleshooting:**

### "Can't hear any audio after setup"
- Check "Spaces Output" has your speakers checked
- Check system volume isn't muted
- Try switching back to regular speakers, then back to Spaces Output

### "Bot doesn't capture audio"
- Verify system Input is "Spaces Input"
- Check BlackHole is checked in Aggregate device
- Reboot Mac if just installed

### "Space doesn't hear bot"
- Check browser is using correct audio input
- Verify system Input is "Spaces Input"
- Test bot audio plays through speakers first

### "Echo or feedback"
- Normal with this setup
- Use headphones instead of speakers
- Lower Space volume

---

## 🎧 **Using Headphones (Recommended)**

To avoid feedback:

1. **Multi-Output Device:**
   - BlackHole 2ch ✅
   - Headphones ✅ (instead of speakers)

2. **Wear headphones** while bot is speaking
3. This prevents feedback loop

---

## 📋 **After Setup - Run Bot:**

### Option 1: Simple Mode
```bash
python3 twitter_simple.py
```

### Option 2: Optimized Mode (Recommended)
```bash
python3 twitter_optimized.py
```

### Option 3: Fully Automated
```bash
python3 twitter_spaces.py
```

---

## 🎉 **You're Ready!**

Once BlackHole is set up:
1. ✅ Clean audio capture from Spaces
2. ✅ Direct audio output to Spaces
3. ✅ No more janky mic-to-speakers
4. ✅ Professional quality audio routing

**Hitler can now argue properly in Twitter Spaces!** 🐦🎙️

---

## 💡 **Pro Tip:**

Once you're comfortable, you can:
- Switch back to normal audio when not using bot
- Or create a shortcut to toggle between configs
- Or use separate audio profiles

---

**Questions?** Run `python3 test_blackhole.py` to diagnose issues!


