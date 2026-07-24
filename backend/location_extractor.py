import re

# List of supported cities
CITIES = [
    "kolkata",
    "mumbai",
    "delhi",
    "chennai",
    "bengaluru",
    "hyderabad",
    "pune",
    "ahmedabad",
    "lucknow",
    "bhubaneswar",
    "visakhapatnam"
]


def extract_city(text: str):
    """
    Extract a city name from the user's question.
    Returns the city name with proper capitalization,
    or None if no city is found.
    """

    text = text.lower()

    for city in CITIES:
        if re.search(rf"\b{city}\b", text):
            return city.title()

    return None