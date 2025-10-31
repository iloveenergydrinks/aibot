# ⚡ FASTEST WAY TO TEST - Skip Discord!

You're right - Discord setup is slow! Here are 3 **MUCH FASTER** options:

---

## 🥇 Option 1: Simple Text Chat (30 seconds!)

**No voice, no Discord, just type and argue.**

```bash
# 1. Install dependencies
pip install openai anthropic python-dotenv

# 2. Create .env
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run!
python simple_chat.py
```

**That's it!** Start typing and arguing.

### Example:
```
💬 You: I think cats are better than dogs
🎭 Carl: That's ridiculous! Dogs are loyal companions...

💬 You: But cats are independent
🎭 Carl: Independent? You mean aloof and uncaring...
```

---

## 🥈 Option 2: Local Voice (2 minutes)

**Use your computer's microphone and speakers - no Discord!**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run!
python local_voice.py
```

**Just talk into your mic!** The bot listens and argues back through your speakers.

### How it works:
1. Script starts
2. Say something into your mic
3. Bot transcribes your speech
4. Bot argues back (speaks out loud)
5. Repeat!

---

## 🥉 Option 3: Discord (10+ minutes)

The full experience but takes longer to set up.

```bash
python main.py
```

Requires:
- Discord bot setup
- Server invite
- Voice channel setup

---

## 📊 Comparison

| Method | Setup Time | Voice | Discord | Best For |
|--------|-----------|-------|---------|----------|
| **simple_chat.py** | 30 sec | ❌ | ❌ | Quick testing |
| **local_voice.py** | 2 min | ✅ | ❌ | Local testing |
| **main.py** | 10+ min | ✅ | ✅ | Full experience |

---

## 🚀 Quick Start (Choose One)

### Absolute Fastest (Text Only):

```bash
cd argue
pip install openai anthropic python-dotenv
echo "OPENAI_API_KEY=sk-your-key" > .env
python simple_chat.py
```

### Fast with Voice:

```bash
cd argue
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-your-key" > .env
python local_voice.py
```

### Full Discord Experience:

```bash
cd argue
pip install -r requirements.txt
# Set up .env with Discord token
python main.py
```

---

## 💡 Recommendation

**Start with `simple_chat.py`** to test the AI character immediately!

Then upgrade to `local_voice.py` when you want to test voice.

Finally move to Discord (`main.py`) when everything works.

---

## 🔑 What You Need

### For simple_chat.py:
- ✅ Just an OpenAI or Anthropic API key

### For local_voice.py:
- ✅ OpenAI or Anthropic API key
- ✅ Working microphone
- ✅ Speakers/headphones

### For main.py (Discord):
- ✅ OpenAI or Anthropic API key
- ✅ Discord bot token
- ✅ Discord server
- ✅ FFmpeg installed

---

## 📝 Example Workflow

### Day 1: Test the AI
```bash
python simple_chat.py
# Play with different personalities
# Make sure AI responses work
```

### Day 2: Add Voice
```bash
python local_voice.py
# Test speech recognition
# Test text-to-speech
# Verify audio quality
```

### Day 3: Go Live on Discord
```bash
python main.py
# Share with friends
# Full autonomous experience
```

---

## 🎯 Bottom Line

**Want to test RIGHT NOW?**

```bash
pip install openai python-dotenv
echo "OPENAI_API_KEY=sk-your-key" > .env
python simple_chat.py
```

**30 seconds. Done.** ✅


