from abc import ABC, abstractmethod


class VectorStoreABC(ABC):
    @abstractmethod
    def batch_insert(self, documents):
        pass

    @abstractmethod
    def initialize(self):
        pass