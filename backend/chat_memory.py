"""
chat_memory.py

Manages conversation history using LangChain's in-memory chat history.
"""

from langchain_core.chat_history import InMemoryChatMessageHistory

# Global chat history
chat_history = InMemoryChatMessageHistory()


def add_user_message(message: str):
    """
    Add a user message to memory.
    """
    chat_history.add_user_message(message)


def add_ai_message(message: str):
    """
    Add an AI response to memory.
    """
    chat_history.add_ai_message(message)


def get_chat_history() -> str:
    """
    Return the conversation history as formatted text.
    """

    history = []

    for msg in chat_history.messages:

        role = "User"

        if msg.type == "ai":
            role = "AI"

        history.append(f"{role}: {msg.content}")

    return "\n".join(history)


def clear_chat_history():
    """
    Clear the entire conversation history.
    """
    chat_history.clear()


def get_message_count():
    """
    Return the number of stored messages.
    """
    return len(chat_history.messages)