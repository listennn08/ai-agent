import time
from langchain_core.embeddings import Embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from configs.settings import settings
from infrastructure.vector_store.base import VectorStoreABC


class VectorStore(VectorStoreABC):
    pc: Pinecone = None
    vector_store: PineconeVectorStore = None
    index_name = "pinecone-index"

    def __init__(self, embedding: Embeddings):
        self.embedding = embedding
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.initialize()

    def batch_insert(self, documents):
        return self.vector_store.add_documents(documents)

    def read_index(self):
        return self.index

    def initialize(self):
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        while not self.pc.describe_index(self.index_name).status["ready"]:
            time.sleep(1)

        self.index = self.pc.Index(self.index_name)
        self.vector_store = PineconeVectorStore(
            index=self.pc.Index(self.index_name), embedding=self.embedding
        )
