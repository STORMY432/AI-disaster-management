from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatbot import ask_ai
from classifier import classify_disaster
from severity_classifier import classify_severity
from location_extractor import extract_city
from weather import get_weather
from news import get_disaster_news

app = FastAPI(
    title="AI Disaster Management API",
    description="AI-powered Disaster Management System",
    version="3.0.0"
)

# ---------------------------------
# Enable CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Request Model
# ---------------------------------

class ChatRequest(BaseModel):
    prompt: str


# ---------------------------------
# Root Endpoint
# ---------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "message": "AI Disaster Management Backend is running successfully"
    }


# ---------------------------------
# Chat Endpoint
# ---------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    question = request.prompt

    # Detect disaster type
    disaster = classify_disaster(question)

    # Detect severity
    severity = classify_severity(question)

    # Detect city
    city = extract_city(question)

    # Get weather
    weather = None

    if city:
        weather = get_weather(city)

    # Get AI response
    result = ask_ai(question, disaster)

    # Get latest disaster news
    news = get_disaster_news(city, disaster)

    return {

        "disaster": disaster,

        "severity": severity,

        "weather": weather,

        "news": news,

        "answer": result["answer"],

        "sources": result["sources"]

    }


# ---------------------------------
# Health Check
# ---------------------------------

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "backend": "FastAPI",

        "model": "llama3.2",

        "weather_api": "OpenWeatherMap",

        "news_api": "NewsAPI"

    }