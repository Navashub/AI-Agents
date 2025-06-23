from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

from dotenv import load_dotenv
load_dotenv()

import asyncio


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args":["mathserver.py"], #ensure corrrect absolute path
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp/",
                "transport": "streamable_http",
            },
        }
    )

    import os
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    # model = ChatGroq(model="qwen-qwq-32b")
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_react_agent(
        model,
        tools
    )


    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is (3 + 5) * 12?"}]}
    )


    print("Math Response: ", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the weather in Nairobi?is it good for driving a convertible car?"}]}
    )
    print("Weather Response: ", weather_response['messages'][-1].content)

asyncio.run(main())




