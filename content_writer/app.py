import streamlit as st
import asyncio
import json
from content_agent import (
    get_transcript, 
    create_content_agent, 
    Runner,
    RunConfig,
    ItemHelpers, 
    trace,
    PROVIDER,
    OPENAI_MODEL,
    OLLAMA_MODEL,
    USE_OPENAI,
    ollama_provider
)

st.set_page_config(
    page_title="audispot254 Content Generator", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark mode and card styling
st.markdown(
    """
    <style>
    body { background-color: #18181b; }
    .stApp { background-color: #18181b; }
    .title { font-size: 2.5rem; font-weight: bold; text-align: center; color: #fff; margin-bottom: 0.5em; }
    .subtitle { font-size: 1.1rem; text-align: center; color: #aaa; margin-bottom: 1em; }
    .provider-badge { 
        text-align: center; 
        padding: 0.5em; 
        margin-bottom: 2em;
        background: #2d2d35;
        border-radius: 8px;
        color: #10b981;
        font-weight: 600;
    }
    .input-section { background: #23232a; border-radius: 12px; padding: 2em 2em 1em 2em; margin-bottom: 2em; }
    .output-card { background: #23232a; border-radius: 12px; padding: 1.5em; margin-top: 1.5em; color: #fff; }
    .platform-header { 
        font-size: 1.3rem; 
        font-weight: bold; 
        color: #10b981; 
        margin-bottom: 0.5em;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    .char-count { 
        color: #aaa; 
        font-size: 0.9em; 
        margin-bottom: 0.5em;
    }
    .char-warning {
        color: #f59e0b;
        font-weight: 600;
    }
    .copy-note { color: #aaa; font-size: 0.95em; margin-bottom: 0.5em; }
    .content-box { 
        white-space: pre-wrap; 
        word-break: break-word; 
        background: #1a1a1f; 
        color: #fff; 
        border-radius: 8px; 
        padding: 1.2em; 
        font-size: 1.05em; 
        line-height: 1.6;
        border-left: 4px solid #10b981;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="title">🚗 audispot254 Content Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate platform-optimized social media content from automotive videos</div>', 
    unsafe_allow_html=True
)

# Provider status badge
provider_display = PROVIDER.upper()
model_display = OPENAI_MODEL if PROVIDER == "openai" else OLLAMA_MODEL
st.markdown(
    f'<div class="provider-badge">🤖 Using: {provider_display} ({model_display})</div>',
    unsafe_allow_html=True
)

# Input section
with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("Input")
    
    col1, col2 = st.columns([2, 3])
    with col1:
        video_id = st.text_input(
            "YouTube Video ID", 
            "6hr6wZr1N_8", 
            help="Extract from URL: youtube.com/watch?v=VIDEO_ID"
        )
    with col2:
        query = st.text_area(
            "Custom Instructions (Optional)", 
            "Create engaging posts from audispot254's perspective as someone who watched this automotive video.",
            height=80
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Select Platforms")
    
    col_l, col_i, col_t = st.columns(3)
    with col_l:
        linkedin = st.checkbox("LinkedIn", value=True)
    with col_i:
        instagram = st.checkbox("Instagram", value=True)
    with col_t:
        twitter = st.checkbox("Twitter", value=False)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Collect selected platforms
platforms = []
if linkedin:
    platforms.append("LinkedIn")
if instagram:
    platforms.append("Instagram")
if twitter:
    platforms.append("Twitter")


def parse_json_content(output: str, platform: str) -> dict:
    """Parse JSON output from agent, with fallback handling"""
    try:
        # Try to parse as JSON array
        data = json.loads(output)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("platform", "").lower() == platform.lower():
                    return item
        # Try as single JSON object
        if isinstance(data, dict) and data.get("platform", "").lower() == platform.lower():
            return data
    except json.JSONDecodeError:
        pass
    
    # Fallback: search for JSON objects in text
    import re
    json_pattern = r'\{[^{}]*"platform"\s*:\s*"' + platform + r'"[^{}]*\}'
    matches = re.findall(json_pattern, output, re.IGNORECASE | re.DOTALL)
    if matches:
        try:
            return json.loads(matches[0])
        except:
            pass
    
    # Last resort: return raw content
    return {"platform": platform, "content": output, "error": "Could not parse JSON"}


def display_platform_content(platform: str, content_data: dict):
    """Display content card for a platform"""
    content = content_data.get("content", "No content generated")
    char_count = content_data.get("char_count", len(content))
    
    st.markdown(f'<div class="output-card">', unsafe_allow_html=True)
    
    # Platform header with emoji
    platform_emoji = {"LinkedIn": "💼", "Instagram": "📸", "Twitter": "🐦"}
    emoji = platform_emoji.get(platform, "📱")
    st.markdown(
        f'<div class="platform-header">{emoji} {platform} Post</div>', 
        unsafe_allow_html=True
    )
    
    # Character count (with warning for Twitter)
    if platform == "Twitter":
        warning_class = "char-warning" if char_count > 280 else ""
        st.markdown(
            f'<div class="char-count {warning_class}">Character count: {char_count}/280</div>',
            unsafe_allow_html=True
        )
        if char_count > 280:
            st.warning("⚠️ Tweet exceeds 280 characters. Consider shortening.")
    
    # Copy instruction
    st.markdown(
        '<div class="copy-note">📋 Select text and copy (Ctrl+C or ⌘+C)</div>', 
        unsafe_allow_html=True
    )
    
    # Content display
    st.markdown(f'<div class="content-box">{content}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


async def run_agent(query: str, video_id: str, platforms: list[str]) -> str:
    """Run the content generation agent"""
    transcript = get_transcript(video_id)
    if not transcript:
        return "ERROR: Could not fetch transcript. Please check the video ID."
    
    platform_list = ", ".join(platforms)
    msg = f"""{query}

Target platforms: {platform_list}

Create SHORT, engaging posts (not long content) from audispot254's perspective.

Video Transcript:
{transcript}"""
    
    input_items = [{"content": msg, "role": "user"}]
    
    # Create agent with only selected platforms
    agent = create_content_agent(platforms)
    
    with trace("Generating content"):
        # Use Ollama provider if not using OpenAI
        if USE_OPENAI:
            result = await Runner.run(agent, input_items)
        else:
            run_config = RunConfig(model_provider=ollama_provider)
            result = await Runner.run(agent, input_items, run_config=run_config)
        output = ItemHelpers.text_message_outputs(result.new_items)
        return output


# Generate button
if st.button("🚀 Generate Content", type="primary"):
    if not video_id.strip():
        st.error("❌ Please enter a YouTube video ID")
    elif not platforms:
        st.error("❌ Please select at least one platform")
    else:
        with st.spinner(f"⏳ Generating content using {PROVIDER.upper()}... This may take a moment."):
            output = asyncio.run(run_agent(query, video_id, platforms))
            
            if output and not output.startswith("ERROR:"):
                st.markdown("---")
                st.markdown("## ✨ Generated Content")
                
                # Display content for each platform
                for platform in platforms:
                    content_data = parse_json_content(output, platform)
                    display_platform_content(platform, content_data)
                
                # Debug section (collapsible)
                with st.expander("🔍 Debug - Raw Output"):
                    st.code(output, language="text")
            else:
                error_msg = output if output and output.startswith("ERROR:") else "Failed to generate content. Please try again."
                st.error(f"❌ {error_msg}")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9em;">Made with ❤️ for automotive content creators</div>',
    unsafe_allow_html=True
)
