"""
Setup script for Content Writer
Checks dependencies and Ollama configuration
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
    except:
        pass
    print("⚠️  Ollama not detected")
    print("   Install from: https://ollama.ai")
    return False

def check_ollama_model():
    """Check if llama3.1:8b is installed"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "llama3.1:8b" in result.stdout or "llama3.1" in result.stdout:
            print("✅ llama3.1:8b model found")
            return True
        else:
            print("⚠️  llama3.1:8b not found")
            print("   Run: ollama pull llama3.1:8b")
            return False
    except:
        print("⚠️  Could not check Ollama models")
        return False

def check_env_file():
    """Check for .env file"""
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file found")
        # Check if it has OpenAI key
        with open(env_path) as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "sk-" in content:
                print("   → Will use OpenAI")
            else:
                print("   → Will use Ollama (no valid OpenAI key)")
        return True
    else:
        print("ℹ️  No .env file (will use Ollama)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ["streamlit", "openai", "agents", "youtube_transcript_api", "dotenv"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Install missing packages:")
        print("   pip install -r requirements.txt")
        return False
    return True

def main():
    print("="*60)
    print("🚗 Content Writer - Setup Check")
    print("="*60)
    print()
    
    print("📦 Python Version:")
    python_ok = check_python_version()
    print()
    
    print("📚 Dependencies:")
    deps_ok = check_dependencies()
    print()
    
    print("🤖 Ollama:")
    ollama_ok = check_ollama()
    if ollama_ok:
        model_ok = check_ollama_model()
    print()
    
    print("⚙️  Configuration:")
    check_env_file()
    print()
    
    print("="*60)
    if python_ok and deps_ok:
        print("✅ Ready to run!")
        print()
        print("Start the app:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Setup incomplete - see messages above")
    print("="*60)

if __name__ == "__main__":
    main()
