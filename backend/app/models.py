from sqlalchemy import Column, Integer, String, JSON

from app.db import Base, engine


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


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class UserPreference(Base):
    __tablename__ = "user_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    preferences = Column(JSON, default={})


Base.metadata.create_all(engine)
