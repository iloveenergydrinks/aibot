#!/usr/bin/env python3
"""
REAL-TIME STREAMING - Text + Audio

Streams LLM output AND TTS simultaneously like ChatGPT:
1. LLM generates tokens
2. Every 10-15 words → send to TTS
3. Play audio while more text generates
4. Seamless, instant responses!
"""
import requests
import threading
import queue
import subprocess
import tempfile
import time
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import config

client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)


def stream_generate_and_speak(prompt, voice_id, endpoint, token):
    """
    Generate text with streaming LLM and speak it in real-time.
    
    Returns: (full_text, was_interrupted)
    """
    
    # Build messages
    messages = [{"role": "system", "content": prompt["system"]}]
    if "history" in prompt:
        messages.extend(prompt["history"])
    messages.append({"role": "user", "content": prompt["user"]})
    
    # vLLM payload with streaming
    payload = {
        "model": "QuixiAI/WizardLM-13B-Uncensored",
        "messages": messages,
        "max_tokens": 120,
        "temperature": 0.85,
        "stream": True  # STREAMING!
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Start streaming LLM
    response = requests.post(
        endpoint + "/v1/chat/completions",
        json=payload,
        headers=headers,
        stream=True,
        timeout=30
    )
    
    if response.status_code != 200:
        return ("Error generating response", False)
    
    # Queues for audio pipeline
    text_queue = queue.Queue()  # Text chunks to convert to audio
    audio_queue = queue.Queue()  # Audio files ready to play
    
    full_text = ""
    current_chunk = ""
    chunk_size = 8  # Smaller chunks = faster first response
    
    # Flag to stop
    stop_flag = threading.Event()
    interrupted = False
    
    def generate_audio_worker():
        """Worker thread: Convert text chunks to audio."""
        while not stop_flag.is_set():
            try:
                text_chunk = text_queue.get(timeout=0.5)
                if text_chunk == "DONE":
                    audio_queue.put("DONE")
                    break
                
                # Generate audio for this chunk
                voice_settings = VoiceSettings(
                    stability=0.7,
                    similarity_boost=0.85,
                    style=0.4,
                    use_speaker_boost=True
                )
                
                audio_gen = client.text_to_speech.convert(
                    text=text_chunk,
                    voice_id=voice_id,
                    model_id="eleven_monolingual_v1",
                    voice_settings=voice_settings
                )
                
                # Save chunk
                temp_file = tempfile.mktemp(suffix=".mp3")
                with open(temp_file, "wb") as f:
                    for chunk in audio_gen:
                        f.write(chunk)
                
                # Add to audio queue
                audio_queue.put(temp_file)
                
            except queue.Empty:
                continue
    
    def play_audio_worker():
        """Worker thread: Play audio chunks as they're ready."""
        nonlocal interrupted
        first_chunk = True
        
        while not stop_flag.is_set():
            try:
                audio_file = audio_queue.get(timeout=0.5)
                if audio_file == "DONE":
                    break
                
                # Play this chunk
                if first_chunk:
                    print(f"🔊 Starting playback (first chunk)...")
                    first_chunk = False
                
                subprocess.run(["afplay", audio_file])
                
                # Clean up
                import os
                os.remove(audio_file)
                
            except queue.Empty:
                continue
    
    # Start worker threads
    audio_gen_thread = threading.Thread(target=generate_audio_worker, daemon=True)
    audio_play_thread = threading.Thread(target=play_audio_worker, daemon=True)
    
    audio_gen_thread.start()
    audio_play_thread.start()
    
    # Stream tokens from LLM
    print("⚡ Streaming: ", end='', flush=True)
    
    for line in response.iter_lines():
        if not line:
            continue
        
        line_str = line.decode('utf-8')
        
        if line_str.startswith('data: '):
            line_str = line_str[6:]
        
        if line_str.strip() == '[DONE]':
            break
        
        try:
            import json
            chunk_data = json.loads(line_str)
            
            if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                delta = chunk_data["choices"][0].get("delta", {})
                content = delta.get("content", "")
                
                if content:
                    full_text += content
                    current_chunk += content
                    print(content, end='', flush=True)
                    
                    # When we have enough words OR hit punctuation, send to audio
                    word_count = len(current_chunk.split())
                    # Send smaller chunks faster!
                    if word_count >= chunk_size or any(p in content for p in ['. ', '! ', '? ', '\n']):
                        if current_chunk.strip():
                            text_queue.put(current_chunk.strip())
                            print(f" [{word_count}w→TTS] ", end='', flush=True)
                            current_chunk = ""
        except:
            pass
    
    print()  # New line
    
    # Send remaining text
    if current_chunk.strip():
        text_queue.put(current_chunk.strip())
    
    # Signal done
    text_queue.put("DONE")
    
    # Wait for audio to finish
    audio_gen_thread.join(timeout=30)
    audio_play_thread.join(timeout=30)
    
    return (full_text, interrupted)


# Test
if __name__ == "__main__":
    prompt = {
        "system": "You are Hitler. Be aggressive.",
        "user": "What about democracy?"
    }
    
    print("\n🧪 Testing REAL-TIME streaming...\n")
    print("Text will stream AND audio will play as it generates!\n")
    
    text, interrupted = stream_generate_and_speak(
        prompt,
        config.ELEVENLABS_VOICE_ID,
        config.CUSTOM_LLM_ENDPOINT,
        config.HUGGINGFACE_API_TOKEN
    )
    
    print(f"\n\n✅ Done! Total: {len(text.split())} words")

