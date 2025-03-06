
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore

from ai.llm import get_llm
from schemas import DrinkRecipes, MessageResponse


class DrinkService:
    """
    Service for retrieving drink recipes from vector store
    """

    _instance = None
    def __new__(cls, vector_store: VectorStore):
        """
        Initialize the service with a vector store
        """
        if cls._instance is None:
            print("== Initialize DrinkService ==")
            cls._instance = super(DrinkService, cls).__new__(cls)
            cls._instance.vector_store = vector_store
        return cls._instance

    def retrieve(self, query: str) -> DrinkRecipes:
        """
        Retrieve drink recipes from vector store, based on the user's preference
        Args:
            query: The query to retrieve drink recipes from
        Returns:
            A list of drink recipes
        """

        llm = get_llm()
        # Retrieve relevant recipes
        recipes = self.vector_store.similarity_search_with_relevance_scores(query, k=3)

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


    def generate(self, user_input: str, recipes: list, history: list ) -> MessageResponse:
        """
        Generate a new drink recipe based on the user's preference
        Args:
            user_input: The user's preference
            recipes: The recipes based on the user's preference
            history: The history of the conversation
        Returns:
            A new drink recipe
        """

        llm = get_llm()

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
                "history": history,
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = prompt | llm | parser

        response = chain.invoke({ "user_input": user_input })

        return response
