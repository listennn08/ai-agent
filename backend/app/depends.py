from fastapi import Depends
from sqlalchemy.orm import Session

from ai.llm_service import LLMService
from ai.agent_supervisor import AgentSupervisor
from infrastructure.vector_store.vector_store import VectorStore
from services.drink_service import DrinkService
from services.chat_history_service import ChatHistory
from repositories.drink_photo_repository import DrinkPhotoRepository
from db import get_db


def get_llm_service() -> LLMService:
    return LLMService()


def get_vector_store(llm_service: LLMService = Depends(get_llm_service)) -> VectorStore:
    return VectorStore(embeddings=llm_service.get_embeddings())


def get_drink_photo_repository(
    db_session: Session = Depends(get_db),
) -> DrinkPhotoRepository:
    return DrinkPhotoRepository(db_session)


def get_drink_service(
    vector_store: VectorStore = Depends(get_vector_store),
    llm_service: LLMService = Depends(get_llm_service),
    drink_photo_repository: DrinkPhotoRepository = Depends(get_drink_photo_repository),
) -> DrinkService:
    return DrinkService(
        vector_store=vector_store.vector_store,
        llm_service=llm_service,
        drink_photo_repository=drink_photo_repository,
    )


def get_chat_history() -> ChatHistory:
    return ChatHistory()


def get_agent_supervisor() -> AgentSupervisor:
    return AgentSupervisor()
