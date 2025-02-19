from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from configs.settings import settings


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(model=settings.LLM_MODEL)
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)

    
    def get_llm(self):
        return self.llm
    
    def get_embeddings(self):
        return self.embeddings
