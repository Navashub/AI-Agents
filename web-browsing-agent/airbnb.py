import asyncio
import os
from dotenv import load_dotenv
# from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from mcp_use import MCPAgent, MCPClient

async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient with Airbnb configuration
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "config/airbnb_mcp.json")
    )

    # Create LLM - you can choose between different models
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    llm = Ollama(model="llama3.2")
    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    try:
        # Run a query to search for accommodations
        result = await agent.run(
            "Find me a nice place to stay in Kisumu for 2 adults "
            "for a week in August. I prefer places with a balcony and "
            "good reviews. Show me the top 3 options.",
            max_steps=30,
        )
        print(f"\nRESULT:\n\n{result[0]['text']}\n\n")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())