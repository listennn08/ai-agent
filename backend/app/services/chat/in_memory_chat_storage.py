import logging
from typing import Dict, List

from langchain_core.messages import BaseMessage
from .chat_storage_base import IChatStorage

main_logger = logging.getLogger("sipp")


class InMemoryChatStorage(IChatStorage):
    def __init__(self):
        main_logger.info("== Initialize ChatHistory ==")
        self.data: Dict[str, List[Dict]] = {}

    def init_user(self, user_id: str):
        self.data[user_id] = []

    def append_message(self, user_id: str, message: BaseMessage):
        self.data[user_id].append({"role": message.type, "message": message.content})

    def get_history(self, user_id: str) -> List[Dict]:
        return self.data.get(user_id, [])

    def clear(self, user_id: str):
        self.data.pop(user_id, None)
