
import streamlit as st
import asyncio
from audispot_content_agent import get_transcript, content_creator_agent, Runner, ItemHelpers, trace
import json
import re

st.set_page_config(page_title="audispot254 Content Generator", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for dark mode and card styling
st.markdown(
    """
    <style>
    body { background-color: #18181b; }
    .stApp { background-color: #18181b; }
    .title { font-size: 2.5rem; font-weight: bold; text-align: center; color: #fff; margin-bottom: 0.5em; }
    .subtitle { font-size: 1.1rem; text-align: center; color: #aaa; margin-bottom: 2em; }
    .input-section { background: #23232a; border-radius: 12px; padding: 2em 2em 1em 2em; margin-bottom: 2em; }
    .output-card { background: #23232a; border-radius: 12px; padding: 1.5em; margin-top: 1.5em; color: #fff; }
    .platform-label { color: #fff; font-weight: 600; }
    .section-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5em; color: #fff; }
    .copy-note { color: #aaa; font-size: 0.95em; margin-bottom: 0.5em; }
    .wrapped-pre { white-space: pre-wrap; word-break: break-word; background: #23232a; color: #fff; border-radius: 8px; padding: 1em; font-size: 1.1em; max-height: 350px; overflow-y: auto; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">audispot254 Content Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate concise social media content about automotive videos from audispot254\'s perspective. Perfect for Audi and car enthusiasts.</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader("Input")
    col1, col2 = st.columns([2, 3])
    with col1:
        video_id = st.text_input("YouTube Video ID", "6hr6wZr1N_8", help="The ID is the part after 'v=' in a YouTube URL. For example, in 'https://www.youtube.com/watch?v=6hr6wZr1N_8', the ID is '6hr6wZr1N_8'.")
    with col2:
        query = st.text_area("Your Query", "Create short, engaging posts for audispot254 based on this automotive video. Write from the perspective of someone who watched the video, not the creator.", height=80)
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

platforms = []
if linkedin:
    platforms.append("LinkedIn")
if instagram:
    platforms.append("Instagram")
if twitter:
    platforms.append("Twitter")

def extract_content(output, platform):
    # Try to parse as JSON or Python literal
    try:
        data = json.loads(output)
    except Exception:
        try:
            import ast
            data = ast.literal_eval(output)
        except Exception:
            data = None
    # If it's a list of dicts
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("platform", "").lower() == platform.lower():
                content = item.get("content", "")
                return clean_content(content)
    # If it's a dict
    if isinstance(data, dict):
        if data.get("platform", "").lower() == platform.lower():
            content = data.get("content", "")
            return clean_content(content)
    # Fallback: regex to extract 'content' value
    match = re.search(r'"?content"?\s*:\s*(["\']).*?\1', output, re.DOTALL)
    if match:
        content = match.group(0)
        content = re.sub(r'"?content"?\s*:\s*', '', content)
        content = content.strip('"\'')
        return clean_content(content)
    # Fallback: try to extract by header
    for header in [f"{platform} Post:", f"Platform: {platform}", f"{platform}:", f"{platform}"]:
        idx = output.lower().find(header.lower())
        if idx != -1:
            next_idx = len(output)
            for other in platforms:
                if other != platform:
                    for other_header in [f"{other} Post:", f"Platform: {other}", f"{other}:", f"{other}"]:
                        oidx = output.lower().find(other_header.lower(), idx + 1)
                        if oidx != -1 and oidx < next_idx:
                            next_idx = oidx
            content = output[idx + len(header):next_idx].strip()
            return clean_content(content)
    # Fallback: just return the output
    return clean_content(output)

def clean_content(content):
    # Replace all \n and \\n with real newlines, remove curly braces and 'content:'
    content = str(content)
    content = content.replace('\\n', '\n').replace('\n', '\n')
    content = re.sub(r'"?content"?\s*:\s*', '', content)
    content = content.strip(' {}[]"\'')
    return content

async def run_agent(query, video_id, platforms):
    transcript = get_transcript(video_id)
    if not transcript:
        return "Error: Could not fetch transcript. Please check the video ID."
    
    # Enhanced message for concise content
    platform_list = ", ".join(platforms)
    msg = f"{query}\n\nTarget platforms: {platform_list}\n\nCreate SHORT, engaging posts (not long content) from audispot254's perspective as someone who watched this video.\n\nVideo Transcript:\n{transcript}"
    
    input_items = [{"content": msg, "role": "user"}]
    with trace("Writing content"):
        result = await Runner.run(content_creator_agent, input_items)
        output = ItemHelpers.text_message_outputs(result.new_items)
        return output

if st.button("Generate Content", type="primary"):
    if not video_id.strip():
        st.error("Please enter a YouTube video ID")
    elif not platforms:
        st.error("Please select at least one platform")
    else:
        with st.spinner("Generating concise content... This may take a minute or two."):
            output = asyncio.run(run_agent(query, video_id, platforms))
            
            if output and not output.startswith("Error:"):
                st.markdown('<div class="section-title">Generated Content</div>', unsafe_allow_html=True)
                for platform in platforms:
                    content = extract_content(output, platform)
                    st.markdown(f'<div class="output-card">', unsafe_allow_html=True)
                    st.markdown(f'<b>{platform} Post</b><br><b>Platform:</b> {platform}<br><b>{platform} Content</b>', unsafe_allow_html=True)
                    st.markdown('<div class="copy-note">Click and drag to select, then copy (Ctrl+C or ⌘+C).</div>', unsafe_allow_html=True)
                    st.markdown(f'<pre class="wrapped-pre">{content}</pre>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                # Debug info
                with st.expander("Debug - Raw Output"):
                    st.text(output)
            else:
                st.error(output if output and output.startswith("Error:") else "Failed to generate content. Please try again.")