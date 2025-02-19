from langchain_core.embeddings.embeddings import Embeddings

from configs.settings import settings


class VectorStore:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings
        self.vector_store = None

        if settings.VECTOR_STORE_TYPE == "faiss":
            from infrastructure.vector_store.faiss import vector_store
        elif settings.VECTOR_STORE_TYPE == "pinecone":
            from infrastructure.vector_store.pinecone import vector_store
        else:
            raise ValueError(f"Unknown vector store: {settings.VECTOR_STORE_TYPE}")

        self.vector_store = vector_store

    