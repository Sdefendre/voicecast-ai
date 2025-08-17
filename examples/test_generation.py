#!/usr/bin/env python3
"""
Test script to verify VoiceCast AI setup
Generates a sample podcast from a Wikipedia article
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

def test_setup():
    """Test if the environment is properly configured"""
    print("🧪 Testing VoiceCast AI Setup")
    print("=" * 40)
    
    # Check for API keys
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY')
    }
    
    has_keys = False
    print("\n✔️ Checking API Keys:")
    for key, value in api_keys.items():
        if value:
            print(f"   ✅ {key.replace('_API_KEY', '')} is configured")
            has_keys = True
        else:
            print(f"   ⚠️  {key.replace('_API_KEY', '')} not found")
    
    if not has_keys:
        print("\n❌ No API keys found!")
        print("   Please copy .env.example to .env and add your API keys")
        return False
    
    # Check if podcastfy is installed
    try:
        import podcastfy
        print("\n✅ Podcastfy is installed")
    except ImportError:
        print("\n❌ Podcastfy not installed!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def generate_test_podcast():
    """Generate a test podcast from a sample URL"""
    print("\n🎙️ Generating Test Podcast")
    print("-" * 40)
    
    # Test URL (Wikipedia article about podcasting)
    test_url = "https://en.wikipedia.org/wiki/Podcast"
    
    print(f"📄 Source: {test_url}")
    print("⏳ Generating podcast... (this may take 2-3 minutes)")
    
    try:
        from podcastfy import Podcastfy
        
        # Initialize Podcastfy with minimal config
        podcaster = Podcastfy()
        
        # Generate podcast
        output_file = "output/test_podcast.mp3"
        
        # Create output directory if it doesn't exist
        Path("output").mkdir(exist_ok=True)
        
        # Simple configuration
        config = {
            "output_path": output_file,
            "tts_config": {
                "model": "openai",  # Using OpenAI by default
                "voice": "alloy",
                "speed": 1.0
            }
        }
        
        # Generate the podcast
        result = podcaster.generate_podcast(
            urls=[test_url],
            config=config
        )
        
        print(f"\n✅ Test podcast generated successfully!")
        print(f"📍 Location: {output_file}")
        
        # Check file size
        file_size = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"📊 Size: {file_size:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error generating podcast: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 VoiceCast AI Test Suite")
    print("=" * 50)
    
    # Test setup
    if not test_setup():
        print("\n⚠️  Please fix the setup issues before continuing")
        sys.exit(1)
    
    # Ask if user wants to generate test podcast
    print("\n" + "=" * 50)
    response = input("Would you like to generate a test podcast? (y/n): ")
    
    if response.lower() == 'y':
        if generate_test_podcast():
            print("\n🎉 All tests passed! VoiceCast AI is ready to use.")
            print("\nTry generating your own podcast:")
            print("  python scripts/generate_podcast.py --url 'https://your-blog.com/post'")
        else:
            print("\n⚠️  Test generation failed. Check your API keys and try again.")
    else:
        print("\n✅ Setup verified! You can start generating podcasts.")

if __name__ == "__main__":
    main()
