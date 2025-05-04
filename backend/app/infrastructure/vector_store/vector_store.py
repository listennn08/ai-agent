from langchain_core.embeddings.embeddings import Embeddings

from configs.settings import settings


class VectorStore:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

        if settings.VECTOR_STORE_TYPE == "faiss":
            from infrastructure.vector_store.faiss_store import FaissVectorStore

            self.vector_store = FaissVectorStore(embedding=embeddings)
        elif settings.VECTOR_STORE_TYPE == "pinecone":
            from infrastructure.vector_store.pinecone_store import PineconeVectorStore

            self.vector_store = PineconeVectorStore(embedding=embeddings)
        else:
            raise ValueError(f"Unknown vector store: {settings.VECTOR_STORE_TYPE}")
