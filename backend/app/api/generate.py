from fastapi import APIRouter, HTTPException
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
import json

from llm import llm
from vector_store import vector_store
from models import BooleanModel, MessageResponse, UserInput

router = APIRouter()
# record the history of interactions
history = []

@router.post("/generate")
def generate_drink(body: UserInput):
    try:
        user_input = body.user_input
        selected_history = trim_messages(
            messages=history,
            token_counter=len,
            max_tokens=5,
            strategy="last",
            start_on="human",
            include_system=True,
            allow_partial=False,
        )

        # If has generated recipes, include in prompt
        recipes = []

        if _check_user_input_is_follow_up(user_input, selected_history):
            recipes = vector_store.similarity_search_with_score(user_input, k=3)

        recipes = [recipe for recipe, score in recipes if score > 0.2]

        # Generate new drink idea
        template = """
        Here is the history of the conversation: {history}
        ---
        Based on these recipes: {recipes} and the user's description: {user_input}.
        According user description, create a new unique drink recipe or get previous generated drink from history.
        If recipes and history are empty, do not generate a new drink. and explain why no need to mention history.

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


def _check_user_input_is_follow_up(user_input: str, history: list):
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