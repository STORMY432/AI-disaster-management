from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


embedding = OllamaEmbeddings(model="nomic-embed-text")


def create_vectorstore():
    loader = DirectoryLoader(
        "data",
        glob="*.txt",
        loader_cls=TextLoader
    )

    docs = loader.load()

    vectorstore = FAISS.from_documents(
        docs,
        embedding
    )

    vectorstore.save_local("faiss_index")
    return vectorstore



if __name__ == "__main__":
    vectorstore = create_vectorstore()
    vectorstore.save_local("faiss_index")
    print("Vector database created successfully!")