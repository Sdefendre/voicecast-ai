# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VoiceCast AI is a Python-based tool that converts blog posts and articles into AI-generated podcasts using the Podcastfy library. It supports multiple TTS (Text-to-Speech) providers including OpenAI and ElevenLabs, with configurable voice options and conversation styles.

## Development Commands

### Environment Setup
```bash
# Initial setup (creates venv and installs dependencies)
python setup.py

# Manual virtual environment setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
```bash
# Copy environment template
cp .env.example .env
# Edit .env to add API keys (OPENAI_API_KEY, GEMINI_API_KEY, ELEVENLABS_API_KEY)
```

### Core Operations
```bash
# Generate podcast from URL
python scripts/generate_podcast.py --url "https://example.com/blog-post"

# Generate with specific TTS model
python scripts/generate_podcast.py --url "URL" --tts elevenlabs

# Generate long-form podcast
python scripts/generate_podcast.py --url "URL" --longform

# Batch generate from URL list
python scripts/generate_podcast.py batch urls.txt

# Test installation and generate sample podcast
python examples/test_generation.py

# Check configuration and API key status
python scripts/generate_podcast.py config
```

## Architecture

### Core Components

**Main Script** (`scripts/generate_podcast.py`):
- CLI interface using Typer framework
- Handles URL processing, TTS model selection, and output configuration
- Integrates with Podcastfy library for content conversion
- Supports batch processing and custom prompts

**Setup Script** (`setup.py`):
- Environment verification and virtual environment creation
- Dependency installation with error handling
- API key validation and configuration assistance

**Test Script** (`examples/test_generation.py`):
- Setup verification and health checks
- Sample podcast generation using Wikipedia article
- Environment troubleshooting

### Configuration System

**YAML Configuration** (`config/podcast_config.yaml`):
- Podcast metadata (name, author, description)
- Conversation settings (style, creativity, chunk processing)
- TTS model configurations (OpenAI/ElevenLabs voice options)
- Audio output settings (format, quality, file naming)

**Environment Variables** (`.env`):
- API keys for OpenAI, Gemini, and ElevenLabs
- Default podcast configuration overrides
- TTS model preferences

### Dependencies and Integration

**Core Dependencies**:
- `podcastfy>=0.4.0`: Main podcast generation engine
- `typer>=0.12.5`: CLI framework
- `python-dotenv>=1.0.1`: Environment variable management
- `pydub>=0.25.1`: Audio processing utilities

**AI Services Integration**:
- OpenAI: Script generation and voice synthesis
- Gemini: Alternative script generation
- ElevenLabs: Premium voice synthesis options

### Output Structure

Generated podcasts are saved to `output/` directory with timestamp-based naming (`podcast_YYYYMMDD_HHMMSS.mp3`). The system supports configurable audio formats, bitrates, and file naming patterns through the YAML configuration.

### Error Handling and Validation

The application includes comprehensive error handling for:
- Missing or invalid API keys
- Network connectivity issues during URL processing
- TTS service failures with automatic fallback options
- Output directory creation and file permissions

## Development Notes

### API Key Requirements
At least one API key is required for operation:
- OpenAI API key enables both script generation and basic TTS
- ElevenLabs API key provides premium voice options
- Gemini API key offers alternative script generation

### Conversation Styles
The system supports multiple conversation styles configurable through CLI arguments or YAML configuration:
- Casual, formal, humorous, educational styles
- Custom prompts for specialized content types (tech, business, personal)
- Creativity levels from 0.0 to 1.0 for varied output

### Audio Processing
Generated podcasts support:
- MP3 output format with configurable bitrates
- Optional background music integration
- Adjustable playback speeds and voice parameters
- Cross-platform audio playback integration