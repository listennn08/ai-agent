from abc import ABC, abstractmethod

from langchain_core.vectorstores import VectorStore


class IVectorStore(ABC):
    @property
    @abstractmethod
    def vector_store(self) -> VectorStore:
        pass

    @abstractmethod
    def batch_insert(self, documents):
        pass

    @abstractmethod
    def read_index():
        pass

    @abstractmethod
    def initialize(self):
        pass
