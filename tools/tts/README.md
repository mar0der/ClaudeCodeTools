# Text-to-Speech (TTS) Tool

A combined TTS solution that provides high-quality speech synthesis with automatic fallback.

## Features

- **Primary**: Microsoft Aria Neural voice (requires internet)
- **Fallback**: macOS native voices (works offline)
- **Automatic detection**: Seamlessly switches based on internet connectivity
- **Voice selection**: Choose specific fallback voices by number

## Installation

### Prerequisites

- Python 3.7+
- macOS (for fallback voices)

### Install Dependencies

```bash
pip install edge-tts pyobjc-framework-AVFoundation
```

## Usage

### Basic Usage

```bash
# Use best available voice (Aria Neural if online, Daniel if offline)
python3 tts.py "Hello, this is a test message"
```

### Voice Selection

```bash
# List all available fallback voices
python3 tts.py --list-voices

# Use specific fallback voice (if offline)
python3 tts.py "Hello Peter" 12
```

### Claude Code Hook Integration

Add to your Claude Code hooks configuration:

```json
{
  "post_tool": "python3 /path/to/tools/tts/tts.py 'Task completed'"
}
```

## Voice Quality

- **Microsoft Aria Neural**: High-quality neural voice, natural and expressive
- **macOS Fallback**: Standard system voices, Daniel (British) is the default fallback
- **Automatic Switching**: Always uses the best available option

## Technical Details

- Internet connectivity is checked by attempting connection to `speech.platform.bing.com`
- Audio files are temporarily stored in `/tmp/` and automatically cleaned up
- Uses `afplay` on macOS for audio playback
- Fallback voices use Apple's AVSpeechSynthesizer framework

## Troubleshooting

### Common Issues

1. **"Edge TTS not available"**: Install with `pip install edge-tts`
2. **"No internet connection"**: Normal behavior, will use macOS fallback
3. **No sound**: Check system volume and audio output device

### Testing Internet Connectivity

```bash
# Test with internet
python3 tts.py "Testing online voice"

# Test fallback (disconnect internet first)
python3 tts.py "Testing offline voice"
```