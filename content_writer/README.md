# 🚗 Content Writer - Hybrid AI Content Generator

An intelligent content generation tool for **audispot254** that creates platform-specific social media posts from YouTube automotive videos. Features **automatic provider switching** between OpenAI and local Ollama models.

## ✨ Key Features

### 🤖 Hybrid AI Provider
- **Smart Auto-Detection**: Uses OpenAI if API key exists, automatically falls back to Ollama
- **No Manual Switching**: Zero configuration needed - just works!
- **Local-First**: Runs completely offline with Ollama (no API costs)
- **Cloud Option**: Seamlessly uses OpenAI when available for higher quality

### 📱 Platform-Specific Content
- **LinkedIn**: Professional, analytical content (180-220 words)
- **Instagram**: Casual, enthusiast-focused with emojis (100-130 words)
- **Twitter**: Sharp, opinionated takes (<280 characters)

### 🎯 Smart Features
- **Selective Generation**: Only generates content for platforms you select
- **JSON Output**: Reliable structured responses for consistent parsing
- **Character Validation**: Automatic Twitter character count with warnings
- **Modern UI**: Clean Streamlit interface with provider status indicator
- **Error Handling**: Robust transcript fetching with detailed logging

---

## 🛠️ Technology Stack

- **Python 3.11+**
- **Streamlit** - Web interface
- **OpenAI GPT-4o** - Cloud AI (optional)
- **Ollama + Llama 3.1 8B** - Local AI (default)
- **YouTube Transcript API** - Video transcript extraction
- **openai-agents** - Agent orchestration

---

## 📋 Prerequisites

### Required
- Python 3.11 or higher
- **Ollama** installed and running (for local mode)

### Optional
- OpenAI API key (for cloud mode)

---

## 🚀 Installation

### 1. Install Ollama (Local AI)

**Windows:**
```bash
# Download from https://ollama.ai/download
# Or use winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull the AI Model

```bash
# Pull Llama 3.1 8B (recommended - 4.7GB)
ollama pull llama3.1:8b

# Start Ollama server (if not auto-started)
ollama serve
```

**Verify Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

### 3. Clone and Setup Project

```bash
# Clone repository
git clone https://github.com/Navashub/AI-Agents.git
cd AI-Agents/content_writer

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration (Optional)

Create a `.env` file for OpenAI (optional):

```bash
# Copy example
cp .env.example .env

# Edit .env and add your OpenAI key (optional)
OPENAI_API_KEY=sk-your-key-here
```

**If no `.env` file exists, the system automatically uses Ollama!**

---

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

### Provider Behavior

The system automatically detects which provider to use:

1. **Checks for `OPENAI_API_KEY`** in `.env`
2. **If found**: Uses OpenAI GPT-4o
3. **If not found**: Uses Ollama with llama3.1:8b
4. **Displays active provider** in the UI

### Using the Interface

1. **Enter YouTube Video ID**
   - Example: For `https://youtube.com/watch?v=6hr6wZr1N_8`, use `6hr6wZr1N_8`

2. **Customize Query** (optional)
   - Add specific instructions or keep the default

3. **Select Platforms**
   - Choose LinkedIn, Instagram, and/or Twitter
   - Only selected platforms will be generated

4. **Generate Content**
   - Click "🚀 Generate Content"
   - Wait for AI processing
   - Copy content from individual platform cards

### Command Line Usage

```bash
# Test the agent directly
python content_agent.py
```

---

## 📁 Project Structure

```
content_writer/
├── app.py                  # Streamlit web interface
├── content_agent.py        # Core AI agent with hybrid provider
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── transcript_errors.log  # Error logging
└── README.md              # This file
```

---

## 🔧 Configuration Details

### Provider Selection Logic

```python
# Automatic detection in content_agent.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip())
PROVIDER = "openai" if USE_OPENAI else "ollama"
```

### Model Configuration

| Provider | Model | Use Case |
|----------|-------|----------|
| OpenAI | `gpt-4o` | Higher quality, costs API credits |
| Ollama | `llama3.1:8b` | Free, local, good quality |

### Changing Ollama Model

Edit `content_agent.py`:

```python
OLLAMA_MODEL = "llama3.1:8b"  # Change to your preferred model
```

**Recommended Ollama models:**
- `llama3.1:8b` - Best balance (4.7GB)
- `llama3.2:3b` - Faster, smaller (2GB)
- `qwen2.5:7b` - Alternative, creative (4.7GB)
- `mistral:7b` - Efficient (4.1GB)

---

## 🎨 Content Strategy

### Platform Differences

| Platform | Tone | Length | Special Features |
|----------|------|--------|------------------|
| **LinkedIn** | Professional, analytical | 180-220 words | Industry hashtags, discussion questions |
| **Instagram** | Casual, excited | 100-130 words | 3-5 emojis, 7-8 trendy hashtags |
| **Twitter** | Sharp, opinionated | <280 chars | 2-3 hashtags, conversation starters |

### Content Perspective
All content is written from **audispot254's viewpoint** as someone who watched the video, not the creator.

---

## 🐛 Troubleshooting

### Ollama Issues

**"Connection refused" error:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify model is installed
ollama list
```

**Model not found:**
```bash
# Pull the model
ollama pull llama3.1:8b
```

### OpenAI Issues

**"Invalid API key" error:**
- Check `.env` file has correct `OPENAI_API_KEY`
- Verify API key at https://platform.openai.com/api-keys
- Check OpenAI account has credits

**Want to force Ollama even with API key:**
- Remove or comment out `OPENAI_API_KEY` in `.env`
- Or delete the `.env` file

### Transcript Issues

**"Could not fetch transcript" error:**
- Verify YouTube video ID is correct
- Check if video has captions/transcripts enabled
- Some videos may have transcripts disabled by creator
- Check `transcript_errors.log` for details

### Performance Issues

**Ollama is slow:**
- Ensure you have adequate RAM (8GB+ recommended)
- Try a smaller model: `ollama pull llama3.2:3b`
- Check GPU availability: `ollama list` shows GPU usage

**OpenAI is slow:**
- Check internet connection
- Verify OpenAI API status: https://status.openai.com

---

## 🔄 Switching Between Providers

### Use OpenAI
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Restart app
streamlit run app.py
```

### Use Ollama
```bash
# Remove or rename .env
mv .env .env.backup

# Restart app
streamlit run app.py
```

The UI will show which provider is active: **🤖 Using: OPENAI (gpt-4o)** or **🤖 Using: OLLAMA (llama3.1:8b)**

---

## 🚀 Advanced Usage

### Custom Ollama Configuration

Edit `content_agent.py`:

```python
OLLAMA_BASE_URL = "http://localhost:11434"  # Change if Ollama runs elsewhere
OLLAMA_MODEL = "your-preferred-model"       # Change model
```

### Running Multiple Instances

```bash
# Terminal 1: Ollama on default port
ollama serve

# Terminal 2: Run app
streamlit run app.py
```

### API-Only Mode (No Ollama)

If you only want OpenAI and don't have Ollama:

1. Ensure `OPENAI_API_KEY` is set in `.env`
2. The app will use OpenAI exclusively
3. If API key is invalid, you'll get clear error messages

---

## 📊 Performance Comparison

| Metric | OpenAI GPT-4o | Ollama Llama 3.1 8B |
|--------|---------------|---------------------|
| **Quality** | Excellent | Very Good |
| **Speed** | 5-15 seconds | 10-30 seconds |
| **Cost** | ~$0.02/request | Free |
| **Internet** | Required | Not required |
| **Privacy** | Cloud | Local |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

---

## 📄 License

Part of the [AI-Agents repository](https://github.com/Navashub/AI-Agents).

---

## 🔗 Links

- **Ollama**: https://ollama.ai
- **Llama 3.1**: https://ollama.ai/library/llama3.1
- **OpenAI Platform**: https://platform.openai.com
- **YouTube Transcript API**: https://pypi.org/project/youtube-transcript-api/
- **Streamlit**: https://streamlit.io

---

## 🙏 Acknowledgments

- Meta AI for Llama 3.1 model
- Ollama team for local AI infrastructure
- OpenAI for GPT-4 API
- YouTube Transcript API by Jonas Depoix
- Streamlit for the web framework

---

**Made with ❤️ for automotive content creators**

*Powered by hybrid AI - the best of both worlds!* 🚀
