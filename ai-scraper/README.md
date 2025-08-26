# 🤖 AI Web Scraper & Q&A

A powerful web scraping tool that combines intelligent content extraction with AI-powered question answering. Built with Streamlit, LangChain, and Ollama for local AI processing.

## 🚀 Features

- **Smart Web Scraping**: Automatically extracts content from any URL using multiple fallback methods
- **AI-Powered Q&A**: Ask questions about scraped content and get intelligent responses
- **Local AI Processing**: Uses Ollama for privacy-focused, offline AI processing
- **Multiple Scraping Methods**: 
  - Selenium WebDriver for JavaScript-heavy sites
  - Simple HTTP requests for basic HTML pages
- **Interactive Chat Interface**: Real-time conversation with the scraped content
- **Content Chunking**: Intelligent text splitting for better context retrieval
- **Source Citations**: See exactly which parts of the content were used to answer your questions
- **Error Recovery**: Robust error handling with graceful fallbacks

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Ollama (llama3.2)
- **Web Scraping**: Selenium WebDriver, BeautifulSoup
- **Text Processing**: LangChain
- **Vector Store**: In-memory vector storage
- **Embeddings**: Ollama embeddings for semantic search

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **Chrome browser** installed (for Selenium)

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ai-scraper
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install and Setup Ollama

#### On Windows/Mac/Linux:
```bash
# Install Ollama from https://ollama.ai
# Then pull the required model
ollama pull llama3.2
```

#### Start Ollama Service:
```bash
ollama serve
```

### 4. Verify Installation
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check if llama3.2 model is installed
ollama list
```

## 🚀 Usage

### Starting the Application
```bash
streamlit run ai_scraper.py
```

The app will open in your browser at `http://localhost:8501`

### How to Use

1. **Enter a URL** in the input field (e.g., `https://example.com`)
2. **Click "Load & Process URL"** to scrape and index the content
3. **Wait for processing** - you'll see progress indicators
4. **Ask questions** in the chat interface about the scraped content
5. **View sources** - expand the sources section to see which content was used

### Example Workflows

#### Scraping a News Article
```
1. Enter: https://example-news-site.com/article
2. Wait for "Documents indexed successfully!"
3. Ask: "What is the main topic of this article?"
4. Ask: "Who are the key people mentioned?"
```

#### Analyzing Documentation
```
1. Enter: https://docs.example.com/api-guide
2. Wait for processing
3. Ask: "How do I authenticate with this API?"
4. Ask: "What are the rate limits?"
```



## ⚙️ Configuration

### Environment Variables (Optional)
```bash
# Set custom Ollama host
export OLLAMA_HOST=http://localhost:11434

# Set custom model
export OLLAMA_MODEL=llama3.2
```

### Customizing the AI Model

You can use different Ollama models by changing the model name in the code:

```python
# In ai_scraper.py, change:
embeddings = OllamaEmbeddings(model="llama3.2")
model = OllamaLLM(model="llama3.2")

# To:
embeddings = OllamaEmbeddings(model="llama2")  # or another model
model = OllamaLLM(model="llama2")
```

Available models:
- `llama3.2` (recommended)
- `llama2`
- `mistral`
- `codellama`

## 🔍 Troubleshooting

### Common Issues

#### Segmentation Fault
- **Cause**: Chrome/Selenium driver issues
- **Solution**: The app automatically handles this with fallback methods

#### "Ollama not found"
```bash
# Check if Ollama is running
ollama serve

# Check if model is installed
ollama pull llama3.2
```

#### Chrome Driver Issues
```bash
# The app automatically downloads Chrome driver
# If issues persist, manually install:
pip install --upgrade webdriver-manager
```

#### Empty Content
- **Cause**: Website blocks automated scraping
- **Solution**: Try different URLs or check the website's robots.txt

#### Slow Processing
- **Cause**: Large pages or complex content
- **Solutions**: 
  - Use more specific URLs
  - Wait for processing to complete
  - Consider using a more powerful model

### Performance Tips

1. **Use specific URLs** rather than homepages
2. **Close unused browser tabs** to free memory
3. **Use headless mode** (already enabled)
4. **Clear chat history** regularly for better performance

## 🔒 Privacy & Security

- **Local Processing**: All AI processing happens locally with Ollama
- **No Data Sent to Cloud**: Your scraped content stays on your machine
- **Secure Scraping**: Respects robots.txt and rate limits
- **No Persistent Storage**: Data is only stored in memory during the session

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone and setup development environment
git clone <your-fork>
cd ai-scraper
pip install -r requirements.txt




# Code formatting
black ai_scraper.py
```

## 📈 Roadmap

- [ ] **Multi-language Support** - Support for more Ollama models
- [ ] **PDF Scraping** - Add PDF document processing
- [ ] **Batch Processing** - Process multiple URLs at once
- [ ] **Export Functionality** - Export Q&A sessions
- [ ] **Advanced Filtering** - Content filtering and preprocessing
- [ ] **API Mode** - REST API for programmatic access
- [ ] **Docker Support** - Containerized deployment
- [ ] **Cloud Deployment** - Deploy to cloud platforms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** - For providing excellent local AI capabilities
- **LangChain** - For the powerful document processing framework
- **Streamlit** - For the amazing web app framework
- **Selenium** - For robust web scraping capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](issues)
3. Create a new issue with:
   - Your operating system
   - Python version
   - Error message (if any)
   - Steps to reproduce

## 🌟 Show Your Support

If this project helped you, please consider:
- ⭐ Starring the repository
- 🔄 Sharing it with others
- 🐛 Reporting bugs
- 💡 Suggesting new features

---

**Happy Scraping! 🎉**

Built with using Python, Streamlit, and Ollama.