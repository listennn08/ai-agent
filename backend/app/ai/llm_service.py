from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from configs.settings import settings


class LLMService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("== Initialize LLMService ==")
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance.llm = ChatOpenAI(model=settings.LLM_MODEL)
            cls._instance.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
        
        return cls._instance

    
    def get_llm(self):
        return self.llm
    
    def get_embeddings(self):
        return self.embeddings
