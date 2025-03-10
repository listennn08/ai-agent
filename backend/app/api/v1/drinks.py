import json
from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from repositories.ingredient_repository import IngredientRepository
from repositories.drink_repository import DrinkRepository
from infrastructure.ingredient_vocab import IngredientVocabulary
from infrastructure.faiss_manager import FaissDrinkManager


router = APIRouter(
    prefix="/drinks",
    tags=["Drinks"],
)


@router.post("/")
def add_drinks(drinks: List[dict], db=Annotated[Session, Depends(get_db)]):
    repo = DrinkRepository(db)
    ingredient_vocab = IngredientVocabulary(IngredientRepository(db))
    faiss_manager = FaissDrinkManager(ingredient_vocab)
    return_drinks = []
    for drink in drinks:
        db_drink = repo.insert_drink(
            {
                "sku": drink["sku"],
                "name": drink["name"],
                "drink_category": drink["drink_category"],
                "json_data": json.dumps(drink),
            }
        )
        return_drinks.append({"id": db_drink.id, "ingredients": drink["ingredients"]})

    faiss_manager.batch_insert(return_drinks)

    return {"message": "Drinks added", "drinks": map(lambda d: d.id, return_drinks)}
