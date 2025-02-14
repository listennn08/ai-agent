from fastapi import APIRouter, HTTPException
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from application.ai.llm import llm
from models import DrinkRecipes
from vector_store import vector_store

router = APIRouter()

@router.get("/retrieve")
def retrieve_drink(user_input: str):
    try:
        # Retrieve relevant recipes
        recipes = vector_store.similarity_search_with_relevance_scores(user_input)

        print(recipes)

        template = """
        Based on these recipes: {recipes}
        and the user's preference: {user_input},
        get the name and ingredients of the drink.
        If no drink is found, return an empty list.
        The second value is the relevant score.

        {format_instructions}
        """

        parser = PydanticOutputParser(pydantic_object=DrinkRecipes)

        prompt = PromptTemplate(
            template=template,
            input_variables=["user_input"],
            partial_variables={
                "recipes": recipes,
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = prompt | llm | parser

        response = chain.invoke({ "user_input": user_input })

        return response
    except HTTPException as e:
        return str(e)