"""Audio processing for speech recognition and text-to-speech."""
import io
import os
import tempfile
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import openai
from config import (
    OPENAI_API_KEY,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    USE_ELEVENLABS,
    SAMPLE_RATE
)

try:
    from elevenlabs.client import ElevenLabs
    if USE_ELEVENLABS:
        elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    elevenlabs_client = None


class AudioProcessor:
    """Handles speech-to-text and text-to-speech conversion."""
    
    def __init__(self):
        """Initialize audio processor."""
        self.recognizer = sr.Recognizer()
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        
        # Configure recognizer
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print("🎤 Audio processor initialized")
        if USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
            print("  - TTS: ElevenLabs")
        elif self.openai_client:
            print("  - TTS: OpenAI TTS")
        else:
            print("  - TTS: Google TTS (fallback)")
        print("  - STT: Google Speech Recognition / OpenAI Whisper")
    
    def speech_to_text(self, audio_data: sr.AudioData, use_whisper: bool = False) -> Optional[str]:
        """Convert speech audio to text.
        
        Args:
            audio_data: Audio data from microphone/voice channel
            use_whisper: Whether to use OpenAI Whisper (more accurate but slower)
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            if use_whisper and self.openai_client:
                # Use OpenAI Whisper API
                text = self._whisper_transcribe(audio_data)
            else:
                # Use Google Speech Recognition (free, faster)
                text = self.recognizer.recognize_google(audio_data)
            
            if text:
                print(f"🎤 Transcribed: {text}")
                return text
            return None
            
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def _whisper_transcribe(self, audio_data: sr.AudioData) -> str:
        """Transcribe audio using OpenAI Whisper API."""
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_data.get_wav_data())
            temp_path = f.name
        
        try:
            with open(temp_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcript.text
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def text_to_speech(self, text: str, output_path: str = None) -> str:
        """Convert text to speech audio file.
        
        Args:
            text: Text to convert to speech
            output_path: Where to save the audio file
            
        Returns:
            Path to the generated audio file
        """
        if not output_path:
            output_path = tempfile.mktemp(suffix=".mp3")
        
        try:
            # Check if forcing OpenAI for speed
            from config import FORCE_OPENAI_TTS
            
            if FORCE_OPENAI_TTS and self.openai_client:
                # Use OpenAI TTS (FASTER - 0.5s vs 1.5s)
                return self._openai_tts(text, output_path)
            elif USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
                # Use ElevenLabs (highest quality but slower)
                return self._elevenlabs_tts(text, output_path)
            elif self.openai_client:
                # Use OpenAI TTS
                return self._openai_tts(text, output_path)
            else:
                # Use gTTS (free fallback)
                return self._gtts_tts(text, output_path)
                
        except Exception as e:
            print(f"❌ TTS error: {e}")
            # Fallback to gTTS
            return self._gtts_tts(text, output_path)
    
    def _elevenlabs_tts(self, text: str, output_path: str) -> str:
        """Generate speech using ElevenLabs."""
        from elevenlabs import VoiceSettings
        
        # Voice settings optimized for deeper, more masculine tone and natural pace
        voice_settings = VoiceSettings(
            stability=0.7,
            similarity_boost=0.85,
            style=0.4,
            use_speaker_boost=True
        )
        
        # Use TURBO model for faster generation while keeping quality
        audio_generator = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_turbo_v2_5",  # Turbo v2.5 = fastest + good quality
            voice_settings=voice_settings
        )
        
        # Save with volume boost
        temp_output = output_path.replace('.mp3', '_temp.mp3')
        with open(temp_output, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        # Just boost volume - no slowdown for faster speech
        try:
            audio = AudioSegment.from_file(temp_output)
            
            # Boost volume only
            boosted_audio = audio + 6
            boosted_audio.export(output_path, format="mp3")
            
            import os
            os.remove(temp_output)
        except:
            import os
            os.rename(temp_output, output_path)
        
        print(f"🔊 Generated speech: {output_path}")
        return output_path
    
    def _elevenlabs_tts_streaming(self, text: str) -> str:
        """Generate and return streaming audio generator."""
        from elevenlabs import VoiceSettings
        
        voice_settings = VoiceSettings(
            stability=0.7,
            similarity_boost=0.85,
            style=0.4,
            use_speaker_boost=True
        )
        
        # Return the generator directly for streaming
        return elevenlabs_client.text_to_speech.convert_as_stream(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_monolingual_v1",
            voice_settings=voice_settings
        )
    
    def _openai_tts(self, text: str, output_path: str) -> str:
        """Generate speech using OpenAI TTS."""
        response = self.openai_client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=text
        )
        
        response.stream_to_file(output_path)
        print(f"🔊 Generated speech (OpenAI): {output_path}")
        return output_path
    
    def _gtts_tts(self, text: str, output_path: str) -> str:
        """Generate speech using Google TTS (free fallback)."""
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        print(f"🔊 Generated speech (gTTS): {output_path}")
        return output_path
    
    def convert_for_discord(self, audio_path: str) -> str:
        """Convert audio file to Discord-compatible format (PCM).
        
        Args:
            audio_path: Path to input audio file
            
        Returns:
            Path to converted PCM audio file
        """
        # Discord requires: 48kHz, 16-bit, 2 channels (stereo)
        output_path = audio_path.rsplit(".", 1)[0] + "_discord.pcm"
        
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(SAMPLE_RATE)
        audio = audio.set_channels(2)
        audio = audio.set_sample_width(2)  # 16-bit
        
        # Export as raw PCM
        audio.export(output_path, format="s16le", codec="pcm_s16le")
        
        return output_path


# Example usage
if __name__ == "__main__":
    processor = AudioProcessor()
    
    # Test TTS
    print("\n🧪 Testing Text-to-Speech...")
    test_text = "I completely disagree with your premise. Your argument is fundamentally flawed."
    audio_file = processor.text_to_speech(test_text, "test_output.mp3")
    print(f"✅ Generated: {audio_file}")
    
    # Test STT (would need actual audio)
    print("\n🧪 To test Speech-to-Text, run the Discord bot and speak in a voice channel.")


