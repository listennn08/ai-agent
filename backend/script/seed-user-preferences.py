import sys
import os

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "../app"))


from sqlalchemy.orm import Session  # noqa: E402
from db import SessionLocal  # noqa: E402
from models import UserPreference  # noqa: E402


def seed_user_preferences():
    db: Session = SessionLocal()
    demo_prefs = [
        {"user_id": 1, "preferences": {"sweetness": "high", "caffeine": "low"}},
        {"user_id": 2, "preferences": {"sweetness": "medium", "caffeine": "high"}},
        # Add more demo users if needed
    ]
    for pref in demo_prefs:
        existing = db.query(UserPreference).filter_by(user_id=pref["user_id"]).first()
        if existing:
            existing.preferences = pref["preferences"]
        else:
            db.add(UserPreference(**pref))
    db.commit()
    db.close()
    print("Seeded user preferences!")


if __name__ == "__main__":
    seed_user_preferences()
