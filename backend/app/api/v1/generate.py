from fastapi import APIRouter, Depends, HTTPException
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
import json

from ai.llm import llm
from schemas import BooleanModel, MessageResponse, UserInput
from services.drink_retrieve_service import DrinkRetrieveService
from depends import get_drink_retrieve_service

router = APIRouter()
# record the history of interactions
history = []


@router.post("/generate")
def generate_drink(
    body: UserInput,
    drink_retrieve_service: DrinkRetrieveService = Depends(get_drink_retrieve_service)
) -> MessageResponse:
    try:
        user_input = body.user_input
        selected_history = []

        # If has generated recipes, include in prompt
        recipes = []

        if _check_user_input_is_follow_up(user_input, selected_history):
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
            recipes = drink_retrieve_service.retrieve(user_input)


        print(recipes)

        # Generate new drink idea
        template = """
        history of the conversation: {history}
        recipes based on user description: {recipes}
        user's description: {user_input}.
        ---
        Please according above information, create a new unique drink recipe.
        the logic of drink reference adopted: history -> recipes, if all history and recipes are empty do not generate new drink

        {format_instructions}
        """

        parser = PydanticOutputParser(pydantic_object=MessageResponse)
        prompt = PromptTemplate(
            template=template,
            input_variables=["user_input", "history"],
            partial_variables={
                "recipes": recipes,
                "history": selected_history,
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = prompt | llm | parser

        response = chain.invoke({ "user_input": user_input })

        history.append(HumanMessage(user_input))
        history.append(AIMessage(json.dumps(response.json())))

        return response
    except Exception as e:
        # print detail and line
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def _check_user_input_is_follow_up(user_input: str, history: list) -> bool:
    template = """
    Based on the history: {history}
    and the user's input: {user_input},
    is this a follow up question?
    
    {format_instructions}
    """

    parser = PydanticOutputParser(pydantic_object=BooleanModel)

    prompt = PromptTemplate(
        template=template,
        input_variables=["user_input"],
        partial_variables={
            "history": history,
            "format_instructions": parser.get_format_instructions()
        }
    )

    chain = prompt | llm | parser

    response = json.loads(chain.invoke({ "user_input": user_input }).json())
    return response.get("bool_value", False)