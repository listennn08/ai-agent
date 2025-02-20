import time
from langchain_core.embeddings import Embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from configs.settings import settings
from infrastructure.vector_store.base import VectorStoreABC

class VectorStore(VectorStoreABC):
    pc: Pinecone = None
    vector_store: PineconeVectorStore = None
    index_name = "pinecone_index"

    def __init__(self, embedding: Embeddings):
        self.embedding = embedding
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.initialize()
    

    def batch_insert(self, documents):
        return self.vector_store.add_documents(documents)


    def initialize(self):
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=len(self.embedding.embed_query("")),
                metric="cosine"
            )
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)
            
            self.vector_store = PineconeVectorStore(
                index=self.pc.Index(self.index_name),
                embedding=self.embedding
            )
        else:
            self.vector_store = PineconeVectorStore.from_documents([], self.embedding, index_name=self.index_name)