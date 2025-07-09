# Speech-to-Text (STT) Tool

A combined speech-to-text solution with local Whisper inference and online API fallback.

## Features

- **Primary**: OpenAI Whisper local inference (tiny model for 2GB RAM)
- **Fallback**: AssemblyAI free online API (5 hours/month)
- **Recording**: Built-in audio recording with configurable duration
- **Live Mode**: Real-time transcription with space bar controls
- **File Processing**: Transcribe existing audio files

## Installation

### Prerequisites

- Python 3.7+
- Microphone access
- 2GB+ RAM recommended

### Install Dependencies

```bash
pip install openai-whisper pyaudio assemblyai keyboard
```

### macOS Additional Setup

```bash
# Install portaudio for pyaudio
brew install portaudio
```

### Get Free API Key (Optional)

For online fallback, get a free AssemblyAI API key:
1. Visit https://www.assemblyai.com/
2. Sign up for free account (5 hours/month)
3. Get your API key from dashboard

```bash
export ASSEMBLYAI_API_KEY=your_key_here
```

## Usage

### Quick Recording

```bash
# Record for 5 seconds and transcribe
python3 stt.py --record 5

# Record for 10 seconds
python3 stt.py --record 10
```

### Transcribe Audio File

```bash
# Transcribe existing audio file
python3 stt.py audio.wav
python3 stt.py recording.mp3
```

### Live Transcription

```bash
# Interactive live transcription
python3 stt.py --live

# Controls in live mode:
# - Press SPACE to start/stop recording
# - Press 'q' to quit
```

### Model Information

```bash
# List available Whisper models
python3 stt.py --models
```

## Whisper Models (Local)

| Model | Size | VRAM | Quality | Speed |
|-------|------|------|---------|-------|
| tiny  | ~40MB | Low | Good | Fastest |
| base  | ~150MB | Low | Better | Fast |
| small | ~500MB | Medium | High | Medium |
| medium | ~1.5GB | High | Higher | Slow |
| large | ~3GB | Very High | Best | Slowest |

**Recommended for 2GB RAM**: `tiny` or `base` models

## Claude Code Integration

### Voice Commands Hook

Add to your Claude Code hooks:

```json
{
  "pre_tool": "python3 /path/to/tools/stt/stt.py --record 3 > /tmp/voice_command.txt"
}
```

### Interactive Voice Input

```bash
# Record voice input for Claude
python3 stt.py --record 5 && cat transcription.txt
```

## Technical Details

### Audio Settings
- **Sample Rate**: 16kHz (optimal for Whisper)
- **Channels**: Mono
- **Format**: 16-bit PCM
- **Chunk Size**: 1024 samples

### Fallback Logic
1. **Local Whisper**: Tries tiny model first (fast, good quality)
2. **Online AssemblyAI**: Falls back if Whisper fails or unavailable
3. **Error Handling**: Graceful degradation with informative messages

### Supported Audio Formats
- WAV (recommended)
- MP3
- FLAC
- M4A
- OGG

## Performance

### Local Whisper (M4 Mac)
- **Tiny Model**: ~1-2 seconds for 5-second audio
- **Base Model**: ~2-4 seconds for 5-second audio
- **Memory Usage**: 200-800MB depending on model

### Online AssemblyAI
- **Latency**: 3-10 seconds depending on connection
- **Accuracy**: Very high for clear speech
- **Rate Limits**: 5 hours/month (free tier)

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   ```bash
   # macOS
   brew install portaudio
   pip install pyaudio
   
   # Linux
   sudo apt-get install portaudio19-dev
   pip install pyaudio
   ```

2. **"Permission denied" (microphone)**
   - Check System Preferences > Security & Privacy > Microphone
   - Grant access to Terminal/iTerm

3. **"AssemblyAI API key not found"**
   ```bash
   export ASSEMBLYAI_API_KEY=your_key_here
   ```

4. **Poor transcription quality**
   - Ensure quiet environment
   - Speak clearly into microphone
   - Try different Whisper model sizes

### Testing Setup

```bash
# Test microphone recording
python3 stt.py --record 3

# Test with existing audio
python3 stt.py test_audio.wav

# Test live mode
python3 stt.py --live
```

## Examples

### Basic Voice Note

```bash
python3 stt.py --record 10
# Speak your message for 10 seconds
# Output: "📝 Transcription: Your spoken message here"
```

### File Processing

```bash
python3 stt.py meeting_recording.mp3
# Output: "📝 Transcription: [Full meeting transcription]"
```

### Live Dictation

```bash
python3 stt.py --live
# Press SPACE, speak, press SPACE again to stop
# Repeat for continuous dictation
```