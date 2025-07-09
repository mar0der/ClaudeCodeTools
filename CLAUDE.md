# CLAUDE.md

External tools to enhance Claude Code CLI capabilities.

## Available Tools

### Text-to-Speech (TTS)
- **Script**: `tools/tts/tts.py`
- **Usage**: `python3 tools/tts/tts.py "message"`
- **Features**: Microsoft Aria Neural voice (online) + macOS fallback (offline)

### Speech-to-Text (STT)
- **Script**: `tools/stt/stt.py`
- **Usage**: `python3 tools/stt/stt.py --record 5`
- **Features**: Local Whisper tiny model + AssemblyAI fallback

## Quick Commands

```bash
# TTS
python3 tools/tts/tts.py "Hello Peter"

# STT
python3 tools/stt/stt.py --record 5
python3 tools/stt/stt.py audio.wav
python3 tools/stt/stt.py --live
```