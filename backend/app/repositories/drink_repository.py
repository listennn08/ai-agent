from sqlalchemy.orm import Session
from models import Drink


class DrinkRepository:
    def __init__(self, db_session: Session):
        self.db = next(db_session)

    def insert_drink(self, drink: Drink):
        db_drink = Drink(**drink)
        self.db.add(db_drink)
        self.db.commit()
        self.db.refresh(db_drink)

        return db_drink

    def get_drink_by_id(self, drink_id: int) -> Drink:
        db_drink = self.db.query(Drink).filter(Drink.id == drink_id).first()

        return db_drink

    def get_all_drinks(self) -> list[Drink]:
        return self.db.query(Drink).all()
