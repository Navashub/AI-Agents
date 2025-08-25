import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient

async def main():
    load_dotenv()
    client = MCPClient.from_config_file(
        os.path.join(os.path.dirname(__file__), "config/browser_mcp.json")
    )
    
    # Create LLM with mock .bind_tools
    class OllamaWithTools(ChatOllama):
        def bind_tools(self, tools, **kwargs):
            return self  # Mock to bypass tool-calling check

    llm = OllamaWithTools(model="llama3.2")

    # Create agent
    agent = MCPAgent(llm=llm, client=client, max_steps=5, verbose=True)

    try:
        result = await agent.run("Find the best restaurant in Nairobi USING GOOGLE SEARCH", max_steps=5)
        print("Result type:", type(result))
        print(f"\nRESULT:\n\n{result if isinstance(result, str) else result.get('text', str(result))}\n\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client.sessions:
            print("Closing sessions:", client.sessions)
            await client.close_all_sessions()
        else:
            print("No open sessions")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()