import os
from pydantic import Field
from pydantic_settings import BaseSettings


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    STORAGE_FILE_PATH: str = Field(default=f"{root}/storage/files/")
    DATABASE_URL: str = Field(
        default=f"sqlite:///{root}/storage/db/local.db", extra="allow_mutation"
    )

    LLM_MODEL: str = Field(default="gpt-4o", extra="allow_mutation")
    EMBEDDING_MODEL: str = Field(
        default="text-embedding-3-large", extra="allow_mutation"
    )
    VECTOR_STORE_TYPE: str = Field(default="faiss", extra="allow_mutation")
    OPENAI_API_KEY: str = Field(default="", extra="allow_mutation")
    PINECONE_API_KEY: str = Field(default="", extra="allow_mutation")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
