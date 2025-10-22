# -----------------------------------------------------
# Audispot Content Writer - Hybrid OpenAI/Ollama Agent
# -----------------------------------------------------
import os
import asyncio
import json
import logging

# Import YouTube Transcript API with error handling
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError as e:
    print(f"❌ Error importing youtube_transcript_api: {e}")
    print("   Install with: pip install youtube-transcript-api")
    raise

from agents import Agent, Runner, RunConfig, function_tool, ItemHelpers, trace
from agents.models.openai_provider import OpenAIProvider
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from typing import Optional, Literal

# -----------------------------------------------------
# Configuration and Provider Detection
# -----------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Smart provider detection
USE_OPENAI = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip())
PROVIDER = "openai" if USE_OPENAI else "ollama"

# Model configuration
OPENAI_MODEL = "gpt-4o"
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"

print(f"🤖 Provider: {PROVIDER.upper()}")
if PROVIDER == "openai":
    print(f"   Model: {OPENAI_MODEL}")
else:
    print(f"   Model: {OLLAMA_MODEL}")
    print(f"   URL: {OLLAMA_BASE_URL}")

# Configure Ollama provider for agents library
ollama_provider = None
if not USE_OPENAI:
    # Set up Ollama as OpenAI-compatible provider
    os.environ["OPENAI_API_KEY"] = "dummy_key_for_ollama"  # Agents library requires this
    # Create OpenAI provider pointing to Ollama
    ollama_provider = OpenAIProvider(
        base_url=f"{OLLAMA_BASE_URL}/v1",
        api_key="ollama"  # Ollama doesn't need a real key
    )

# -----------------------------------------------------
# Unified LLM Client
# -----------------------------------------------------
class LLMClient:
    """Unified client that works with both OpenAI and Ollama"""
    
    def __init__(self):
        self.provider = PROVIDER
        if self.provider == "openai":
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = OPENAI_MODEL
        else:
            # Ollama uses OpenAI-compatible API
            self.client = OpenAI(
                base_url=f"{OLLAMA_BASE_URL}/v1",
                api_key="ollama"  # Ollama doesn't need real key
            )
            self.model = OLLAMA_MODEL
    
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate content with automatic provider handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"Error with {self.provider}: {str(e)}"
            logging.error(error_msg)
            return json.dumps({"error": error_msg})

# Global client instance
llm_client = LLMClient()

# -----------------------------------------------------
# Platform-Specific Content Tools with JSON Output
# -----------------------------------------------------

@function_tool
def create_linkedin_content(video_transcript: str) -> str:
    """Creates professional LinkedIn content for automotive industry professionals.
    Returns JSON: {"platform": "LinkedIn", "content": "..."}"""
    
    linkedin_prompt = f"""Create a LinkedIn post for audispot254 (automotive account).

TRANSCRIPT: {video_transcript}

LINKEDIN REQUIREMENTS:
- AUDIENCE: Automotive professionals, engineers, business leaders
- TONE: Professional, analytical, thought-provoking
- FOCUS: Technical insights, industry trends, business implications
- LENGTH: 180-220 words
- HASHTAGS: 4-5 professional ones (#AutomotiveInnovation #AudiTechnology #IndustryInsights)
- PERSPECTIVE: Industry analyst who watched this video
- INCLUDE: Discussion questions for professional engagement

Write as: "Recently analyzed this automotive review..." or "This technical breakdown highlights..."

DO NOT write casual language or use emojis.

CRITICAL: Return ONLY valid JSON in this exact format:
{{"platform": "LinkedIn", "content": "your post content here"}}"""

    result = llm_client.generate(linkedin_prompt, max_tokens=500, temperature=0.7)
    
    # Ensure valid JSON response
    try:
        parsed = json.loads(result)
        if "platform" not in parsed:
            parsed["platform"] = "LinkedIn"
        return json.dumps(parsed)
    except json.JSONDecodeError:
        # Fallback: wrap raw content
        return json.dumps({"platform": "LinkedIn", "content": result})


@function_tool  
def create_instagram_content(video_transcript: str) -> str:
    """Creates engaging Instagram content for car enthusiasts and younger audience.
    Returns JSON: {"platform": "Instagram", "content": "..."}"""
    
    instagram_prompt = f"""Create an Instagram post for audispot254 (automotive account).

TRANSCRIPT: {video_transcript}

INSTAGRAM REQUIREMENTS:
- AUDIENCE: Car enthusiasts, Gen Z/Millennial car lovers, visual-focused users
- TONE: Excited, casual, community-driven
- FOCUS: Cool features, performance specs, visual appeal, lifestyle
- LENGTH: 100-130 words maximum
- EMOJIS: Use 3-5 relevant car/fire/racing emojis
- HASHTAGS: 7-8 trendy ones (#AudiLife #CarsOfInstagram #CarEnthusiast #SpeedDemon)
- PERSPECTIVE: Passionate car fan who just watched this
- INCLUDE: Call-to-action for engagement

Write as: "Just watched this sick review! 🔥" or "This car is absolutely insane! 🚗💨"

MUST use casual language and car slang.

CRITICAL: Return ONLY valid JSON in this exact format:
{{"platform": "Instagram", "content": "your post content here"}}"""

    result = llm_client.generate(instagram_prompt, max_tokens=400, temperature=0.8)
    
    try:
        parsed = json.loads(result)
        if "platform" not in parsed:
            parsed["platform"] = "Instagram"
        return json.dumps(parsed)
    except json.JSONDecodeError:
        return json.dumps({"platform": "Instagram", "content": result})


@function_tool
def create_twitter_content(video_transcript: str) -> str:
    """Creates concise Twitter content for quick engagement.
    Returns JSON: {"platform": "Twitter", "content": "...", "char_count": 123}"""
    
    twitter_prompt = f"""Create a Twitter/X post for audispot254 (automotive account).

TRANSCRIPT: {video_transcript}

TWITTER REQUIREMENTS:
- AUDIENCE: Quick scrollers, debate starters, car Twitter community
- TONE: Sharp, opinionated, conversation-starter
- FOCUS: One surprising fact, hot take, or debate point
- LENGTH: 200-250 characters maximum (including hashtags)
- HASHTAGS: 2-3 only (#Audi #CarTwitter #AutomotiveDebate)
- PERSPECTIVE: Someone dropping automotive knowledge/hot takes
- INCLUDE: Question or statement that sparks replies

Write as: "Hot take:" or "This review proves..." or "Am I the only one who thinks..."

MUST be under 250 characters total. Be bold and opinionated.

CRITICAL: Return ONLY valid JSON in this exact format:
{{"platform": "Twitter", "content": "your tweet here", "char_count": 123}}"""

    result = llm_client.generate(twitter_prompt, max_tokens=250, temperature=0.9)
    
    try:
        parsed = json.loads(result)
        if "platform" not in parsed:
            parsed["platform"] = "Twitter"
        # Add character count if not present
        if "char_count" not in parsed and "content" in parsed:
            parsed["char_count"] = len(parsed["content"])
        return json.dumps(parsed)
    except json.JSONDecodeError:
        char_count = len(result)
        return json.dumps({"platform": "Twitter", "content": result, "char_count": char_count})


# -----------------------------------------------------
# Dynamic Agent with Platform Selection
# -----------------------------------------------------

def create_content_agent(platforms: list[str]) -> Agent:
    """Creates an agent that only generates content for selected platforms"""
    
    # Map platform names to tools
    tool_map = {
        "LinkedIn": create_linkedin_content,
        "Instagram": create_instagram_content,
        "Twitter": create_twitter_content
    }
    
    # Select only requested tools
    selected_tools = [tool_map[p] for p in platforms if p in tool_map]
    
    platform_list = ", ".join(platforms)
    
    instructions = f"""You are audispot254's content creator. Generate DISTINCT content for these platforms: {platform_list}

MANDATORY PROCESS:
"""
    
    if "LinkedIn" in platforms:
        instructions += "1. Call create_linkedin_content() for professional LinkedIn post\n"
    if "Instagram" in platforms:
        instructions += "2. Call create_instagram_content() for casual Instagram post\n"
    if "Twitter" in platforms:
        instructions += "3. Call create_twitter_content() for sharp Twitter post\n"
    
    instructions += """
CRITICAL RULES:
- Each platform must have COMPLETELY DIFFERENT content and tone
- LinkedIn = Professional analysis
- Instagram = Casual excitement with emojis
- Twitter = Sharp hot takes under 250 chars
- All tools return JSON format
- Call ALL selected tools, never skip any

Your job is to call the tools and return their JSON outputs."""

    return Agent(
        name="Platform-Specific Content Creator",
        instructions=instructions,
        model="gpt-4o-mini" if USE_OPENAI else OLLAMA_MODEL,
        tools=selected_tools
    )


# -----------------------------------------------------
# Transcript Fetcher
# -----------------------------------------------------

def get_transcript(video_id: str) -> str:
    """Fetch YouTube transcript with error logging"""
    logging.basicConfig(
        filename='transcript_errors.log',
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    
    try:
        # Use the new API: create instance and call fetch()
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        
        # Access text attribute from FetchedTranscriptSnippet objects
        transcript_text = " ".join([entry.text for entry in transcript])
        return transcript_text
    except Exception as e:
        import traceback
        error_message = f"Error fetching transcript for video_id {video_id}: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        return ""


# -----------------------------------------------------
# Main Execution
# -----------------------------------------------------

async def main():
    """Test the agent with all platforms"""
    video_id = "6hr6wZr1N_8"
    platforms = ["LinkedIn", "Instagram", "Twitter"]
    
    transcript = get_transcript(video_id)
    if not transcript:
        print("❌ Failed to fetch transcript")
        return

    msg = f"""Create platform-specific posts for audispot254 from this automotive video.

Target platforms: {', '.join(platforms)}

Video transcript: {transcript[:1000]}...

Generate distinct content for each platform."""

    input_items = [{"content": msg, "role": "user"}]
    
    # Create agent with selected platforms
    agent = create_content_agent(platforms)
    
    with trace("Creating platform-specific content"):
        if USE_OPENAI:
            result = await Runner.run(agent, input_items)
        else:
            run_config = RunConfig(model_provider=ollama_provider)
            result = await Runner.run(agent, input_items, run_config=run_config)
        output = ItemHelpers.text_message_outputs(result.new_items)
        
        print("\n" + "="*60)
        print("GENERATED CONTENT:")
        print("="*60)
        print(output)
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
