from abc import ABC, abstractmethod

from state import AgentState
from schemas import UserPreference


class IUserPreferenceService(ABC):
    @abstractmethod
    def get_user_preference(self, user_id: int) -> UserPreference:
        pass

    @abstractmethod
    def create_or_update_user_preference(
        self, user_id: int, state: AgentState
    ) -> UserPreference:
        pass

    @abstractmethod
    def delete_user_preference(self, user_id: int):
        pass
