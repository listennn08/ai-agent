import logging
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.vectorstores import VectorStore

from .chat.chat_storage_base import IChatStorage
from schemas import MessageResponse, KeywordMessage
from repositories.drink_photo_repository import DrinkPhotoRepository
from ai.llm_service import LLMService
from ai.prompts.utils import build_prompt
from ai.prompts.templates import (
    WELCOME_PROMPT,
    RECOMMENDATION_PROMPT,
    CLARIFICATION_PROMPT,
    EXTRACT_KEYWORDS_PROMPT,
)
from state import AgentState


main_logger = logging.getLogger("sipp")


class DrinkService:
    """
    Service for retrieving drink recipes from vector store
    """

    vector_store: VectorStore
    llm_service: LLMService
    drink_photo_repository: DrinkPhotoRepository

    def __init__(
        self,
        vector_store: VectorStore,
        llm_service: LLMService,
        drink_photo_repository: DrinkPhotoRepository,
        chat_storage: IChatStorage,
    ):
        """
        Initialize the service with a vector store
        """
        main_logger.info("== Initialize DrinkService ==")
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.drink_photo_repository = drink_photo_repository
        self.chat_storage = chat_storage

    def generate_welcome_message(self, sid: str) -> str:
        """
        Generate a welcome message for the user
        """
        llm = self.llm_service.get_llm()
        prompt = build_prompt(
            template=WELCOME_PROMPT,
            input_variables=["history"],
        )
        chain = prompt | llm

        response = chain.invoke({"history": self.chat_storage.get_history(sid)})

        return response.content

    def extract_keywords(self, sid: str, agent_state: AgentState) -> AgentState:
        """
        Extract keywords about taste/flavor or drink-related description from the user's request.
        """
        llm = self.llm_service.get_llm()
        parser = PydanticOutputParser(pydantic_object=KeywordMessage)
        prompt = build_prompt(
            template=EXTRACT_KEYWORDS_PROMPT,
            input_variables=["user_input", "context"],
            format_instructions=parser.get_format_instructions(),
        )

        chain = prompt | llm | parser

        result: KeywordMessage = chain.invoke(
            {
                "user_input": agent_state.query[-1],
                "context": self.chat_storage.get_history(sid),
            }
        )
        self.chat_storage.append_message(sid, AIMessage(result.message))
        agent_state.keywords = result.keywords
        agent_state.anti_keywords = result.anti_keywords

        return agent_state

    def verify_user_input_and_get_clarification(
        self, sid: str, agent_state: AgentState
    ) -> AgentState:
        """
        Verify the user's input and get clarification
        """
        llm = self.llm_service.get_llm()
        parser = PydanticOutputParser(pydantic_object=KeywordMessage)
        prompt = build_prompt(
            template=CLARIFICATION_PROMPT,
            input_variables=["user_input", "keywords", "anti_keywords"],
            format_instructions=parser.get_format_instructions(),
        )

        chain = prompt | llm | parser

        result: KeywordMessage = chain.invoke(
            {
                "user_input": agent_state.query[-1],
                "keywords": agent_state.keywords,
                "anti_keywords": agent_state.anti_keywords,
            }
        )

        self.chat_storage.append_message(sid, AIMessage(result.message))

        return agent_state

    def retrieve(self, sid: str, agent_state: AgentState) -> AgentState:
        """
        Retrieve drink recipes from vector store, based on the user's preference
        Args:
            agent_state: The agent state
        Returns:
            A list of drink recipes
        """

        llm = self.llm_service.get_llm()
        # Retrieve relevant recipes
        drinks = self.vector_store.similarity_search_with_relevance_scores(
            ", ".join(agent_state.keywords), k=3
        )

        parser = PydanticOutputParser(pydantic_object=MessageResponse)

        prompt = build_prompt(
            template=RECOMMENDATION_PROMPT,
            input_variables=["user_input"],
            format_instructions=parser.get_format_instructions(),
            partial_variables={"drinks": drinks},
        )

        chain = prompt | llm | parser

        result: MessageResponse = chain.invoke(
            {
                "user_input": agent_state.query[-1],
                "context": self.chat_storage.get_history(sid),
            }
        )
        agent_state.drinks = result.drinks

        if len(agent_state.drinks) > 0:
            self.chat_storage.append_message(sid, AIMessage(result.message))
        else:
            self.chat_storage.append_message(
                sid,
                AIMessage(
                    "I'm sorry, I don't have any drinks that match your preferences."
                ),
            )

        return agent_state

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
        prompt = build_prompt(
            template=template,
            input_variables=["user_input", "history"],
            format_instructions=parser.get_format_instructions(),
            partial_variables={
                "recipes": recipes,
                "history": history,
            },
        )

        chain = prompt | llm | parser

        payload = {
            "user_input": user_input,
            "history": history,
        }
        main_logger.info(f"Prompt template: {prompt.format(payload)}")
        response = chain.invoke(payload)

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
