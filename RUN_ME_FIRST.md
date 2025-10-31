## 🚀 AUTONOMOUS ARGUING BOT - START HERE!

### What is this?

An AI bot that **joins Discord voice channels and automatically argues with you.**

Just talk → Bot listens → Bot argues back!

---

## ⚡ Super Quick Start (5 minutes)

### Step 1: Install FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

### Step 2: Install Python packages

```bash
cd argue
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Get your API keys

1. **Discord Bot Token**
   - https://discord.com/developers/applications
   - Create app → Bot → Copy token
   - Enable "Message Content Intent" and "Server Members Intent"

2. **OpenAI API Key** (OR Anthropic)
   - https://platform.openai.com → API Keys
   - Create new key → Copy it

### Step 4: Create `.env` file

```bash
cp .env.example .env
nano .env  # or use any text editor
```

Add your keys:
```
DISCORD_BOT_TOKEN=your_discord_token_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 5: Invite bot to your Discord server

In Discord Developer Portal:
- OAuth2 → URL Generator
- Scopes: `bot`
- Permissions: `Send Messages`, `Connect`, `Speak`
- Open the URL and add to your server

### Step 6: RUN IT!

```bash
python main.py
```

You should see:
```
🚀 STARTING AUTONOMOUS ARGUING BOT
✅ Configuration validated
✅ Character: Contrarian Carl (contrarian)
🎙️ Starting Discord bot...
🤖 AUTONOMOUS ARGUING BOT - ONLINE
```

### Step 7: Test in Discord

1. **Join a voice channel**
2. **Type:** `!join`
3. **Start talking!**
4. **Bot will argue with you automatically!**

---

## 🧪 Test First (Recommended)

Before running on Discord, test everything works:

```bash
python test_local.py
```

This checks:
- ✅ All dependencies installed
- ✅ API keys working
- ✅ AI character works
- ✅ Audio processing works
- ✅ FFmpeg installed

---

## 🎮 How to Use

### In Discord:

```
You:  *join voice channel*
You:  !join
Bot:  🎙️ JOINED! Just start talking...

You:  "I think cats are better than dogs"
Bot:  "That's completely wrong! Dogs are loyal companions 
       while cats are indifferent creatures who barely 
       tolerate your existence..."

You:  "But cats are independent!"
Bot:  "Independent? You mean lazy and aloof! That's not 
       a virtue, that's just cats being selfish..."
```

### Commands:

- `!join` - Bot joins and starts listening
- `!leave` - Bot leaves
- `!personality provocateur` - Make bot more aggressive
- `!status` - Check if bot is listening

---

## 🎭 Personalities

Try different debate styles:

```
!personality contrarian      # Disagrees with everything (default)
!personality devils_advocate # Explores counterarguments
!personality provocateur     # Aggressive and inflammatory
!personality sophist        # Wins through rhetoric
!personality logical_debater # Uses facts and logic
```

---

## ⚠️ Troubleshooting

### Bot doesn't hear me?
- Check you're not muted in Discord
- Speak clearly and loudly
- Check Discord voice settings

### Bot doesn't speak?
- Check FFmpeg is installed: `ffmpeg -version`
- Make sure bot has "Speak" permission
- Try `!leave` then `!join`

### Bot doesn't respond?
- Check API keys in `.env`
- Check you have API credits
- Look at terminal for errors

### Still not working?
```bash
python test_local.py
```

This will tell you exactly what's wrong!

---

## 📖 Full Documentation

See `README.md` for complete documentation.

---

## 🎉 That's It!

You now have an AI that argues with you in voice channels!

**Have fun!** 😈



