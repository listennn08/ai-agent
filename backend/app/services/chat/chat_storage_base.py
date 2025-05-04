from abc import ABC, abstractmethod
from typing import List, Dict

from langchain_core.messages import BaseMessage


class IChatStorage(ABC):
    @abstractmethod
    async def init_user(self, user_id: str):
        pass

    @abstractmethod
    def append_message(self, user_id: str, message: BaseMessage):
        pass

    @abstractmethod
    def get_history(self, user_id: str) -> List[Dict]:
        pass

    @abstractmethod
    def clear(self, user_id: str):
        pass
