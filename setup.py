#!/usr/bin/env python3
"""
Setup script for VoiceCast AI
Helps configure the environment and verify installation
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Create and setup virtual environment"""
    print_header("Setting up Virtual Environment")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
    else:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created")
    
    # Provide activation instructions
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"\n📌 To activate the virtual environment, run:")
    print(f"   {activate_cmd}")
    
    return True

def install_dependencies():
    """Install required Python packages"""
    print_header("Installing Dependencies")
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  Virtual environment not activated!")
        print("   Please activate it first and run this script again")
        return False
    
    print("Installing packages from requirements.txt...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_env_file():
    """Create .env file from template"""
    print_header("Setting up Environment Variables")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        print("   Make sure to add your API keys if you haven't already")
    else:
        if env_example.exists():
            # Copy .env.example to .env
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
            print("\n⚠️  IMPORTANT: Edit .env and add your API keys:")
            print("   - OPENAI_API_KEY for OpenAI")
            print("   - ELEVENLABS_API_KEY for ElevenLabs (optional)")
        else:
            print("❌ .env.example not found")
            return False
    
    return True

def verify_api_keys():
    """Check if API keys are configured"""
    print_header("Checking API Keys")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY')
    }
    
    configured = []
    missing = []
    
    for key, value in api_keys.items():
        service = key.replace('_API_KEY', '')
        if value and value != f"your_{service.lower()}_key_here":
            configured.append(service)
            print(f"✅ {service} API key configured")
        else:
            missing.append(service)
            print(f"⚠️  {service} API key not configured")
    
    if not configured:
        print("\n❌ No API keys configured!")
        print("   You need at least one API key to use VoiceCast AI")
        print("\n   Get your API keys from:")
        print("   - OpenAI: https://platform.openai.com/api-keys")
        print("   - ElevenLabs: https://elevenlabs.io")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 VoiceCast AI Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        sys.exit(1)
    
    # Check if in virtual environment for dependency installation
    if sys.prefix != sys.base_prefix:
        # Install dependencies
        if not install_dependencies():
            sys.exit(1)
    else:
        print("\n⚠️  Please activate the virtual environment and run this script again to install dependencies")
    
    # Setup .env file
    if not setup_env_file():
        sys.exit(1)
    
    # Verify API keys
    if sys.prefix != sys.base_prefix:
        verify_api_keys()
    
    print_header("Setup Complete!")
    print("\n📋 Next steps:")
    print("1. If not done, activate virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Add your API keys to .env file")
    print("3. Run the test script:")
    print("   python examples/test_generation.py")
    print("4. Generate your first podcast:")
    print("   python scripts/generate_podcast.py --url 'https://your-blog.com/post'")
    print("\nHappy podcasting! 🎙️")

if __name__ == "__main__":
    main()
