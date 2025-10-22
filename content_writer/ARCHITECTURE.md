# 🏗️ Architecture Overview

## System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)               │
│  - Video ID Input                                            │
│  - Platform Selection (LinkedIn/Instagram/Twitter)           │
│  - Provider Status Display                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Content Agent (content_agent.py)           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Provider Detection                                │   │
│  │     - Check for OPENAI_API_KEY in .env               │   │
│  │     - If exists → Use OpenAI                         │   │
│  │     - If not → Use Ollama                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  2. Transcript Fetching                               │   │
│  │     - YouTube Transcript API                          │   │
│  │     - Error logging to transcript_errors.log          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  3. Dynamic Agent Creation                            │   │
│  │     - Build agent with only selected platform tools   │   │
│  │     - LinkedIn tool (if selected)                     │   │
│  │     - Instagram tool (if selected)                    │   │
│  │     - Twitter tool (if selected)                      │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Unified LLM Client (LLMClient class)            │
│                                                               │
│  ┌─────────────────────┐      ┌─────────────────────┐       │
│  │   OpenAI Branch     │      │   Ollama Branch     │       │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │       │
│  │  │ OpenAI Client │  │      │  │ OpenAI Client │  │       │
│  │  │ API Key: Real │  │      │  │ Base URL:     │  │       │
│  │  │ Model: gpt-4o │  │      │  │ localhost:    │  │       │
│  │  │               │  │      │  │ 11434/v1      │  │       │
│  │  │               │  │      │  │ Model:        │  │       │
│  │  │               │  │      │  │ llama3.1:8b   │  │       │
│  │  └───────────────┘  │      │  └───────────────┘  │       │
│  └─────────────────────┘      └─────────────────────┘       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Platform-Specific Tools                         │
│                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │ LinkedIn Tool    │  │ Instagram Tool   │  │Twitter Tool│ │
│  │                  │  │                  │  │            │ │
│  │ • Professional   │  │ • Casual         │  │• Sharp     │ │
│  │ • 180-220 words  │  │ • 100-130 words  │  │• <280 char │ │
│  │ • No emojis      │  │ • 3-5 emojis     │  │• 2-3 tags  │ │
│  │ • 4-5 hashtags   │  │ • 7-8 hashtags   │  │• Hot takes │ │
│  │                  │  │                  │  │            │ │
│  │ Returns JSON:    │  │ Returns JSON:    │  │Returns JSON│ │
│  │ {                │  │ {                │  │{           │ │
│  │   platform: "LI" │  │   platform: "IG" │  │  platform: │ │
│  │   content: "..." │  │   content: "..." │  │  "Twitter" │ │
│  │ }                │  │ }                │  │  content:  │ │
│  │                  │  │                  │  │  "..."     │ │
│  │                  │  │                  │  │  char_count│ │
│  │                  │  │                  │  │}           │ │
│  └──────────────────┘  └──────────────────┘  └────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Processing                         │
│  - Parse JSON responses                                      │
│  - Extract platform-specific content                         │
│  - Validate Twitter character count                          │
│  - Format for display                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    UI Display                                │
│  - Platform cards with emojis                                │
│  - Character count indicators                                │
│  - Copy-friendly formatting                                  │
│  - Debug panel (collapsible)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Provider Detection (`content_agent.py`)
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip())
PROVIDER = "openai" if USE_OPENAI else "ollama"
```

**Logic:**
- Checks `.env` for `OPENAI_API_KEY`
- If valid key exists → OpenAI
- If no key or empty → Ollama
- Zero configuration needed!

### 2. Unified LLM Client
```python
class LLMClient:
    def __init__(self):
        if provider == "openai":
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = "gpt-4o"
        else:
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama"
            )
            self.model = "llama3.1:8b"
```

**Benefits:**
- Single interface for both providers
- Ollama uses OpenAI-compatible API
- Easy to add more providers

### 3. Dynamic Agent Creation
```python
def create_content_agent(platforms: list[str]) -> Agent:
    tool_map = {
        "LinkedIn": create_linkedin_content,
        "Instagram": create_instagram_content,
        "Twitter": create_twitter_content
    }
    selected_tools = [tool_map[p] for p in platforms if p in tool_map]
    return Agent(name="...", tools=selected_tools)
```

**Benefits:**
- Only generates selected platforms
- Saves compute/API costs
- Faster execution

### 4. JSON Output Schema
```json
{
  "platform": "LinkedIn",
  "content": "Recently analyzed this automotive review..."
}
```

**Benefits:**
- Reliable parsing
- No regex needed
- Easy to extend with metadata

## Data Flow Example

### User Request: Generate LinkedIn + Instagram content

```
1. User Input
   ├─ Video ID: "6hr6wZr1N_8"
   ├─ Platforms: ["LinkedIn", "Instagram"]
   └─ Query: "Create posts from audispot254's perspective"

2. Transcript Fetch
   └─ YouTube API → "This Audi RS6 features..."

3. Provider Check
   ├─ Check .env for OPENAI_API_KEY
   └─ Result: OLLAMA (no key found)

4. Agent Creation
   ├─ Tools: [create_linkedin_content, create_instagram_content]
   └─ Model: llama3.1:8b

5. Content Generation
   ├─ LinkedIn Tool
   │  ├─ Prompt: Professional, 180-220 words...
   │  ├─ LLM Call: Ollama llama3.1:8b
   │  └─ Output: {"platform": "LinkedIn", "content": "..."}
   │
   └─ Instagram Tool
      ├─ Prompt: Casual, emojis, 100-130 words...
      ├─ LLM Call: Ollama llama3.1:8b
      └─ Output: {"platform": "Instagram", "content": "..."}

6. Output Processing
   ├─ Parse JSON from each tool
   ├─ Validate formats
   └─ Combine results

7. UI Display
   ├─ LinkedIn Card: 💼 Professional content
   └─ Instagram Card: 📸 Casual content with emojis
```

## File Responsibilities

| File | Purpose | Key Functions |
|------|---------|---------------|
| `content_agent.py` | Core logic | Provider detection, LLM client, tools, agent |
| `app.py` | User interface | Streamlit UI, input handling, display |
| `setup.py` | Setup checker | Verify dependencies, Ollama, models |
| `test_agent.py` | Testing | Quick functionality tests |
| `requirements.txt` | Dependencies | Package list |
| `pyproject.toml` | Project config | Python version, dependencies |
| `.env.example` | Config template | Environment variable example |
| `.gitignore` | Git rules | Ignore sensitive files |

## Configuration Points

### Environment Variables (`.env`)
```bash
OPENAI_API_KEY=sk-...  # Optional - triggers OpenAI mode
```

### Code Constants (`content_agent.py`)
```python
OPENAI_MODEL = "gpt-4o"           # Change OpenAI model
OLLAMA_MODEL = "llama3.1:8b"      # Change Ollama model
OLLAMA_BASE_URL = "http://localhost:11434"  # Change Ollama URL
```

### Platform Prompts
Each tool function has its own prompt template:
- `create_linkedin_content()` - Professional tone
- `create_instagram_content()` - Casual tone
- `create_twitter_content()` - Sharp tone

## Error Handling

### Transcript Fetching
```python
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
except Exception as e:
    logging.error(f"Error: {e}")
    return ""
```

### LLM Generation
```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    return json.dumps({"error": str(e)})
```

### JSON Parsing
```python
try:
    parsed = json.loads(result)
except json.JSONDecodeError:
    # Fallback: wrap raw content
    return json.dumps({"platform": "...", "content": result})
```

## Performance Considerations

### OpenAI Mode
- **Latency**: 5-15 seconds (network + API)
- **Cost**: ~$0.02 per generation
- **Quality**: Excellent
- **Concurrent**: Limited by API rate limits

### Ollama Mode
- **Latency**: 10-30 seconds (local compute)
- **Cost**: $0 (free)
- **Quality**: Very good
- **Concurrent**: Limited by hardware (RAM/GPU)

### Optimization Tips
1. **Select fewer platforms** - Faster generation
2. **Use shorter transcripts** - Less tokens to process
3. **Adjust temperature** - Lower = faster, more deterministic
4. **Batch requests** - Process multiple videos in sequence

## Security

### API Key Protection
- `.env` file in `.gitignore`
- Never commit API keys
- Use `.env.example` as template

### Local Data
- Transcripts not stored permanently
- Logs in `transcript_errors.log` (local only)
- No data sent to external services (Ollama mode)

## Extensibility

### Adding New Platforms
1. Create new tool function:
```python
@function_tool
def create_tiktok_content(video_transcript: str) -> str:
    # Your prompt here
    return json.dumps({"platform": "TikTok", "content": "..."})
```

2. Add to tool map in `create_content_agent()`
3. Add UI checkbox in `app.py`

### Adding New Providers
1. Extend `LLMClient.__init__()`:
```python
elif self.provider == "anthropic":
    self.client = Anthropic(api_key=...)
```

2. Update provider detection logic
3. Add configuration constants

### Custom Prompts
Edit the prompt strings in each tool function to match your brand voice.

---

## Questions?

- **Setup issues?** → Run `python setup.py`
- **Testing?** → Run `python test_agent.py`
- **Full docs?** → See `README.md`
- **Quick start?** → See `QUICKSTART.md`
