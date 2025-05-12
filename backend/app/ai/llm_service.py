import logging
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.configs.settings import settings

main_logger = logging.getLogger("sipp")


class LLMService:
    def __init__(self):
        main_logger.info("== Initialize LLMService ==")
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL
        )

    def get_llm(
        self, model: str = settings.LLM_MODEL, temperature: float = 0.8
    ) -> BaseChatModel:
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature,
        )
        return self.llm

    def get_embeddings(self):
        return self.embeddings
