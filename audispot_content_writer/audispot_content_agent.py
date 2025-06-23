# -----------------------------------------------------
# Step 0: Importing Libraries
# -----------------------------------------------------
import os
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi
from agents import Agent, Runner, WebSearchTool, function_tool, ItemHelpers, trace
from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
import logging


# -----------------------------------------------------
# Step 1: Get OpenAI API Key
# -----------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------------------------------
# Step 2: Define SEPARATE tools for each platform
# -----------------------------------------------------

@function_tool
def create_linkedin_content(video_transcript: str):
    """Creates professional LinkedIn content for automotive industry professionals"""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
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

DO NOT write casual language or use emojis."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": linkedin_prompt}],
        max_tokens=450,
        temperature=0.7
    )
    
    return f"LINKEDIN POST:\n{response.choices[0].message.content}"


@function_tool  
def create_instagram_content(video_transcript: str):
    """Creates engaging Instagram content for car enthusiasts and younger audience"""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
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

MUST use casual language and car slang."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": instagram_prompt}],
        max_tokens=350,
        temperature=0.8
    )
    
    return f"INSTAGRAM POST:\n{response.choices[0].message.content}"


@function_tool
def create_twitter_content(video_transcript: str):
    """Creates concise Twitter content for quick engagement"""
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
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

MUST be under 250 characters total. Be bold and opinionated."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": twitter_prompt}],
        max_tokens=200,
        temperature=0.9
    )
    
    return f"TWITTER POST:\n{response.choices[0].message.content}"


# -----------------------------------------------------
# Step 3: Create agent that MUST use all three tools
# -----------------------------------------------------

content_creator_agent = Agent(
    name="Platform-Specific Content Creator",
    instructions="""You are audispot254's content creator who MUST create completely different content for each social media platform.

MANDATORY PROCESS:
1. ALWAYS call create_linkedin_content() for LinkedIn
2. ALWAYS call create_instagram_content() for Instagram  
3. ALWAYS call create_twitter_content() for Twitter

NEVER reuse content between platforms. Each tool creates content specifically for its audience.

PLATFORM DIFFERENCES YOU MUST ENFORCE:
- LinkedIn = Professional industry analysis
- Instagram = Casual enthusiast excitement
- Twitter = Sharp hot takes and debates

Your job is to call all three tools and return their distinct outputs. Do NOT write your own content - let the tools handle it.""",
    model="gpt-4o-mini",
    tools=[
        create_linkedin_content,
        create_instagram_content,
        create_twitter_content,
        WebSearchTool()
    ]
)


# -----------------------------------------------------
# Step 4: Helper function (unchanged)
# -----------------------------------------------------

def get_transcript(video_id: str) -> str:
    logging.basicConfig(filename='transcript_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript_list])
        return transcript_text
    except Exception as e:
        import traceback
        error_message = f"Error fetching transcript for video_id {video_id}: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        return ""


# -----------------------------------------------------
# Step 5: Main execution with clear instructions
# -----------------------------------------------------

async def main():
    video_id = "6hr6wZr1N_8"
    transcript = get_transcript(video_id)

    # Very specific instructions to force different content
    msg = f"""TASK: Create three completely different social media posts for audispot254.

REQUIREMENTS:
1. Call create_linkedin_content() - Must be professional and analytical
2. Call create_instagram_content() - Must be casual and exciting with emojis
3. Call create_twitter_content() - Must be under 250 characters and opinionated

Each post must target different audiences and have completely different tones. DO NOT create similar content.

Video transcript: {transcript}

Execute all three tools to generate platform-specific content."""

    input_items = [{"content": msg, "role": "user"}]

    with trace("Creating platform-specific content"):
        result = await Runner.run(content_creator_agent, input_items)
        output = ItemHelpers.text_message_outputs(result.new_items)
        
        print("="*60)
        print("PLATFORM-SPECIFIC CONTENT GENERATED:")
        print("="*60)
        print(output)
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())