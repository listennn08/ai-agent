from sqlalchemy import Column, Integer, String, JSON

from db import Base


class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    drink_category = Column(String)
    json_data = Column(JSON)


class DrinkRepository:
    def __init__(self, db_session):
        self.db = db_session

    def insert_drink(self, drink):
        db_drink = Drink(**drink)
        self.db.add(db_drink)
        self.db.commit()
        self.db.refresh(db_drink)

        return db_drink

    def get_drink_by_id(self, drink_id):
        db_drink = self.db.query(Drink).filter(Drink.id == drink_id).first()

        return db_drink

    def get_all_drinks(self):
        return self.db.query(Drink).all()
