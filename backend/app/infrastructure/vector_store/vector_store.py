from langchain_core.embeddings.embeddings import Embeddings

from configs.settings import settings


class VectorStore:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

        if settings.VECTOR_STORE_TYPE == "faiss":
            from infrastructure.vector_store.faiss_store import VectorStore
        elif settings.VECTOR_STORE_TYPE == "pinecone":
            from infrastructure.vector_store.pinecone_store import VectorStore
        else:
            raise ValueError(f"Unknown vector store: {settings.VECTOR_STORE_TYPE}")

        self.vector_store = VectorStore(embedding=embeddings).vector_store
