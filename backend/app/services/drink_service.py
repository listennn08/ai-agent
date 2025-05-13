import logging
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.vectorstores import VectorStore

from app.ai.llm_service import LLMService
from app.ai.prompts.utils import build_llm_context, build_prompt
from app.ai.prompts.templates import (
    WELCOME_PROMPT,
    RECOMMENDATION_PROMPT,
    CLARIFICATION_PROMPT,
    EXTRACT_KEYWORDS_PROMPT,
)
from app.configs.settings import settings
from app.services.chat.chat_storage_base import IChatStorage
from app.services.user.basic import IUserPreferenceService
from app.repositories.drink_photo_repository import DrinkPhotoRepository
from app.schemas import MessageResponse, KeywordMessage
from app.state import AgentState


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
        user_preference_service: IUserPreferenceService,
    ):
        """
        Initialize the service with a vector store
        """
        main_logger.info("== Initialize DrinkService ==")
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.drink_photo_repository = drink_photo_repository
        self.chat_storage = chat_storage
        self.user_preference_service = user_preference_service

    def generate_welcome_message(self, sid: str) -> str:
        """
        Generate a welcome message for the user
        """
        if not settings.ENABLE_AI_WELCOME_MESSAGE:
            return "🍹 Welcome! I'm your exclusive bartender, please tell me your preferences, I will recommend the perfect drink for you!"

        llm = self.llm_service.get_llm()
        context = build_llm_context(
            sid=sid,
            agent_state=AgentState(),
            chat_storage=self.chat_storage,
            user_preference_service=self.user_preference_service,
        )
        prompt = build_prompt(
            template=WELCOME_PROMPT,
            input_variables=["history"],
            partial_variables={"preferences": context["preferences"]},
        )
        chain = prompt | llm

        response = chain.invoke({"history": context["history"]})

        return response.content

    def extract_keywords(self, sid: str, agent_state: AgentState) -> AgentState:
        """
        Extract keywords about taste/flavor or drink-related description from the user's request.
        """
        main_logger.debug(f"{sid} - Extracting keywords...")
        llm = self.llm_service.get_llm()
        parser = PydanticOutputParser(pydantic_object=KeywordMessage)
        context = build_llm_context(
            sid=sid,
            agent_state=agent_state,
            chat_storage=self.chat_storage,
            user_preference_service=self.user_preference_service,
        )
        prompt = build_prompt(
            template=EXTRACT_KEYWORDS_PROMPT,
            input_variables=["user_input", "context", "keywords"],
            format_instructions=parser.get_format_instructions(),
            partial_variables={"preferences": context["preferences"]},
        )

        chain = prompt | llm | parser

        result: KeywordMessage = chain.invoke(
            {
                "user_input": context["user_input"],
                "context": context["history"],
                "keywords": agent_state.keywords,
            }
        )
        agent_state.keywords.extend(result.keywords)
        agent_state.anti_keywords.extend(result.anti_keywords)

        main_logger.debug(f"{sid} - Extracted keywords: {agent_state.keywords}")
        return agent_state

    def verify_user_input_and_get_clarification(
        self, sid: str, agent_state: AgentState
    ) -> AgentState:
        """
        Verify the user's input and get clarification
        """
        main_logger.debug(f"{sid} - Verifying user input...")
        llm = self.llm_service.get_llm()
        parser = PydanticOutputParser(pydantic_object=KeywordMessage)
        context = build_llm_context(
            sid=sid,
            agent_state=agent_state,
            chat_storage=self.chat_storage,
            user_preference_service=self.user_preference_service,
        )
        prompt = build_prompt(
            template=CLARIFICATION_PROMPT,
            input_variables=["user_input", "keywords", "anti_keywords"],
            format_instructions=parser.get_format_instructions(),
            partial_variables={"preferences": context["preferences"]},
        )

        chain = prompt | llm | parser

        result: KeywordMessage = chain.invoke(
            {
                "user_input": context["user_input"],
                "keywords": agent_state.keywords,
                "anti_keywords": agent_state.anti_keywords,
            }
        )

        self.chat_storage.append_message(sid, AIMessage(result.message))

        main_logger.debug(f"{sid} - Verified user input: {result}")
        return agent_state

    def retrieve(self, sid: str, agent_state: AgentState) -> AgentState:
        """
        Retrieve drink recipes from vector store, based on the user's preference
        Args:
            agent_state: The agent state
        Returns:
            A list of drink recipes
        """

        main_logger.debug(f"{sid} - Retrieving drinks...")

        llm = self.llm_service.get_llm()
        # Retrieve relevant recipes
        drinks = self.vector_store.similarity_search_with_relevance_scores(
            ", ".join(agent_state.keywords), k=3
        )

        context = build_llm_context(
            sid=sid,
            agent_state=agent_state,
            chat_storage=self.chat_storage,
            user_preference_service=self.user_preference_service,
        )
        parser = PydanticOutputParser(pydantic_object=MessageResponse)

        prompt = build_prompt(
            template=RECOMMENDATION_PROMPT,
            input_variables=["user_input"],
            format_instructions=parser.get_format_instructions(),
            partial_variables={"drinks": drinks, "preferences": context["preferences"]},
        )

        chain = prompt | llm | parser

        result: MessageResponse = chain.invoke(
            {
                "user_input": context["user_input"],
                "context": context["history"],
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

        main_logger.debug(f"{sid} - Retrieved drinks: {agent_state.drinks}")
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
