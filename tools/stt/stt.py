#!/usr/bin/env python3
"""
Speech-to-Text (STT) tool for Claude Code hooks
- Primary: OpenAI Whisper local inference (tiny model for 2GB RAM)
- Fallback: AssemblyAI free online API

Usage:
  python stt.py --record 5    # Record 5 seconds and transcribe
  python stt.py audio.wav     # Transcribe existing audio file
  python stt.py --live        # Live transcription (press space to record)

Requirements:
  pip install openai-whisper pyaudio assemblyai
"""

import sys
import os
import time
import wave
import threading
import tempfile
import platform
import subprocess
from pathlib import Path

try:
    import pyaudio
    import whisper
    import assemblyai as aai
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install openai-whisper pyaudio assemblyai")
    sys.exit(1)

class SpeechToText:
    def __init__(self):
        self.whisper_model = None
        self.recording = False
        self.frames = []
        
        # AssemblyAI API key (free tier: 5 hours/month)
        # You can get a free API key at https://www.assemblyai.com/
        self.assemblyai_key = None  # Set this or use environment variable
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
    def load_whisper_model(self, model_size="tiny"):
        """Load Whisper model for local inference"""
        try:
            print(f"Loading Whisper {model_size} model...")
            self.whisper_model = whisper.load_model(model_size)
            print(f"Whisper {model_size} model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            return False
    
    def transcribe_with_whisper(self, audio_file):
        """Transcribe using local Whisper model"""
        if not self.whisper_model:
            if not self.load_whisper_model("tiny"):
                return None
        
        try:
            print("Transcribing with Whisper (local)...")
            result = self.whisper_model.transcribe(audio_file)
            return result["text"].strip()
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return None
    
    def transcribe_with_assemblyai(self, audio_file):
        """Transcribe using AssemblyAI online API"""
        try:
            # Try to get API key from environment or instance variable
            api_key = self.assemblyai_key or os.getenv('ASSEMBLYAI_API_KEY')
            
            if not api_key:
                print("AssemblyAI API key not found. Set ASSEMBLYAI_API_KEY environment variable.")
                print("Get free API key at: https://www.assemblyai.com/")
                return None
            
            print("Transcribing with AssemblyAI (online)...")
            aai.settings.api_key = api_key
            
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file)
            
            if transcript.status == aai.TranscriptStatus.error:
                print(f"AssemblyAI error: {transcript.error}")
                return None
            
            return transcript.text
            
        except Exception as e:
            print(f"AssemblyAI transcription error: {e}")
            return None
    
    def record_audio(self, duration=5, output_file=None):
        """Record audio for specified duration"""
        if output_file is None:
            output_file = tempfile.mktemp(suffix='.wav')
        
        try:
            audio = pyaudio.PyAudio()
            
            # Open stream
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print(f"Recording for {duration} seconds...")
            self.frames = []
            
            for i in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                self.frames.append(data)
            
            print("Recording finished")
            
            # Stop recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            # Save audio file
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            
            return output_file
            
        except Exception as e:
            print(f"Recording error: {e}")
            return None
    
    def transcribe_file(self, audio_file):
        """Transcribe audio file with fallback options"""
        if not os.path.exists(audio_file):
            print(f"Audio file not found: {audio_file}")
            return None
        
        # Try Whisper first (local)
        text = self.transcribe_with_whisper(audio_file)
        if text:
            print("✅ Transcribed with Whisper (local)")
            return text
        
        # Fallback to AssemblyAI (online)
        text = self.transcribe_with_assemblyai(audio_file)
        if text:
            print("✅ Transcribed with AssemblyAI (online)")
            return text
        
        print("❌ All transcription methods failed")
        return None
    
    def live_transcription(self):
        """Live transcription with space bar to record"""
        print("Live transcription mode:")
        print("- Press SPACE to start/stop recording")
        print("- Press 'q' to quit")
        print("- Each recording will be transcribed automatically")
        
        try:
            import keyboard
        except ImportError:
            print("keyboard library not installed. Install with: pip install keyboard")
            return
        
        recording_count = 0
        
        while True:
            print("\\nPress SPACE to record, 'q' to quit...")
            
            # Wait for space or q
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'space':
                    recording_count += 1
                    temp_file = f"/tmp/recording_{recording_count}.wav"
                    
                    print("Recording... Press SPACE again to stop")
                    self.start_recording()
                    
                    # Wait for space again to stop
                    while True:
                        event = keyboard.read_event()
                        if event.event_type == keyboard.KEY_DOWN and event.name == 'space':
                            break
                    
                    audio_file = self.stop_recording(temp_file)
                    if audio_file:
                        text = self.transcribe_file(audio_file)
                        if text:
                            print(f"\\n📝 Transcription: {text}")
                        
                        # Clean up temp file
                        try:
                            os.remove(audio_file)
                        except:
                            pass
                
                elif event.name == 'q':
                    print("Exiting live transcription...")
                    break
    
    def start_recording(self):
        """Start recording in background thread"""
        self.recording = True
        self.frames = []
        
        def record_thread():
            try:
                audio = pyaudio.PyAudio()
                stream = audio.open(
                    format=self.format,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    frames_per_buffer=self.chunk_size
                )
                
                while self.recording:
                    data = stream.read(self.chunk_size)
                    self.frames.append(data)
                
                stream.stop_stream()
                stream.close()
                audio.terminate()
                
            except Exception as e:
                print(f"Recording thread error: {e}")
        
        self.record_thread = threading.Thread(target=record_thread)
        self.record_thread.start()
    
    def stop_recording(self, output_file):
        """Stop recording and save file"""
        self.recording = False
        if hasattr(self, 'record_thread'):
            self.record_thread.join()
        
        if not self.frames:
            print("No audio recorded")
            return None
        
        try:
            # Save audio file
            audio = pyaudio.PyAudio()
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(self.frames))
            audio.terminate()
            
            return output_file
            
        except Exception as e:
            print(f"Error saving recording: {e}")
            return None

def main():
    stt = SpeechToText()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python stt.py --record 5        # Record 5 seconds")
        print("  python stt.py audio.wav         # Transcribe file")
        print("  python stt.py --live            # Live transcription")
        print("  python stt.py --models          # List available models")
        print()
        print("Setup:")
        print("  export ASSEMBLYAI_API_KEY=your_key_here")
        print("  Get free key at: https://www.assemblyai.com/")
        sys.exit(1)
    
    if sys.argv[1] == "--models":
        print("Available Whisper models (local):")
        print("  tiny   - ~40MB VRAM, fastest")
        print("  base   - ~150MB VRAM, good quality")
        print("  small  - ~500MB VRAM, better quality")
        print("  medium - ~1.5GB VRAM, high quality")
        print("  large  - ~3GB VRAM, best quality")
        sys.exit(0)
    
    elif sys.argv[1] == "--record":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        temp_file = tempfile.mktemp(suffix='.wav')
        
        audio_file = stt.record_audio(duration, temp_file)
        if audio_file:
            text = stt.transcribe_file(audio_file)
            if text:
                print(f"\\n📝 Transcription: {text}")
            
            # Clean up
            try:
                os.remove(audio_file)
            except:
                pass
    
    elif sys.argv[1] == "--live":
        stt.live_transcription()
    
    else:
        # Transcribe existing file
        audio_file = sys.argv[1]
        text = stt.transcribe_file(audio_file)
        if text:
            print(f"\\n📝 Transcription: {text}")

if __name__ == "__main__":
    main()