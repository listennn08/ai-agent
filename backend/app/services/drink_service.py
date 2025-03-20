from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore

from schemas import DrinkRecipes, MessageResponse, KeywordMessage
from repositories.drink_photo_repository import DrinkPhotoRepository
from ai.llm_service import LLMService
from prompts import WELCOME_PROMPT, RECOMMENDATION_PROMPT, CLARIFICATION_PROMPT


class DrinkService:
    """
    Service for retrieving drink recipes from vector store
    """

    _instance: "DrinkService" = None
    vector_store: VectorStore
    llm_service: LLMService
    drink_photo_repository: DrinkPhotoRepository

    def __new__(
        cls,
        vector_store: VectorStore,
        llm_service: LLMService,
        drink_photo_repository: DrinkPhotoRepository,
    ):
        """
        Initialize the service with a vector store
        """
        if cls._instance is None:
            print("== Initialize DrinkService ==")
            cls._instance = super(DrinkService, cls).__new__(cls)
            cls._instance.vector_store = vector_store
            cls._instance.llm_service = llm_service
            cls._instance.drink_photo_repository = drink_photo_repository

        return cls._instance

    def generate_welcome_message(self, history: list) -> str:
        """
        Generate a welcome message for the user
        """
        llm = self.llm_service.get_llm()
        chain = WELCOME_PROMPT | llm

        response = chain.invoke({"history": history})

        return response.content

    def verify_user_input_and_get_clarification(
        self, user_input: str, context: str
    ) -> str:
        """
        Verify the user's input and get clarification
        """
        llm = self.llm_service.get_llm()
        parser = PydanticOutputParser(pydantic_object=KeywordMessage)
        prompt = PromptTemplate(
            template=CLARIFICATION_PROMPT,
            input_variables=["user_input", "context"],
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        response = chain.invoke({"user_input": user_input, "context": context})

        print(response)

        return response

    def retrieve(self, query: str) -> DrinkRecipes:
        """
        Retrieve drink recipes from vector store, based on the user's preference
        Args:
            query: The query to retrieve drink recipes from
        Returns:
            A list of drink recipes
        """

        llm = self.llm_service.get_llm()
        # Retrieve relevant recipes
        drinks = self.vector_store.similarity_search_with_relevance_scores(query, k=3)

        print(drinks)

        # parser = PydanticOutputParser(pydantic_object=DrinkRecipes)
        parser = PydanticOutputParser(pydantic_object=MessageResponse)

        prompt = PromptTemplate(
            template=RECOMMENDATION_PROMPT,
            input_variables=["user_input"],
            partial_variables={
                "drinks": drinks,
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        response = chain.invoke({"user_input": query})

        return response

    def generate(
        self, user_input: str, recipes: list, history: list
    ) -> MessageResponse:
        """
        Generate a new drink recipe based on the user's preference
        Args:
            user_input: The user's preference
            recipes: The recipes based on the user's preference
            history: The history of the conversation
        Returns:
            A new drink recipe
        """

        llm = self.llm_service.get_llm()

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
                "format_instructions": parser.get_format_instructions(),
            },
        )

        chain = prompt | llm | parser

        response = chain.invoke({"user_input": user_input})

        return response

    def get_drink_photo(self, sku: str) -> str:
        """
        Get the photo of a drink
        """

        drink_photo = self.drink_photo_repository.get_drink_photo(sku)

        if drink_photo:
            return drink_photo.photo
        else:
            return ""
