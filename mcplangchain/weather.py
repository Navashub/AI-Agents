# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Weather")

# @mcp.tool()
# async def get_weather(location: str) -> str:
#     """"Get the weather for a given location"""
#     return f"The weather in {location} is sunny"

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")


from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Weather")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@mcp.tool()
async def get_weather(location: str) -> dict:
    """Get the current weather in a given location and return structured data"""
    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            data = response.json()

            if response.status_code != 200:
                return {
                    "error": f"Could not fetch weather for {location}: {data.get('message', 'Unknown error')}"
                }

            weather = data["weather"][0]["description"]
            temp = round(data["main"]["temp"], 1)
            feels_like = round(data["main"]["feels_like"], 1)
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]

            return {
                "location": location,
                "description": weather,
                "temperature_c": temp,
                "feels_like_c": feels_like,
                "humidity_percent": humidity,
                "wind_speed_mps": wind
            }

        except Exception as e:
            return {"error": f"Exception occurred: {str(e)}"}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

