import os
import requests


from disaster_retriever import retrieve_disaster_docs



# -----------------------------
# Ollama Configuration
# -----------------------------

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "llama3.2:latest"




# -----------------------------
# Main AI Function
# -----------------------------

def ask_ai(question, disaster_type):


    # Retrieve disaster specific documents

    docs = retrieve_disaster_docs(
        question,
        disaster_type
    )



    # Create context

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )



    # Collect sources

    sources = []


    for doc in docs:


        source = doc.metadata.get(
            "source",
            "Unknown"
        )


        source = os.path.basename(source)


        source = os.path.splitext(source)[0]


        source = source.replace(
            "_",
            " "
        ).title()



        if source not in sources:

            sources.append(source)




    # Final Prompt

    final_prompt = f"""

You are DisasterAI, a disaster management assistant.

Use ONLY the information from the Context.

Rules:

- Do not invent information.
- Do not guess.
- If information is missing, say:
"I don't have information about that in my disaster knowledge base."

- Give practical emergency guidance.
- Use bullet points.
- Keep the answer clear.

Context:

{context}


Question:

{question}


Answer:

"""



    try:


        response = requests.post(

            OLLAMA_URL,

            json={

                "model": MODEL,

                "prompt": final_prompt,

                "stream": False

            },

            timeout=120

        )



        response.raise_for_status()



        answer = response.json()["response"]



        return {

            "answer": answer,

            "sources": sources

        }



    except requests.exceptions.RequestException as e:


        return {

            "answer":
            f"Error communicating with Ollama: {str(e)}",

            "sources": []

        }