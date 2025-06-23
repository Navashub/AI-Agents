# 🚗 Audispot Content Writer

An AI-powered content generation tool that creates platform-specific social media content for automotive enthusiasts. Built specifically for audispot254, this tool generates engaging posts for LinkedIn, Instagram, and Twitter from YouTube automotive video transcripts.

## 🌟 Features

- **YouTube Integration**: Automatically extracts transcripts from YouTube automotive videos
- **Platform-Specific Content**: Creates tailored content for different social media platforms:
  - **LinkedIn**: Professional, analytical content for automotive industry professionals
  - **Instagram**: Casual, enthusiast-focused content with emojis and hashtags
  - **Twitter**: Concise, opinionated takes designed to spark engagement
- **Modern UI**: Clean, dark-mode Streamlit interface
- **AI-Powered**: Uses OpenAI GPT-4 for intelligent content generation
- **Real-time Generation**: Live content creation with loading indicators

## 🎯 Target Platforms

### LinkedIn
- **Audience**: Automotive professionals, engineers, business leaders
- **Tone**: Professional, analytical, thought-provoking
- **Focus**: Technical insights, industry trends, business implications
- **Length**: 180-220 words with professional hashtags

### Instagram
- **Audience**: Car enthusiasts, Gen Z/Millennial car lovers
- **Tone**: Excited, casual, community-driven
- **Focus**: Cool features, performance specs, visual appeal
- **Length**: 100-130 words with emojis and trendy hashtags

### Twitter
- **Audience**: Quick scrollers, debate starters, car Twitter community
- **Tone**: Sharp, opinionated, conversation-starter
- **Focus**: Hot takes, surprising facts, debate points
- **Length**: Under 250 characters with strategic hashtags

## 🛠️ Technology Stack

- **Python 3.11+**
- **Streamlit** - Web interface
- **OpenAI GPT-4** - Content generation
- **YouTube Transcript API** - Video transcript extraction
- **python-dotenv** - Environment variable management
- **openai-agents** - Agent orchestration

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key
- UV package manager (recommended)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Navashub/AI-Agents.git
cd AI-Agents/audispot_content_writer
```

### 2. Set Up Virtual Environment with UV

This project uses UV for dependency management. Install UV if you haven't already:

```bash
# Install UV (if not already installed)
pip install uv

# Initialize virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies from requirements.txt
uv add -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: 
- Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Never commit your `.env` file to version control
- The `.env` file should be added to your `.gitignore`

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Interface

1. **Enter YouTube Video ID**: 
   - Extract the ID from a YouTube URL (e.g., for `https://www.youtube.com/watch?v=6hr6wZr1N_8`, the ID is `6hr6wZr1N_8`)
   
2. **Customize Your Query**: 
   - Modify the default query or add specific instructions
   - The tool works best with automotive content
   
3. **Select Platforms**: 
   - Choose which social media platforms you want content for
   - Each platform generates unique, tailored content
   
4. **Generate Content**: 
   - Click "Generate Content" and wait for the AI to process
   - Content will be displayed in separate cards for each platform

### Example Usage

```python
# Direct API usage example
from audispot_content_agent import get_transcript, content_creator_agent

# Get transcript
video_id = "6hr6wZr1N_8"
transcript = get_transcript(video_id)

# Generate content (async)
result = await Runner.run(content_creator_agent, input_items)
```

## 📁 Project Structure

```
audispot_content_writer/
├── app.py                      # Streamlit web interface
├── audispot_content_agent.py   # Core AI agent and content generation logic
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration
├── uv.lock                    # UV lock file
├── transcript_errors.log      # Error logging
├── .env                       # Environment variables (create this)
└── README.md                  # Project documentation
```

## 🔧 Key Components

### Content Generation Agent
- **Platform-specific tools**: Separate functions for LinkedIn, Instagram, and Twitter
- **Intelligent prompting**: Tailored prompts for each platform's audience
- **Error handling**: Robust transcript fetching with logging

### Web Interface
- **Dark mode design**: Modern, professional appearance
- **Responsive layout**: Works on desktop and mobile
- **Real-time processing**: Live updates and loading states
- **Content extraction**: Smart parsing of AI-generated content

## 🎨 Content Strategy

The tool follows audispot254's content strategy:

- **Perspective**: Content written from the viewpoint of someone who watched the video
- **Authenticity**: Natural, genuine reactions to automotive content
- **Platform Optimization**: Each platform receives content optimized for its audience
- **Engagement Focus**: Content designed to drive comments, shares, and interactions

## 🐛 Troubleshooting

### Common Issues

1. **"Could not fetch transcript" error**:
   - Verify the YouTube video ID is correct
   - Check if the video has available transcripts/captions
   - Some videos may have transcripts disabled

2. **OpenAI API errors**:
   - Verify your API key is correct in the `.env` file
   - Check your OpenAI account has available credits
   - Ensure the `.env` file is in the project root

3. **UV dependency issues**:
   - Make sure UV is properly installed: `pip install uv`
   - Try recreating the virtual environment: `uv venv --force`
   - Reinstall dependencies: `uv add -r requirements.txt`

### Error Logging

Check `transcript_errors.log` for detailed error information when transcript fetching fails.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is part of the [AI-Agents repository](https://github.com/Navashub/AI-Agents/tree/main/audispot_content_writer).

## 🔗 Links

- **Project Repository**: [GitHub - Audispot Content Writer](https://github.com/Navashub/AI-Agents/tree/main/audispot_content_writer)
- **YouTube Transcript API**: [PyPI - youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
- **OpenAI Platform**: [OpenAI API](https://platform.openai.com/)
- **Streamlit Documentation**: [Streamlit Docs](https://docs.streamlit.io/)

## 🙏 Acknowledgments

- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/) by Jonas Depoix
- OpenAI for GPT-4 API
- Streamlit for the web framework
- UV for modern Python dependency management

---

**Made with for automotive content creators**
