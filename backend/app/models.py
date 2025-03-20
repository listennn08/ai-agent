from sqlalchemy import Column, Integer, String, JSON

from db import Base


class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    drink_category = Column(String)
    json_data = Column(JSON)


class DrinkPhoto(Base):
    __tablename__ = "drink_photos"
    sku = Column(String, primary_key=True)
    photo = Column(String)
