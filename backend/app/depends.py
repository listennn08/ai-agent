from fastapi import Depends
from sqlalchemy.orm import Session

from ai.llm_service import LLMService
from ai.agent_supervisor import AgentSupervisor
from services.user.basic import IUserPreferenceService
from services.user.preference_service import UserPreferenceService
from infrastructure.vector_store.base import IVectorStore
from infrastructure.vector_store.vector_store import VectorStore
from services.drink_service import DrinkService
from services.chat.chat_storage_base import IChatStorage
from services.chat.in_memory_chat_storage import InMemoryChatStorage
from repositories.drink_photo_repository import DrinkPhotoRepository
from db import get_db


def get_llm_service() -> LLMService:
    return LLMService()


def get_vector_store(
    llm_service: LLMService = Depends(get_llm_service),
) -> IVectorStore:
    return VectorStore(embeddings=llm_service.get_embeddings())


def get_drink_photo_repository(
    db_session: Session = Depends(get_db),
) -> DrinkPhotoRepository:
    return DrinkPhotoRepository(db_session)


def get_chat_history() -> IChatStorage:
    return InMemoryChatStorage()


def get_user_preference_service(
    db_session: Session = Depends(get_db),
) -> IUserPreferenceService:
    return UserPreferenceService(db_session)


def get_drink_service(
    vector_store: IVectorStore = Depends(get_vector_store),
    llm_service: LLMService = Depends(get_llm_service),
    drink_photo_repository: DrinkPhotoRepository = Depends(get_drink_photo_repository),
    chat_storage: InMemoryChatStorage = Depends(get_chat_history),
    user_preference_service: IUserPreferenceService = Depends(
        get_user_preference_service
    ),
) -> DrinkService:
    return DrinkService(
        vector_store=vector_store.vector_store,
        llm_service=llm_service,
        drink_photo_repository=drink_photo_repository,
        chat_storage=chat_storage,
        user_preference_service=user_preference_service,
    )


def get_agent_supervisor() -> AgentSupervisor:
    return AgentSupervisor()
