import os
import requests
from datetime import datetime
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType, Tool
from langchain_core.tools import tool
from langchain_community.llms import Together

load_dotenv()

class OpenWeatherMapTool(Tool):
    def __init__(self):
        super().__init__(
            name="OpenWeatherMap",
            description=(
                "Use this tool to get the current weather in a city. "
                "Only give the city name, for example: 'Delhi'."
            ),
            func=self._run,
        )

    def _run(self, city: str) -> str:
        api_key = os.environ["OPENWEATHER_API_KEY"]
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(complete_url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] != 200:
                return f"Error fetching weather for {city}. API says: {data['message']}"

            main = data["main"]
            weather = data["weather"][0]
            wind = data["wind"]
            sys_info = data["sys"]
            city_name = data["name"]
            clouds = data["clouds"]["all"]

            sunrise_ts = sys_info["sunrise"]
            sunset_ts = sys_info["sunset"]
            sunrise_time = datetime.fromtimestamp(sunrise_ts).strftime("%H:%M")
            sunset_time = datetime.fromtimestamp(sunset_ts).strftime("%H:%M")

            weather_desc = weather["description"]
            umbrella_needed = (
                "rain" in weather_desc or
                "drizzle" in weather_desc or
                "thunderstorm" in weather_desc or
                "snow" in weather_desc or
                "mist" in weather_desc or
                "fog" in weather_desc or
                weather["main"].lower() in ["rain", "drizzle", "thunderstorm", "snow"]
            )

            umbrella_msg = "Yes, you might want to carry an umbrella." if umbrella_needed else "No umbrella needed."

            return (
                f"Current weather in {city_name}: {weather_desc}. "
                f"Temperature: {main['temp']}°C (feels like {main['feels_like']}°C). "
                f"Min: {main['temp_min']}°C, Max: {main['temp_max']}°C. "
                f"Humidity: {main['humidity']}%. Pressure: {main['pressure']} hPa. "
                f"Wind speed: {wind['speed']} m/s. Cloudiness: {clouds}%. "
                f"Sunrise: {sunrise_time}, Sunset: {sunset_time}. "
                f"Umbrella suggestion: {umbrella_msg}"
            )

        except Exception as e:
            return f"Error: {str(e)}"

    

def main():
    if "TOGETHER_API_KEY" not in os.environ:
        print("TOGETHER_API_KEY is not set.")
        return
    if "OPENWEATHER_API_KEY" not in os.environ:
        print("OPENWEATHER_API_KEY is not set.")
        return

    llm = Together(
        model="meta-llama/Llama-3-8b-chat-hf",  
        temperature=0,
        together_api_key=os.environ["TOGETHER_API_KEY"]
    )

    weather_tool = OpenWeatherMapTool()
    tools = [weather_tool]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    prompt = "What's the current weather in vijayawada and should I carry an umbrella?"

    print(f"\n--- Asking: {prompt} ---\n")
    try:
        result = agent.invoke(prompt)
        print("\n--- Answer ---\n")
        print(result)
    except Exception as e:
        print(f"Agent failed: {e}")

if __name__ == "__main__":
    main()
