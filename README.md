# VoiceCast AI

🎙️ Transform your blog posts into engaging podcasts using AI-powered voice synthesis.

## Overview

VoiceCast AI is a local podcast generation tool that converts blog posts and articles into professional-sounding podcasts using Podcastfy. Perfect for content creators who want to repurpose their written content into audio format.

## Features

- 🔄 Convert any blog post URL to podcast
- 🎭 Multiple voice options (OpenAI, ElevenLabs)
- 📝 Automatic script generation
- 🎵 Background music support
- 🌐 Works with any public blog/article URL
- 💻 Runs completely locally

## Quick Start

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Sdefendre/voicecast-ai.git
cd voicecast-ai
```

2. Set up Python environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Usage

Generate a podcast from any URL:
```bash
python scripts/generate_podcast.py --url "https://your-blog-post.com"
```

Or use the quick test:
```bash
python examples/test_generation.py
```

## API Keys Required

You'll need at least one of these:
- **OpenAI API Key**: For script generation and voice synthesis
- **ElevenLabs API Key**: For premium voice quality (optional)

Get your keys:
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs: https://elevenlabs.io

## Project Structure

```
voicecast-ai/
├── config/             # Configuration files
├── scripts/            # Main generation scripts
├── examples/           # Example usage scripts
├── output/             # Generated podcasts
└── requirements.txt    # Python dependencies
```

## Examples

### Basic podcast generation:
```python
python scripts/generate_podcast.py --url "https://example.com/blog-post"
```

### With custom voice:
```python
python scripts/generate_podcast.py --url "https://example.com/blog-post" --tts elevenlabs
```

### Long-form content:
```python
python scripts/generate_podcast.py --url "https://example.com/blog-post" --longform
```

## License

MIT License - See LICENSE file for details

## Contributing

Pull requests are welcome! For major changes, please open an issue first.

## Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using [Podcastfy](https://github.com/souzatharsis/podcastfy)
