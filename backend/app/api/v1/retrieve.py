from fastapi import APIRouter, HTTPException, Depends
from services.drink_retrieve_service import DrinkRetrieveService
from .depends import get_drink_retrieve_service

router = APIRouter()

@router.get("/retrieve")
def retrieve_drink(user_input: str, drink_retrieve_service: DrinkRetrieveService = Depends(get_drink_retrieve_service)):
    try:
        # Retrieve relevant recipes
        return drink_retrieve_service.retrieve(user_input)
    except HTTPException as e:
        return str(e)