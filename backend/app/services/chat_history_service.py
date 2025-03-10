from typing import List

from langchain_core.messages import HumanMessage, AIMessage


class ChatHistory:
    _instance = None
    history: List[str] = []

    def __new__(cls):
        if cls._instance is None:
            print("== Initialize ChatHistory ==")
            cls._instance = super(ChatHistory, cls).__new__(cls)
        return cls._instance

    def add_human_message(self, message: str):
        self.history.append(HumanMessage(message))

    def add_ai_message(self, message: str):
        self.history.append(AIMessage(message))

    def get_history(self):
        return self.history
