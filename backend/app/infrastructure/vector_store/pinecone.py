from langchain_core.embeddings import Embeddings
from langchain_pinecone import PineconeVectorStore

class VectorStore():
    def __init__(self, embedding: Embeddings):
        self.client = PineconeVectorStore(index="", embedding=embedding)
        pass