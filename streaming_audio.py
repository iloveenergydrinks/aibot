#!/usr/bin/env python3
"""
Streaming Audio Player with Interrupt Support

Uses ElevenLabs streaming API + PyAudio for real-time playback.
Can be interrupted mid-speech!
"""
import pyaudio
import threading
import queue
import speech_recognition as sr
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import config

client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)


class StreamingPlayer:
    """Plays streaming audio and can be interrupted."""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_playing = False
        self.should_stop = False
        self.audio_queue = queue.Queue()
        
    def play_streaming(self, text, voice_id):
        """Play text with streaming TTS - can be interrupted!"""
        self.is_playing = True
        self.should_stop = False
        
        # Get streaming audio from ElevenLabs
        voice_settings = VoiceSettings(
            stability=0.7,
            similarity_boost=0.85,
            style=0.4,
            use_speaker_boost=True
        )
        
        # Generate streaming audio
        try:
            # Save to temp file first, then stream it
            # (ElevenLabs API returns generator, we need to handle it properly)
            import tempfile
            temp_file = tempfile.mktemp(suffix=".mp3")
            
            audio_generator = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_monolingual_v1",
                voice_settings=voice_settings
            )
            
            # Write chunks as they arrive
            with open(temp_file, "wb") as f:
                for chunk in audio_generator:
                    if self.should_stop:
                        print("🔇 Generation stopped!")
                        break
                    f.write(chunk)
            
            if self.should_stop:
                import os
                os.remove(temp_file)
                self.is_playing = False
                return
            
            # Now play the file with mpv (can be killed mid-playback)
            import subprocess
            self.process = subprocess.Popen(
                ["afplay", temp_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for playback, but check if should stop
            while self.process.poll() is None:
                if self.should_stop:
                    self.process.terminate()
                    print("🔇 Playback stopped!")
                    break
                import time
                time.sleep(0.05)
            
            self.process.wait()
            
            # Cleanup
            import os
            os.remove(temp_file)
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.is_playing = False
    
    def stop(self):
        """Stop playback immediately."""
        self.should_stop = True
    
    def cleanup(self):
        """Cleanup audio resources."""
        if self.stream:
            self.stream.close()
        self.audio.terminate()


def play_with_interrupts(text, voice_id, mic_params=None):
    """
    Play text with streaming TTS and monitor for interrupts.
    
    Returns: True if interrupted, False if completed
    """
    player = StreamingPlayer()
    interrupted = False
    
    # Start playing in background thread
    play_thread = threading.Thread(target=player.play_streaming, args=(text, voice_id))
    play_thread.start()
    
    # Wait a bit before checking for interrupts
    import time
    time.sleep(1.0)
    
    # Monitor for interrupts while playing
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 3000
    
    mic_params = mic_params or {}
    
    mic_params_safe = mic_params if mic_params else {}
    
    while player.is_playing and not player.should_stop:
        try:
            with sr.Microphone(**mic_params_safe) as source:
                try:
                    # Quick listen for interrupt
                    audio = recognizer.listen(source, timeout=0.3, phrase_time_limit=1)
                    
                    # Someone is speaking - interrupt!
                    import audioop
                    rms = audioop.rms(audio.get_raw_data(), 2)
                    
                    if rms > 800:  # Loud enough to be real speech
                        print("\n⚠️ INTERRUPTED by speech!")
                        player.stop()
                        interrupted = True
                        
                        # Return the interruption audio for processing
                        return (True, audio)
                        
                except sr.WaitTimeoutError:
                    pass  # No interruption
        except:
            pass
        
        time.sleep(0.1)
    
    # Wait for playback to finish
    play_thread.join()
    player.cleanup()
    
    return (False, None)


# Test
if __name__ == "__main__":
    print("\n🧪 Testing Streaming TTS with Interrupts...\n")
    print("Hitler will speak. Try talking to interrupt him!\n")
    
    test_text = "Nein! Democracy is a weak system invented by die Juden to control das Volk! The Weimar Republic proved this when it collapsed into chaos and allowed the communists to nearly take over Germany!"
    
    print(f"🎭 Hitler: \"{test_text}\"\n")
    print("🔊 Streaming... (speak now to interrupt!)\n")
    
    interrupted, int_audio = play_with_interrupts(test_text, config.ELEVENLABS_VOICE_ID)
    
    if interrupted:
        print("\n✅ Successfully interrupted!")
        print("   (In real bot, would process the interruption here)")
    else:
        print("\n✅ Completed without interruption")

