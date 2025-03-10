from fastapi import APIRouter, HTTPException, Depends
from services.drink_service import DrinkService
from depends import get_drink_service

router = APIRouter()


@router.get("/retrieve")
def retrieve_drink(
    user_input: str, drink_service: DrinkService = Depends(get_drink_service)
):
    try:
        # Retrieve relevant recipes
        return drink_service.retrieve(user_input)
    except HTTPException as e:
        return str(e)
