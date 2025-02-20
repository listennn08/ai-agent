from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_FILE_PATH: str = Field(default="./app/storage/files/")
    DATABASE_URL: str = Field(default="sqlite:///app/storage/db/local.db", extra="allow_mutation")

    
    LLM_MODEL: str = Field(default="gpt-4o", extra="allow_mutation")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", extra="allow_mutation")
    VECTOR_STORE_TYPE: str = Field(default="faiss", extra="allow_mutation")
    OPENAI_API_KEY: str = Field(default="", extra="allow_mutation")
    PINECONE_API_KEY: str = Field(default="", extra="allow_mutation")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
