from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from ai.llm import llm
from vector_store import vector_store
from schemas import DrinkRecipes


class DrinkRetrieveService:
    def __init__(self):
        pass
  
    @staticmethod
    def retrieve(query: str) -> DrinkRecipes:
        # Retrieve relevant recipes
        recipes = vector_store.similarity_search_with_relevance_scores(query, k=3)

        print(recipes)

        template = """
        Based on these recipes: {recipes}
        and the user's preference: {user_input},
        get the name and ingredients of the drink.
        If drinks do not have the flavors the user wanted, return an empty list.
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

        response = chain.invoke({ "user_input": query })

        return response
