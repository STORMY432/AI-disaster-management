import os

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)


vectorstore = FAISS.load_local(
    "faiss_index",
    embedding,
    allow_dangerous_deserialization=True
)



def retrieve_disaster_docs(question, disaster_type):

    docs = vectorstore.similarity_search(
        question,
        k=5
    )


    filtered_docs = []


    for doc in docs:

        source = doc.metadata.get(
            "source",
            ""
        ).lower()


        if disaster_type in source:

            filtered_docs.append(doc)


    return filtered_docs