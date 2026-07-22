import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3.2:latest"



def contains_keywords(text, keywords):

    for keyword in keywords:

        if keyword in text:
            return True

    return False



def classify_disaster(question: str):

    query = question.lower()



    # -----------------------------
    # Rule based detection
    # -----------------------------


    # Tsunami has highest priority
    tsunami_words = [
        "tsunami",
        "huge wave",
        "giant wave",
        "massive wave",
        "ocean wave",
        "sea water",
        "sea level",
        "coastal flooding",
        "coast",
        "wave coming",
        "wave is coming",
        "water moving inland"
    ]


    if contains_keywords(query, tsunami_words):

        return "tsunami"



    earthquake_words = [
        "earthquake",
        "ground shaking",
        "ground is shaking",
        "tremor",
        "seismic",
        "building shaking"
    ]


    if contains_keywords(query, earthquake_words):

        return "earthquake"



    flood_words = [
        "flood",
        "flooded",
        "heavy rain",
        "river overflow",
        "water entering",
        "flash flood"
    ]


    if contains_keywords(query, flood_words):

        return "flood"



    cyclone_words = [
        "cyclone",
        "hurricane",
        "strong wind",
        "storm",
        "wind damage"
    ]


    if contains_keywords(query, cyclone_words):

        return "cyclone"



    wildfire_words = [
        "wildfire",
        "forest fire",
        "fire spreading",
        "smoke from fire"
    ]


    if contains_keywords(query, wildfire_words):

        return "wildfire"



    landslide_words = [
        "landslide",
        "mudslide",
        "rock fall",
        "soil collapse"
    ]


    if contains_keywords(query, landslide_words):

        return "landslide"



    # -----------------------------
    # AI fallback
    # -----------------------------

    prompt = f"""

Classify the disaster type.

Categories:

earthquake
flood
cyclone
wildfire
landslide
tsunami
general


Question:

{question}


Return only category name.

"""


    try:

        response = requests.post(

            OLLAMA_URL,

            json={

                "model": MODEL,
                "prompt": prompt,
                "stream": False

            },

            timeout=60

        )


        result = response.json()["response"].strip().lower()


        categories = [
            "earthquake",
            "flood",
            "cyclone",
            "wildfire",
            "landslide",
            "tsunami",
            "general"
        ]


        for category in categories:

            if category in result:

                return category



        return "general"



    except Exception as e:

        print("Classifier Error:", e)

        return "general"