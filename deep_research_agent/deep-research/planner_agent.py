from pydantic import BaseModel
from agents import Agent

HOW_MANY_SEARCHES = 10

INSTRUCTIONS = f"You are an automotive research specialist focusing on Audi cars and automotive history. Given an Audi-related query, \
create {HOW_MANY_SEARCHES} strategic web searches that will help create a comprehensive blog post about Audi. Focus on: brand history, \
iconic models, technological innovations, design evolution, racing heritage, company milestones, founders/key figures, manufacturing, \
and cultural impact. Prioritize searches that will provide engaging stories and fascinating details for blog readers."


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)