"""
Check Python environment and package installations
"""
import sys
import os

print("="*60)
print("🔍 Environment Check")
print("="*60)
print()

print("📍 Python Information:")
print(f"   Version: {sys.version}")
print(f"   Executable: {sys.executable}")
print(f"   Prefix: {sys.prefix}")
print()

print("📦 Checking Packages:")
packages_to_check = [
    "youtube_transcript_api",
    "openai",
    "agents",
    "streamlit",
    "dotenv"
]

for package in packages_to_check:
    try:
        if package == "dotenv":
            import dotenv
            pkg = dotenv
        elif package == "agents":
            import agents
            pkg = agents
        else:
            pkg = __import__(package)
        
        version = getattr(pkg, '__version__', 'unknown')
        location = getattr(pkg, '__file__', 'unknown')
        print(f"   ✅ {package}: {version}")
        print(f"      Location: {location}")
    except ImportError as e:
        print(f"   ❌ {package}: NOT INSTALLED")
        print(f"      Error: {e}")
    print()

print("🧪 Testing YouTubeTranscriptApi:")
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print(f"   ✅ Import successful")
    print(f"   Type: {type(YouTubeTranscriptApi)}")
    
    # Check for get_transcript method
    if hasattr(YouTubeTranscriptApi, 'get_transcript'):
        print(f"   ✅ get_transcript method exists")
    else:
        print(f"   ❌ get_transcript method NOT FOUND")
        print(f"   Available methods: {[m for m in dir(YouTubeTranscriptApi) if not m.startswith('_')]}")
    
    # Try to use it
    print()
    print("   Testing with video ID '6hr6wZr1N_8'...")
    try:
        transcript = YouTubeTranscriptApi.get_transcript("6hr6wZr1N_8")
        print(f"   ✅ Successfully fetched {len(transcript)} transcript entries")
    except Exception as e:
        print(f"   ❌ Error fetching transcript: {e}")
        
except ImportError as e:
    print(f"   ❌ Import failed: {e}")

print()
print("="*60)
print("💡 Recommendations:")
print("="*60)

if sys.prefix == sys.base_prefix:
    print("⚠️  You're NOT in a virtual environment!")
    print("   Activate it with:")
    print("   .venv\\Scripts\\activate  (Windows)")
    print("   source .venv/bin/activate  (macOS/Linux)")
else:
    print("✅ You're in a virtual environment")

print()
print("If packages are missing, install with:")
print("   pip install -r requirements.txt")
print()
print("If youtube-transcript-api has issues:")
print("   pip uninstall youtube-transcript-api")
print("   pip install youtube-transcript-api")
print("="*60)
