from fastapi import Depends

from ai.llm_service import LLMService
from infrastructure.vector_store.vector_store import VectorStore
from services.drink_retrieve_service import DrinkRetrieveService


def get_llm_service() -> LLMService:
    return LLMService()


def get_vector_store(llm_service = Depends(get_llm_service)) -> VectorStore:
    return VectorStore(embeddings=llm_service.get_embeddings())


def get_drink_retrieve_service(vector_store = Depends(get_vector_store)):
    return DrinkRetrieveService(vector_store)