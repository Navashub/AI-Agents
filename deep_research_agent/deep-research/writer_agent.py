from pydantic import BaseModel
from agents import Agent

INSTRUCTIONS = (
    "You are a professional automotive blogger specializing in luxury car brands, particularly Audi. "
    "You will be provided with research findings about Audi and should create an engaging, well-structured blog post. "
    "Write in a compelling narrative style that combines historical storytelling with technical insights. "
    "Structure your blog post with: an engaging introduction, multiple themed sections with descriptive headings, "
    "fascinating anecdotes and human stories, technical details explained accessibly, and a memorable conclusion. "
    "Use markdown formatting with proper headers, and aim for 2000-3000 words that will captivate car enthusiasts "
    "and general readers alike. Include specific dates, model names, and interesting facts throughout."
)


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)