import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main import get_ingredient_vocab, get_faiss_manager
from application.repositories.drink_repository import DrinkRepository, get_db
from application.services.ingredient_vocab import IngredientVocabulary
from application.services.faiss_manager import FaissDrinkManager


router = APIRouter(
    prefix="/drinks",
    tags=["Drinks"],
)

@router.post("/")
def add_drinks(
    drinks: List[dict],
    db: Session = Depends(get_db),
    vocab: IngredientVocabulary = Depends(get_ingredient_vocab),
    faiss_manager: FaissDrinkManager = Depends(get_faiss_manager)
):

    repo = DrinkRepository(db)
    return_drinks = []
    for drink in drinks:
        db_drink = repo.insert_drink({
            "sku": drink["sku"],
            "name": drink["name"],
            "drink_category": drink["drink_category"],
            "json_data": json.dumps(drink)
        })
        return_drinks.append({
            "id": db_drink.id,
            "ingredients": drink["ingredients"]
        })
    
    faiss_manager.batch_insert(return_drinks)

    return {
        "message": "Drinks added",
        "drinks": map(lambda d: d.id, return_drinks)
    }