from abc import ABC, abstractmethod
from langchain_core.documents import Document


class VectorPreprocessor(ABC):
    """Abstract class for vector document preprocessor"""

    @abstractmethod
    def preprocess(self, raw_data: list[dict]) -> list[Document]:
        """Abstract method for preprocessing a vector"""
        pass