#!/usr/bin/env python3
"""
Combined TTS script for Claude Code hooks
- Primary: Microsoft Edge TTS (Aria Neural voice)
- Fallback: macOS native voices (Daniel - voice #7)

Usage: 
  python tts.py "Your message here"
  python tts.py "Your message here" 7
  python tts.py --list-voices

Requirements: 
  pip install edge-tts pyobjc-framework-AVFoundation
"""

import sys
import time
import asyncio
import subprocess
import platform
import os
import socket
from AVFoundation import AVSpeechSynthesizer, AVSpeechUtterance, AVSpeechSynthesisVoice

class CombinedTTS:
    def __init__(self):
        self.synthesizer = AVSpeechSynthesizer.alloc().init()
        self.finished = False
        
    def check_internet(self):
        """Check if internet connection is available"""
        try:
            # Try to connect to Microsoft's server
            socket.create_connection(("speech.platform.bing.com", 443), timeout=3)
            return True
        except OSError:
            return False
    
    def speak_with_edge_tts(self, message):
        """Use Microsoft Edge TTS with Aria Neural voice"""
        try:
            import edge_tts
            
            # Use Aria Neural voice (high quality US female)
            voice = "en-US-AriaNeural"
            
            async def generate_speech():
                output_file = "/tmp/claude_tts_output.mp3"
                
                # Generate speech
                communicate = edge_tts.Communicate(message, voice)
                await communicate.save(output_file)
                
                # Play the audio file
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(["afplay", output_file], check=True)
                elif platform.system() == "Linux":
                    subprocess.run(["mpg123", output_file], check=True)
                
                # Clean up
                os.remove(output_file)
            
            # Run the async function
            asyncio.run(generate_speech())
            return True
            
        except ImportError:
            print("Edge TTS not available. Install with: pip install edge-tts")
            return False
        except Exception as e:
            print(f"Edge TTS error: {e}")
            return False
    
    def get_voices(self):
        """Get all available macOS voices"""
        voices = AVSpeechSynthesisVoice.speechVoices()
        english_voices = []
        
        for voice in voices:
            if voice.language().startswith('en'):
                english_voices.append({
                    'name': voice.name(),
                    'language': voice.language(),
                    'identifier': voice.identifier(),
                    'quality': voice.quality()
                })
        
        return english_voices
    
    def list_voices(self):
        """List all available English voices with numbers"""
        voices = self.get_voices()
        print("Available macOS voices (fallback):")
        print("-" * 50)
        
        for i, voice in enumerate(voices, 1):
            quality = "Premium" if voice['quality'] == 2 else "Standard"
            marker = " <- DEFAULT FALLBACK" if i == 7 else ""
            print(f"{i:2d}. {voice['name']} ({voice['language']}) - {quality}{marker}")
        
        print("\\nPrimary voice: Microsoft Aria Neural (requires internet)")
        return voices
    
    def speak_with_macos(self, message, voice_index=7):
        """Speak using macOS native voices"""
        voices = self.get_voices()
        
        if 1 <= voice_index <= len(voices):
            selected_voice = voices[voice_index - 1]
            voice_id = selected_voice['identifier']
            print(f"Using macOS voice: {selected_voice['name']}")
        else:
            print(f"Invalid voice index. Using Daniel (voice 7)")
            voice_id = voices[6]['identifier']  # Daniel is voice 7 (index 6)
        
        # Create utterance
        utterance = AVSpeechUtterance.speechUtteranceWithString_(message)
        voice = AVSpeechSynthesisVoice.voiceWithIdentifier_(voice_id)
        utterance.setVoice_(voice)
        
        # Set speech parameters
        utterance.setRate_(0.5)  # Normal speed
        utterance.setPitchMultiplier_(1.0)  # Normal pitch
        utterance.setVolume_(1.0)  # Full volume
        
        # Start speaking
        self.synthesizer.speakUtterance_(utterance)
        
        # Wait for completion
        while self.synthesizer.isSpeaking():
            time.sleep(0.1)
        
        return True
    
    def speak(self, message, voice_index=None):
        """Main speak function - tries Edge TTS first, falls back to macOS"""
        # Check internet connectivity
        if self.check_internet():
            print("Internet available - using Microsoft Aria Neural voice")
            if self.speak_with_edge_tts(message):
                return True
            else:
                print("Edge TTS failed, falling back to macOS voice")
        else:
            print("No internet connection - using macOS fallback voice")
        
        # Fallback to macOS voice
        fallback_voice = voice_index if voice_index else 7  # Default to Daniel
        return self.speak_with_macos(message, fallback_voice)

def main():
    tts = CombinedTTS()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tts.py \"Your message here\"")
        print("  python tts.py \"Your message here\" 7")
        print("  python tts.py --list-voices")
        print()
        print("Primary: Microsoft Aria Neural (requires internet)")
        print("Fallback: macOS Daniel voice (voice #7)")
        sys.exit(1)
    
    # List voices
    if sys.argv[1] == "--list-voices":
        tts.list_voices()
        sys.exit(0)
    
    # Get message
    message = sys.argv[1]
    
    # Get voice index if provided (for fallback only)
    voice_index = None
    if len(sys.argv) > 2:
        try:
            voice_index = int(sys.argv[2])
        except ValueError:
            print("Voice index must be a number")
            sys.exit(1)
    
    # Speak the message
    if not tts.speak(message, voice_index):
        sys.exit(1)

if __name__ == "__main__":
    main()