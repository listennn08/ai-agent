from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
import json

from schemas import MessageResponse, UserInput
from services.drink_service import DrinkService
from depends import get_drink_service
from ai.utils import check_user_input_is_follow_up

router = APIRouter()
# record the history of interactions
history = []


@router.post("/generate")
def generate_drink(
    body: UserInput,
    drink_service: DrinkService = Depends(get_drink_service)
) -> MessageResponse:
    try:
        user_input = body.user_input
        selected_history = []

        # If has generated recipes, include in prompt
        recipes = []

        if check_user_input_is_follow_up(user_input, selected_history):
            trim_messages(
                messages=history,
                token_counter=len,
                max_tokens=5,
                strategy="last",
                start_on="human",
                include_system=True,
                allow_partial=False,
            )
        else:
            recipes = drink_service.retrieve(user_input)


        print(recipes)

        # Generate new drink idea
        response = drink_service.generate(user_input, recipes)

        history.append(HumanMessage(user_input))
        history.append(AIMessage(json.dumps(response.json())))

        return response
    except Exception as e:
        # print detail and line
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
