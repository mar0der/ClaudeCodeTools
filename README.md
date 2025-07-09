# Claude Code Tools

A collection of external tools designed to enhance Claude Code CLI capabilities through hooks and integrations.

## Overview

This repository contains tools that extend Claude Code's functionality, particularly through the hooks system. Each tool is designed to work seamlessly with Claude Code's workflow while providing additional capabilities.

## Available Tools

### 🔊 Text-to-Speech (TTS)
**Location**: `tools/tts/`

A combined TTS solution that provides high-quality speech synthesis with automatic fallback.

**Features**:
- Microsoft Aria Neural voice (online)
- macOS native voices (offline fallback)
- Automatic internet detection
- Perfect for Claude Code hooks

**Quick Start**:
```bash
cd tools/tts
pip install edge-tts pyobjc-framework-AVFoundation
python3 tts.py "Hello from Claude Code"
```

## Installation

### Prerequisites
- Python 3.7+
- macOS (for TTS fallback voices)
- Claude Code CLI

### Clone Repository
```bash
git clone https://github.com/petarpetkov/ClaudeCodeTools.git
cd ClaudeCodeTools
```

### Install Individual Tools
Each tool has its own installation instructions in its respective README file.

## Claude Code Integration

### Using with Hooks

Add tools to your Claude Code hooks configuration:

```json
{
  "post_tool": "python3 /path/to/ClaudeCodeTools/tools/tts/tts.py 'Task completed'",
  "pre_tool": "python3 /path/to/ClaudeCodeTools/tools/tts/tts.py 'Starting task'"
}
```

### CLAUDE.md Integration

Update your project's `CLAUDE.md` file to include tool information:

```markdown
## Available Tools

### TTS Notifications
- **Script**: `python3 /path/to/ClaudeCodeTools/tools/tts/tts.py "message"`
- **Purpose**: Audio notifications for task completion
```

## Development

### Project Structure
```
ClaudeCodeTools/
├── README.md
├── CLAUDE.md
├── tools/
│   └── tts/
│       ├── README.md
│       └── tts.py
```

### Adding New Tools

1. Create a new directory in `tools/`
2. Add your tool script(s)
3. Include a README.md with installation and usage instructions
4. Update the main README.md to list your tool

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tool with proper documentation
4. Submit a pull request

## Future Tools

Planned additions:
- File monitoring tools
- Notification systems
- Integration helpers
- Development workflow tools

## Requirements

- Python 3.7+
- macOS (for TTS tools)
- Internet connection (for cloud-based features)

## License

MIT License - see individual tool directories for specific licensing information.

## Support

For issues and questions:
- Check individual tool README files
- Open an issue on GitHub
- Refer to Claude Code documentation