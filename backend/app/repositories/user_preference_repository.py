from sqlalchemy.orm import Session
from app.models import UserPreference


class UserPreferenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_preference(self, user_id: int, preferences: dict):
        user_pref = UserPreference(user_id=user_id, preferences=preferences)
        self.db.add(user_pref)
        self.db.commit()
        self.db.refresh(user_pref)
        return user_pref

    def get_user_preference(self, user_id: int):
        return (
            self.db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .first()
        )

    def update_user_preference(self, user_id: int, preferences: dict):
        user_pref = (
            self.db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .first()
        )
        if user_pref:
            user_pref.preferences = preferences
            self.db.commit()
            self.db.refresh(user_pref)
        return user_pref

    def delete_user_preference(self, user_id: int):
        user_pref = (
            self.db.query(UserPreference)
            .filter(UserPreference.user_id == user_id)
            .first()
        )
        if user_pref:
            self.db.delete(user_pref)
            self.db.commit()
        return user_pref
