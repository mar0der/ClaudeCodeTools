# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

Repository for exploring Claude Code CLI capabilities and developing external tools to enhance its functionality.

## Available Tools

### Text-to-Speech (TTS)
- **Location**: `tools/tts/tts.py`
- **Usage**: `python3 tools/tts/tts.py "Your message here"`
- **Purpose**: High-quality TTS with Microsoft Aria Neural voice (online) and macOS fallback (offline)
- **Installation**: `pip install edge-tts pyobjc-framework-AVFoundation`
- **Hook Integration**: Perfect for Claude Code hooks to provide audio notifications

## Development Commands

### TTS Tool Testing
- `python3 tools/tts/tts.py --list-voices` - List available voices
- `python3 tools/tts/tts.py "test message"` - Test TTS functionality
- `python3 tools/tts/tts.py "test message" 7` - Test with specific fallback voice

## Architecture Overview

### Project Structure
```
tools/
├── tts/
│   ├── README.md
│   └── tts.py
```

Each tool is self-contained in its own directory with installation instructions and documentation.