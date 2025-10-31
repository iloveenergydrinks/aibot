#!/bin/bash

echo "🎭 Argue Bot Setup Script"
echo "=========================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

# Check if FFmpeg is installed
echo ""
echo "🔊 Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "   ✅ FFmpeg is installed"
else
    echo "   ❌ FFmpeg not found!"
    echo "   Please install FFmpeg:"
    echo "   - macOS: brew install ffmpeg"
    echo "   - Ubuntu: sudo apt install ffmpeg"
    echo "   - Windows: Download from https://ffmpeg.org"
    exit 1
fi

# Create virtual environment
echo ""
echo "🐍 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "   ✅ Created .env file"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   Required:"
    echo "   - DISCORD_BOT_TOKEN"
    echo "   - OPENAI_API_KEY or ANTHROPIC_API_KEY"
else
    echo "ℹ️  .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env and add your API keys"
echo "   2. Create a Discord bot at https://discord.com/developers/applications"
echo "   3. Invite the bot to your server"
echo "   4. Run: python bot.py"
echo ""
echo "🎉 Have fun arguing!"



