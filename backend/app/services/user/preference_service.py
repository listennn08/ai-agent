from state import AgentState
from schemas import UserPreference
from repositories.user_preference_repository import UserPreferenceRepository
from .basic import IUserPreferenceService


class UserPreferenceService(IUserPreferenceService):
    def __init__(self, db_session):
        self.repo = UserPreferenceRepository(db_session)

    def create_or_update_user_preference(
        self, user_id: int, state: AgentState
    ) -> UserPreference:
        user_pref = self.repo.get_user_preference(user_id)
        if user_pref:
            self.repo.update_user_preference(user_id, state.keywords)
        else:
            self.repo.create_user_preference(user_id, state.keywords)
        return state

    def get_user_preference(self, user_id: int) -> UserPreference:
        return self.repo.get_user_preference(user_id)

    def delete_user_preference(self, user_id: int):
        return self.repo.delete_user_preference(user_id)
