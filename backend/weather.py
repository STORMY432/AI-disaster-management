import requests

# ==========================================
# OpenWeather Configuration
# ==========================================
API_KEY = "315ffac4a2ba1386a4b9cb74f8cc65b7"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# ==========================================
# Get Current Weather
# ==========================================
def get_weather(city: str):
    """
    Fetch current weather information for a city.

    Returns:
    {
        "city": "...",
        "temperature": 30.2,
        "humidity": 72,
        "weather": "Light Rain",
        "wind_speed": 4.5
    }

    OR

    {
        "error": "message"
    }
    """

    if not city or city.strip() == "":
        return {
            "error": "City name cannot be empty."
        }

    params = {
        "q": city.strip(),
        "appid": API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
    "city": data["name"],
    "country": data["sys"]["country"],

    # NEW
    "lat": data["coord"]["lat"],
    "lon": data["coord"]["lon"],

    "temperature": round(data["main"]["temp"], 1),
    "feels_like": round(data["main"]["feels_like"], 1),
    "humidity": data["main"]["humidity"],
    "pressure": data["main"]["pressure"],
    "weather": data["weather"][0]["description"].title(),
    "wind_speed": data["wind"]["speed"],
    "visibility": data.get("visibility", 0) // 1000,
}

    except requests.exceptions.HTTPError:

        if response.status_code == 404:
            return {
                "error": "City not found."
            }

        if response.status_code == 401:
            return {
                "error": "Invalid OpenWeather API key."
            }

        return {
            "error": f"HTTP Error {response.status_code}"
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Weather service timed out."
        }

    except requests.exceptions.ConnectionError:
        return {
            "error": "Unable to connect to OpenWeather."
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ==========================================
# Testing
# ==========================================
if __name__ == "__main__":

    city = input("Enter city: ")

    result = get_weather(city)

    print("\nResult:\n")

    for key, value in result.items():
        print(f"{key}: {value}")