from langchain_core.documents import Document

from base import VectorPreprocessor

class SimplePreprocessor(VectorPreprocessor):
    def __init__(self):
        pass
    
    
    def preprocess(self, raw_data: list[dict]) -> list[Document]:
        return [Document(page_content=doc.get("text"), metadata=doc) for doc in raw_data]
    