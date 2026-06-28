import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 404:
        return {"error": f"City '{city}' not found."}
    if response.status_code != 200:
        return {"error": f"Weather API error: {response.status_code}"}

    data = response.json()
    return {
        "city": data["name"],
        "temperature": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"].capitalize(),
        "wind_speed": data["wind"]["speed"]
    }