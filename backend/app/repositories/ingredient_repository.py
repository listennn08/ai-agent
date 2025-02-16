from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Session

from db import Base

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    json_data = Column(JSON)


class IngredientRepository:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def batch_insert(self, ingredients):
        db_ingredients = [Ingredient(**ingredient) for ingredient in ingredients]
        self.db.bulk_save_objects(db_ingredients)
        self.db.commit()
        self.db.refresh()

        return db_ingredients

    def insert_ingredient(self, ingredient):
        db_ingredient = Ingredient(**ingredient)
        self.db.add(db_ingredient)
        self.db.commit()
        self.db.refresh(db_ingredient)

        return db_ingredient
    
    def get_ingredient_by_id(self, ingredient_id):
        db_ingredient = self.db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

        return db_ingredient
    
    def get_all_ingredients(self):
        return self.db.query(Ingredient).all()