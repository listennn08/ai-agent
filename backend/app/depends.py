from fastapi import Depends

from ai.llm_service import LLMService
from infrastructure.vector_store.vector_store import VectorStore
from services.drink_service import DrinkService
from services.chat_history_service import ChatHistory

def get_llm_service() -> LLMService:
    return LLMService()


def get_vector_store(llm_service = Depends(get_llm_service)) -> VectorStore:
    return VectorStore(embeddings=llm_service.get_embeddings())


def get_drink_service(vector_store = Depends(get_vector_store), llm_service = Depends(get_llm_service)):
    return DrinkService(vector_store=vector_store.vector_store, llm_service=llm_service)


def get_chat_history():
    return ChatHistory()