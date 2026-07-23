import requests

# Replace with your own API key
API_KEY = "315ffac4a2ba1386a4b9cb74f8cc65b7"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str):

    try:

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"].title(),
            "wind_speed": data["wind"]["speed"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }