#!/usr/bin/env python3
"""
Twitter Spaces Integration - Join and argue in Twitter Spaces

Uses browser automation to:
1. Login to Twitter/X
2. Join or create a Space
3. Capture audio from speakers
4. Play bot's responses

Requirements:
- Playwright for browser automation
- Virtual audio devices for audio routing
"""
import asyncio
import os
import sys
from playwright.async_api import async_playwright
from character import AICharacter
from audio_processor import AudioProcessor
import config
import speech_recognition as sr
import subprocess
import time

# Twitter credentials from .env
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")

# Initialize
character = AICharacter()
audio_processor = AudioProcessor()


class TwitterSpacesBot:
    """Bot that joins Twitter Spaces and argues with speakers."""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.is_listening = False
        self.is_speaking = False
        
    async def start(self):
        """Start the browser and login to Twitter."""
        print("\n" + "="*70)
        print("🐦 TWITTER SPACES BOT - Starting")
        print("="*70 + "\n")
        
        playwright = await async_playwright().start()
        
        # Launch browser (headful so you can see what's happening)
        print("🌐 Launching browser...")
        self.browser = await playwright.chromium.launch(
            headless=False,  # Show browser
            args=[
                '--use-fake-ui-for-media-stream',  # Auto-allow mic
                '--use-fake-device-for-media-stream',
            ]
        )
        
        # Create context
        self.context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            permissions=['microphone']
        )
        
        self.page = await self.context.new_page()
        
        print("✅ Browser launched\n")
        
        # Login to Twitter
        await self.login_twitter()
        
    async def login_twitter(self):
        """Login to Twitter/X."""
        print("🔐 Logging into Twitter...\n")
        
        if not TWITTER_USERNAME or not TWITTER_PASSWORD:
            print("❌ Need TWITTER_USERNAME and TWITTER_PASSWORD in .env!")
            print("\nAdd to .env:")
            print("  TWITTER_USERNAME=your_username")
            print("  TWITTER_PASSWORD=your_password")
            print("  TWITTER_EMAIL=your_email")
            return False
        
        try:
            # Go to Twitter
            await self.page.goto("https://twitter.com/i/flow/login", wait_until="networkidle")
            await asyncio.sleep(2)
            
            # Enter username
            print("📝 Entering username...")
            username_input = await self.page.wait_for_selector('input[autocomplete="username"]', timeout=10000)
            await username_input.fill(TWITTER_USERNAME)
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(2)
            
            # Check if email verification needed
            try:
                email_input = await self.page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=3000)
                if email_input and TWITTER_EMAIL:
                    print("📧 Email verification required...")
                    await email_input.fill(TWITTER_EMAIL)
                    await self.page.keyboard.press("Enter")
                    await asyncio.sleep(2)
            except:
                pass  # No email verification needed
            
            # Enter password
            print("🔑 Entering password...")
            password_input = await self.page.wait_for_selector('input[name="password"]', timeout=10000)
            await password_input.fill(TWITTER_PASSWORD)
            await self.page.keyboard.press("Enter")
            await asyncio.sleep(3)
            
            # Check if logged in
            await self.page.wait_for_selector('[data-testid="AppTabBar_Home_Link"]', timeout=15000)
            
            print("✅ Logged into Twitter!\n")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("\n💡 Make sure your credentials in .env are correct")
            return False
    
    async def create_space(self, title="Come Argue with Hitler"):
        """Create a new Twitter Space."""
        print(f"🎙️ Creating Space: '{title}'...\n")
        
        try:
            # Click on Spaces icon (in sidebar or compose)
            # Note: Twitter's UI changes frequently, these selectors may need updates
            
            # Try to find Spaces button
            await self.page.goto("https://twitter.com/i/spaces/start", wait_until="networkidle")
            await asyncio.sleep(3)
            
            print("✅ Space creation page loaded")
            print("⚠️  Complete the Space setup manually in the browser:")
            print("   1. Click 'Create Space' or 'Start your Space'")
            print("   2. Set title: '{title}'")
            print("   3. Click 'Start your Space'")
            print("\nWaiting for Space to start...")
            
            # Wait for Space to be created (manual step)
            input("\n👉 Press Enter once you've started the Space...")
            
            print("✅ Space is live!\n")
            return True
            
        except Exception as e:
            print(f"❌ Error creating Space: {e}")
            return False
    
    async def join_space(self, space_url):
        """Join an existing Twitter Space.
        
        Args:
            space_url: URL of the Space to join
        """
        print(f"🎙️ Joining Space: {space_url}\n")
        
        try:
            await self.page.goto(space_url, wait_until="networkidle")
            await asyncio.sleep(3)
            
            # Click join/listen button
            try:
                join_button = await self.page.wait_for_selector('button:has-text("Join this Space")', timeout=5000)
                await join_button.click()
                print("✅ Clicked 'Join this Space'")
            except:
                pass  # Might already be in
            
            await asyncio.sleep(2)
            
            # Request to speak
            print("🎤 Requesting speaker access...")
            try:
                request_button = await self.page.wait_for_selector('[aria-label="Request"]', timeout=5000)
                await request_button.click()
                print("✅ Requested speaker access")
                print("⏳ Wait for host to approve you as speaker...")
            except:
                print("ℹ️  Already a speaker or button not found")
            
            print("\n✅ In the Space!\n")
            return True
            
        except Exception as e:
            print(f"❌ Error joining Space: {e}")
            return False
    
    async def listen_and_respond(self):
        """Main loop - listen to Space and respond."""
        print("="*70)
        print("🎧 AUTONOMOUS ARGUING MODE - ACTIVE")
        print("="*70)
        print(f"\n🎭 Character: {character.name}")
        print(f"🔥 Personality: {character.personality}")
        print(f"\n⚠️  IMPORTANT:")
        print("   Due to browser limitations, audio capture is complex.")
        print("   The bot will use your system microphone/speakers.")
        print(f"\n{'='*70}\n")
        
        print("💡 How it works:")
        print("   1. Bot listens to your computer's audio output")
        print("   2. Transcribes what people say in the Space")
        print("   3. Generates argumentative response")
        print("   4. Speaks through your mic into the Space")
        print(f"\n{'='*70}\n")
        
        input("Press Enter to start autonomous arguing...")
        
        self.is_listening = True
        exchange_count = 0
        
        recognizer = sr.Recognizer()
        
        print("\n🎧 Listening to Space...\n")
        
        while self.is_listening:
            try:
                # Listen to microphone (captures Space audio if routed)
                with sr.Microphone() as source:
                    print("🎤 Listening...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    
                    print("💭 Processing speech...")
                    
                    # Transcribe
                    text = audio_processor.speech_to_text(audio)
                    
                    if text and len(text) > 5:
                        print(f"\n💬 Speaker: {text}")
                        
                        # Generate response
                        response = character.generate_response(text, speaker_name="Speaker")
                        print(f"🎭 Hitler: {response}\n")
                        
                        # Speak response (goes through your mic into the Space)
                        audio_file = audio_processor.text_to_speech(response)
                        subprocess.run(["afplay", audio_file])
                        os.remove(audio_file)
                        
                        exchange_count += 1
                        print(f"\n  ─── Exchange {exchange_count} ───\n")
                        
                        # Small delay before listening again
                        await asyncio.sleep(1)
            
            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                print("\n\n👋 Stopping...")
                break
            except Exception as e:
                print(f"⚠️  Error: {e}")
                await asyncio.sleep(1)
        
        print(f"\n📊 Total exchanges: {exchange_count}")
    
    async def cleanup(self):
        """Close browser."""
        if self.browser:
            await self.browser.close()
            print("\n🚪 Browser closed")


async def main():
    """Main entry point."""
    bot = TwitterSpacesBot()
    
    try:
        # Start browser and login
        await bot.start()
        
        print("\n" + "="*70)
        print("CHOOSE MODE:")
        print("="*70)
        print("  1. Create a new Space")
        print("  2. Join an existing Space")
        print("="*70 + "\n")
        
        choice = input("Choose (1 or 2): ").strip()
        
        if choice == "1":
            # Create Space
            await bot.create_space()
        elif choice == "2":
            # Join Space
            space_url = input("\nEnter Space URL: ").strip()
            await bot.join_space(space_url)
        else:
            print("❌ Invalid choice")
            return
        
        # Start listening and responding
        await bot.listen_and_respond()
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.cleanup()


if __name__ == "__main__":
    print("\n🐦 TWITTER SPACES ARGUING BOT")
    print(f"Character: {character.name} ({character.personality})\n")
    
    asyncio.run(main())


