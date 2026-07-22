from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


from router import route_query
from classifier import classify_disaster
from severity_classifier import classify_severity



app = FastAPI(

    title="AI Disaster Management API",

    description="Backend API for AI-powered Disaster Management System",

    version="2.0.0"

)



# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



# -----------------------------
# Request Model
# -----------------------------

class ChatRequest(BaseModel):

    prompt: str




# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
def home():

    return {

        "status": "running",

        "message":
        "AI Disaster Management Backend is running successfully"

    }




# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    try:


        user_prompt = request.prompt



        # Detect disaster type

        disaster_type = classify_disaster(
            user_prompt
        )



        # Detect emergency severity

        severity = classify_severity(
            user_prompt
        )



        # Send to correct disaster agent

        ai_response = route_query(
            user_prompt
        )



        return {


            "disaster": disaster_type,


            "severity": severity,


            "answer": ai_response["answer"],


            "sources": ai_response["sources"]


        }



    except Exception as e:


        return {

            "error": str(e)

        }





# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():

    return {


        "status": "healthy",


        "backend": "FastAPI",


        "ai_model": "llama3.2:latest"


    }