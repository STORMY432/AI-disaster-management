import requests

# -----------------------------
# NewsAPI Configuration
# -----------------------------
API_KEY = "39c4dfeed0f443d08766e4ba3e31cef7"

BASE_URL = "https://newsapi.org/v2/everything"

# Disaster keywords
DISASTER_KEYWORDS = [
    "flood",
    "earthquake",
    "cyclone",
    "wildfire",
    "fire",
    "landslide",
    "tsunami",
    "storm",
    "hurricane",
    "typhoon",
    "heavy rain",
    "cloudburst",
    "heatwave",
    "disaster",
    "emergency",
    "evacuation",
]

# Words that indicate the article is NOT disaster-related
EXCLUDED_KEYWORDS = [
    "football",
    "cricket",
    "formula 1",
    "f1",
    "tennis",
    "ipl",
    "movie",
    "cinema",
    "actor",
    "actress",
    "election",
    "politics",
    "minister",
    "stock",
    "share market",
    "celebrity",
    "entertainment",
]


def get_disaster_news(city=None, disaster=None):
    """
    Fetch latest disaster-related news.
    """

    if disaster and city:
        query = (
            f'("{disaster}" OR flood OR earthquake OR cyclone OR wildfire '
            f'OR landslide OR tsunami OR "heavy rain") AND "{city}"'
        )

    elif disaster:
        query = (
            f'"{disaster}" OR flood OR earthquake OR cyclone '
            f'OR wildfire OR landslide OR tsunami OR "heavy rain"'
        )

    elif city:
        query = (
            f'(flood OR earthquake OR cyclone OR wildfire '
            f'OR landslide OR tsunami OR "heavy rain") AND "{city}"'
        )

    else:
        query = (
            'flood OR earthquake OR cyclone OR wildfire '
            'OR landslide OR tsunami OR "heavy rain"'
        )

    try:

        response = requests.get(
            BASE_URL,
            params={
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 15,   # Fetch more so filtering still leaves enough
                "apiKey": API_KEY,
            },
            timeout=10,
        )

        data = response.json()

        if data.get("status") != "ok":
            return []

        articles = []

        for article in data.get("articles", []):

            title = article.get("title", "")
            description = article.get("description", "")

            full_text = f"{title} {description}".lower()

            # Skip non-disaster news
            if any(word in full_text for word in EXCLUDED_KEYWORDS):
                continue

            # Keep only articles containing disaster-related words
            if not any(word in full_text for word in DISASTER_KEYWORDS):
                continue

            articles.append(
                {
                    "title": title,
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name"),
                }
            )

            # Return only top 5 filtered articles
            if len(articles) == 5:
                break

        return articles

    except Exception as e:
        print("News Error:", e)
        return []