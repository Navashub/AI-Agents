# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Activate your virtual environment first
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

## Step 2: Setup Ollama Model

```bash
# Pull the AI model (4.9GB download)
ollama pull llama3.1:8b

# Verify it's installed
ollama list
```

## Step 3: (Optional) Add OpenAI Key

If you want to use OpenAI instead of Ollama:

```bash
# Create .env file
echo OPENAI_API_KEY=sk-your-key-here > .env
```

**Skip this step to use free local Ollama!**

## Step 4: Run Setup Check

```bash
python setup.py
```

This will verify everything is configured correctly.

## Step 5: Start the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## Usage

1. **Enter YouTube Video ID** (e.g., `6hr6wZr1N_8`)
2. **Select platforms** (LinkedIn, Instagram, Twitter)
3. **Click "Generate Content"**
4. **Copy the generated posts!**

---

## Troubleshooting

### Ollama not running?
```bash
ollama serve
```

### Model not found?
```bash
ollama pull llama3.1:8b
```

### Want to test without the UI?
```bash
python test_agent.py
```

---

## Provider Status

The app shows which AI provider is active:

- **🤖 Using: OPENAI** - You have an API key in `.env`
- **🤖 Using: OLLAMA** - Using local AI (free!)

To switch providers, just add/remove the `OPENAI_API_KEY` in `.env` and restart the app.

---

**That's it! You're ready to generate content! 🎉**
