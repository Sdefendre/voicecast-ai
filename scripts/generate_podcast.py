#!/usr/bin/env python3
"""
Main podcast generation script for VoiceCast AI
Converts blog posts to podcasts using Podcastfy
"""

import os
import sys
import typer
from pathlib import Path
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = typer.Typer()

def setup_environment():
    """Verify environment setup and API keys"""
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY')
    }
    
    # Check if at least one API key is present
    if not any(api_keys.values()):
        typer.echo("❌ No API keys found! Please set up your .env file.")
        typer.echo("   Copy .env.example to .env and add your API keys.")
        raise typer.Exit(1)
    
    # Show which services are available
    typer.echo("✅ Available services:")
    for key, value in api_keys.items():
        if value:
            service = key.replace('_API_KEY', '')
            typer.echo(f"   - {service}")
    
    return api_keys

@app.command()
def generate(
    url: str = typer.Argument(..., help="URL of the blog post to convert"),
    tts_model: str = typer.Option("openai", "--tts", help="TTS model: openai or elevenlabs"),
    longform: bool = typer.Option(False, "--longform", help="Generate longer podcast format"),
    output_dir: str = typer.Option("output", "--output", help="Output directory for podcast"),
    conversation_style: Optional[str] = typer.Option(None, "--style", help="Conversation style"),
    custom_prompt: Optional[str] = typer.Option(None, "--prompt", help="Custom prompt for generation")
):
    """
    Generate a podcast from a blog post URL
    """
    typer.echo(f"🎙️ VoiceCast AI - Podcast Generator")
    typer.echo(f"=" * 40)
    
    # Setup environment
    api_keys = setup_environment()
    
    # Validate TTS model
    if tts_model == "elevenlabs" and not api_keys['ELEVENLABS_API_KEY']:
        typer.echo("⚠️  ElevenLabs API key not found, falling back to OpenAI")
        tts_model = "openai"
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    typer.echo(f"\n📄 Source: {url}")
    typer.echo(f"🎤 Voice Model: {tts_model}")
    typer.echo(f"📝 Format: {'Long-form' if longform else 'Standard'}")
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_path / f"podcast_{timestamp}.mp3"
    
    try:
        # Import podcastfy here to avoid import errors if not installed
        from podcastfy import Podcastfy
        
        typer.echo(f"\n⏳ Generating podcast... (this may take a few minutes)")
        
        # Initialize Podcastfy
        podcaster = Podcastfy()
        
        # Build configuration
        config = {
            "conversation_config": {
                "creativity": 0.7,
                "max_num_chunks": 10 if longform else 5,
            },
            "tts_config": {
                "model": tts_model,
                "voice": "alloy" if tts_model == "openai" else "Rachel",
                "speed": 1.0,
            },
            "output_path": str(output_file)
        }
        
        if conversation_style:
            config["conversation_config"]["conversation_style"] = conversation_style
        
        if custom_prompt:
            config["conversation_config"]["custom_prompt"] = custom_prompt
        
        # Generate the podcast
        result = podcaster.generate_podcast(
            urls=[url],
            config=config
        )
        
        typer.echo(f"\n✅ Podcast generated successfully!")
        typer.echo(f"📍 Location: {output_file}")
        typer.echo(f"📊 Size: {output_file.stat().st_size / (1024*1024):.2f} MB")
        
        # Play prompt (optional)
        if typer.confirm("\n🎧 Would you like to play the podcast now?"):
            if sys.platform == "darwin":  # macOS
                os.system(f"open {output_file}")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {output_file}")
            else:  # Linux
                os.system(f"xdg-open {output_file}")
        
    except ImportError:
        typer.echo("\n❌ Podcastfy not installed! Please run:")
        typer.echo("   pip install -r requirements.txt")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"\n❌ Error generating podcast: {e}")
        raise typer.Exit(1)

@app.command()
def batch(
    urls_file: str = typer.Argument(..., help="Text file containing URLs (one per line)"),
    tts_model: str = typer.Option("openai", "--tts", help="TTS model: openai or elevenlabs"),
    output_dir: str = typer.Option("output", "--output", help="Output directory for podcasts")
):
    """
    Generate podcasts from multiple URLs listed in a file
    """
    typer.echo(f"🎙️ Batch Podcast Generation")
    
    # Read URLs from file
    try:
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        typer.echo(f"❌ File not found: {urls_file}")
        raise typer.Exit(1)
    
    typer.echo(f"📋 Found {len(urls)} URLs to process")
    
    # Process each URL
    for i, url in enumerate(urls, 1):
        typer.echo(f"\n[{i}/{len(urls)}] Processing: {url}")
        generate(url, tts_model=tts_model, output_dir=output_dir)

@app.command()
def config():
    """
    Show current configuration and API key status
    """
    typer.echo("🔧 VoiceCast AI Configuration")
    typer.echo("=" * 40)
    
    # Check API keys
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY')
    }
    
    typer.echo("\nAPI Keys Status:")
    for key, value in api_keys.items():
        status = "✅ Configured" if value else "❌ Not set"
        service = key.replace('_API_KEY', '')
        typer.echo(f"  {service}: {status}")
    
    # Show other config
    typer.echo(f"\nDefault Settings:")
    typer.echo(f"  Podcast Name: {os.getenv('PODCAST_NAME', 'VoiceCast AI Podcast')}")
    typer.echo(f"  Author: {os.getenv('PODCAST_AUTHOR', 'Not set')}")
    typer.echo(f"  Default TTS: {os.getenv('DEFAULT_TTS_MODEL', 'openai')}")

if __name__ == "__main__":
    app()
